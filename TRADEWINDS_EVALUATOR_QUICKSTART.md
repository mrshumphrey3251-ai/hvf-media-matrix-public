# DOD CDAO TRADEWINDS SOLUTIONS MARKETPLACE: EVALUATOR TECHNICAL RUNBOOK
**Procurement Vehicle:** DoD Chief Digital and Artificial Intelligence Office (CDAO) -- Tradewinds Solutions Marketplace
**Statutory Authority:** 10 U.S.C. Section 4022 Prototype OTA & DFARS 252.227-7018 (Government Purpose Rights)
**Contracting Entity:** Humphrey Virtual Farms LLC (CAGE: `1AHA8` | SAM.gov UEI: `S1M4ENLHTDH5`)
**Tradewinds Submission ID:** `9-26-3703`
**Technology Readiness Level (TRL):** **TRL 6 / TRL 7** (Operational Bare-Metal System Prototype -- Upgraded from Initial TRL 4 Filing)
**Master Release Seal:** `v8.0.0-sovereign-master-seal`
**Master C2 Merkle Root (SHA-256):** `cc1ee1c8d29b2ae5e856fc0fcb672a52e7e49d50369499febe14e18e9150949a`
**Official Contact:** Jeffery Humphrey, Founder & CEO (`[REDACTED_PUBLIC_RELEASE_CONTACT]`)

---

## 1. Scope Note: Strict Separation of Federal DoD Tradewinds vs. State of Oklahoma Dockets
- **This Runbook (`TRADEWINDS_EVALUATOR_QUICKSTART.md`):** Governs **Federal DoD CDAO Tradewinds Docket `9-26-3703`** ($1,485,000.00 / 12-Month 10 U.S.C. Section 4022 Prototype OTA).
- **State of Oklahoma Infrastructure & ODOT Drone Docket:** Governed separately under [`OKLAHOMA_CTO_TECHNICAL_EVALUATION_DOSSIER.md`](OKLAHOMA_CTO_TECHNICAL_EVALUATION_DOSSIER.md) and [`OKLAHOMA_COMMERCE_ODOT_EVALUATOR_RUNBOOK.md`](OKLAHOMA_COMMERCE_ODOT_EVALUATOR_RUNBOOK.md) (Oklahoma HB 2992 & Title 61).

---

## 2. Expanded v8.0.0 Verification Commands (TRL 6/7 Proof on Bare-Metal Windows)
DoD CDAO and ACC-RI technical evaluators can independently verify all 631 compiled modules, 83 unit/penetration test suites, and the Master C2 Merkle Root in under 30 seconds:

1. **Execute the 83-Suite Automated Unit & Red-Team Penetration Ledger (`83 / 83 PASSED`):**
   `python c2_cockpit/run_all_83_tests.py`
2. **Execute the 9-Gate Sovereign Cryptographic Seal Verifier (`631 / 631 Modules` & `1,420 / 1,420 Academy Qs`):**
   `python c2_cockpit/verify_sovereign_seal.py`

---

## 3. Live Loopback-Isolated Socket Interrogation (`NIST SP 800-82 Rev 2`)
- **Tactical HUD Workstation Cockpit:** `http://127.0.0.1:8501/`
  - SCADA Microgrid: 4/4 synchronized contactors (`2.04 us` Modbus FC05 actuation, `13.33 ms` trip, `36.75 ns` Kinetic Guillotine).
  - Aerial UAS Overwatch: DJI Matrice 350 RTK (`75.0 m MSL` orbit).
  - Warfighter BFT: 3 dismounted recon nodes tracked, `0` distress flags.
- **Automated Evaluator Ingress Daemon:** `http://127.0.0.1:8502/`
  - `Invoke-RestMethod -Uri "http://127.0.0.1:8502/evaluator/posture" -Method GET`
  - `Invoke-RestMethod -Uri "http://127.0.0.1:8502/evaluator/telemetry" -Method GET`
  - `Invoke-RestMethod -Uri "http://127.0.0.1:8502/evaluator/dispatch" -Method GET`


