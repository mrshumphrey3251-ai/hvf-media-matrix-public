# Executive Engineering Directive - DC-DC-001
## Dual-Redundant SiC MOSFET DC-DC Converters (DC-DC-RED-A/B)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Power Envelope & Core Semiconductors
- Input Voltage: 1150V - 1250V DC (1200V DC Nominal from Turbine/Traction Bus)
- Primary Output: 48V DC @ up to 10 kW continuous
- Secondary Output: 24V DC @ up to 5 kW continuous
- Switching Semiconductors: Wolfspeed 1200V SiC MOSFET Modules (R_DS(on) <= 30 mOhm)
- Gate Drivers: UCC21520-A dual-channel SiC drivers (4.5 kV rating, 50 ns dead-time, 10 ms soft-start)
- Switching Frequency: 150 kHz fixed PWM carrier
- Conversion Efficiency: >= 97.0% - 97.5% across 30% - 100% load profiles

### 2. Dual-Redundancy & Active Load-Share Architecture
- Redundancy Model: Dual-converter N+1 hot-standby topology (Converters A & B in parallel)
- Load Balancing: 2-wire I2C current-share bus with PI loop regulating +/- 2% current balance
- Failover Switching Time: Hardware gate-level fault isolation and transfer <= 5 ms
- Fault Detection: Real-time over-current, over-voltage, thermal, and 1 kHz watchdog timeout

### 3. Galvanic Isolation & Creepage Envelopes (IEC 60747-5-1)
- HV Input to 48V Low-Voltage Bus: >= 4 kV DC isolation
- HV Input to 24V Low-Voltage Bus: >= 4 kV DC isolation
- Logic / Control Signal Lines: >= 4 kV DC opto-isolated barrier

### 4. Liquid Cold-Plate Thermal Integration
- Substrate: CNC-machined aluminum cold-plate with internal serpentine channels (Re ~ 4000)
- Coolant: 30% Ethylene Glycol / 70% De-ionized Water at 1.5 L/min per converter
- Thermal Interface: 0.1mm graphite-based TIM (<= 0.5 °C*mm^2/W)
- Junction Temperature Limit: <= 85°C junction temperature under continuous 100% load