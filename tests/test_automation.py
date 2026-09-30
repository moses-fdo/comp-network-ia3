import ipaddress
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import pytest

from scripts.generate_configs import (
    load_csv,
    validate_ip,
    build_device_contexts,
    generate_configurations,
)
from scripts.verify_network import audit_device_config, run_compliance_audit

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output_configs"


def test_ip_validation_helper():
    assert validate_ip("192.168.1.1") is True
    assert validate_ip("10.0.0.1") is True
    assert validate_ip("256.0.0.1") is False
    assert validate_ip("invalid-ip") is False
    assert validate_ip("", allow_empty=True) is True
    assert validate_ip("", allow_empty=False) is False


def test_inventory_csv_schema():
    inventory = load_csv(DATA_DIR / "inventory.csv")
    assert len(inventory) == 5
    hostnames = [d["hostname"] for d in inventory]
    assert "R1-Core" in hostnames
    assert "SW1-Dist" in hostnames
    assert "SW2-Eng" in hostnames
    assert "SW3-HR" in hostnames
    assert "SW4-Sales" in hostnames

    for dev in inventory:
        assert validate_ip(dev["mgmt_ip"]) is True
        assert dev["admin_user"]
        assert dev["admin_password"]
        assert dev["enable_secret"]
        assert dev["domain_name"] == "novacorp.local"


def test_vlans_csv_schema():
    vlans = load_csv(DATA_DIR / "vlans.csv")
    vlan_ids = [int(v["vlan_id"]) for v in vlans]
    assert 10 in vlan_ids
    assert 20 in vlan_ids
    assert 30 in vlan_ids
    assert 40 in vlan_ids
    assert 99 in vlan_ids
    assert 999 in vlan_ids


def test_generate_configurations():
    generated_files = generate_configurations(BASE_DIR, OUTPUT_DIR, TEMPLATES_DIR)
    assert len(generated_files) == 6  # 5 devices + 1 consolidated paste file

    expected_names = [
        "R1-Core.cfg",
        "SW1-Dist.cfg",
        "SW2-Eng.cfg",
        "SW3-HR.cfg",
        "SW4-Sales.cfg",
        "all_devices_paste.txt",
    ]
    for name in expected_names:
        assert (OUTPUT_DIR / name).exists()
        assert (OUTPUT_DIR / name).stat().st_size > 0


def test_router_configuration_syntax():
    cfg_path = OUTPUT_DIR / "R1-Core.cfg"
    content = cfg_path.read_text(encoding="utf-8")

    assert "hostname R1-Core" in content
    assert "ip ssh version 2" in content
    assert "banner motd" in content
    assert "interface GigabitEthernet0/0.10" in content
    assert "encapsulation dot1Q 10" in content
    assert "ip dhcp pool POOL_ENG" in content
    assert "router ospf 1" in content


def test_switch_configuration_syntax():
    cfg_path = OUTPUT_DIR / "SW1-Dist.cfg"
    content = cfg_path.read_text(encoding="utf-8")

    assert "hostname SW1-Dist" in content
    assert "spanning-tree mode rapid-pvst" in content
    assert "switchport mode trunk" in content
    assert "switchport trunk native vlan 999" in content
    assert "interface Vlan99" in content
    assert "ip default-gateway 192.168.99.1" in content


def test_all_devices_security_compliance():
    inventory = load_csv(DATA_DIR / "inventory.csv")
    audits = run_compliance_audit(OUTPUT_DIR, inventory)
    assert len(audits) == 5
    for a in audits:
        assert a["score"] == 100.0, f"Device {a['hostname']} failed security audit: {a['checks']}"
