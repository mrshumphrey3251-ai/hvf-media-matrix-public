# Executive Engineering Directive - LOAD-TEST-001
## Resistive/Reactive Load-Bank Commissioning Protocol (LOAD-TEST-01)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Test Envelope
- Standards: UL 508A, IEEE 519-2022, IEEE 1547-2022, IEC 61850-8-1
- Test Equipment: 250 kW / 125 kVAR 480V 3-phase programmable load bank (0.80 lag PF)
- Power Quality Monitoring: IEC 61000-4-30 class-A power analyzer synchronized to SCADA (IP: 10.0.0.20)

### 2. Stepped Load Profiles & Transient Limits
- Profile Staging:
  - S-01 (25% / 62.5 kW / 31.3 kVAR): 5 min dwell (Sag < 2%, Freq dev < 0.05 Hz)
  - S-02 (50% / 125.0 kW / 62.5 kVAR): 5 min dwell (Sag < 3%, Freq dev < 0.10 Hz)
  - S-03 (75% / 187.5 kW / 93.8 kVAR): 5 min dwell (Sag < 4%, Freq dev < 0.15 Hz)
  - S-04 (100% / 250.0 kW / 125.0 kVAR): 10 min dwell (Sag < 5%, Freq dev < 0.20 Hz)
  - S-05 (110% / 275.0 kW / 137.5 kVAR): 3 min overload test (Auto-trip if V < 440V for > 2s)
- Transient Step Response: Recovery to within 1% nominal <= 50 ms; THD <= 5% across all steps

### 3. Battery Thermal Ramp (KORE Power 500 kWh LFP)
- Discharge Rate: 1C continuous (500A @ 48V nominal)
- Maximum Cell Temperature: <= 55°C (<= 30°C rise above ambient)
- Thermal Uniformity: Temperature gradient between cells <= 3°C after 10 min steady-state
- Voltage Sag: <= 5% drop from nominal pack voltage during 100% load

### 4. SCADA Logging & Safety Triggers
- Sampling Rate: 1 Hz continuous telemetry on WORM storage; hourly SHA-256 Merkle hashes
- Trip Conditions:
  - Voltage Sag: V < 456V for > 0.5s -> ALARM-VOLTSAG
  - Over-Temperature: Temp_CellAvg > 55°C -> BMS-SHUTDOWN
  - Overload: Load > 110% for > 2s -> LOAD-BANK-TRIP