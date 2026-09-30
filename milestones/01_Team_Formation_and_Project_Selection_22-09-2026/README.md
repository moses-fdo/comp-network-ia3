# Milestone 01: Team Formation & Project Selection

**Scheduled Date:** 22-09-2026  
**Status:** `COMPLETED & APPROVED`  
**Deliverable Focus:** Team Structure, Roles, Selected Computer Networks Use Case, and Project Proposal  

---

## 1. Project Selection & Problem Statement

### Selected Project Title
**Python-Based Network Configuration Automation**

### Domain & Specialization
Computer Networks, Infrastructure-as-Code (IaC), Network Automation & NetDevOps, Cisco IOS Enterprise Switching & Routing.

### Problem Statement
In traditional network engineering, administrators manually configure switches and routers by connecting via serial console or terminal and manually typing commands. This manual approach presents critical challenges:
1. **Human Error & Syntax Inconsistency:** Typing repetitive commands leads to typos, misconfigured subnets, and incomplete security configurations.
2. **Configuration Drift:** Inconsistent configurations across devices make auditing and troubleshooting difficult.
3. **Slow Deployment Velocity:** Provisioning a 5-device campus topology manually takes hours; scaling to dozens of devices is infeasible.
4. **Neglected Disaster Recovery:** Running configurations are rarely backed up systematically, leading to long outage recovery times.

### Proposed Solution
An automated, template-driven network orchestration framework using:
- **Python 3** as the automation controller.
- **Jinja2** to build reusable, standardized Cisco IOS templates.
- **CSV Data Modeling** as the Single Source of Truth for network inventory, VLANs, and interfaces.
- **Netmiko (SSH)** for automated remote deployment.
- **Centralized TFTP Server** for automated configuration backups.
- **Automated Verification Engine** to validate reachability and enforce a 100% security baseline.

---

## 2. Team Composition & Role Allocation Matrix

| Role | Team Member | Student ID / Roll | Core Responsibilities |
| :--- | :--- | :--- | :--- |
| **Team Lead & Network Architect** | [Student Name 1] | [ID-001] | Campus topology design, VLSM IP scheme, ROAS routing, Packet Tracer `.pkt` file construction. |
| **Automation & Software Lead** | [Student Name 2] | [ID-002] | Python automation scripts (`generate_configs.py`, `deploy_configs.py`), Jinja2 template engineering, CSV parsing. |
| **Security & Auditing Lead** | [Student Name 3] | [ID-003] | Security hardening (SSHv2, AAA, Port Security, STP, MOTD), TFTP backup automation (`backup_tftp.py`), compliance checks (`verify_network.py`). |
| **Documentation & Quality Lead** | [Student Name 4] | [ID-004] | Technical project report, presentation deck, NetAcad certification coordination, test scenario verification. |

---

## 3. Technology Stack & Feasibility Analysis

| Component | Selected Technology | Feasibility Justification |
| :--- | :--- | :--- |
| **Simulation Platform** | Cisco Packet Tracer 8.x+ | Provides Cisco 2911 router, Catalyst 2960 switches, TFTP server, and realistic CLI environment. |
| **Automation Language**| Python 3.12+ | Rich networking ecosystem, robust standard library, native CSV and IP address validation. |
| **Templating Engine** | Jinja2 3.1.6 | Industry standard for network IaC, supports conditionals, loops, and template inheritance. |
| **SSH Automation** | Netmiko 4.8.0 / Paramiko | Multi-vendor network SSH automation with timing, prompt detection, and enable mode handling. |
| **Archival Protocol** | TFTP (UDP 69) | Standard lightweight protocol natively supported across all Cisco IOS routers and switches. |

---

## 4. Faculty Sign-Off & Approval Record

```text
[✓] Project Topic Approved
[✓] Team Roster & Role Distribution Verified
[✓] Scope Aligned with IA-3 Evaluation Rubrics (40 Marks)

Reviewing Faculty Signature: __________________________
Date of Approval: 22-09-2026
```