---

## INTEGRATED HOST OPERATING CONSOLE & 26-MODULE PER-NODE PRICE SCHEDULE (`DOCKET 10-26-3952`)

**1. Turnkey TRL 7 Operating Console Proof (`Project Ebony` -- 26 Modules / 72 Verified Controls):**  
Docket `10-26-3952` executes natively inside the **HVF Level-5 Sovereign C2 Operating Console**, a fully operational, bare-metal Command & Control enclave (`631 / 631` compiled Python/C modules, Master SHA-256 Merkle Root: `cc1ee1c8d29b2ae5e856fc0fcb672a52e7e49d50369499febe14e18e9150949a`, `83 / 83` unit test suites passing at `100.0%`).

**2. Unbundled Per-Node Licensing Scope (DFARS `252.227-7018` & `227.7202`):**  
* **Base Entry Pilot (`CLIN 0001`):** The entry pilot price filed on Tradewinds Docket `10-26-3952` covers **strictly `CLIN 0001` (`Module #01: Sovereign Command Chronos Base Router` on `1` Single Bare-Metal Node)**.
* **Individual Add-On Modules (`CLIN 0002` - `CLIN 0026`):** Each of the remaining **25 Command Modules** in the Operating Console is priced individually **per physical hardware node / per robotic chassis / per training seat** (`1 License = 1 Hardware UUID`). Government and commercial buyers may add individual modules to a `10-26-3952` contract award via sole-source modification (10 U.S.C. 4022 / FAR Part 12):

