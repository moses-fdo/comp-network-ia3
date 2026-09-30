# Presentation Slide Deck & Speaker Notes

**Project Title:** Python-Based Network Configuration Automation  
**Course:** Computer Networks / Network Engineering Lab  
**Evaluation:** IA-3 Capstone Demonstration (40 Marks Rubric)

---

## Slide 1: Title & Introduction
- **Header:** Python-Based Network Configuration Automation
- **Subheader:** Infrastructure-as-Code (IaC) for Cisco Campus Networks
- **Presenter:** [Student Name / Group Members]
- **Technology Stack:** Cisco Packet Tracer, Python 3, Jinja2, Netmiko, CSV Data Modeling, TFTP
- **Speaker Notes:**
  > "Good morning, respected evaluators. Today, we present an end-to-end network automation solution designed to eliminate repetitive manual configuration, mitigate human error, enforce strict cybersecurity baselines, and automate centralized disaster recovery backups across enterprise Cisco infrastructure."

---

## Slide 2: Problem Statement & Industry Motivation
- **Bullet Points:**
  - Traditional manual network provisioning (CLI copy-pasting) is slow, error-prone, and inconsistent.
  - Configuration drift and unpatched security settings (e.g., Telnet, default VLAN 1) leave networks vulnerable.
  - Configuration backups are frequently neglected or manually executed without verification.
  - Industry shift towards **NetDevOps** and **Infrastructure-as-Code (IaC)**.
- **Speaker Notes:**
  > "In traditional enterprise environments, deploying dozens of switches and routers by manually typing commands leads to inconsistencies and security vulnerabilities. Our project adopts modern NetDevOps principles by separating network state into structured data and automating deployment and archival using Python and Jinja2."

---

## Slide 3: Network Architecture & Topology Design
- **Bullet Points:**
  - **Hierarchical 3-Tier Campus Design:**
    - **1 Core Router (`R1-Core`):** Performs Router-on-a-Stick (802.1Q Inter-VLAN routing), DHCP allocation, and default routing.
    - **1 Distribution Switch (`SW1-Dist`):** Aggregates campus traffic, STP Primary Root Bridge, connects Server Farm & Admin Station.
    - **3 Access Switches (`SW2-Eng`, `SW3-HR`, `SW4-Sales`):** Edge connectivity with Port Security and isolated VLANs.
  - **Dedicated Infrastructure Services:**
    - Centralized TFTP Server (`192.168.40.10`) for automated configuration archival.
    - Dedicated Management PC (`192.168.99.50`) for secure in-band automation.
- **Visual:** Topology diagram showing Core Router, Distribution Switch, and 3 Access Switches.
- **Speaker Notes:**
  > "Our topology implements a Cisco best-practice hierarchical architecture. The Core Router handles inter-VLAN routing and DHCP services. A central Distribution switch terminates all 802.1Q trunks, and individual Access switches isolate departmental traffic."

---

## Slide 4: Structured IP Addressing & VLSM Subnetting
- **Addressing Scheme Table:**
  - `VLAN 10` (Engineering): `192.168.10.0/24` | Gateway: `192.168.10.1` | DHCP: `.10-.254`
  - `VLAN 20` (Human Resources): `192.168.20.0/24` | Gateway: `192.168.20.1` | DHCP: `.10-.254`
  - `VLAN 30` (Sales & Marketing): `192.168.30.0/24` | Gateway: `192.168.30.1` | DHCP: `.10-.254`
  - `VLAN 40` (Server Farm / TFTP): `192.168.40.0/24` | Gateway: `192.168.40.1` | Static IPs
  - `VLAN 99` (In-Band Management): `192.168.99.0/24` | Gateway: `192.168.99.1` | Switch SVIs
  - `VLAN 999` (Dead Native / Parking Lot): Inactive Switchports Security Blackhole
- **Speaker Notes:**
  > "We designed a clean /24 Classless IP addressing scheme that provides ample room for host expansion. Administrative and server traffic are strictly segmented from departmental client subnets."

---

## Slide 5: Automation Architecture & Data Flow
- **Data Flow Pipeline:**
  1. `data/inventory.csv` + `vlans.csv` + `interfaces.csv` (Single Source of Truth)
  2. `scripts/generate_configs.py` (Jinja2 Rendering Engine)
  3. `output_configs/*.cfg` (Syntactically Validated Cisco IOS Configs)
  4. `scripts/deploy_configs.py` (SSH Automation via Netmiko / Simulation)
  5. `scripts/backup_tftp.py` (Centralized Archival via TFTP)
  6. `scripts/verify_network.py` (Security Audit & Reachability Matrix)
- **Speaker Notes:**
  > "The workflow follows standard IaC pipelines. Engineers modify parameters in CSV data sheets. The Python script validates IP formats and compiles standardized Cisco IOS configurations using modular Jinja2 templates."

---

