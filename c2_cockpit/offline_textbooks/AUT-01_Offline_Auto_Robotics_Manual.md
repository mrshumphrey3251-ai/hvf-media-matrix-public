# SAE J1979 / J1939 CAN-Bus Diagnostics, ASE Master Technician Series & ANSI B71.1 Small-Engine Service Manual (LOCAL OFFLINE AIR-GAP EDITION)
- **Course Code:** `AUT-01` | **Sovereign Air-Gap Vault:** `c2_cockpit/offline_textbooks/AUT-01_Offline_Auto_Robotics_Manual.md`
- **Governing Authority:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OK Title 61)

## Covered Syllabus & Governing Standards
Ch 1: SAE J1979/ISO 11898 CAN-Bus (60-Ohm) | Ch 2: 4-Stroke Otto/Diesel Compression & Leakdown | Ch 3: Wideband Lambda & Fuel Trim | Ch 4: Charging/Starting Voltage Drop | Ch 5-10: Hydraulics, 2-Stroke/Small-Engine, Brakes, HVAC & Three-Brain Interlock

## Module-by-Module Reading & Exam Focus Directives (Units 01 - 10)
- **Unit 01 — Assigned Reading:** `ISO 11898-2 High-Speed CAN Spec & SAE J1979 / J1939 Physical Layer Manual`  
  *What to Focus On for the Exam Gate:* Focus on parallel 120-Ohm termination resistance (R_bus = 60.0 Ohms), dominant differential voltage V_diff = V_CANH - V_CANL = 2.0V, and OSHA 1910.147 LOTO chassis stabilization.
- **Unit 02 — Assigned Reading:** `ASE A1/A2 Engine Repair Manual & Heywood Internal Combustion Engine Fundamentals Ch. 2`  
  *What to Focus On for the Exam Gate:* Focus on Swept Displacement V_d = (pi/4)*B^2*S*N, Static Compression Ratio CR = (V_d + V_c)/V_c, and cylinder differential leakdown limits (<= 10-12%).
- **Unit 03 — Assigned Reading:** `SAE J1979 OBD-II Mode $01/$06 Fuel System Spec & Bosch Automotive Handbook (Fuel Management)`  
  *What to Focus On for the Exam Gate:* Focus on Stoichiometric Air-Fuel Ratio (14.7:1 gasoline / 14.5:1 diesel), Lambda equivalence ratio, and combined Short-Term + Long-Term Fuel Trim (STFT + LTFT) fault thresholds.
- **Unit 04 — Assigned Reading:** `SAE J537 Storage Battery Standards & Heavy-Duty Starting/Charging Diagnostics Manual`  
  *What to Focus On for the Exam Gate:* Focus on Ohm's Law parasitic draw (< 50 mA), starter-circuit maximum allowable voltage drop (<= 0.50V total cable drop under cranking load), and alternator ripple (< 50 mV AC).
- **Unit 05 — Assigned Reading:** `ISO 4413 Hydraulic Fluid Power & Mobile Agricultural Tractor Hydraulics Manual`  
  *What to Focus On for the Exam Gate:* Focus on Pascal's Law actuator force F = P * A, hydraulic pump volumetric efficiency, and high-pressure pinhole fluid-injection life-safety lockout.
- **Unit 06 — Assigned Reading:** `ANSI/OPEI B71.1 Commercial Turf/Small-Engine Safety Standard & 2-Stroke/4-Stroke Service Manual`  
  *What to Focus On for the Exam Gate:* Focus on magneto ignition air-gap (0.010-0.014 in), 2-stroke fuel-to-oil mixing ratios (50:1 = 2.6 fl oz oil per gallon), and blade tip speed safety limits (<= 19,000 ft/min).
- **Unit 07 — Assigned Reading:** `FMVSS 105 / 121 Hydraulic & Air Brake Systems Manual`  
  *What to Focus On for the Exam Gate:* Focus on rotor minimum machine-to/discard thickness tolerances, lateral runout (<= 0.002 in), and dual-circuit master cylinder hydraulic pressure ratios.
- **Unit 08 — Assigned Reading:** `SAE J639 Mobile Air Conditioning Standards & EPA Section 609 Refrigerant Recovery Manual`  
  *What to Focus On for the Exam Gate:* Focus on R-134a / R-1234yf pressure-temperature saturation relationships, superheat/subcooling diagnostics, and manifold gauge high/low-side fault isolation.
- **Unit 09 — Assigned Reading:** `SAE J429 / ISO 898-1 Fastener Metallurgy & Torque-Tension Engineering Manual`  
  *What to Focus On for the Exam Gate:* Focus on the Torque-Preload equation T = K * D * F / 12, dry vs. lubricated K-factor reductions, and extracting sheared bolts without damaging parent threads.
- **Unit 10 — Assigned Reading:** `EBONY-RTOS Hardware Guillotine Spec & ISO 26262 ASIL-D Functional Safety Manual`  
  *What to Focus On for the Exam Gate:* Focus on the 36.75 ns hardware safety interlock, CAN-Bus command authentication, and WORM cryptographic shop sign-off.

## Offline Field Reference Notes
This local file is stored permanently on your NVMe/SSD inside `c2_cockpit/offline_textbooks/` so it remains 100% accessible when operating in **Offline (Sovereign Fortress Air-Gap)** mode without internet connectivity.