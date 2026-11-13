# NDAA Section 889 / DFARS 252.204-7012 Physical Prototype BOM RFQ Package (PROC-RFQ-04)
**Effective Date:** 2026-11-13 | **Organization:** Humphrey Virtual Farm - CAGE: 1AHA8  
**Issued By:** Jeffery Humphrey, Chief Executive Officer | **Baseline Merkle Root:** `0c5caaf75f9a358d1b5745a61a4a06ea304acff9f543cc9be1cdf1db193b3023`

### 1. Statutory Supply-Chain & Part-Level RFQ Matrix
- **WBS 1.0 — KORE Power (`KORE-LFP-500-BESS` | Qty: 1 | Gate A: 8 Weeks):**
  - `500 kWh` LiFePO4 BESS (`>= 475 kWh` usable @ `80%` DoD, `600-750V` DC, `150 kW` continuous / `300 kW` 15s peak, glycol thermal loop, isolated CAN 2.0B & Modbus-TCP).
  - *Mandatory Attestations:* `NDAA Section 889`, `DFARS 252.204-7012`, `UL 9540A` test report, U.S. `Certificate of Origin`.
- **WBS 1.1 — Wolfspeed (`1200V` SiC MOSFET Modules | Qty: 12 for 4x3 DC-DC | Gate B: 12 Weeks):**
  - `1200V` Silicon-Carbide MOSFET modules (`<= 3.5 mOhm` R_DS(on), `200 deg C` junction, `>= 98%` DC-DC efficiency).
  - *Mandatory Attestations:* `Wafer-Source Declaration` (U.S. fab origin), `NDAA Section 889`, `DFARS 252.204-7012`.
- **WBS 1.2 — Victron Energy (`480V` 3-Phase Inverter | Qty: 1 | Gate C: 10 Weeks):**
  - `480V` 3-Phase AC inverter (`150 kW` continuous / `300 kW` surge, `Modbus-TCP` & `CANopen`, `UL 9540A`).
  - *Mandatory Attestations:* `NDAA Section 889`, `DFARS 252.204-7012` firmware hash & cyber plan.
- **WBS 2.0 — Crystal Group (`RS-Series` Rugged Server Chassis | Qty: 1 | Gate D: 6 Weeks):**
  - `MIL-STD-810H` / `MIL-STD-461F` rugged rackmount chassis with EMI shielding and front optical fiber I/O.
  - *Mandatory Attestations:* U.S. `Certificate of Origin`, `NDAA Section 889`, `DFARS 252.204-7012`.
- **WBS 2.1 — Owl Cyber Defense (`1U` Hardware Data Diode | Qty: 1 | Gate E: 4 Weeks):**
  - Hardware-enforced unidirectional optical air-gap (`Modbus-TCP`, `DNP3`, `OPC-UA`, `Syslog`, `18-36V` DC fail-closed).
  - *Mandatory Attestations:* `Common Criteria EAL 4+` certificate, U.S. `Certificate of Origin`, `NDAA Section 889`.
- **WBS 2.2 — NVIDIA (`Jetson AGX Orin Industrial` | Qty: 2 — Primary + Hot-Spare | Gate F: 8 Weeks):**
  - `-40 deg C` to `+85 deg C` industrial edge AI compute (`275 TOPS` INT8, dual `10GbE`, encrypted secure boot).
  - *Mandatory Attestations:* `NDAA Section 889` / TAA declaration, `DFARS 252.204-7012` secure-boot attestation.
- **WBS 2.3 — National Instruments (`NI PXIe` Real-Time HIL/DAQ Chassis + FPGA | Qty: 1 Chassis + 2 FPGA | Gate G: 10 Weeks):**
  - Real-time `<= 10 us` deterministic HIL chassis with `MIL-STD-1553`, `CAN-FD`, and Ethernet timing modules.
  - *Mandatory Attestations:* U.S. `Certificate of Origin`, `NDAA Section 889`, `DFARS 252.204-7012`.
- **WBS 3.0 — 5-Ton `MIL-SPEC` ECU & Trailer Integration (Qty: 1 | Gate H: 12 Weeks):**
  - Hardened `CAN-FD` / `MIL-STD-1553` / `Ethernet-AVB` 5-ton ECU integrated into reinforced drop-deck trailer (`FASTEN-001`).
- **WBS 4.0 — HIL Regression & Third-Party Certification Reserve (`$45,000` USD | Gate I: 4 Weeks Post-Gate G):**
  - Dedicated `UL 9540A`, `MIL-STD-810H`, and `64`-threshold physical HIL regression validation reserve.

**Authorized Signatory:** Jeffery Humphrey, Chief Executive Officer — Humphrey Virtual Farm (`CAGE: 1AHA8`)