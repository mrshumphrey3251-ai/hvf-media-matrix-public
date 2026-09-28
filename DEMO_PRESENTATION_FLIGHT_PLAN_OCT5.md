# PROJECT EBONY: DOD EVALUATOR DEMONSTRATION FLIGHT PLAN
**Session Target:** CDAO / ACC-RI Formal Demo Presentation  
**Scheduled Date:** Monday, October 5, 2026 @ 10:00 AM CDT  
**Audience:** Leshia Pearson & ACC-RI Evaluation Directorate  
**Presenter:** Jeffery Humphrey, CEO & Subject Matter Expert (Humphrey Virtual Farms LLC, CAGE: 1AHA8)  
**Submission Identifier:** Tradewinds Solutions Marketplace #9-26-3703  
**Classification / Rights:** UNCLASSIFIED // DFARS 252.227-7018 Government Purpose Rights  

---

## 30-Minute Executive Demonstration Agenda

### Phase 1: Authority & Statutory Posture (00:00 - 05:00)
* **Opening Statement:** Introduce Humphrey Virtual Farms LLC (CAGE: 1AHA8) and Project Ebony as an operational bare-metal C2 and microgrid defense platform.
* **Data Rights Declaration:** Affirm DFARS 252.227-7018 GPR and Oklahoma HB 2992 statutory protections.
* **Architecture Briefing:** Explain the bare-metal Windows architecture, zero cloud dependencies, and air-gapped dual-repository model.

### Phase 2: Live Tactical HUD & Kinetic SCADA Execution (05:00 - 15:00)
* **Workstation Cockpit:** Display Streamlit Tactical HUD (http://127.0.0.1:8501) isolated to loopback.
* **Vector 1 (Microgrid SCADA):** Showcase 4/4 synchronized contactors (CH1_UTILITY_GRID, CH2_PV_ARRAYS, CH3_BESS_STORAGE, CH4_AUX_GENERATOR). Demonstrate 2.04 µs Modbus FC05 coil response.
* **Vector 2 (Aerial UAS):** Highlight DJI Matrice 350 RTK tracking on Sortie Delta 02 at 75.0m MSL.
* **Vector 3 (Dismounted BFT):** Review tracking of EBONY_ACTUAL, PHANTOM_RECON, and VALKYRIE_ONE with 0 active distress flags.

### Phase 3: Cryptographic Root of Trust & Anti-Fabrication Boundary (15:00 - 22:00)
* **Vector 4 (Merkle Ledger):** Query forensic_audit_ledger live on terminal. Demonstrate Ed25519 asymmetric signature authentication across 82 unbroken blocks.
* **Vector 5 (Reality Firewall):** Execute live interrogation drill. Demonstrate instant runtime interception (RealityAssertionError) against synthetic hallucinations or non-existent files.

### Phase 4: Machine-Readable Evaluator Ingress (22:00 - 27:00)
* **Vector 8 (Ingress Daemon):** Interrogate Port 8502 live via curl or python probe. Show real-time HTTP 200 responses for /evaluator/posture, /evaluator/telemetry, and /evaluator/dispatch.
* **Forensic Autologging:** Open SQLite database and show immediate forensic recording inside evaluator_ingress_audit_log with microsecond latency tags.

### Phase 5: Transition to Awardability & Q&A (27:00 - 30:00)
* **Deliverable Review:** Present TRADEWINDS_CDAO_EVALUATOR_BUNDLE_v1.0.0.zip (SHA256: 4baa0287...).
* **Closing:** Reaffirm production readiness (TRL 7/8) and invite technical evaluation cross-examination.

---

*Authored and certified under Level 5 Unrestricted Authority by Jeffery Humphrey, CEO / SME.*
