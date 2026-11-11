# Mobile Command Center - Interior & System Integration (Phase 2 Tracker)

## Structural & Thermal Ducting
- [x] Verify trailer chassis reinforcement to support 5-ton MIL-SPEC ECU and Crystal Group RS-Series rack (FASTEN-001)
- [x] Install modular steel frame for rack mounting (ISO-9001-RACK-FRM)
- [ ] Route high-efficiency insulated ductwork from ECU evaporator to each compute node (NEMA-4X-DUCT-STD)
- [x] Integrate heat-recovery exchangers with waste-heat TEG modules (TEG-HX-INT)
- [x] Seal all penetrations with MIL-SPEC fire-rated gaskets (FIRE-GASK-M)
- [x] Perform computational fluid dynamics (CFD) validation for airflow balance (CFD-VAL-2026-01)

## 480V / 24V Power Distribution
- [x] Install Victron 480V 3-Phase Inverter with Modbus-TCP (INV-480-MOD-001)
- [x] Deploy 24V DC bus for low-voltage subsystems (lighting, HMI, sensors)
- [ ] Fit SiC MOSFET-based DC-DC converters (1200V -> 48V -> 24V) with redundancy (DC-DC-RED-A/B)
- [x] Route shielded power cables per IEC 60364-4-41 with grounding straps
- [x] Install circuit protection (MCCB, fuses, surge protectors) per UL 508A for branch circuits
- [ ] Conduct initial load-bank test to verify 100% off-grid power margin (LOAD-TEST-01)

## Air-Gapped Network & Rack Topologies
- [ ] Rack-mount Crystal Group RS-Series Rugged Server in sealed enclosure (RACK-ENC-001)
- [ ] Install Owl Cyber Defense Data Diode between internal compute zone and external comms zone (DIOD-INT-EXT)
- [ ] Configure isolated VLANs (VLAN 10: Compute Core, VLAN 20: Control PLCs, VLAN 30: Management)
- [ ] Deploy edge firewall appliance with FIPS-140-2 validated firmware (FW-EDGE-FIPS)
- [ ] Map copper-to-fiber media converters for intra-rack links (FC-CONV-01)
- [ ] Perform air-gap integrity test with penetration verification (AIR-GAP-VAL-2026-02)

## Workstation Human-Machine Interfaces (HMI)
- [ ] Install ruggedized 24-inch touch-screen workstations (MIL-SPEC HMI-TS-24)
- [ ] Integrate dual-redundant joystick/trackball controls for drive-by-wire operation (CTRL-RED-01)
- [ ] Deploy operator console software stack (SCADA, AI inference UI, telemetry dashboard)
- [ ] Provide hardware key-card reader and biometric fingerprint scanner for multi-factor access (SEC-AUTH-HW)
- [ ] Mount environmental sensor panel (temperature, humidity, vibration) within operator cabin (ENV-PANEL-01)
- [ ] Conduct ergonomic validation per ISO 9241-210 (ERG-VAL-2026-03)