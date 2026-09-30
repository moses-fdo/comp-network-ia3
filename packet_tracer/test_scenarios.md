# Comprehensive Test Scenarios & Verification Playbook

This document provides formal test cases for demonstrating and evaluating the **Python-Based Network Configuration Automation** system. Each test scenario includes the objective, execution commands, expected outputs, and rubric mapping.

---

## Summary Matrix of Test Scenarios

| Test ID | Test Scenario | Objective | Devices Involved | Rubric Component |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | DHCP Address Allocation | Verify dynamic IP assignment for departmental VLANs | R1-Core, PCs (10, 20, 30) | Routing & Connectivity |
| **TC-02** | Intra-VLAN Switching | Verify high-speed Layer 2 forwarding within same VLAN | PC-Eng1, PC-Eng2 | Topology & Design |
| **TC-03** | Inter-VLAN Routing (ROAS) | Verify 802.1Q subinterface routing across departments | PC-Eng1, PC-HR1, PC-Sales1 | Routing & Connectivity |
| **TC-04** | 802.1Q Trunking & Native VLAN | Verify trunk allowed list and Native VLAN 999 | R1-Core, SW1-Dist, SW2-4 | Device Configuration |
| **TC-05** | Port Security Enforcement | Validate MAC limiting and sticky MAC addresses | Access Switches, Host PCs | Device Configuration |
| **TC-06** | Secure SSH Remote Access | Verify SSHv2 encryption and local AAA credentials | Admin-PC, All 5 Cisco Devices | Device Configuration |
| **TC-07** | TFTP Config Archival | Validate backup transfer to central repository | All Cisco Devices, TFTP Server | Simulation & Demo |
| **TC-08** | Rapid-PVST+ Convergence | Verify Spanning Tree root bridge & loop prevention | SW1-Dist (Root), SW2,3,4 | Topology & Design |
| **TC-09** | Parking Lot Port Isolation | Confirm unused switchports are shutdown in VLAN 999 | All Catalyst 2960 Switches | Device Configuration |
| **TC-10** | Enterprise Routing & OSPF | Validate routing table convergence and default routes | R1-Core | Routing & Connectivity |

---

## Detailed Test Cases

### TC-01: DHCP Address Allocation
- **Objective:** Verify that end hosts in VLANs 10, 20, and 30 obtain valid IP configurations automatically from `R1-Core`.
- **Steps:**
  1. Open `PC-Eng1` -> Desktop -> IP Configuration -> Click **DHCP**.
  2. Open `PC-HR1` -> Desktop -> IP Configuration -> Click **DHCP**.
  3. Open `PC-Sales1` -> Desktop -> IP Configuration -> Click **DHCP**.
- **Verification Command (on R1-Core):**
  ```ios
  R1-Core# show ip dhcp binding
  ```
- **Expected Output:**
  ```text
  IP address       Client-ID/              Lease expiration        Type
                   Hardware address
  192.168.10.10    0001.96D2.32A1          --                      Automatic
  192.168.20.10    0001.96D2.32B2          --                      Automatic
  192.168.30.10    0001.96D2.32C3          --                      Automatic
  ```
- **Status:** **PASS**

---

### TC-02: Intra-VLAN Layer 2 Switching
- **Objective:** Validate wire-speed packet forwarding between hosts located in the same broadcast domain without router involvement.
- **Steps:**
  1. Open Command Prompt on `PC-Eng1` (`192.168.10.10`).
  2. Ping second workstation `PC-Eng2` (`192.168.10.11`).
- **Command:**
  ```cmd
  ping 192.168.10.11
  ```
- **Expected Output:**
  ```text
  Pinging 192.168.10.11 with 32 bytes of data:
  Reply from 192.168.10.11: bytes=32 time<1ms TTL=128
  Reply from 192.168.10.11: bytes=32 time<1ms TTL=128
  Reply from 192.168.10.11: bytes=32 time<1ms TTL=128
  Reply from 192.168.10.11: bytes=32 time<1ms TTL=128
  Ping statistics for 192.168.10.11:
      Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
  ```
- **Status:** **PASS**

---

### TC-03: Inter-VLAN Layer 3 Routing (ROAS)
- **Objective:** Verify that `R1-Core` routes traffic across distinct VLANs via 802.1Q subinterfaces.
- **Steps:**
  1. From `PC-Eng1` (`192.168.10.10`), ping HR host `PC-HR1` (`192.168.20.10`).
  2. From `PC-Eng1`, execute traceroute to Sales host `PC-Sales1` (`192.168.30.10`).
- **Commands:**
  ```cmd
  ping 192.168.20.10
  tracert 192.168.30.10
  ```
- **Expected Output:**
  ```text
  Tracing route to 192.168.30.10 over a maximum of 30 hops:
    1   <1 ms   <1 ms   <1 ms   192.168.10.1 (R1-Core Subinterface)
    2    1 ms    1 ms    1 ms   192.168.30.10 (PC-Sales1)
  Trace complete.
  ```
- **Status:** **PASS**

---

### TC-04: 802.1Q Trunking & Native VLAN Hardening
- **Objective:** Verify that inter-switch links and router uplinks operate in 802.1Q trunk mode with restricted VLAN lists and isolated native VLAN 999.
- **Command (on SW1-Dist):**
  ```ios
  SW1-Dist# show interfaces trunk
  ```
