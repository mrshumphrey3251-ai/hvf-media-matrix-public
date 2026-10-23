# SAE J1979 / J1939 CAN-Bus Diagnostics, ASE Master Technician Series & ANSI B71.1 Small-Engine Service Manual (LOCAL OFFLINE AIR-GAP EDITION)
- **Course Code:** `AUT-01` | **Sovereign Air-Gap Vault:** `c2_cockpit/offline_textbooks/AUT-01_Offline_Auto_Robotics_Manual.md`
- **Governing Authority:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OK Title 61)

## Module-by-Module Reading & Exam Focus Directives (Units 01 - 10)
- **Unit 01 — Assigned Reading:** `ISO 11898-2 High-Speed CAN Spec & SAE J1979 / J1939 Physical Layer Manual`  
  *What to Focus On for the Exam Gate:* Focus on parallel 120-Ohm termination resistance (R_bus = 60.0 Ohms), dominant differential voltage V_diff = V_CANH - V_CANL = 2.0V, and Portable NVIDIA Three-Brain Enclave signal isolation.
- **Unit 02 — Assigned Reading:** `SAE J1979 Mode 0x01 Fuel System Spec & Heywood ICE Fundamentals (Stoichiometry & VE)`  
  *What to Focus On for the Exam Gate:* Focus on Stoichiometric Combustion (Lambda = 1.00, AFR = 14.7:1), MAF Volumetric Efficiency (VE_%), and Combined Short-Term + Long-Term Fuel Trim (STFT + LTFT) P0171 lean fault thresholds.
- **Unit 03 — Assigned Reading:** `SAE J1979 Mode 0x06 Misfire Monitor Spec & Secondary Ignition Waveform Diagnostics Manual`  
  *What to Focus On for the Exam Gate:* Focus on Ignition Secondary KV firing/spark-line waveforms, Crankshaft Position (CKP) angular acceleration drop, and Mode 0x06 EWMA misfire counters (P0300).
- **Unit 04 — Assigned Reading:** `SAE J1939 High-Pressure Common-Rail (HPCR) & Piezo/Solenoid Direct-Injection Service Manual`  
  *What to Focus On for the Exam Gate:* Focus on rail pressure control loop dynamics (P0087 low rail pressure), injector return-flow volume limits, and low-pressure lift-pump hydraulic supply verification.
- **Unit 05 — Assigned Reading:** `Turbocharger Thermodynamics & Variable Geometry (VGT) / Wastegate PID Control Manual`  
  *What to Focus On for the Exam Gate:* Focus on compressor pressure ratio (PR = P_out / P_in), VGT vane duty-cycle hysteresis (P0299 underboost), and charge-air cooler (intercooler) thermal effectiveness.
- **Unit 06 — Assigned Reading:** `SAE J1939 / ISO 14229 Automatic Transmission Hydraulics & TCM Calibration Manual`  
  *What to Focus On for the Exam Gate:* Focus on line-pressure solenoid hydraulics (P0700), Torque Converter Clutch (TCC) slip RPM limits, and TCM Clutch Volume Index (CVI) adaptive fast-learn volumes.
- **Unit 07 — Assigned Reading:** `EPA Tier 4 / OBD-II Catalyst Monitor Spec & Three-Way Catalytic (TWC) Chemistry Manual`  
  *What to Focus On for the Exam Gate:* Focus on Oxygen Storage Capacity (OSC), upstream wideband vs. downstream switching O2 frequency ratio (P0420), and exhaust backpressure limits (<= 1.25 psi at idle).
- **Unit 08 — Assigned Reading:** `FMVSS 126 Electronic Stability Control (ESC) & ABS Chassis Dynamics Manual`  
  *What to Focus On for the Exam Gate:* Focus on wheel-speed sensor reluctance/active air-gap faults (C0035), Steering Angle Sensor (SAS) 0.0-deg zero-point calibration, and yaw-rate lateral deceleration physics.
- **Unit 09 — Assigned Reading:** `API SP / SAE J300 Tribology & SAE J429 / ISO 898-1 Fastener Torque-to-Yield Manual`  
  *What to Focus On for the Exam Gate:* Focus on 0-100k+ mile fluid shear stability, Torque-Preload mechanics (T = K * D * F / 12), and Torque-to-Yield (TTY) plastic-region angular clamping.
- **Unit 10 — Assigned Reading:** `ISO 14229 Unified Diagnostic Services (UDS) & SAE J2534 Pass-Thru / Brain-3 WORM Spec`  
  *What to Focus On for the Exam Gate:* Focus on UDS services (0x10 Session, 0x22 ReadData, 0x27 SecurityAccess, 0x2E WriteData, 0x31 RoutineControl), EEPROM CRC-32 checksums (B1000), and 36.75ns Brain-3 WORM sealing.

## Offline Field Reference Notes
This local file is stored permanently on your NVMe/SSD inside `c2_cockpit/offline_textbooks/` so it remains 100% accessible when operating in **Offline (Sovereign Fortress Air-Gap)** mode without internet connectivity.