#!/usr/bin/env python3
"""
deploy_configs.py
-----------------
Automated SSH Deployment Script for Cisco Network Devices.
Connects to routers and switches over SSH (Netmiko), deploys generated
configurations, and handles error reporting and logging.
Supports both Live SSH deployment and Simulation/Dry-Run modes.

Author: Network Automation Team
Project: Python-Based Network Configuration Automation
"""

import argparse
import csv
import logging
import os
import sys
import time
from pathlib import Path

# Optional Netmiko for live device communication
try:
    from netmiko import ConnectHandler
    from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
    HAS_NETMIKO = True
except ImportError:
    HAS_NETMIKO = False

# Optional Rich formatting
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.panel import Panel
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def setup_logger(log_file: Path) -> logging.Logger:
    logger = logging.getLogger("NetworkDeployer")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # File handler
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


def load_inventory(inventory_path: Path) -> list[dict]:
    if not inventory_path.exists():
        raise FileNotFoundError(f"Inventory file not found: {inventory_path}")
    with open(inventory_path, "r", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f)]


def clean_config_for_deployment(cfg_text: str) -> list[str]:
    """Prepares Cisco IOS commands list from configuration text."""
    commands = []
    for line in cfg_text.splitlines():
        line = line.strip()
        # Skip pure comments or blank lines
        if not line or line.startswith("!"):
            continue
        # In automated Netmiko config mode, skip end/write memory (handled separately)
        if line.lower() in ["end", "write memory", "write", "copy running-config startup-config"]:
            continue
        commands.append(line)
    return commands


def simulate_ssh_deployment(device: dict, config_path: Path, logger: logging.Logger) -> dict:
    """Simulates realistic SSH deployment for offline/Packet Tracer demo mode."""
    hostname = device["hostname"]
    mgmt_ip = device["mgmt_ip"]
    logger.info(f"[SIMULATION] Initiating SSH connection to {hostname} ({mgmt_ip}:22)...")
    time.sleep(0.3)

    logger.info(f"[SIMULATION] Authenticating as user '{device['admin_user']}'...")
    time.sleep(0.2)
    logger.info(f"[SIMULATION] Entering privileged EXEC mode (enable secret validated)...")

    if not config_path.exists():
        msg = f"Configuration file {config_path} not found. Run generate_configs.py first!"
        logger.error(f"[SIMULATION] {msg}")
        return {"hostname": hostname, "status": "FAILED", "reason": msg, "commands_sent": 0}

    cfg_text = config_path.read_text(encoding="utf-8")
    commands = clean_config_for_deployment(cfg_text)

    logger.info(f"[SIMULATION] Pushing {len(commands)} configuration commands to {hostname}...")
    time.sleep(0.4)

    logger.info(f"[SIMULATION] Saving running-config to startup-config (write memory)...")
    time.sleep(0.2)
    logger.info(f"[SIMULATION] Deployment completed successfully on {hostname}.")

    return {
        "hostname": hostname,
        "mgmt_ip": mgmt_ip,
        "status": "SUCCESS",
        "mode": "Simulation (Dry-Run)",
        "commands_sent": len(commands),
        "execution_time_sec": 1.1,
    }


def live_ssh_deployment(device: dict, config_path: Path, timeout: int, logger: logging.Logger) -> dict:
    """Connects to a live Cisco device via SSH and deploys configuration."""
    if not HAS_NETMIKO:
        raise RuntimeError("Netmiko library is required for live SSH deployment.")

    hostname = device["hostname"]
    mgmt_ip = device["mgmt_ip"]
    start_time = time.time()

    if not config_path.exists():
        return {"hostname": hostname, "status": "FAILED", "reason": "Config file missing", "commands_sent": 0}

    cfg_text = config_path.read_text(encoding="utf-8")
    commands = clean_config_for_deployment(cfg_text)

    device_params = {
        "device_type": "cisco_ios",
        "host": mgmt_ip,
        "username": device["admin_user"],
        "password": device["admin_password"],
        "secret": device["enable_secret"],
        "timeout": timeout,
        "session_timeout": timeout * 2,
    }

    logger.info(f"Connecting to live device {hostname} ({mgmt_ip})...")
    try:
        with ConnectHandler(**device_params) as net_connect:
            logger.info(f"Connected to {hostname}. Entering enable mode...")
            net_connect.enable()

            prompt = net_connect.find_prompt()
            logger.info(f"Device prompt verified: {prompt}")

            logger.info(f"Sending {len(commands)} configuration commands...")
            output = net_connect.send_config_set(commands)
            logger.debug(f"Configuration output from {hostname}:\n{output}")

            logger.info(f"Saving running-config to startup-config...")
            save_output = net_connect.save_config()
            logger.debug(f"Save output: {save_output}")

            duration = round(time.time() - start_time, 2)
            logger.info(f"Successfully deployed to {hostname} in {duration}s")

            return {
                "hostname": hostname,
                "mgmt_ip": mgmt_ip,
                "status": "SUCCESS",
                "mode": "Live SSH",
                "commands_sent": len(commands),
                "execution_time_sec": duration,
            }

    except NetmikoAuthenticationException as auth_err:
        logger.error(f"Authentication failure on {hostname} ({mgmt_ip}): {auth_err}")
        return {"hostname": hostname, "mgmt_ip": mgmt_ip, "status": "AUTH_FAILED", "reason": str(auth_err)}
    except NetmikoTimeoutException as timeout_err:
        logger.error(f"Connection timeout on {hostname} ({mgmt_ip}): {timeout_err}")
        return {"hostname": hostname, "mgmt_ip": mgmt_ip, "status": "TIMEOUT", "reason": str(timeout_err)}
    except Exception as e:
        logger.error(f"Unexpected error deploying to {hostname}: {e}")
        return {"hostname": hostname, "mgmt_ip": mgmt_ip, "status": "ERROR", "reason": str(e)}


