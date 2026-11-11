# Executive Engineering Directive - VLAN-ISO-001
## Isolated Network Segmentation Across Managed Layer-3 Switch (VLAN-ISO-001)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Layer-3 Rugged Switch Architecture
- Standards: NIST SP 800-53 Rev 5 (SC-7, AC-4, IA-2), CIS Cisco Benchmark v8.0, DoD Network Device STIG
- Switch Core: Layer-3 Ruggedized Managed Switch (48x 10 GbE SFP+ + 4x 40 GbE QSFP+, dual redundant PSU)
- Physical & High-Availability Architecture: Dual-supervisor active/standby, HSRP/VRRP VIP gateways (.254), LACP trunk aggregation

### 2. Logical VLAN & Subnet Allocation (802.1Q)
- VLAN 10 (AI Compute / Inference): 10.10.10.0/24 | Gateway: 10.10.10.1 (VIP: 10.10.10.254) | Ports Gi1/0/25-32
- VLAN 20 (Industrial PLCs / SCADA): 10.10.20.0/24 | Gateway: 10.10.20.1 (VIP: 10.10.20.254) | Ports Gi1/0/33-40
- VLAN 30 (Out-of-Band IPMI / iLO): 10.10.30.0/24 | Gateway: 10.10.30.1 (VIP: 10.10.30.254) | Ports Gi1/0/41-44
- Uplinks / Core Trunks: Ports Gi1/0/1-24 (Tagged VLAN 10, 20, 30)

### 3. Access Control Lists (ACLs) & Inter-VLAN Routing
- ACL_VLAN10_IN (Compute): Stateless drop-all inter-VLAN routing (`deny ip any any log`)
- ACL_VLAN20_IN (PLC/SCADA): Strict Modbus-TCP/UDP whitelist on Port 502 (`permit tcp/udp any any eq 502`), drop-all cross-traffic
- ACL_VLAN30_IN (OOB Management): Administrative traffic whitelist (SSH port 22, HTTPS port 443, SNMP port 161 to SVI 10.10.30.1 only)

### 4. Port Security & IEEE 802.1X Enforcement
- Authentication Mechanism: EAP-TLS certificate-based authentication against internal HVF PKI RADIUS server (10.10.30.10)
- Legacy Support: MAC Authentication Bypass (MAB) enabled on VLAN 20 PLC access ports
- Port-Security Rules: Single sticky MAC per interface (`switchport port-security maximum 1 mac-address sticky`); violation action = `shutdown`
- Multicast Management: IGMP Snooping enabled across VLANs 10, 20, 30; fast-leave configured on VLAN 20