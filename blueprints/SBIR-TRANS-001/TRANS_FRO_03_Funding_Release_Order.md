# SBIR Phase II/III Funding Release Order (FRO) & Treasury Capital-Allocation Directive (TRANS-FRO-03)
**Created:** 2026-11-13 | **Organization:** Humphrey Virtual Farm - CAGE: 1AHA8  
**Authority:** Jeffery Humphrey, Chief Executive Officer | **Reference Merkle Root:** `0c5caaf75f9a358d1b5745a61a4a06ea304acff9f543cc9be1cdf1db193b3023`

### 1. Work-Breakdown-Structure (WBS) Cost-Pool Allocation Matrix (`Cerberus_Treasury_Matrix.py`)
- **WBS 1.0 — Long-Lead Powertrain & Microgrid Hardware (Capital Equipment):**
  - `500 kWh` KORE Power LFP BESS, `150 kW` JP-8/Diesel Turbine APU, Wolfspeed `1200V -> 48V` SiC DC-DC converters, Victron `480V` 3-phase inverter (`Modbus-TCP`).
- **WBS 2.0 — Rugged C2 & Air-Gap Compute Hardware (Capital Equipment):**
  - Crystal Group RS-Series rugged rack (`MIL-SPEC`), Owl Cyber Defense hardware Data Diode, `NVIDIA Jetson AGX Orin` Industrial edge GPU nodes, `NI PXIe` modular HIL & DAQ chassis.
- **WBS 3.0 — 5-Ton MIL-SPEC ECU & Trailer Integration (Integration Services):**
  - 5-ton `MIL-SPEC` Environmental Control Unit (ECU), reinforced trailer chassis (`FASTEN-001`), `480V / 24V` power distribution bus, and insulated thermal-ducting / TEG heat-recovery loop.
- **WBS 4.0 — HIL Regression & Field-Certification Reserve (Test & Certification):**
  - Full `64`-threshold physical HIL regression campaign, third-party `MIL-STD-461G / 810H` & `NFPA 101` verification, and DoD Delivery Acceptance Report (`DAR`).

### 2. Cryptographic Treasury Release & WORM Audit Controls
- Every WBS disbursement transaction is hashed via SHA-256 into `matrix_ledger.db`, bound to Master Merkle Root `0c5caaf75f9a358d1b5745a61a4a06ea304acff9f543cc9be1cdf1db193b3023`, and authorized solely by **Jeffery Humphrey, CEO (`CAGE: 1AHA8`)** via `EBONY_TIER_1_CEO` HMAC-SHA256.