# Executive Engineering Directive - FW-EDGE-001
## Tactical Edge Firewall Appliance with FIPS-140-2 Level 3 Firmware (FW-EDGE-FIPS)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Cryptographic Compliance
- Governing Standards: FIPS-140-2 Level 3, NIST SP 800-56C, NIST SP 800-77, MIL-STD-810H, DoD 5000-7
- Hardware Platform: Ruggedized 2U Edge Firewall Chassis (4x 10 GbE SFP+, 2x 40 GbE QSFP+, TPM 2.0, hardware crypto off-load)
- Stateful Throughput: >= 5 Gbps full packet inspection (2M concurrent sessions, 150 kpps setup rate, <= 2 us latency)
- Encrypted IPsec Throughput: >= 4.5 Gbps line rate

### 2. IPsec VPN Tunnel Cryptographic Suites
- Key Exchange: IKEv2 with X.509 certificate mutual authentication (HVF Internal PKI Root CA)
- Cipher & Integrity: AES-256-GCM encryption + HMAC-SHA-384 integrity
- Diffie-Hellman Group: Group 21 (3072-bit security) with mandatory per-tunnel Perfect Forward Secrecy (PFS)
- SA Lifecycle: 8-hour soft / 24-hour hard lifetime; re-key trigger at 75% lifetime or 1 GB transfer

### 3. Physical Anti-Tamper & Automated Zeroization Kill-Switch
- Physical Encapsulation: 3mm high-impact anti-drill UV-curable epoxy potting (EPX-M-RUG) over PCBs and I/O modules
- Chassis Interlocks: Honeywell break-circuit micro-switches (HT-TD-01) hard-wired to TPM watchdog
- Kill-Switch Triggers: Chassis tamper breach, UPS input drop (< 90% for > 2s), TPM watchdog timeout (> 5s), or signed C2 kill-switch command on VLAN 30
- Zeroization Execution: Immediate `TPM2_Clear`, SecureFlash hardware block-erase, crypto key register zeroing, and RNG firmware overwrite

### 4. Zero-Trust Packet Filtering Posture
- Default Posture: Implicit drop-all across all interfaces; rules signed with TPM private key
- Explicit Whitelists:
  - Rule 1: Permit VLAN 30 to WAN VPN peers on UDP 500/4500 (IKEv2 DPI)
  - Rule 2/3: Permit bidirectional SSH/HTTPS (TCP 22, 443) between VLAN 30 and VLAN 10 with FIPS TLS-inspection
  - Rule 4: Permit intra-VLAN 20 Modbus-TCP (502) and SNMP (161) without NAT
- Telemetry: Syslog-TLS exported to VLAN 30 SIEM (10.10.30.20) with SHA-256 Merkle ledger anchoring