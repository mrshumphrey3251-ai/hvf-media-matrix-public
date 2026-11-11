# Executive Engineering Directive - PROT-001
## Industrial Control Panel Circuit Protection per UL 508A (PROT-UL508A-001)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Short-Circuit Performance Envelope
- Governing Standards: UL 508A, UL 489, UL 1449 4th Ed, UL 248, NEMA-4X
- Service Entrance Available Short-Circuit Current: 65 kA @ 480V 3-Phase AC
- System SCCR Rating: 100 kA with upstream current-limiting surge and fuse coordination

### 2. Molded Case Circuit Breakers (MCCB) Staging
- AC Main (MCCB-AC-U1): 480V AC, 600A, 65 kAIC, Inverse-time Curve C (Trips within 0.2s at 10x In)
- AC Feeder (MCCB-AC-D1): 480V AC, 250A, 65 kAIC, Inverse-time Curve D (Selective backup to compute rack)
- DC Main (MCCB-DC-U1): 24V DC, 250A, 30 kAIC DC rating, Curve C, with ground-fault leakage trip
- DC Feeder (MCCB-DC-D1): 24V DC, 125A, 30 kAIC DC rating, Curve D

### 3. Branch Fusing Architecture (Class CC & Class T)
- FUSE-CC-01 / 02: 480V AC Class CC (100A & 150A, 65 kAIC, clears < 0.01s, let-through < 5 J)
- FUSE-T-01: 480V AC Class T (250A, 65 kAIC, time-delay for lighting/HVAC)
- FUSE-CC-DC-01: 24V DC Class CC (50A, 30 kAIC) protecting edge-GPU modules
- FUSE-T-DC-01: 24V DC Class T (125A, 30 kAIC) protecting instrumentation buses

### 4. Surge Protective Devices (SPD)
- Main Entrance SPD (SPD-T1-U): Type 1, UL 1449, >= 100 kA SCCR, 8 kA (8/20 µs)
- Panel-Level SPD (SPD-T2-D): Type 2, UL 1449, >= 100 kA SCCR, 6 kA (8/20 µs)
- DC Bus SPD (SPD-DC-U): Type 2 DC-rated, >= 100 kA SCCR, 2 kA (8/20 µs) with PLC status contacts