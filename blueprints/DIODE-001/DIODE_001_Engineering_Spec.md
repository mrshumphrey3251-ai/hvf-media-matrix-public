# Executive Engineering Directive - DIODE-001
## Owl Cyber Defense Hardware-Enforced One-Way Data Diode Integration (DIODE-DATA-001)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Physical Air-Gap Architecture
- Standards: Common Criteria EAL 6+ (CC-2020), NIST SP 800-53 Rev 5 (AC-3, SC-7, SC-8, SC-12, SI-4), MIL-STD-810H, MIL-STD-461F
- Isolation Topology: Hardware-enforced one-way optical link separating ZONE-A (Internal Tactical Compute) from ZONE-B (External Comms / Starlink / Peplink)
- Optical Layer: Single-mode OS2 fiber (9/125 um) LC-LC; physical return path severed (RX laser transmitter depowered)
- Conduit & Air-Gap: 10mm ID sealed stainless-steel conduit (AG-TUBE-SS-010-001) with NEMA-4X end-cap gaskets and MIL-SPEC quick-release latches

### 2. Line-Rate Performance & Proxy Streaming
- Sustained Throughput: >= 1 Gbps uncompressed line-rate pass-through (UDP / TCP proxy)
- Latency & Jitter: One-way latency <= 2 ms; peak-to-peak jitter <= 0.5 ms
- Packet Handling: Transparent framing (64B - 1500B standard MTU) with static MAC provisioning (no learning tables)
- Flow Control: Hardware-based backpressure on TX side only; physical inability for RX to assert upstream ACKs

### 3. Hardware Tamper Detection & Safety Response
- Tamper Interlock: Magnetic reed switch loop on conduit/enclosure monitored via 4-20 mA loop (12 mA trip threshold)
- Automated Response: Loss of continuity immediately executes CE-ALARM-001, triggering automated compute shutdown via Modbus-TCP to Victron inverter <= 5s
- Reset Protocol: Requires 30-second manual lockout verification and CEO MFA token authorization

### 4. Zero Back-Channel Optical Verification
- Bidirectional Optical Isolation: Optical loopback leakage power < -70 dBm
- Power & Grounding: Independent isolated AC-DC supplies for TX and RX chassis; isolated single-point earth bonding per IEC 60364-4-41