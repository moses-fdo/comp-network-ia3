# Cisco Packet Tracer Lab Setup & Execution Guide

This comprehensive guide walks you through building, cabling, configuring, and testing the **Python-Based Network Configuration Automation** enterprise topology in **Cisco Packet Tracer (v8.x or later)**.

---

## 1. Required Hardware Devices in Packet Tracer

Open Cisco Packet Tracer and drag the following devices onto the workspace canvas:

| Device Role | Device Label / Hostname | Packet Tracer Model | Quantity | Notes |
| :--- | :--- | :--- | :---: | :--- |
| **Core Router** | `R1-Core` | **Cisco 2911** or **4331** | 1 | Provides Router-on-a-Stick (ROAS), DHCP server, and default gateway. |
| **Distribution Switch** | `SW1-Dist` | **Catalyst 2960-24TT** | 1 | Connects Core Router, Servers, and Access Switches. |
| **Engineering Access Switch** | `SW2-Eng` | **Catalyst 2960-24TT** | 1 | Access layer for Engineering / Dev VLAN 10. |
| **HR Access Switch** | `SW3-HR` | **Catalyst 2960-24TT** | 1 | Access layer for Human Resources VLAN 20. |
| **Sales Access Switch** | `SW4-Sales` | **Catalyst 2960-24TT** | 1 | Access layer for Sales / Marketing VLAN 30. |
| **Central TFTP Server** | `TFTP-Server` | **Server-PT (Generic)** | 1 | Archival repository for device running configs. |
| **Management PC** | `Admin-PC` | **PC-PT (Generic)** | 1 | Used for in-band SSH and network automation. |
| **End Host Workstations** | `PC-Eng1`, `PC-Eng2` | **PC-PT** | 2 | Engineering Dept test hosts (VLAN 10). |
| **End Host Workstations** | `PC-HR1`, `PC-HR2` | **PC-PT** | 2 | HR Dept test hosts (VLAN 20). |
| **End Host Workstations** | `PC-Sales1`, `PC-Sales2`| **PC-PT** | 2 | Sales Dept test hosts (VLAN 30). |

---

## 2. Physical Cabling & Port Interconnection Matrix

Connect the devices using standard **Copper Straight-Through** cables (Packet Tracer automatically handles Auto-MDIX). Follow this exact cabling table:

### A. Infrastructure Uplinks (Trunk Links)
| Source Device | Source Port | Target Device | Target Port | Link Type | Native VLAN |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `R1-Core` | **GigabitEthernet 0/0** | `SW1-Dist` | **GigabitEthernet 0/1** | 802.1Q Trunk | 999 |
| `SW1-Dist` | **FastEthernet 0/1** | `SW2-Eng` | **FastEthernet 0/24** | 802.1Q Trunk | 999 |
| `SW1-Dist` | **FastEthernet 0/2** | `SW3-HR` | **FastEthernet 0/24** | 802.1Q Trunk | 999 |
| `SW1-Dist` | **FastEthernet 0/3** | `SW4-Sales` | **FastEthernet 0/24** | 802.1Q Trunk | 999 |

### B. Servers & Management Station Connections
| Source Device | Source Port | Target Device | Target Port | Access VLAN | Subnet |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `SW1-Dist` | **FastEthernet 0/10** | `TFTP-Server` | **FastEthernet 0** | VLAN 40 | `192.168.40.0/24` |
| `SW1-Dist` | **FastEthernet 0/20** | `Admin-PC` | **FastEthernet 0** | VLAN 99 | `192.168.99.0/24` |

### C. End User Workstations Connections
| Source Device | Source Port | Target Host | Target Port | Access VLAN | Subnet |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `SW2-Eng` | **FastEthernet 0/1** | `PC-Eng1` | **FastEthernet 0** | VLAN 10 | `192.168.10.0/24` |
| `SW2-Eng` | **FastEthernet 0/2** | `PC-Eng2` | **FastEthernet 0** | VLAN 10 | `192.168.10.0/24` |
| `SW3-HR` | **FastEthernet 0/1** | `PC-HR1` | **FastEthernet 0** | VLAN 20 | `192.168.20.0/24` |
| `SW3-HR` | **FastEthernet 0/2** | `PC-HR2` | **FastEthernet 0** | VLAN 20 | `192.168.20.0/24` |
| `SW4-Sales` | **FastEthernet 0/1** | `PC-Sales1` | **FastEthernet 0** | VLAN 30 | `192.168.30.0/24` |
| `SW4-Sales` | **FastEthernet 0/2** | `PC-Sales2` | **FastEthernet 0** | VLAN 30 | `192.168.30.0/24` |

---

## 3. Static IP Configuration for Dedicated Endpoints

Configure the following two static devices manually in Packet Tracer:

### A. TFTP Server Configuration
1. Click **TFTP-Server** -> Navigate to the **Desktop** tab -> Click **IP Configuration**.
2. Select **Static** and input:
   - **IPv4 Address**: `192.168.40.10`
   - **Subnet Mask**: `255.255.255.0`
   - **Default Gateway**: `192.168.40.1`
   - **DNS Server**: `192.168.40.10`
3. Navigate to the **Services** tab -> Click **TFTP**.
4. Ensure the **Service** toggle is set to **On**.

