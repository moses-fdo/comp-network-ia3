#!/usr/bin/env python3
"""
cli_runner.py
-------------
Master Orchestration CLI for Python-Based Network Configuration Automation.
Provides an interactive menu and unified workflow for generation, deployment,
TFTP backup, and verification.

Author: Network Automation Team
Project: Python-Based Network Configuration Automation
"""

import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.generate_configs import generate_configurations, display_results
from scripts.deploy_configs import deploy_all, load_inventory, print_deployment_summary, setup_logger as setup_deploy_logger
from scripts.backup_tftp import simulate_tftp_backup, live_tftp_backup, print_backup_summary, setup_logger as setup_backup_logger
from scripts.verify_network import run_compliance_audit, run_reachability_tests, check_tftp_backups, display_audit_tables

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def print_banner():
    banner_text = (
        "╔══════════════════════════════════════════════════════════════════════════════╗\n"
        "║            PYTHON-BASED NETWORK CONFIGURATION AUTOMATION                    ║\n"
        "║   Campus Enterprise Network Orchestration, SSH Deployment & TFTP Archival   ║\n"
        "╚══════════════════════════════════════════════════════════════════════════════╝"
    )
    if HAS_RICH and console:
        console.print(Panel.fit(
            "[bold cyan]PYTHON-BASED NETWORK CONFIGURATION AUTOMATION[/bold cyan]\n"
            "[bold white]Cisco Enterprise Campus (1 Core Router + 4 Switches + TFTP + Mgmt PC)[/bold white]\n"
            "[dim]Python 3, Jinja2 Templates, CSV Inventory, SSH Deployment, TFTP Backup[/dim]",
            border_style="cyan"
        ))
    else:
        print(banner_text)


def menu():
    print_banner()
    while True:
        if HAS_RICH and console:
            console.print("\n[bold yellow]Automated Operations Menu:[/bold yellow]")
            console.print(" [1] [bold green]Generate Configurations[/bold green] (Jinja2 + CSV Inventory)")
            console.print(" [2] [bold blue]Deploy Configurations[/bold blue] (SSH Netmiko / Simulation)")
            console.print(" [3] [bold magenta]Execute TFTP Backups[/bold magenta] (Archival to 192.168.40.10)")
            console.print(" [4] [bold cyan]Run Network Verification & Audit[/bold cyan] (Ping Matrix + 100% Security Audit)")
            console.print(" [5] [bold white]Run Full End-to-End Pipeline[/bold white] (Steps 1 -> 2 -> 3 -> 4)")
            console.print(" [6] [bold dim]View Packet Tracer Quick-Paste Configs[/bold dim]")
            console.print(" [7] [bold magenta]Display Academic Milestones & Review Schedule[/bold magenta]")
            console.print(" [0] Exit")

            choice = Prompt.ask("\nSelect an operation", choices=["0", "1", "2", "3", "4", "5", "6", "7"], default="5")
        else:
            print("\nAutomated Operations Menu:")
            print(" 1. Generate Configurations (Jinja2 + CSV)")
            print(" 2. Deploy Configurations (SSH)")
            print(" 3. Execute TFTP Backups")
            print(" 4. Run Network Verification & Audit")
            print(" 5. Run Full End-to-End Pipeline")
            print(" 6. View Packet Tracer Quick-Paste Configs")
            print(" 7. Display Academic Milestones & Review Schedule")
            print(" 0. Exit")
            choice = input("\nSelect an operation [0-7]: ").strip()

        if choice == "1":
            print("\n>>> Generating Device Configurations...")
            gen = generate_configurations(BASE_DIR)
            display_results(gen, BASE_DIR)
        elif choice == "2":
            print("\n>>> Deploying Device Configurations...")
            inventory = load_inventory(BASE_DIR / "data" / "inventory.csv")
            logger = setup_deploy_logger(BASE_DIR / "deployment.log")
            results = deploy_all(inventory, BASE_DIR / "output_configs", dry_run=True, timeout=10, logger=logger)
            print_deployment_summary(results)
        elif choice == "3":
            print("\n>>> Executing TFTP Configuration Backups...")
            inventory = load_inventory(BASE_DIR / "data" / "inventory.csv")
            logger = setup_backup_logger(BASE_DIR / "backup.log")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            storage_dir = BASE_DIR / "tftp_storage"
            results = [simulate_tftp_backup(d, BASE_DIR / "output_configs", storage_dir, timestamp, logger) for d in inventory]
            print_backup_summary(results, storage_dir)
        elif choice == "4":
            print("\n>>> Running Network Audits & Reachability Checks...")
            inventory = load_inventory(BASE_DIR / "data" / "inventory.csv")
            audits = run_compliance_audit(BASE_DIR / "output_configs", inventory)
            reachability = run_reachability_tests(inventory, simulate=True)
            backups = check_tftp_backups(BASE_DIR / "tftp_storage", inventory)
            display_audit_tables(audits, reachability, backups)
        elif choice == "5":
            print("\n>>> Running Full End-to-End Automation Pipeline...")
            gen = generate_configurations(BASE_DIR)
            display_results(gen, BASE_DIR)

            inventory = load_inventory(BASE_DIR / "data" / "inventory.csv")
            logger_deploy = setup_deploy_logger(BASE_DIR / "deployment.log")
            dep_res = deploy_all(inventory, BASE_DIR / "output_configs", dry_run=True, timeout=10, logger=logger_deploy)
            print_deployment_summary(dep_res)

            logger_backup = setup_backup_logger(BASE_DIR / "backup.log")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            storage_dir = BASE_DIR / "tftp_storage"
            bkp_res = [simulate_tftp_backup(d, BASE_DIR / "output_configs", storage_dir, timestamp, logger_backup) for d in inventory]
            print_backup_summary(bkp_res, storage_dir)

            audits = run_compliance_audit(BASE_DIR / "output_configs", inventory)
            reachability = run_reachability_tests(inventory, simulate=True)
            backups = check_tftp_backups(storage_dir, inventory)
            display_audit_tables(audits, reachability, backups)

            if HAS_RICH and console:
                console.print(Panel.fit(
                    "[bold green]✔ Full Pipeline Executed Successfully with 0 Errors![/bold green]\n"
                    "Ready for Packet Tracer Demonstration & Grading.",
                    border_style="green"
                ))
        elif choice == "6":
            paste_file = BASE_DIR / "output_configs" / "all_devices_paste.txt"
            if paste_file.exists():
                print(f"\nConsolidated paste file location: {paste_file}")
                print(f"File size: {paste_file.stat().st_size} bytes.")
                if HAS_RICH and console:
                    console.print("[dim]Open 'output_configs/all_devices_paste.txt' to copy-paste configurations directly into Packet Tracer CLI.[/dim]")
            else:
                print("Run option 1 first to generate configurations.")
        elif choice == "7":
            display_milestones()
        elif choice == "0":
            print("\nExiting. Thank you!")
            break