- **Expected Output:**
  ```text
  Port        Mode         Encapsulation  Status        Native vlan
  Gig0/1      on           802.1q         trunking      999
  Fa0/1       on           802.1q         trunking      999
  Fa0/2       on           802.1q         trunking      999
  Fa0/3       on           802.1q         trunking      999

  Port        Vlans allowed on trunk
  Gig0/1      10,20,30,40,99
  Fa0/1       10,20,30,40,99
  Fa0/2       10,20,30,40,99
  Fa0/3       10,20,30,40,99
  ```
- **Status:** **PASS**

---

### TC-05: Switchport Port Security Enforcement
- **Objective:** Confirm MAC address binding, maximum address limits, and violation restrictions on access ports.
- **Command (on SW2-Eng):**
  ```ios
  SW2-Eng# show port-security interface FastEthernet 0/1
  ```
- **Expected Output:**
  ```text
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
- **Status:** **PASS**

---

### TC-06: In-Band Remote SSHv2 Access
- **Objective:** Verify that devices refuse insecure Telnet and mandate SSH v2 authentication with local credentials.
- **Steps:**
  1. From `Admin-PC`, run:
     ```cmd
     ssh -l netadmin 192.168.99.1
     ```
  2. Input password `Cisco@123!`.
- **Command (on R1-Core):**
  ```ios
  R1-Core# show ip ssh
  R1-Core# show users
  ```
- **Expected Output:**
  ```text
  SSH Enabled - version 2.0
  Authentication timeout: 60 secs; Authentication retries: 3

      Line       User       Host(s)              Idle       Location
   *  0 vty 0    netadmin   idle                 00:00:00   192.168.99.50
  ```
- **Status:** **PASS**

---

### TC-07: Centralized TFTP Configuration Archival
- **Objective:** Verify automated archival of running configs to `TFTP-Server` (`192.168.40.10`).
- **Command (on SW1-Dist):**
  ```ios
  SW1-Dist# copy running-config tftp://192.168.40.10/SW1-Dist-backup.cfg
  ```
- **Expected Output:**
  ```text
  Writing SW1-Dist-backup.cfg...!!
  [OK - 5679 bytes]
  5679 bytes copied in 0.082 secs
  ```
- **Verification on TFTP Server:**
  Open `TFTP-Server` -> **Services** -> **TFTP** -> Verify file `SW1-Dist-backup.cfg` exists in storage.
- **Status:** **PASS**

---

### TC-08: Spanning Tree Protocol (Rapid-PVST+) Topology
- **Objective:** Verify that `SW1-Dist` acts as Root Bridge for all enterprise VLANs and secondary switches maintain alternate blocking links.
- **Command (on SW1-Dist):**
  ```ios
  SW1-Dist# show spanning-tree vlan 10
  ```
- **Expected Output:**
  ```text
  VLAN0010
    Spanning tree enabled protocol rstp
    Root ID    Priority    24586
               Address     000A.41AA.B101
               This bridge is the root
               Hello Time  2 sec  Max Age 20 sec  Forward Delay 15 sec
  ```
- **Status:** **PASS**

---

### TC-09: Unused Switchport Security Isolation
- **Objective:** Verify that inactive switchports are disabled (`shutdown`) and assigned to parking lot VLAN 999.
- **Command (on SW2-Eng):**
  ```ios
  SW2-Eng# show interfaces status
  ```
- **Expected Output:**
  ```text
  Port      Name               Status       Vlan       Duplex  Speed Type
  Fa0/1     Eng Workstation 01 connected    10         a-full  a-100 10/100BaseTX
  Fa0/2     Eng Workstation 02 connected    10         a-full  a-100 10/100BaseTX
  Fa0/3     Unused Port        disabled     999          auto   auto 10/100BaseTX
  ...
  Fa0/23    Unused Port        disabled     999          auto   auto 10/100BaseTX
  Fa0/24    Trunk Uplink       connected    trunk      a-full  a-100 10/100BaseTX
  ```
- **Status:** **PASS**

---

### TC-10: Enterprise Routing Table Verification
- **Objective:** Confirm that `R1-Core` routing table maintains direct connected routes for all VLAN subinterfaces and a valid default gateway route.
- **Command (on R1-Core):**
  ```ios
  R1-Core# show ip route
  ```
- **Expected Output:**
  ```text
  Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
         O - OSPF, IA - OSPF inter area, N1 - OSPF NSSA external type 1

  Gateway of last resort is 203.0.113.2 to network 0.0.0.0

  S*    0.0.0.0/0 [1/0] via 203.0.113.2
        192.168.10.0/24 is subnetted, 1 subnets
  C        192.168.10.0 is directly connected, GigabitEthernet0/0.10
        192.168.20.0/24 is subnetted, 1 subnets
  C        192.168.20.0 is directly connected, GigabitEthernet0/0.20
        192.168.30.0/24 is subnetted, 1 subnets
  C        192.168.30.0 is directly connected, GigabitEthernet0/0.30
        192.168.40.0/24 is subnetted, 1 subnets
  C        192.168.40.0 is directly connected, GigabitEthernet0/0.40
        192.168.99.0/24 is subnetted, 1 subnets
  C        192.168.99.0 is directly connected, GigabitEthernet0/0.99
        203.0.113.0/30 is subnetted, 1 subnets
  C        203.0.113.0 is directly connected, GigabitEthernet0/1
  ```
- **Status:** **PASS**
