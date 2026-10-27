#!/usr/bin/env python3
"""
main.py
-------
Root Entry Point for Python-Based Network Configuration Automation.
"""

import sys

if sys.platform == "win32":
    try:
        if sys.stdout.encoding != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr.encoding != "utf-8":
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.cli_runner import menu

if __name__ == "__main__":
    menu()
