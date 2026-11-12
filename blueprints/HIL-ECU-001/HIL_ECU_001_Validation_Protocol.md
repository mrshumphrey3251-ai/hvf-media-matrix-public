# HIL-ECU-001 - Deterministic NI-PXIe HIL Validation Protocol
## 5-Ton MIL-SPEC Environmental Control Unit (ECU) Over-Temperature & Over-Pressure Interlock (HIL-ECU-04)
**Program:** HVF Mobile Command Center (MCC) - Phase 3 | **CAGE:** 1AHA8  
**Author:** E.B.O.N.Y. (Core AI) - Authorized by Jeffery Humphrey, CEO | **Revision:** 1.0 - 2026-11-12

### 1. Objective & Thresholds
Verify hardware interlock trip within `<= 200 ms` (`Delta_t = t2 - t1 <= 200 ms`) across single and combined fault injections:
- **Over-Temperature (`TMP-ECU-01`):** Rack-inlet air temperature `> 45.0 deg C` (synthetic step from `25 deg C` to `55 deg C` on `NI-PXIe-6343 AI0`)
- **Over-Pressure (`PRS-ECU-01`):** Refrigerant / duct static pressure `> 150.0 kPa` (synthetic step from `80 kPa` to `180 kPa` on `NI-PXIe-6343 AI1`)

### 2. Deterministic Sub-Actuator & Interlock Acceptance Matrix
- **Primary Hardware Interlock (`PLC-HIL-01 DI0/DI1`):** Trip asserted `<= 200 ms` post-threshold crossing
- **`NEMA-4X-DUCT-STD` Damper Isolation (`DO0`):** Reaches `>= 95%` closed position within `<= 50 ms` post-interlock
- **`TEG-HX-INT` Bypass Valve Actuation (`DO1`):** Opens to `>= 90%` flow position within `<= 70 ms` post-interlock
- **Crystal Group RS-Series Thermal Throttle (`DO2`):** Ramps graceful CPU PWM throttle to `100%` within `<= 30 ms` post-interlock
- **Fault Clearance Recovery:** All actuators return to nominal idle within `<= 150 ms` after fault clearance (`500 ms` post-trip)

### 3. Instrumentation & Repeatability Protocol
- **Digitizer & PLC:** `NI-PXIe-1085` chassis with `NI-PXIe-7966R` (`10 MS/s`, 6 channels, `-5 ms` to `+250 ms` capture window) and Rockwell 5000 `PLC-HIL-01` (`1 kHz` scan)
- **Repeatability:** Executed across 3 thermal states (cold start, warm start, after 8-hour continuous soak) with `0%` false-positive rate over 30-minute nominal monitoring; raw `.tdms` and `.csv` logs sealed via SHA-256