### B. Admin-PC (Management Station)
1. Click **Admin-PC** -> Navigate to the **Desktop** tab -> Click **IP Configuration**.
2. Select **Static** and input:
   - **IPv4 Address**: `192.168.99.50`
   - **Subnet Mask**: `255.255.255.0`
   - **Default Gateway**: `192.168.99.1`
   - **DNS Server**: `192.168.40.10`

---

## 4. Applying Automated Configurations to Cisco Devices

All configurations are generated automatically by our Python script and saved in the `output_configs/` folder.

You can apply them in under **2 minutes**:

### Method 1: Using the Consolidated Paste File (Fastest)
1. Open the file `output_configs/all_devices_paste.txt`.
2. Locate the block for each device:
   - **For R1-Core**:
     - Click `R1-Core` in Packet Tracer -> Open the **CLI** tab.
     - If prompted `Would you like to enter the initial configuration dialog? [yes/no]:`, type **`no`** and press `Enter`.
     - Press `Enter` to reach the `Router>` prompt.
     - Type:
       ```ios
       enable
       configure terminal
       ```
     - Copy the configuration text for `R1-Core` and click **Paste** in the Packet Tracer CLI window.
     - Press `Enter`. The configuration, subinterfaces, DHCP pools, and security credentials will be applied instantly!
   - **For SW1-Dist, SW2-Eng, SW3-HR, SW4-Sales**:
     - Repeat the same steps for each switch:
       ```ios
       enable
       configure terminal
       ```
     - Paste the corresponding configuration from `output_configs/SW1-Dist.cfg`, `SW2-Eng.cfg`, `SW3-HR.cfg`, and `SW4-Sales.cfg`.

> **Note on RSA Keys in Packet Tracer:**  
> The generated script includes `crypto key generate rsa modulus 2048`. In Packet Tracer, if it prompts `How many bits in the modulus [512]:`, simply press `Enter` or type `1024` / `2048`.

---

## 5. Verification & Testing Procedures

### A. Testing Dynamic IP Assignment via DHCP
1. Click **PC-Eng1** -> Open **Desktop** tab -> Click **IP Configuration**.
2. Switch radio button from **Static** to **DHCP**.
3. Within 2-3 seconds, verify that it receives:
   - IP Address: `192.168.10.10` (or `192.168.10.x`)
   - Subnet Mask: `255.255.255.0`
   - Default Gateway: `192.168.10.1`
   - DNS Server: `192.168.40.10`
4. Repeat this for `PC-Eng2`, `PC-HR1`, `PC-HR2`, `PC-Sales1`, and `PC-Sales2`. All PCs will receive valid DHCP leases from their respective pools!

### B. Testing Inter-VLAN Routing & Connectivity
1. On **PC-Eng1** (`192.168.10.x`), open the **Command Prompt**.
2. Ping the local gateway:
   ```cmd
   ping 192.168.10.1
   ```
   *(Expected: 4/4 replies received, 0% loss)*
3. Ping across VLANs to **PC-HR1** (`192.168.20.10`):
   ```cmd
   ping 192.168.20.10
   ```
   *(Expected: First packet may timeout due to ARP resolution, followed by 3-4 replies)*
4. Ping across VLANs to **PC-Sales1** (`192.168.30.10`):
   ```cmd
   ping 192.168.30.10
   ```
5. Ping the **Central TFTP Server** (`192.168.40.10`):
   ```cmd
   ping 192.168.40.10
   ```

### C. Testing Secure Remote In-Band SSH Access
1. Click **Admin-PC** -> Open **Command Prompt** (or **Telnet/SSH Client**).
2. Connect to the Core Router via SSH:
   ```cmd
   ssh -l netadmin 192.168.99.1
   ```
3. Enter Password: `Cisco@123!`
4. Verify you see the **NovaCorp Security MOTD Banner** and reach `R1-Core#`.
5. Enter Privileged Exec:
   ```cmd
   enable
   ```
   *(Password: `cisco123`)*
6. Repeat for Distribution and Access Switches:
   - `ssh -l netadmin 192.168.99.11` (SW1-Dist)
   - `ssh -l netadmin 192.168.99.12` (SW2-Eng)
   - `ssh -l netadmin 192.168.99.13` (SW3-HR)
   - `ssh -l netadmin 192.168.99.14` (SW4-Sales)

### D. Executing TFTP Configuration Backups
1. While logged into `R1-Core` (via CLI or Admin-PC SSH):
   ```ios
   copy running-config tftp:
   Address or name of remote host []? 192.168.40.10
   Destination filename [R1-Core-confg]? R1-Core-backup.cfg
   ```
   Output:
   ```text
   Writing R1-Core-backup.cfg...!! [OK - 5026 bytes]
   5026 bytes copied in 0.088 secs
   ```
2. Repeat on `SW1-Dist`:
   ```ios
   copy running-config tftp://192.168.40.10/SW1-Dist-backup.cfg
   ```
3. **Verify on the TFTP Server**:
   - Click **TFTP-Server** -> Open **Services** tab -> Click **TFTP**.
   - Scroll through the file list to verify that `R1-Core-backup.cfg` and `SW1-Dist-backup.cfg` appear in the repository!

---

## 6. Fast-Forward Time Shortcut in Packet Tracer

If any switch links show amber lights due to Spanning Tree Protocol (STP) listening/learning states, click the **Fast Forward Time** button (or press `Alt + Fast Forward` / double click the fast forward icon at the bottom left) to immediately converge the network to forwarding mode.
