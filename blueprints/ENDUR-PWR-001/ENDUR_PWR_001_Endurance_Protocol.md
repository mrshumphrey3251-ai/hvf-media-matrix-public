# ENDUR-PWR-001 - 24-Hour Continuous Off-Grid Islanded Endurance Run
## KORE Power 500 kWh LFP BESS + Anti-Glint ETFE Solar Array + TEG-HX-INT Waste-Heat Recovery (ENDUR-PWR-06)
**Program:** HVF Mobile Command Center (MCC) - Phase 3 | **CAGE:** 1AHA8  
**Author:** E.B.O.N.Y. (Core AI) - Authorized by Jeffery Humphrey, CEO | **Revision:** 1.0 - 2026-11-12

### 1. Powertrain Architecture & Governing Thresholds
- **Energy Storage:** KORE Power `500 kWh` LFP BESS (`475 kWh` usable @ 80% DoD, `600-750 V` DC, `150 kW` continuous / `300 kW` surge)
- **Renewable & Waste-Heat Generation:** Anti-glint ETFE roof solar array (`MPPT CAN-FD 0x010-0x01F`, `20 Hz`) + Exhaust `TEG-HX-INT` (`30 kW` thermal -> `5 kW` electrical @ `>= 150 deg C` hot-side, `CAN-FD 0x020-0x02F`, `10 Hz`)
- **Acceptance Thresholds:**
  - Cumulative BESS SoC `>= 30%` across autonomous window (`< 20%` triggers `ENDUR-APU-07` turbine auto-start)
  - Intra-module cell thermal delta `Delta_T_max <= 3.5 deg C` across all `48` PT1000 RTD sensors (`BMS IDs 0x011-0x018`)
  - CAN-FD bus error frame rate `< 0.1%`

### 2. Deterministic Hourly Execution & WORM Merkle Sealing (`t = 0` to `24 h`)
- **Hourly Energy Balance:** `E_net = (P_solar + P_TEG - P_load) * 1 h`; `SoC_new = SoC_prev + (E_net / 475 kWh) * 100%`
- **Mid-Hour Thermal Guard (`hh:30:00`):** Automated compute step-down (`120 kW -> 80 kW`) if `Delta_T_max > 3.5 deg C`
- **Hourly WORM Merkle Chain:** Package `hour_XX.json` + `candump_hour_XX.bin` + `temp_hour_XX.csv`, compute `merkle_root_n = SHA256(merkle_root_{n-1} || SHA256(hour_XX.json))`, and seal in `matrix_ledger.db` with CEO-level HMAC-SHA256