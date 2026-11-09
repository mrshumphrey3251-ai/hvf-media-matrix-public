# PHASE 1: 6-MONTH HARDWARE-IN-THE-LOOP (HIL) BENCHTOP TEST PLAN
**Contractor:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)  
**Objective:** Benchtop Electrical & Telemetry Validation of 480V SiC Interlocks & C2 Software  
**Baseline Posture:** Laboratory Testing (TRL 4) prior to physical vehicle packaging (TRL 5/6)  

---

## 1. MONTH-BY-MONTH TECHNICAL MILESTONES

### Month 1: Test Bench Instrumentation & Low-Voltage Setup
* Commission National Instruments PXIe real-time test chassis with high-speed analog/CAN I/O.
* Wire low-voltage gate drive control loop and link bare-metal C2 telemetry scripts.
* Validate CAN bus transmission under baseline non-fault conditions.

### Month 2: SiC Solid-State Gate Driver Interconnect & Timing
* Integrate Wolfspeed 1200V Silicon Carbide (SiC) power MOSFET evaluation module.
* Measure gate turn-off latency with Keysight high-bandwidth oscilloscope.
* **Pass Criterion:** Quench gate voltage within <40 nanoseconds upon synthetic fault trigger.

### Month 3: 480V 3-Phase Low-Current Switched Injection
* Energize isolated 480V 3-phase benchtop feed using controlled bench power supply (10A current limit).
* Execute synthetic over-current and phase-imbalance injections.
* **Pass Criterion:** Zero arc-flash propagation; solid-state galvanic isolation maintained.

### Month 4: Full 150 kW Load-Bank Thermal & Arc-Fault Quench
* Connect resistive/inductive 150 kW load bank matching Capstone turbine generator output profile.
* Stress-test SiC thermal dissipative spreaders and active cooling loops under continuous load.
* Simulate dead short at load terminals to verify microsecond fault clearing without thermal runaway.

### Month 5: C2 Cryptographic Telemetry Saturation & Merkle Validation
* Saturate CAN bus network with simulated vehicle sensor traffic (1,000 frames/sec).
* Execute bit-tamper injection into active telemetry frames to verify real-time rejection.
* Validate Merkle DAG hash recomputation across dynamic operational audit logs.

### Month 6: Final Feasibility Report & Phase 2 Integration Blueprint
* Compile oscilloscope captures, thermal imaging logs, and latency distributions.
* Deliver complete Phase 1 Technical Closeout Report and Phase 2 vehicle integration package.