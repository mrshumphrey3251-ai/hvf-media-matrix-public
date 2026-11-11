# Executive Engineering Directive - BUS-24V-001
## 24V DC Low-Voltage Distribution Bus Architecture
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Electrical Architecture & Load Capacity
- System Voltage: 24V DC Nominal (Floating Ground, Galvanically Isolated)
- Continuous Current Rating: 200A continuous (300A 10s surge rating)
- Primary Feed: Victron 48V -> 24V DC-DC Step-Down Stage (250A capacity)
- Downstream Subsystems: Tactical LED lighting (Branch A), Operator HMIs (Branch B), Safety Interlocks/Sensors (Branch C)

### 2. Conductor Sizing & Voltage Drop Verification (53-ft Trailer Run)
- Physical Run: 53 ft (16.15 m one-way; 32.31 m round-trip loop)
- Conductor Material: OFHC Copper (99.99% purity, rho = 1.724e-8 Ohm*m)
- Effective Cross-Section: 200 mm^2 (Four 50 mm^2 conductors in parallel twisted bundles)
- Loop Resistance: R_loop = 0.00278 Ohms
- Voltage Drop at 200A Full Load: Delta-V = 0.56V (2.33% drop <= 2.5% / 0.6V limit)
- Conduit & Insulation: Rigid schedule-40 EMT conduit with UL-94 V-0 2mm heat-shrink sleeving

### 3. Floating Ground & Ground Fault Detection (GFD)
- Chassis Isolation: Polypropylene isolation bushings rated for 30 kV galvanic breakdown
- GFD Module: Dedicated Class-T GFD tripping at 30 mA leakage to chassis (IEC 60364-4-41)
- Main Circuit Protection: 250A DC-rated circuit breaker, instantaneous trip at 500A (2x)
- Surge Suppression: 30V clamp Transient Voltage Suppressor (TVS) arrays on all bus taps

### 4. Modular Branch Distribution Blocks (Class-T / MIDI)
- Branch Block 30A (Class-T-30): 4x 7.5A circuits (LED strips <= 5A), 12 AWG tinned copper
- Branch Block 60A (Class-T-60): 4x 15A circuits (HMI consoles <= 12A), 8 AWG tinned copper
- Branch Block 100A (Class-T-100): 2x 50A circuits (Sensor hub & safety interlocks <= 40A), 4 AWG armored run
- Form Factor: DIN-rail mounted (ISO-DIN-Rail-35), LED status indicators, key-controlled lockout