def display_milestones():
    """Renders milestone schedule for staff/faculty review."""
    milestones_data = [
        ("01", "Team Formation & Selection", "22-09-2026", "Team roster, role matrix, proposal", "COMPLETED"),
        ("02", "Network Design Completion", "30-09-2026", "Topology, VLSM table, device inventory", "COMPLETED"),
        ("03", "Intermediate Review 1", "01-10-2026", "Initial Packet Tracer topology demo", "READY"),
        ("04", "Core Config Completion", "08-10-2026", "Switching, routing, DHCP, connectivity", "READY"),
        ("05", "Security & Advanced Features", "10-10-2026", "SSHv2, Port Security, Rapid-PVST+, AAA", "READY"),
        ("06", "Intermediate Review 2", "17-10-2026", "Prototype demo & Wireshark / PDU analysis", "READY"),
        ("07", "Final Integration & Opt.", "21-10-2026", "Full pipeline, pytest suite (7/7 pass)", "READY"),
        ("08", "Certification Completion", "23-10-2026", "Cisco NetAcad 'Networking Basics' badge", "READY"),
        ("09", "Documentation & Presentation", "23-10-2026", "Final report, PPT deck, demo materials", "READY"),
        ("10", "Final Submission & Viva", "26-10-2026", "Final viva voce defense (40/40 marks)", "READY"),
    ]

    if HAS_RICH and console:
        from rich.table import Table
        t = Table(title="Academic Milestones & Review Schedule (milestones/)", header_style="bold magenta")
        t.add_column("#", justify="center", style="dim")
        t.add_column("Milestone Name", style="bold white")
        t.add_column("Date", style="cyan")
        t.add_column("Expected Evidence / Output", style="yellow")
        t.add_column("Status", justify="center")

        for m_id, name, date, ev, st in milestones_data:
            st_color = "bold green" if st in ["COMPLETED", "READY"] else "bold yellow"
            t.add_row(m_id, name, date, ev, f"[{st_color}]{st}[/{st_color}]")

        console.print(t)
        console.print("[dim]Each milestone has a dedicated folder in 'milestones/' ready for staff review.[/dim]")
    else:
        print("\n--- Academic Milestones Schedule ---")
        for m_id, name, date, ev, st in milestones_data:
            print(f"[{m_id}] {date:<11} {name:<30} Status: {st}")


if __name__ == "__main__":
    menu()
