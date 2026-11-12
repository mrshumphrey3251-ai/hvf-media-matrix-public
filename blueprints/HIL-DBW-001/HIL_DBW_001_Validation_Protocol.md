# HIL-DBW-001 - Deterministic NI-PXIe HIL Validation Protocol
## Dual-Redundant Hall-Effect Drive-by-Wire (CTRL-RED-01) & Jetson AGX Orin Arbitration (HIL-DBW-05)
**Program:** HVF Mobile Command Center (MCC) - Phase 3 | **CAGE:** 1AHA8  
**Author:** E.B.O.N.Y. (Core AI) - Authorized by Jeffery Humphrey, CEO | **Revision:** 1.0 - 2026-11-12

### 1. Objective & Governing Standards
- **Failover Latency (`CTRL-RED-01`):** Transfer torque command authority (`T_cmd`) from primary Hall-effect channel to secondary channel in `<= 10.0 ms` (`>= 95% T_cmd` on secondary PWM) following primary Loss-of-Signal (`LOS`)
- **Sensor-Suite Arbitration (`Jetson AGX Orin`):** Ouster OS-1-64 LiDAR (`100 Hz`) & Continental ARS-408 Radar (`50 Hz`) failover from primary CAN-FD (`0x010`-`0x01F`) to secondary CAN-FD (`0x020`-`0x02F`) with perception stream gap `<= 10.0 ms`
- **Transient Immunity:** Full compliance under `MIL-STD-1275E` (`ES-G-1275E` `120 V` transient burst, `<= 8 us` rise/fall) with zero latch-up or reboot

### 2. Deterministic Testbed & Capture Matrix
- **HIL Hardware:** `NI-PXIe-1085` chassis (`10 MHz` Ref + `IEEE-1588 PTP` + `1 ppm` GPSDO), `NI-PXIe-7966R` (`10 MS/s`, 4-ch Hall A/B & Primary/Secondary PWM), `NI-PXIe-6343` (`1 us` digital I/O), `NI-PXIe-8510` dual-port CAN-FD, Rockwell 5000 `PLC-HIL-01` (`1 kHz` scan), Keysight Infiniium (`5 GS/s`)
- **Dead-Man Interlock Holdoff:** `PLC-HIL-01` maintains `FAIL-OVER` flag (`<= 2 ms` transition) and keeps dead-man interlock engaged across the `5 ms` secondary channel stabilization window (zero unintended E-Stop)
- **Repeatability:** 30 independent runs across cold start (`5 deg C`), warm start (`25 deg C`), and 8-hour hot soak (`70%` duty) with `0%` false-negative rate