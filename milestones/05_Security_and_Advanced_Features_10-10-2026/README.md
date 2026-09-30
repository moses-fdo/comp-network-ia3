# Milestone 05: Security & Advanced Features Completion

**Scheduled Date:** 10-10-2026  
**Status:** `READY FOR FACULTY REVIEW`  
**Deliverable Focus:** Device Hardening, AAA Security, Switchport Port Security, Rapid-PVST+, and Parking Lot Isolation  

---

## 1. Implemented Security & Hardening Features

This milestone verifies defense-in-depth network security across all 5 infrastructure devices.

```
+-------------------------------------------------------------------------------+
|                       DEFENSE-IN-DEPTH SECURITY MATRIX                        |
+-------------------------------------------------------------------------------+
| Layer 7: Application & Management | SSHv2 Enforced, RSA 2048-bit, Legal MOTD   |
| Layer 3: Control Plane Protection | AAA Priv 15, Inactivity Timeouts, OSPF Auth|
| Layer 2: Switching Hardening      | Native VLAN 999, Rapid-PVST+, PortFast    |
| Layer 1: Physical Port Security   | Sticky MACs, Max 2 Devices, Restrict Mode |
| Parking Lot Security             | Unused Ports Disabled into Blackhole VLAN  |
+-------------------------------------------------------------------------------+
```

### A. Management Plane Hardening
1. **SSH Version 2 Mandatory Enforcement:**
   - Insecure Telnet is completely disabled (`transport input ssh` on VTY lines `0 4` and `5 15`).
   - Dedicated RSA 2048-bit modulus key generated.
   - SSH parameters: Timeout set to 60 seconds, max 3 authentication retries.
2. **Privileged AAA Credentials:**
   - Account `netadmin` created with maximum privilege level 15 and secret hashing.
   - `enable secret cisco123` overrides default plaintext enable passwords.
   - `service password-encryption` obfuscates all stored passwords.
3. **Session & Physical Console Security:**
   - `exec-timeout 5 0` terminates idle sessions after 5 minutes.
   - `logging synchronous` prevents console output from interrupting active commands.
   - `no exec` and `transport input none` applied to auxiliary lines (`line aux 0`).
4. **Legal Warning MOTD Banner:**
   - Explicit warning of authorized access only, continuous monitoring, and criminal prosecution under cyber laws.

### B. Layer 2 & Access Layer Security
1. **Switchport Port Security:**
   - Enabled on all active access ports (`Fa0/1`, `Fa0/2`, `Fa0/10`, `Fa0/20`).
   - Maximum MAC addresses per port: **2**.
   - Violation mode: **`restrict`** (drops unauthorized traffic, sends SNMP trap / syslog notification, and increments violation counter without dropping legitimate traffic).
   - Dynamic MAC learning: **`mac-address sticky`** dynamically binds the connected host's MAC address to the running configuration.
2. **Spanning Tree Protocol (STP) Hardening:**
   - High-speed **Rapid-PVST+** (`spanning-tree mode rapid-pvst`) eliminates standard 30-50 second STP convergence delays.
   - **PortFast** (`spanning-tree portfast`) enabled on all host-facing ports to transition directly to forwarding state.
3. **VLAN Hopping & Double-Tagging Mitigation:**
   - Default Native VLAN 1 is stripped from all 802.1Q trunks and replaced with inactive **VLAN 999** (`switchport trunk native vlan 999`).
4. **Unused Switchport Blackholing (Parking Lot):**
   - Inactive switchports (`Fa0/3 - 23` on access switches; `Fa0/4 - 9`, `Fa0/11 - 19`, `Fa0/21 - 23` on distribution) are explicitly disabled (`shutdown`) and assigned to dead VLAN 999.

---

## 2. Security Verification & Test Evidence

### A. SSH Version 2 Verification (`show ip ssh`)
```text
R1-Core# show ip ssh
SSH Enabled - version 2.0
Authentication timeout: 60 secs; Authentication retries: 3
```

### B. Active Admin SSH Session (`show users`)
```text
R1-Core# show users
    Line       User       Host(s)              Idle       Location
 *  0 vty 0    netadmin   idle                 00:00:00   192.168.99.50
```

### C. Port Security Status (`show port-security interface Fa0/1`)
```text
SW2-Eng# show port-security interface FastEthernet 0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Restrict
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 1
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : 0001.96D2.32A1:10
Security Violation Count   : 0
```

### D. Unused Ports Parking Lot Verification (`show interfaces status`)
```text
SW2-Eng# show interfaces status
Port      Name               Status       Vlan       Duplex  Speed Type
Fa0/1     Eng Workstation 01 connected    10         a-full  a-100 10/100BaseTX
Fa0/2     Eng Workstation 02 connected    10         a-full  a-100 10/100BaseTX
Fa0/3     Unused Port        disabled     999          auto   auto 10/100BaseTX
...
Fa0/23    Unused Port        disabled     999          auto   auto 10/100BaseTX
Fa0/24    Trunk Uplink       connected    trunk      a-full  a-100 10/100BaseTX
```

---

## 3. Automated Security Compliance Audit

Running `scripts/verify_network.py` validates that all 5 devices pass 100% of security checks:

```text
                Device Configuration Security & Compliance Audit                
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Device         ┃ Role           ┃ Checks Passed ┃     Compliance ┃ Status    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ R1-Core        │ CORE_ROUTER    │    13 / 13    │         100.0% │ COMPLIANT │
│ SW1-Dist       │ DISTRIBUTION_… │    14 / 14    │         100.0% │ COMPLIANT │
│ SW2-Eng        │ ACCESS_SWITCH  │    14 / 14    │         100.0% │ COMPLIANT │
│ SW3-HR         │ ACCESS_SWITCH  │    14 / 14    │         100.0% │ COMPLIANT │
│ SW4-Sales      │ ACCESS_SWITCH  │    14 / 14    │         100.0% │ COMPLIANT │
└────────────────┴────────────────┴───────────────┴────────────────┴───────────┘
```

---

## 4. Review Checklist for Milestone 05
- [x] Insecure Telnet disabled; SSHv2 enforced with RSA 2048-bit keys across all devices.
- [x] Privilege 15 local authentication and encrypted passwords configured.
- [x] Port security configured with sticky MACs and restrict violation mode.
- [x] Native VLAN isolated to 999 and unused ports shutdown into blackhole VLAN.
- [x] 100% score achieved in automated security compliance audit.
