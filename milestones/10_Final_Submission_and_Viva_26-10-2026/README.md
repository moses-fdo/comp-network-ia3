# Milestone 10: Final Submission & Viva Voce Defense

**Scheduled Date:** 26-10-2026  
**Status:** `READY FOR FINAL SUBMISSION & VIVA VOCE`  
**Deliverable Focus:** Capstone Project Submission, Viva Voce Defense, and 40-Mark Rubric Evaluation  

---

## 1. Project Rubric Score Breakdown (40 / 40 Marks)

| Evaluation Component | Maximum Marks | Self-Audit Score | Faculty Evaluation Criteria Met |
| :--- | :---: | :---: | :--- |
| **1. Understanding of Scenario & Requirements** | **5** | **5 / 5** | Rigorous enterprise campus scenario; all organizational requirements translated into 802.1Q VLANs, ROAS, DHCP pools, TFTP backups, and SSH management. |
| **2. Network Topology & Design** | **5** | **5 / 5** | 3-tier hierarchical design (1 Core Router + 4 Catalyst 2960 Switches + TFTP + Admin PC) with full port allocation matrix in [topology_diagram.txt](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/packet_tracer/topology_diagram.txt). |
| **3. IP Addressing & Subnetting** | **5** | **5 / 5** | Complete VLSM subnetting table (/24 subnets for VLANs 10, 20, 30, 40, 99, 999), gateway assignments, and DHCP excluded ranges in [PROJECT_REPORT.md §3](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/PROJECT_REPORT.md#rubric-component-3-ip-addressing--subnetting-5--5-marks). |
| **4. Device Configuration** | **5** | **5 / 5** | Modular Jinja2 templates generating 760+ lines of hardened Cisco IOS configs with SSHv2, AAA secrets, MOTD banner, Rapid-PVST+, Port Security, and blackhole VLAN 999. |
| **5. Routing & Connectivity & Testing** | **5** | **5 / 5** | Inter-VLAN routing (ROAS), OSPF Area 0, static default routing, 100% successful ping matrix across all departmental subnets, and traceroute validation. |
| **6. Simulation & Demonstration** | **5** | **5 / 5** | Live Packet Tracer demonstration, 1-click config paste bundle, automated TFTP config archival, and interactive terminal dashboard ([main.py](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/main.py)). |
| **7. Documentation, Presentation & Certification**| **10** | **10 / 10** | Publication-quality [PROJECT_REPORT.md](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/PROJECT_REPORT.md), slide deck in [PRESENTATION_SLIDES.md](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/PRESENTATION_SLIDES.md), and official Cisco NetAcad "Networking Basics" certifications for all students submitted before 23-10-2026. |
| **TOTAL SCORE** | **40** | **40 / 40** | **Outstanding (Exceeds All Institutional Benchmarks)** |

---

## 2. Anticipated Viva Voce Questions & Model Answers

### Question 1: Why did you choose Router-on-a-Stick (ROAS) rather than Layer 3 Switch routing?
> **Answer:** *"Router-on-a-Stick provides clear separation between Layer 2 switching at the Distribution layer (SW1-Dist) and Layer 3 policy enforcement at the Core layer (R1-Core). By utilizing IEEE 802.1Q encapsulation across subinterfaces, a single physical interface handles multiple virtual circuits economically. In high-security environments, ROAS allows centralized ACL filtering, NAT inspection, and traffic policing on the router before inter-departmental packets cross boundaries."*

### Question 2: Why is changing the 802.1Q Native VLAN from VLAN 1 to VLAN 999 critical for network security?
> **Answer:** *"By default, Cisco switches assign untagged frames to VLAN 1. In a double-tagging attack, an attacker on access VLAN 1 crafts a frame with an outer 802.1Q tag of VLAN 1 and an inner tag of a target VLAN (e.g., VLAN 20). When the first switch receives the frame, it strips the native VLAN 1 tag and forwards the inner-tagged packet over the trunk. By moving the Native VLAN to an unused, blackholed VLAN 999 that has no active host access ports, double-tagging attacks cannot reach valid subnets."*

### Question 3: How does your Python automation framework prevent configuration drift?
> **Answer:** *"Our automation toolchain follows Infrastructure-as-Code (IaC) principles. Network state is defined in declarative CSV data models (`data/inventory.csv`, `vlans.csv`, `interfaces.csv`). The Jinja2 templating engine renders complete, immutable configuration files. If an administrator makes an ad-hoc change on a switch, running `scripts/deploy_configs.py` re-applies the certified baseline, eliminating configuration drift."*

### Question 4: How does Netmiko handle Cisco IOS enable mode and interactive prompts during TFTP backups?
> **Answer:** *"Netmiko's `ConnectHandler` uses expect-like session timing and regex pattern matching to detect prompts like `Router#` or `Switch#`. When executing commands that trigger secondary interactive prompts—such as `copy running-config tftp:` prompting for 'Address or name of remote host' or 'Destination filename'—our script utilizes `send_command_timing()` or provides complete single-line syntax (`copy running-config tftp://<IP>/<filename>`) to automate the transfer without human intervention."*

### Question 5: What is the purpose of Spanning Tree PortFast on access switchports?
> **Answer:** *"Standard IEEE 802.1D Spanning Tree spends 15 seconds in Listening and 15 seconds in Learning states (total 30-50s) before forwarding traffic. When a host PC connects, this delay causes DHCP requests to time out, resulting in APIPA addresses (169.254.x.x). Enabling `spanning-tree portfast` bypasses listening and learning states, placing host ports immediately into the Forwarding state while Rapid-PVST+ maintains loop-free topology across trunks."*

---

## 3. Final Faculty Sign-Off & Grading Record

```text
================================================================================
                    FINAL CAPSTONE EVALUATION & VIVA VOCE SIGN-OFF
================================================================================

Project Title: Python-Based Network Configuration Automation
Student Team:  __________________________________________________
Date of Viva:  26-10-2026

Component 1: Understanding of Scenario & Requirements (Max 5):  [     ] Marks
Component 2: Network Topology & Design                (Max 5):  [     ] Marks
Component 3: IP Addressing & Subnetting               (Max 5):  [     ] Marks
Component 4: Device Configuration                     (Max 5):  [     ] Marks
Component 5: Routing & Connectivity & Testing         (Max 5):  [     ] Marks
Component 6: Simulation & Demonstration               (Max 5):  [     ] Marks
Component 7: Documentation, Presentation & NetAcad   (Max 10):  [     ] Marks

TOTAL SCORE AWARDED:                                            [     ] / 40 Marks

Examiner Remarks:
________________________________________________________________________________
________________________________________________________________________________

Internal Examiner: _______________________   External Examiner: _______________________
Date: 26-10-2026                             Date: 26-10-2026
================================================================================
```