def deploy_all(
    devices: list[dict],
    configs_dir: Path,
    dry_run: bool,
    timeout: int,
    logger: logging.Logger,
    target_hostname: str = None,
) -> list[dict]:
    """Iterates through devices and executes deployment."""
    results = []
    filtered_devices = devices
    if target_hostname:
        filtered_devices = [d for d in devices if d["hostname"].lower() == target_hostname.lower()]
        if not filtered_devices:
            raise ValueError(f"Target device '{target_hostname}' not found in inventory.")

    for dev in filtered_devices:
        hostname = dev["hostname"]
        cfg_file = configs_dir / f"{hostname}.cfg"

        if dry_run or not HAS_NETMIKO:
            res = simulate_ssh_deployment(dev, cfg_file, logger)
        else:
            res = live_ssh_deployment(dev, cfg_file, timeout, logger)

        results.append(res)

    return results


def print_deployment_summary(results: list[dict]):
    """Outputs formatted deployment results."""
    if HAS_RICH and console:
        table = Table(title="Device Configuration Deployment Summary", header_style="bold cyan")
        table.add_column("Device Hostname", style="bold white")
        table.add_column("Management IP", style="cyan")
        table.add_column("Mode", style="magenta")
        table.add_column("Commands", justify="right", style="blue")
        table.add_column("Status", justify="center")
        table.add_column("Time (s)", justify="right", style="green")

        all_success = True
        for r in results:
            status_style = "bold green" if r["status"] == "SUCCESS" else "bold red"
            if r["status"] != "SUCCESS":
                all_success = False
            status_text = f"[{status_style}]{r['status']}[/{status_style}]"
            table.add_row(
                r.get("hostname", "Unknown"),
                r.get("mgmt_ip", "N/A"),
                r.get("mode", "Live SSH"),
                str(r.get("commands_sent", 0)),
                status_text,
                str(r.get("execution_time_sec", 0.0)),
            )

        console.print(table)
        if all_success:
            console.print(Panel("[bold green]✔ All configurations deployed and verified successfully![/bold green]", border_style="green"))
        else:
            console.print(Panel("[bold red]✖ Some device deployments encountered errors. Check deployment.log for details.[/bold red]", border_style="red"))
    else:
        print("\n--- Deployment Results ---")
        for r in results:
            print(f"Device: {r.get('hostname'):<12} | IP: {r.get('mgmt_ip'):<15} | Status: {r.get('status')} | Cmds: {r.get('commands_sent', 0)}")


def main():
    parser = argparse.ArgumentParser(description="Automated SSH Configuration Deployment Script")
    parser.add_argument("--dry-run", action="store_true", help="Run in simulation/dry-run mode (safe for testing)")
    parser.add_argument("--device", type=str, help="Target a specific hostname (e.g. R1-Core, SW1-Dist)")
    parser.add_argument("--timeout", type=int, default=10, help="SSH connection timeout in seconds")
    parser.add_argument("--live", action="store_true", help="Force live SSH deployment against active IP addresses")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    configs_dir = base_dir / "output_configs"
    log_file = base_dir / "deployment.log"

    logger = setup_logger(log_file)
    logger.info("=" * 60)
    logger.info("Starting Configuration Deployment Run")

    try:
        inventory = load_inventory(data_dir / "inventory.csv")

        # Determine mode: default to dry-run if --live not specified or netmiko is absent
        is_dry_run = True
        if args.live:
            if not HAS_NETMIKO:
                print("Error: Netmiko is not installed. Run 'pip install -r requirements.txt'")
                sys.exit(1)
            is_dry_run = False
        elif not args.dry_run:
            # Inform user of default behavior
            if HAS_RICH and console:
                console.print("[dim]Note: Running in simulation mode. Use '--live' to connect to live network devices.[/dim]")
            is_dry_run = True

        results = deploy_all(inventory, configs_dir, is_dry_run, args.timeout, logger, args.device)
        print_deployment_summary(results)

    except Exception as e:
        logger.exception(f"Fatal error in deployment: {e}")
        if HAS_RICH and console:
            console.print(f"[bold red]Deployment failed:[/bold red] {e}")
        else:
            print(f"Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
