# Purchase Order (PO) Execution & Critical-Path Delivery Schedule (PROC-PO-05)
**Effective Date:** 2026-11-13 (Week 0 Kick-Off) | **Organization:** Humphrey Virtual Farm - CAGE: 1AHA8  
**Issued By:** Jeffery Humphrey, Chief Executive Officer | **Reference Merkle Root:** `0c5caaf75f9a358d1b5745a61a4a06ea304acff9f543cc9be1cdf1db193b3023`

### 1. 12-Week Critical-Path PO Issuance Sequence
- **Week 0 (12-Week Critical Path):**
  - `PO-W-001` — **Wolfspeed** `1200V` SiC MOSFET Modules (Qty: 12 modules / 48 dies) -> `QA-Gate-1` (`CoO`, U.S. `Wafer-Source Declaration`, `NDAA Section 889`).
  - `PO-E-001` — **5-Ton MIL-SPEC ECU** (`HVF-MECU-5000`, Qty: 1) -> `QA-Gate-1` (Functional power-up & signed firmware hash).
- **Week 1 (4-Week Lead Time):**
  - `PO-D-001` — **Owl Cyber Defense** Hardware Data Diode (Qty: 1-2) -> `QA-Gate-2` (`CC EAL 4+`, physical tamper-seal & unidirectional optical test).
- **Week 2 (6-Week Lead Time):**
  - `PO-C-001` — **Crystal Group** `RS-Series` Rugged Server Chassis (Qty: 1-2) -> `QA-Gate-2` (`MIL-STD-810H` dimensional/EMI audit & `CoO`).
- **Week 3 (8-Week Lead Time):**
  - `PO-J-001` — **NVIDIA** `Jetson AGX Orin Industrial` (Qty: 2 — Primary + Hot-Spare) -> `QA-Gate-3` (Encrypted secure-boot key hash match & `-40 deg C` to `+85 deg C` thermal check).
- **Week 4 (8-Week Lead Time):**
  - `PO-B-001` — **KORE Power** `500 kWh` LFP BESS (`KORE-LFP-500-BESS`, Qty: 1) -> `QA-Gate-3` (`UL 9540A` fire-safety report, cell-level BMS telemetry & `CoO`).
- **Week 5 (10-Week Lead Time):**
  - `PO-I-001` — **Victron Energy** `480V` 3-Phase Inverter (`150 kW` continuous / `300 kW` surge, Qty: 1) -> `QA-Gate-4` (Isolation resistance `> 10 MOhm` & `Modbus-TCP` verification).
  - `PO-N-001` — **National Instruments** `NI PXIe` Real-Time HIL/DAQ Chassis + FPGA Modules (Qty: 1 chassis + 2 FPGA) -> `QA-Gate-4` (Deterministic `<= 10 us` timing & firmware hash check).
- **Week 12 (Final Integration Gate):**
  - `QA-Gate-5` — Full prototype system-level integration, `DFARS 252.204-7012` cyber audit, and WORM PO hash closure in `matrix_ledger.db`.

**Authorized Signatory:** Jeffery Humphrey, Chief Executive Officer — Humphrey Virtual Farm (`CAGE: 1AHA8`)