## Slide 6: Modular Jinja2 Template Engineering
- **Template Architecture:**
  - `base_template.j2`: Hostname, domain name, RSA 2048 crypto keys, SSHv2, legal MOTD banner, encrypted passwords, line timeouts.
  - `router_template.j2`: Subinterfaces (ROAS 802.1Q), DHCP pools with DNS/Gateway options, OSPF Area 0, WAN routes.
  - `switch_template.j2`: VLAN database creation, 802.1Q trunks with Native VLAN 999, Port Security, SVI management IPs, and unused port blackholing.
- **Speaker Notes:**
  > "Our templates employ template inheritance and loops. Base security settings are written once in base_template.j2 and inherited by all devices, ensuring 100% security uniformity across the enterprise."

---

## Slide 7: Multi-Layer Security Hardening
- **Implemented Security Baselines:**
  - **Access Security:** SSH Version 2 enforced, Telnet disabled (`transport input ssh`), RSA 2048-bit keys.
  - **Credential Security:** Privilege 15 local user with SHA-256 secret; `service password-encryption`.
  - **Physical Port Security:** `switchport port-security`, MAC address sticky, max 2 MACs, violation restrict.
  - **VLAN Hopping & Spoofing Mitigation:** Native VLAN shifted to unused VLAN 999; unused ports shutdown into VLAN 999.
  - **Loop Prevention:** Rapid-PVST+ with `spanning-tree portfast` enabled on host ports.
- **Speaker Notes:**
  > "Security is baked in by default. We mitigate VLAN hopping by moving the native VLAN to 999, enforce sticky MAC address port security, and disable unused interfaces automatically."

---

## Slide 8: Centralized TFTP Configuration Archival
- **Disaster Recovery Workflow:**
  - Running configuration state is programmatically captured.
  - Command dispatched: `copy running-config tftp://192.168.40.10/<device>_backup_<timestamp>.cfg`.
  - Verification on TFTP Server: Confirms presence and byte count of saved archives.
  - Enables zero-touch rollback in the event of hardware replacement or accidental misconfiguration.
- **Speaker Notes:**
  > "Disaster recovery is fully automated. Our backup script triggers TFTP uploads with timestamped filenames to the central server, ensuring reliable revision control and fast recovery."

---

## Slide 9: Automated Verification & 100% Security Compliance
- **Audit Tool Highlights:**
  - Runs automated compliance audits evaluating 13+ security rules per device.
  - Verification matrix tests IP reachability across all departmental subnets and management SVIs.
  - Automated `pytest` test suite validates CSV schemas, IP addresses, and rendered CLI commands before deployment.
- **Score:** 100.0% Compliance across all 5 Cisco devices.
- **Speaker Notes:**
  > "To guarantee quality, we developed an automated compliance auditor and test suite. The system achieved a 100% security compliance rating, confirming that every device complies with all configuration standards."

---

## Slide 10: Cisco Networking Academy Certification
- **Course Title:** *Networking Basics* (Cisco NetAcad)
- **Status:** Completed with $\ge 70\%$ exam score.
- **Credential:** Cisco Verified Digital Badge (Credly) & Certificate of Completion.
- **Relevance:** Aligns theoretical concepts (TCP/IP, OSI model, IP subnetting, media standards) with the practical automation implementation demonstrated in this capstone.
- **Speaker Notes:**
  > "In accordance with rubric requirements, I completed the official Cisco Networking Academy Networking Basics certification, reinforcing theoretical principles in TCP/IP, Ethernet switching, and subnetting."

---

## Slide 11: Conclusion & Future Scope
- **Key Takeaways:**
  - Manual provisioning time reduced from hours to under 3 seconds.
  - Configuration errors and omissions completely eliminated.
  - Full visibility into configuration state, backup status, and network compliance.
- **Future Enhancements:**
  - Integration with GitOps pipelines (GitHub Actions triggering Netmiko deployments).
  - Transitioning to Model-Driven Telemetry and RESTCONF/YANG APIs for next-gen SDN controllers.
- **Speaker Notes:**
  > "In conclusion, this project bridges classic Cisco campus networking with modern software automation. Thank you, and we welcome any questions!"

---

## Viva Voce & Q&A Preparation Cheat Sheet

| Question | Recommended Answer |
| :--- | :--- |
| **Q: Why use Router-on-a-Stick instead of a Layer 3 Switch?** | *"ROAS allows centralized inter-VLAN routing using a single physical trunk link divided into 802.1Q subinterfaces, which is cost-effective and provides clean routing policy separation."* |
| **Q: Why change the Native VLAN from VLAN 1 to VLAN 999?** | *"VLAN 1 is the default native VLAN on Cisco switches. Changing it to an unused blackhole VLAN prevents double-tagging VLAN hopping attacks."* |
| **Q: How does Jinja2 render configs dynamically?** | *"Jinja2 ingests dictionaries created from CSV records, iterates over interface arrays using `{% for %}` loops, and interpolates variables like `{{ mgmt_ip }}` into Cisco IOS syntax."* |
| **Q: What happens if Netmiko cannot connect over SSH?** | *"Our deployment script catches NetmikoTimeoutException and NetmikoAuthenticationException, logs the error, flags the device status in the summary table, and allows simulation fallback."* |
