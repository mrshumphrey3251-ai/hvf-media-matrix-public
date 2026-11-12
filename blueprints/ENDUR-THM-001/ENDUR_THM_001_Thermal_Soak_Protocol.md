# ENDUR-THM-001 - Full-Load 4-Hour Cabin & Server-Rack Thermal Gradient Verification
## 45°C (113°F) Solar-Load Ambient Soak, PT1000 Quadrants & FLIR LWIR Thermography (ENDUR-THM-08)
**Program:** HVF Mobile Command Center (MCC) - Phase 3 | **CAGE:** 1AHA8  
**Author:** E.B.O.N.Y. (Core AI) - Authorized by Jeffery Humphrey, CEO | **Revision:** 1.0 - 2026-11-12

### 1. Environmental Chamber & Load Pre-Conditions
- **Ambient Soak:** `45.0 +/- 0.5 deg C` (`113 deg F`) with `800 W/m^2` solar irradiance (`ISO 13786`), `4.0 hours` continuous full load (`150 kW` turbine APU + `100%` CPU / `80%` GPU Crystal Group RS-Series compute workload)
- **Instrumentation:** Four NIST-traceable PT1000 sensor clusters (`Q-NE`, `Q-NW`, `Q-SE`, `Q-SW`, `+/- 0.1 deg C`, `10 Hz`), FLIR A700 LWIR radiometer (`7.5-13 um`, `+/- 0.5 deg C`, `16-bit TIFF` sweeps every `30 min`), and `DP-250-NEMA4X` differential-pressure transducer (`0-500 Pa`, `5 Hz`)

### 2. Thermal, Radiometric & Plenum Acceptance Matrix
- **Quadrant Thermal Gradient (`PT1000`):** `Delta_T (max - min) <= 2.5 deg C` continuously across all 4 quadrants
- **5-Ton MIL-SPEC ECU Cold-Aisle Containment:** `Delta_T_ECU (T_out - T_in) <= 2.5 deg C` continuously
- **Exhaust Plenum Differential Pressure (`NEMA-4X-DUCT-STD`):** Steady-state `Delta_P <= 150 Pa` with peak-to-peak pressure ripple `<= 5 Pa`
- **FLIR LWIR Surface Envelope:** Max cabin/rack surface temperature `<= 55.0 deg C` and local thermal gradient `<= 2.5 deg C` per `1 m^2`
- **WORM Sealing:** All telemetry streams and radiometric hashes sealed in `matrix_ledger.db` with CEO-level HMAC-SHA256