#!/usr/bin/env python3
"""
generate_configs.py
-------------------
Automated Network Configuration Generator
Reads device inventory, VLANs, and interface mappings from CSV files,
validates network data, and renders Cisco IOS configuration files via Jinja2.

Author: Network Automation Team
Project: Python-Based Network Configuration Automation
"""

import csv
import ipaddress
import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Optional rich formatting for premium CLI UX
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def print_info(msg: str):
    if HAS_RICH:
        console.print(f"[bold cyan][INFO][/bold cyan] {msg}")
    else:
        print(f"[INFO] {msg}")


def print_success(msg: str):
    if HAS_RICH:
        console.print(f"[bold green][SUCCESS][/bold green] {msg}")
    else:
        print(f"[SUCCESS] {msg}")


def print_warning(msg: str):
    if HAS_RICH:
        console.print(f"[bold yellow][WARNING][/bold yellow] {msg}")
    else:
        print(f"[WARNING] {msg}")


def print_error(msg: str):
    if HAS_RICH:
        console.print(f"[bold red][ERROR][/bold red] {msg}")
    else:
        print(f"[ERROR] {msg}")


def validate_ip(ip_str: str, allow_empty: bool = False) -> bool:
    """Validates IPv4 string."""
    if not ip_str and allow_empty:
        return True
    try:
        ipaddress.IPv4Address(ip_str.strip())
        return True
    except ValueError:
        return False


def load_csv(filepath: Path) -> list[dict]:
    """Reads CSV file and returns list of dictionaries."""
    if not filepath.exists():
        raise FileNotFoundError(f"Required CSV file not found: {filepath}")
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def build_device_contexts(inventory: list[dict], vlans: list[dict], interfaces: list[dict]) -> list[dict]:
    """Merges inventory, VLANs, and interfaces for template rendering."""
    # Group interfaces by hostname
    iface_map: dict[str, list[dict]] = {}
    for iface in interfaces:
        h = iface.get("hostname", "").strip()
        iface_map.setdefault(h, []).append(iface)

    contexts = []
    for dev in inventory:
        hostname = dev["hostname"].strip()
        # IP validation
        if not validate_ip(dev.get("mgmt_ip")):
            raise ValueError(f"Invalid management IP address '{dev.get('mgmt_ip')}' for device {hostname}")
        if dev.get("default_gateway") and not validate_ip(dev.get("default_gateway")):
            raise ValueError(f"Invalid default gateway '{dev.get('default_gateway')}' for device {hostname}")

        ctx = dict(dev)
        ctx["interfaces"] = iface_map.get(hostname, [])
        ctx["vlans"] = vlans
        contexts.append(ctx)

    return contexts


def generate_configurations(
    base_dir: Path = None,
    output_dir: Path = None,
    templates_dir: Path = None,
) -> list[Path]:
    """Main configuration generation function."""
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent.parent
    if output_dir is None:
        output_dir = base_dir / "output_configs"
    if templates_dir is None:
        templates_dir = base_dir / "templates"

    data_dir = base_dir / "data"
    inventory_path = data_dir / "inventory.csv"
    vlans_path = data_dir / "vlans.csv"
    interfaces_path = data_dir / "interfaces.csv"

    print_info(f"Loading data models from {data_dir}...")
    inventory = load_csv(inventory_path)
    vlans = load_csv(vlans_path)
    interfaces = load_csv(interfaces_path)

    print_info(f"Found {len(inventory)} devices, {len(vlans)} VLANs, {len(interfaces)} interface mappings.")

    contexts = build_device_contexts(inventory, vlans, interfaces)

    # Initialize Jinja2 Environment
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files: list[Path] = []
    paste_blocks: list[str] = []

    for ctx in contexts:
        hostname = ctx["hostname"]
        role = ctx.get("role", "")
        if role == "core_router":
            template_name = "router_template.j2"
        else:
            template_name = "switch_template.j2"

        template = env.get_template(template_name)
        rendered_config = template.render(ctx)

        # Write to individual .cfg file
        cfg_path = output_dir / f"{hostname}.cfg"
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(rendered_config.strip() + "\n")
        generated_files.append(cfg_path)

        # Build Packet Tracer consolidated paste block
        block = [
            f"! {'#' * 76}",
            f"! DEVICE: {hostname} ({role.upper()}) - MGMT IP: {ctx.get('mgmt_ip')}",
            f"! HOW TO APPLY IN PACKET TRACER:",
            f"! 1. Open Device '{hostname}' -> CLI tab",
            f"! 2. Type 'enable' -> 'configure terminal'",
            f"! 3. Paste the configuration block below",
            f"! {'#' * 76}",
            rendered_config.strip(),
            "\n",
        ]
        paste_blocks.append("\n".join(block))

    # Write consolidated paste file for easy Packet Tracer testing
    paste_file_path = output_dir / "all_devices_paste.txt"
    with open(paste_file_path, "w", encoding="utf-8") as pf:
        pf.write(
            "! ==============================================================================\n"
            "! CONSOLIDATED CISCO PACKET TRACER READY-TO-PASTE CONFIGURATION BUNDLE\n"
            "! Project: Python-Based Network Configuration Automation\n"
            "! Generated Automatically by scripts/generate_configs.py\n"
            "! ==============================================================================\n\n"
        )
        pf.write("\n".join(paste_blocks))
    generated_files.append(paste_file_path)

    return generated_files


def display_results(generated_files: list[Path], base_dir: Path):
    """Prints a styled summary table of generated configurations."""
    if HAS_RICH and console:
        table = Table(title="Generated Cisco IOS Configurations", show_header=True, header_style="bold magenta")
        table.add_column("Filename", style="cyan", no_wrap=True)
        table.add_column("Lines", justify="right", style="green")
        table.add_column("Size (Bytes)", justify="right", style="yellow")
        table.add_column("Path", style="dim")

        for f in generated_files:
            rel_path = f.relative_to(base_dir)
            lines = len(f.read_text().splitlines())
            size = f.stat().st_size
            table.add_row(f.name, str(lines), str(size), str(rel_path))

        console.print(table)
        console.print(Panel.fit(
            f"[bold green]Successfully generated {len(generated_files)} configuration files![/bold green]\n"
            f"[bold white]Output Directory:[/bold white] {base_dir / 'output_configs'}",
            border_style="green"
        ))
    else:
        print("\n--- Summary of Generated Files ---")
        for f in generated_files:
            lines = len(f.read_text().splitlines())
            print(f" - {f.name:<25} ({lines:>4} lines, {f.stat().st_size:>5} bytes)")
        print(f"\nAll files saved to {base_dir / 'output_configs'}")


def main():
    base_dir = Path(__file__).resolve().parent.parent
    try:
        generated = generate_configurations(base_dir)
        display_results(generated, base_dir)
    except Exception as e:
        print_error(f"Failed to generate configurations: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
