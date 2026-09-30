# Milestone 03: Intermediate Review 1

**Scheduled Date:** 01-10-2026  
**Status:** `READY FOR FACULTY REVIEW`  
**Deliverable Focus:** Network Design Defense & Initial Cisco Packet Tracer Topology Demonstration  

---

## 1. Review Objectives & Agenda

Intermediate Review 1 validates the theoretical foundation, architectural soundess, and preliminary implementation of the campus network.

### Review Agenda (15-Minute Session):
1. **Introduction & Requirement Analysis (3 mins):** Presentation of NovaCorp campus scenario and translation into networking requirements.
2. **Topology & Subnetting Walkthrough (4 mins):** Justification of the Three-Tier Hierarchical model, 802.1Q ROAS, and VLSM scheme.
3. **Packet Tracer Live Topology Demonstration (5 mins):** Live inspection of physical cabling, interface status, and initial device reachability.
4. **Faculty Q&A & Feedback (3 mins):** Reviewer questions and sign-off.

---

## 2. Demonstration Checklist for Evaluators

Staff can verify the initial Packet Tracer network by testing the following checkpoints:

| # | Inspection Item | Verification Method | Expected Result | Verified |
| :-: | :--- | :--- | :--- | :---: |
| **1** | **Device Inventory** | Inspect Packet Tracer workspace | 1x Router (2911), 4x Switches (2960), 1x Server, 7x PCs present | [ ] |
| **2** | **Physical Cabling** | Inspect port link lights | All interconnecting links show **green link lights** (no amber) | [ ] |
| **3** | **Trunk Link Encapsulation** | Run `show interfaces trunk` on `SW1-Dist` | Uplink to `R1-Core` and downlinks to `SW2,3,4` in 802.1Q trunking | [ ] |
| **4** | **Subinterface Status** | Run `show ip interface brief` on `R1-Core` | Subinterfaces `Gi0/0.10`, `.20`, `.30`, `.40`, `.99` are `up/up` | [ ] |
| **5** | **VLAN Database** | Run `show vlan brief` on switches | VLANs 10, 20, 30, 40, 99, 999 exist with standardized names | [ ] |
| **6** | **Static Server Configuration** | Open `TFTP-Server` desktop config | IP `192.168.40.10/24`, Gateway `192.168.40.1`, TFTP active | [ ] |

Step-by-step lab replication guide: [packet_tracer/PACKET_TRACER_GUIDE.md](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/packet_tracer/PACKET_TRACER_GUIDE.md)

---

## 3. Rubric Components Assessed in Review 1

| Rubric Component | Max Marks | Targeted Score | Evidence Presented |
| :--- | :---: | :---: | :--- |
| **Understanding of Scenario & Requirements** | **5** | **5 / 5** | Rigorous requirement breakdown in [PROJECT_REPORT.md §1](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/PROJECT_REPORT.md#rubric-component-1-understanding-of-scenario--requirements-5--5-marks). |
| **Network Topology & Design** | **5** | **5 / 5** | Clean hierarchical design, wiring matrix in [topology_diagram.txt](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/packet_tracer/topology_diagram.txt). |

---

## 4. Evaluator Feedback & Sign-Off Record

```text
Student Team: __________________________________________________
Review Date: 01-10-2026
Topology & Cabling Verification: [  ] Satisfactory  [  ] Good  [  ] Excellent
Addressing & VLSM Verification:  [  ] Satisfactory  [  ] Good  [  ] Excellent

Faculty Comments:
____________________________________________________________________________________
____________________________________________________________________________________

Faculty Evaluator Signature: __________________________
```
