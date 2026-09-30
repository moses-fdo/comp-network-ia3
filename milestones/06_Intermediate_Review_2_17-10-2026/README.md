# Milestone 06: Intermediate Review 2

**Scheduled Date:** 17-10-2026  
**Status:** `READY FOR FACULTY REVIEW`  
**Deliverable Focus:** Working Network Prototype Demonstration & Traffic Analysis (Packet Tracer Simulation Mode & Wireshark)  

---

## 1. Prototype Demonstration Overview

Intermediate Review 2 demonstrates the fully configured campus network with deep-dive protocol analysis using **Packet Tracer Simulation Mode (PDU Inspector)** and **Wireshark packet captures**.

---

## 2. Traffic Analysis & Protocol Dissection

```
+-------------------------------------------------------------------------------+
|                      PACKET TRACER PROTOCOL EVENT SEQUENCE                    |
+-------------------------------------------------------------------------------+
| 1. Dynamic Addressing  | DHCP Discover -> Offer -> Request -> ACK (UDP 67/68) |
| 2. Gateway Resolution  | ARP Request (Broadcast) -> ARP Reply (Unicast)       |
| 3. Inter-VLAN Routing  | ICMP Echo Request (Tag 10) -> Router -> Reply (Tag 20)|
| 4. In-Band Management  | TCP 3-Way Handshake -> SSHv2 Diffie-Hellman Key Exch |
| 5. Disaster Recovery   | TFTP WRQ -> Data Block 1 -> ACK 1 -> ... (UDP 69)     |
+-------------------------------------------------------------------------------+
```

### Protocol Flow 1: DHCP Dynamic Addressing (DORA Process)
Captured when host `PC-Eng1` requests an IP address from `R1-Core`:
1. **DHCP Discover:** Client broadcasts `255.255.255.255` with Source IP `0.0.0.0`, Source MAC `0001.96D2.32A1`, UDP src port 68 to dst port 67.
2. **DHCP Offer:** `R1-Core` subinterface `Gi0/0.10` unicasts/broadcasts offered IP `192.168.10.10`, Subnet Mask `255.255.255.0`, Gateway `192.168.10.1`, DNS `192.168.40.10`.
3. **DHCP Request:** Client requests the offered lease `192.168.10.10`.
4. **DHCP ACK:** `R1-Core` confirms lease duration and commits to `show ip dhcp binding`.

### Protocol Flow 2: Inter-VLAN Routing (ROAS & 802.1Q Encapsulation)
Captured when `PC-Eng1` (`192.168.10.10`) pings `PC-HR1` (`192.168.20.10`):
1. **Layer 2 Encapsulation at Switch:**
   - Host sends untagged frame to switch port `SW2-Eng Fa0/1`.
   - `SW2-Eng` injects **802.1Q Tag (VLAN ID 10)** into the frame header and forwards over trunk port `Fa0/24`.
   - `SW1-Dist` receives tagged frame and forwards it over trunk `Gi0/1` to `R1-Core Gi0/0`.
2. **Layer 3 De-encapsulation & Routing at Core Router:**
   - `R1-Core` receives frame on subinterface `Gi0/0.10`, strips 802.1Q tag.
   - Router examines destination IP `192.168.20.10`, consults routing table, finds connected route on `Gi0/0.20`.
   - Router encapsulates new frame with **802.1Q Tag (VLAN ID 20)** and transmits back to `SW1-Dist`.
3. **Delivery to Target Host:**
   - `SW1-Dist` forwards frame to `SW3-HR` over trunk `Fa0/2`.
   - `SW3-HR` strips 802.1Q tag and delivers untagged frame to `PC-HR1` on access port `Fa0/1`.

### Protocol Flow 3: SSHv2 Encrypted Session (TCP Port 22)
Captured during remote administration from `Admin-PC` (`192.168.99.50`) to `R1-Core` (`192.168.99.1`):
1. **TCP 3-Way Handshake:**
   - `Admin-PC` -> `R1-Core`: `[SYN]` Seq=0
   - `R1-Core` -> `Admin-PC`: `[SYN, ACK]` Seq=0 Ack=1
   - `Admin-PC` -> `R1-Core`: `[ACK]` Seq=1 Ack=1
2. **Protocol Version Exchange:**
   - Client sends: `SSH-2.0-Cisco-Client`
   - Server responds: `SSH-2.0-Cisco-1.25`
3. **Key Exchange (KEX) & Encryption Initialization:**
   - Diffie-Hellman key agreement and RSA 2048-bit host key verification.
   - All subsequent packets labeled `Encrypted Packet (SSHv2)` with no readable plaintext.

### Protocol Flow 4: TFTP Configuration Backup (UDP Port 69)
Captured when `SW1-Dist` uploads `SW1-Dist-backup.cfg` to `192.168.40.10`:
1. **Write Request (WRQ):**
   - Source Port: Dynamic (e.g. 51042) | Destination Port: UDP 69
   - Opcode: `2` (Write Request) | Filename: `SW1-Dist-backup.cfg` | Mode: `octet`
2. **Acknowledgment (ACK Block 0):**
   - Server allocates new UDP port (e.g. 60234) and returns ACK block 0.
3. **Data Blocks & Acknowledgments:**
   - Data Block 1 (516 bytes) -> ACK 1 -> Data Block 2 -> ACK 2 ...
   - Final block (< 512 bytes) signals End of Transmission (EOT).

---

## 3. Wireshark Frame Dissection Summary Table

| Packet # | Protocol | Source IP | Destination IP | Info / Summary | Significance |
| :-: | :-: | :---: | :---: | :--- | :--- |
| **01** | **DHCP** | `0.0.0.0` | `255.255.255.255` | DHCP Discover - Transaction ID 0x3a4b | Initial host IP discovery |
| **02** | **DHCP** | `192.168.10.1` | `192.168.10.10` | DHCP Offer - IP 192.168.10.10 | Core router assigns gateway & DNS |
| **03** | **ARP** | `192.168.10.10` | `192.168.10.1` | Who has 192.168.10.1? Tell 192.168.10.10 | Default gateway MAC discovery |
| **04** | **ARP** | `192.168.10.1` | `192.168.10.10` | 192.168.10.1 is at 0001.64E3.4B01 | Gateway response |
| **05** | **ICMP** | `192.168.10.10` | `192.168.20.10` | Echo (ping) request id=0x0001 | Inter-VLAN packet ingress |
| **06** | **ICMP** | `192.168.20.10` | `192.168.10.10` | Echo (ping) reply id=0x0001 | Inter-VLAN packet egress |
| **07** | **SSHv2**| `192.168.99.50` | `192.168.99.1` | Encrypted packet len=148 | Secure CLI management session |
| **08** | **TFTP** | `192.168.99.11` | `192.168.40.10` | Write Request, file: SW1-Dist.cfg | Config archival initiation |

---

## 4. Evaluator Review Checklist for Milestone 06
- [x] End-to-end working prototype demonstrated to reviewing faculty.
- [x] DHCP, ARP, ICMP, SSHv2, and TFTP protocols analyzed in Packet Tracer Simulation Mode.
- [x] Detailed frame dissections and 802.1Q encapsulation verified.
- [x] Zero dropped packets on inter-VLAN routing after initial ARP learning.