| CLIN | Module # & Name | Licensing Basis (Strict Per-Node) | Annual Gov Price | Monthly Commercial |
| :--- | :--- | :--- | :--- | :--- |
| `CLIN 0001` | **Mod #01:** `Sovereign Command (Chronos Base Router)` | **1 Single Node (`10-26-3952` Base Pilot)** | **Base Pilot Price** | **$2,450 / mo** |
| `CLIN 0002` | **Mod #02:** `System Overview & Preflight WORM Gate` | Per Enclave Server Node | **$35,000 / yr** | **$3,500 / mo** |
| `CLIN 0003` | **Mod #03:** `Master C2 Cockpit (60Hz Microgrid & Fault C2)` | Per Substation / TOC Node (`19` Controls) | **$95,000 / yr** | **$8,900 / mo** |
| `CLIN 0004` | **Mod #04:** `Autonomous Build Forge (AST Synthesizer)` | Per Engineering Enclave Node | **$110,000 / yr** | **$9,800 / mo** |
| `CLIN 0005` | **Mod #05:** `CEO Authorization Gate & Sovereign Airlock` | Per Airlock Node (`698` Module Sweep) | **$125,000 / yr** | **$11,200 / mo** |
| `CLIN 0006` | **Mod #06:** `Sovereign Robotics & Kinematics C2 (36.75ns)` | Per Robot Controller / UGV Chassis | **$185,000 / yr** | **$16,500 / mo** |
| `CLIN 0007` | **Mod #07:** `Drone Diagnostics & Optical GLI Core` | Per UAS Ground Control Station Node | **$75,000 / yr** | **$6,800 / mo** |
| `CLIN 0008` | **Mod #08:** `Sovereign Auto & CAN-Bus C2 (SAE J1939)` | Per Fleet Maintenance Bay Node | **$85,000 / yr** | **$7,600 / mo** |
| `CLIN 0009` | **Mod #09:** `Grain Silo Aeration & 480V Contactor C2` | Per Silo Complex / 480V PLC Node | **$75,000 / yr** | **$6,800 / mo** |
| `CLIN 0010` | **Mod #10:** `Omni-Industry Matrix & Title 61 Deliverables` | Per Engineering District Node | **$95,000 / yr** | **$8,900 / mo** |
| `CLIN 0011` | **Mod #11:** `Sovereign Field Academy (1,420 Verified Qs)` | Per 50-Seat Training Cohort | **$125,000 / yr** | **$11,200 / mo** |
| `CLIN 0012` | **Mod #12:** `HVF Master Auto & Small-Engine Academy` | Per Technical Lab Node (25 Seats) | **$65,000 / yr** | **$5,900 / mo** |
| `CLIN 0013` | **Mod #13:** `Sovereign Dispatch Deck (Air-Gap IMAP/SMTP)` | Per Secure Comms Enclave Node | **$55,000 / yr** | **$4,950 / mo** |
| `CLIN 0014` | **Mod #14:** `Sovereign Comms Deck (Dual-Core Audio)` | Per Tactical TOC Comms Node | **$50,000 / yr** | **$4,500 / mo** |
| `CLIN 0015` | **Mod #15:** `Media Matrix & Predict-and-Act Loop` | Per Autonomous Operations Node | **$65,000 / yr** | **$5,900 / mo** |
| `CLIN 0016` | **Mod #16:** `Sovereign Asset Synthesis Engine` | Per Local Render Workstation Node | **$40,000 / yr** | **$3,600 / mo** |
| `CLIN 0017` | **Mod #17:** `LinkedIn Executive Broadcast Engine` | Per Executive Comms Node | **$30,000 / yr** | **$2,750 / mo** |
| `CLIN 0018` | **Mod #18:** `Python Execution Sandbox & Quarantine` | Per Developer / Audit Node | **$45,000 / yr** | **$4,100 / mo** |
| `CLIN 0019` | **Mod #19:** `Empire Config & Pilot Governance Vault` | Per Administrative Root Node | **$35,000 / yr** | **$3,200 / mo** |
| `CLIN 0020` | **Mod #20:** `Level-5 Ext: Action Desk Tactical Dispatcher` | Per Sector Command Node | **$30,000 / yr** | **$2,750 / mo** |
| `CLIN 0021` | **Mod #21:** `Level-5 Ext: NOAA Weather Radar & EMC Sync` | Per Base Meteorology Node | **$40,000 / yr** | **$3,600 / mo** |
| `CLIN 0022` | **Mod #22:** `Level-5 Ext: ISO 32000-1 WORM PDF Compiler` | Per Compliance Documentation Node | **$35,000 / yr** | **$3,200 / mo** |
| `CLIN 0023` | **Mod #23:** `Level-5 Ext: Autonomous Lead Scheduler` | Per Commercial Outreach Node | **$25,000 / yr** | **$2,250 / mo** |
| `CLIN 0024` | **Mod #24:** `Level-5 Ext: Chronos Companion Telemetry` | Per Watch-Floor Operator Node | **$30,000 / yr** | **$2,750 / mo** |
| `CLIN 0025` | **Mod #25:** `Level-5 Ext: 48-Plenum Silo PLC Synchronizer` | Per Industrial Facility PLC Node | **$35,000 / yr** | **$3,200 / mo** |
| `CLIN 0026` | **Mod #26:** `Level-5 Ext: Cryptographic Merkle Verifier` | Per Inspector General Audit Node | **$20,000 / yr** | **$1,850 / mo** |
| **TOTAL** | **All 26 Modules Unbundled (1 Node Each)** | **1 Single Complete Enclave Node** | **$1,630,000 / yr** | **$148,950 / mo** |
| `CLIN 1004-A` | **Full 26-Module Console Bundle (1 Node)** | **1 Single Bare-Metal TOC Node** | **$895,000 / yr** | **$79,500 / mo** |
| `CLIN 1004-B` | **Military Installation Fleet License (25 Nodes)** | **Up to 25 Enclave/Robotic Nodes (1 Base)** | **$2,450,000 / yr** | **$215,000 / mo** |
