# Milestone 09: Documentation & Presentation

**Scheduled Date:** 23-10-2026  
**Status:** `READY FOR FACULTY REVIEW`  
**Deliverable Focus:** Master Project Report, PPT Presentation Deck, Packet Tracer (.pkt) Assets, and Demo Materials  

---

## 1. Documentation & Media Inventory

This milestone packages all academic deliverables required for formal evaluation and project defense.

```
comp-network-ia3/
├── PROJECT_REPORT.md              <-- Master Academic Report (40/40 Marks Rubric)
├── PRESENTATION_SLIDES.md         <-- 15-Slide Presentation Deck + Speaker Notes
├── NETACAD_CERTIFICATION_GUIDE.md <-- Cisco Certification Submission Dossier
│
├── packet_tracer/                 <-- Packet Tracer Simulation Assets
│   ├── PACKET_TRACER_GUIDE.md     <-- Step-by-Step Lab Setup Walkthrough
│   ├── topology_diagram.txt       <-- ASCII Topology & Wiring Matrix
│   └── test_scenarios.md          <-- 10 Formal Test Scenarios with Expected Outputs
│
├── output_configs/                <-- Cisco IOS Configuration Bundle
│   ├── R1-Core.cfg                <-- Core Router 802.1Q ROAS & DHCP
│   ├── SW1-Dist.cfg               <-- Catalyst 2960 Distribution Switch
│   ├── SW2-Eng.cfg                <-- Catalyst 2960 Engineering Switch
│   ├── SW3-HR.cfg                 <-- Catalyst 2960 HR Switch
│   ├── SW4-Sales.cfg              <-- Catalyst 2960 Sales Switch
│   └── all_devices_paste.txt      <-- 1-Click Consolidated Paste File
│
└── tftp_storage/                  <-- Verified Centralized TFTP Archives
```

---

## 2. Key Deliverable Links

1. **Master Technical Report:**  
   [PROJECT_REPORT.md](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/PROJECT_REPORT.md) — Comprehensive 40-mark report covering Scenario Analysis, Topology Design, VLSM Subnetting, Device Configurations, Routing Tests, and NetAcad Certifications.
2. **Slide Deck & Presentation Script:**  
   [PRESENTATION_SLIDES.md](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/PRESENTATION_SLIDES.md) — 15 professional presentation slides equipped with slide-by-slide speaker notes, talking points, and anticipated examiner Q&A answers.
3. **Cisco Packet Tracer Setup Playbook:**  
   [packet_tracer/PACKET_TRACER_GUIDE.md](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/packet_tracer/PACKET_TRACER_GUIDE.md) — Lab building manual covering hardware dragging, cabling, IP setups, and test commands.
4. **Packet Tracer Consolidated Paste Bundle:**  
   [output_configs/all_devices_paste.txt](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/output_configs/all_devices_paste.txt) — Clean, pre-compiled Cisco IOS configurations ready for copy-pasting directly into Packet Tracer CLI.
5. **Formal Verification Test Cases:**  
   [packet_tracer/test_scenarios.md](file:///mnt/win-newvol/Projects/GitHub/comp-network-ia3/packet_tracer/test_scenarios.md) — 10 structured test cases covering DHCP, Intra-VLAN switching, ROAS, Trunking, Port Security, SSHv2, and TFTP.

---

## 3. Demonstration Script for Viva / Presentation

Use this 5-minute timed script during the capstone demonstration:

- **Minute 1: The Automation Value Proposition:**
  > *"Respected evaluators, manual configuration of enterprise networks takes hours and is error-prone. Our solution defines the network state in CSV data models and automates Cisco IOS configuration generation using Python and Jinja2."*
- **Minute 2: Configuration Generation in 1 Second:**
  > *"Notice how running `python scripts/generate_configs.py` parses our inventory and instantly compiles over 760 lines of hardened Cisco IOS configuration across 5 devices in under a second."*
- **Minute 3: Packet Tracer Topology & Inter-VLAN Routing:**
  > *"In Packet Tracer, our Core Router dynamically provisions IP leases to VLANs 10, 20, and 30 using DHCP pools. Notice that when PC-Eng1 pings PC-HR1, traffic is seamlessly routed across 802.1Q subinterfaces."*
- **Minute 4: Security Hardening & 100% Audit Score:**
  > *"All devices enforce SSHv2 with RSA 2048-bit keys, sticky MAC port security, and Rapid-PVST+. Running `verify_network.py` validates that 100% of our security baselines are satisfied."*
- **Minute 5: TFTP Disaster Recovery & Conclusion:**
  > *"Finally, running `backup_tftp.py` exports running configurations directly to our central TFTP server (192.168.40.10). Every team member has completed the Cisco NetAcad Networking Basics course. Thank you!"*

---

## 4. Review Checklist for Milestone 09
- [x] Publication-quality report completed and formatted for PDF export.
- [x] 15-slide presentation deck with speaker notes and Q&A cheat sheet finalized.
- [x] Complete Packet Tracer demo bundle and consolidated paste file verified.
- [x] All materials organized in repository for faculty evaluation.
