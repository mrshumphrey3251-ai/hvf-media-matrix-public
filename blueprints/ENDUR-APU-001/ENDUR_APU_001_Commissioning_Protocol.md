# ENDUR-APU-001 - 150 kW JP-8/Diesel Series-Hybrid Turbine APU Commissioning Protocol
## Autonomous Cold-Start, Closed-Transition Load Pickup (20% SoC) & 85% SoC Charge Cutoff (ENDUR-APU-07)
**Program:** HVF Mobile Command Center (MCC) - Phase 3 | **CAGE:** 1AHA8  
**Author:** E.B.O.N.Y. (Core AI) - Authorized by Jeffery Humphrey, CEO | **Revision:** 1.0 - 2026-11-12

### 1. Turbine Ramp & Rectifier Synchronization Tolerances
- **Cold-Start Envelope:** `0 deg C <= T_amb <= 40 deg C`, JP-8/Diesel fuel rail `3.0 +/- 0.1 bar` (`CAN-FD 0x1B2`), chassis isolation `>= 10 MOhm` (`ENV-PANEL-01`, `CAN-FD 0x1D0`)
- **EGT / RPM Ramp Profile (`CAN-FD 0x1A0`):**
  - Ignition & Spool-Up: `10,000 +/- 200 RPM` in `<= 30 s` (`EGT <= 650 deg C`)
  - Intermediate Ramp: `20,000 +/- 150 RPM` at `300 RPM/s` (`66 s`)
  - Rated Speed & Power: `36,000 +/- 200 RPM` (`150 kW`) at `400 RPM/s` (`90 s`, steady-state `EGT <= 800 deg C`)
- **Rectifier DC-Bus Sync (`MIL-STD-704`):** `400 V +/- 1%` (`+/- 4 V`), ripple `<= 5 V` within `<= 5 s` prior to closed-transition load transfer (`<= 2 s`)

### 2. Thermal Handoff & BESS Charge Cutoff Thresholds
- **`TEG-HX-INT` Coupling (`CAN-FD 0x1E0/0x1E2`):** Actuate bypass valve (`1.0 L/min` flow) within `<= 5 s` of turbine steady state
- **BESS Protection (`CAN-FD 0x1C0`):** Trigger auto-start at `<= 20%` SoC (`100 kWh`), maintain module `Delta_T <= 3.5 deg C`, and execute automated charge cutoff within `<= 1 s` at `>= 85%` SoC while sustaining islanded C2 load
- **WORM Sealing:** Hourly SHA-256 Merkle chain sealed in `matrix_ledger.db` with CEO-level HMAC-SHA256