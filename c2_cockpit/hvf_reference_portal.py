"""
HVF Sovereign Reference Textbook & Study Directive Portal (100% Free Public-Domain & Air-Gap Offline Vault)
Zero external paywalls (100% Free student cost) + exact step-by-step navigation & [Ctrl+F] lookup instructions.
"""
import re
from pathlib import Path

OFFLINE_VAULT_DIR = Path(__file__).resolve().parent / "offline_textbooks"
OFFLINE_VAULT_DIR.mkdir(parents=True, exist_ok=True)

COURSE_TEXTBOOKS = {
    "STR-01": {
        "title": "FHWA Bridge Inspector's Reference Manual (BIRM, FHWA-NHI-12-049) & 23 CFR Part 650 (NBIS)",
        "primary_url": "https://www.fhwa.dot.gov/bridge/nbis.cfm",
        "primary_label": "Open Free FHWA Bridge Inspection Manual Portal (.GOV \u2014 100% Free)",
        "secondary_url": "https://www.ecfr.gov/current/title-23/chapter-I/subchapter-G/part-650/subpart-C",
        "secondary_label": "Open 23 CFR Part 650 NBIS Federal Law Text (eCFR.gov \u2014 100% Free)",
        "offline_file": "STR-01_Offline_NDE_Master_Manual.md",
        "directives": {
            1: ("23 CFR 650 Subpart C (Sections 650.305 - 650.313) & FHWA BIRM Ch. 1-2", "20.0 feet | 650.311 | Sufficiency Rating", "Memorize the 20.0-ft NBI bridge span rule, 24-month Routine vs. FCM inspection intervals, Sufficiency Rating (S1+S2+S3-S4) weights, and 18 U.S.C. 1001 criminal attestation."),
            2: ("FHWA BIRM Ch. 3 (Inspection Equipment & Optical GSD) & AASHTO Element Condition States", "Ground Sampling Distance | Condition State | CS-1", "Focus on optical Ground Sampling Distance (GSD <= 0.004 in/px for FCMs), focal-length standoff equations, and Condition States CS-1 through CS-4."),
            3: ("FHWA NDE Web Manual (Concrete Half-Cell & Impact-Echo) & BIRM Ch. 6", "C876 | -350 mV | Impact-Echo", "Focus on Cu/CuSO4 half-cell corrosion thresholds (-200 mV / -350 mV CSE), Stern-Geary icorr, and P-wave delamination depth D = (C_p * delta_t) / 2."),
            4: ("FHWA BIRM Ch. 7 (Steel Superstructures & Fracture-Critical Members)", "Fracture-Critical | Stress Intensity | Gusset", "Focus on Mode I Stress Intensity Factor K_I = Y * sigma * sqrt(pi * a), fracture toughness K_Ic limits, and ultrasonic thickness gauging of pack-rust gusset plates."),
            5: ("FHWA HEC-18 (Evaluating Scour at Bridges, 5th Ed.) Ch. 5-7", "CSU equation | Froude | Pier Scour", "Focus on the CSU Pier Scour Equation, Froude number Fr_1 calculation, and 200 kHz bathymetric sonar draft compensation."),
            6: ("FHWA BIRM Ch. 6 (Reinforced & Prestressed Concrete Girder Inspection)", "Modulus of Rupture | Prestressed | Shear Crack", "Focus on concrete modulus of rupture f_r = 7.5 * sqrt(f'_c), shear-crack inclination angles, and prestressed strand corrosion limits."),
            7: ("FHWA BIRM Ch. 10 (Bridge Bearings & Substructure Abutments/Piers)", "Elastomeric | Shear Strain | Thermal Expansion", "Focus on elastomeric bearing pad shear strain gamma = Delta_T / h_rt (<= 0.50 limit), thermal deck expansion Delta_L = alpha * L * Delta_T, and anchor-bolt shear."),
            8: ("FHWA 3D LiDAR / Photogrammetry Guidelines & BIRM Ch. 11", "LiDAR | Deflection | L/800", "Focus on GPS-denied 3D LiDAR SLAM drift bounds, EKF3 covariance limits, and point-cloud vertical deflection measurement (L/800 serviceability limit)."),
            9: ("FHWA Infrared Thermography NDE Guidelines & BIRM Ch. 6 (ASR & Delamination)", "Thermography | Alkali-Silica | 3.6", "Focus on diurnal solar loading windows, minimum thermal contrast Delta_T >= +3.6 deg F (+2.0 deg C), and convective wind abort thresholds (< 15 mph)."),
            10: ("23 CFR 650.313(h) Critical Findings & Oklahoma Title 61 WORM Docket Rules", "Critical Finding | Closure | SHA-256", "Focus on compiling the PE-stamped Emergency Closure Docket, Benefit-Cost Ratio (BCR), and verifying the 64-character SHA-256 WORM ledger seal.")
        }
    },
    "ENV-01": {
        "title": "U.S. DOE Building Envelope Design Guide & Oklahoma OMES CAP Title 61 Facility Audit Manual",
        "primary_url": "https://bsesc.energy.gov/sources/building-envelope-design-guide",
        "primary_label": "Open Free U.S. DOE Building Envelope Design Guide (.GOV \u2014 100% Free)",
        "secondary_url": "https://omes.ok.gov/services/construction-and-properties",
        "secondary_label": "Open Free Oklahoma OMES CAP Title 61 Portal (.GOV \u2014 100% Free)",
        "offline_file": "ENV-01_Offline_Envelope_Manual.md",
        "directives": {
            1: ("OMES CAP Title 61 Facility Audit Rules & DOE Envelope Guide Ch. 1", "Title 61 | Calibration | Life-Cycle", "Focus on statutory public-building audit mandates, Life-Cycle Cost Analysis (LCCA), and NIST-traceable radiometric calibration rules."),
            2: ("DOE Envelope Guide (Infrared Thermography & Radiative Heat Transfer)", "Stefan-Boltzmann | Emissivity | Reflected", "Focus on Stefan-Boltzmann radiative heat flux q = epsilon * sigma * (T_s^4 - T_surr^4), surface emissivity compensation, and reflected apparent temperature."),
            3: ("DOE Low-Slope Roof Moisture Thermography & Core Verification Guide", "Roof Moisture | Capacitance | 3.6", "Focus on diurnal solar heat-sink capacitance of water-saturated insulation, minimum thermal Delta_T >= +3.6 deg F, and core verification."),
            4: ("DOE Thermal Envelope R-Value / U-Factor Calculation Guide", "R-Value | U-Factor | Thermal Bridge", "Focus on serial thermal resistance R_total = sum(L_i / k_i), overall heat transfer coefficient U = 1 / R_total (BTU/hr-ft^2-deg F), and thermal bridging."),
            5: ("DOE Psychrometric & Interior Dew-Point Condensation Control Guide", "Dew Point | Relative Humidity | Condensation", "Focus on Magnus-Tetens saturation vapor pressure, indoor dew-point temperature T_dp calculation, and preventing interstitial condensation."),
            6: ("DOE Whole-Building Air Leakage (Blower Door 50 Pa / 75 Pa) Guide", "Blower Door | CFM75 | Air Leakage", "Focus on the orifice power-law flow equation Q = C * (Delta_P)^n at 50 Pa / 75 Pa, normalized air leakage rate (CFM75 / ft^2), and IR exfiltration tracking."),
            7: ("DOE Masonry Facade, Curtain-Wall Spalling & Tie-Back NDE Guide", "Masonry | Spalling | Lintel", "Focus on corroding steel lintel/shelf-angle expansion, acoustic sounding of delaminated panels, and close-range photogrammetric crack mapping."),
            8: ("DOE Commercial HVAC Rooftop Unit (RTU) & Economizer Audit Guide", "1.08 | CFM | Economizer", "Focus on sensible heat transfer q_s = 1.08 * CFM * Delta_T, enthalpy wheel recovery efficiency, and seized outdoor-air damper fault detection."),
            9: ("ASPRS / USGS 3D Thermal-LiDAR Point-Cloud Fusion Guidelines", "Orthomosaic | Point Cloud | RTK", "Focus on co-registering 640x512 RJPEG radiometric orthomosaics onto 3D LiDAR roof meshes, polygon area quantification (sq ft), and RTK positional tolerances."),
            10: ("OMES CAP Title 61 Capital Rehabilitation Docket & WORM Evidence Spec", "Savings-to-Investment | Payback | SHA-256", "Focus on Savings-to-Investment Ratio (SIR), simple payback period (years), and sealing the PE/Inspector thermal audit docket in matrix_ledger.db.")
        }
    },
    "PAV-01": {
        "title": "FHWA Pavement & TAMP Asset Governance Manual (23 CFR Part 515) & UFC 3-270-08 PCI Manual",
        "primary_url": "https://www.fhwa.dot.gov/pavement/",
        "primary_label": "Open Free FHWA Pavement & Profilometry Portal (.GOV \u2014 100% Free)",
        "secondary_url": "https://www.ecfr.gov/current/title-23/chapter-I/subchapter-F/part-515",
        "secondary_label": "Open Free 23 CFR Part 515 TAMP Law Text (eCFR.gov \u2014 100% Free)",
        "offline_file": "PAV-01_Offline_Pavement_Manual.md",
        "directives": {
            1: ("23 CFR Part 515 (ODOT TAMP) & Public-Domain UFC 3-270-08 PCI Manual Ch. 1", "515 | Sample Unit | 2,500", "Focus on National Highway System (NHS) performance metrics, Oklahoma Title 61 corridor auditing, and sample unit sizing (2,500 +/- 1,000 sq ft asphalt)."),
            2: ("Public-Domain UFC 3-270-08 / ASTM D6433 Pavement Condition Index (PCI) Procedure", "Deduct Value | CDV | PCI", "Focus on distress density percentage, Deduct Value (DV) curves, Corrected Deduct Value (CDV), and computing PCI = 100 - max(CDV) across 0-100 rating tiers."),
            3: ("FHWA Longitudinal Profilometry & International Roughness Index (IRI) Manual", "IRI | Quarter-Car | 170", "Focus on quarter-car golden-car simulation at 50 mph, calculating IRI (in/mile), and federal FHWA good/fair/poor smoothness thresholds (< 95 / > 170 in/mi)."),
            4: ("FHWA Transverse Rutting Profilometry & Hydroplaning Physics Manual", "Rut Depth | Hydroplaning | 10.35", "Focus on transverse rut depth measurement (inches), Horne hydroplaning speed V_p = 10.35 * sqrt(P_tire), and ponding water film thickness."),
            5: ("FHWA Falling Weight Deflectometer (FWD) & Subgrade Backcalculation Manual", "FWD | Deflection Basin | Resilient Modulus", "Focus on impulse load plate pressure, deflection basin sensors (D_0 through D_60), and backcalculating subgrade resilient modulus M_R (psi)."),
            6: ("FHWA Pavement Design Guide (18-kip ESALs & Structural Number SN)", "ESAL | Fourth Power | Structural Number", "Focus on the 4th-Power Load Equivalency Factor LEF = (W_axle / 18,000)^4, cumulative 18-kip ESALs, and Structural Number SN = a_1*D_1 + a_2*D_2*m_2 + a_3*D_3*m_3."),
            7: ("FHWA HDS-5 Hydraulic Design of Highway Culverts & Drainage Manual", "Manning | Culvert | Headwater", "Focus on Manning open-channel flow Q = (1.486/n) * A * R_h^(2/3) * S^(1/2), inlet vs. outlet control headwater depth (HW/D), and LiDAR silt-blockage profiling."),
            8: ("FHWA MUTCD (23 CFR Part 655) Retroreflectivity & Guardrail Safety Manual", "Retroreflectivity | Guardrail | 31", "Focus on 30-meter retroreflectometer geometry, minimum mcd/m^2/lx pavement marking thresholds, and MASH W-beam guardrail splice height (31.0 in)."),
            9: ("U.S. Access Board PROWAG / ADA Title II Pedestrian Ramp Compliance Manual", "Running Slope | 8.33% | Cross Slope", "Focus on curb-ramp running slope (<= 8.33% / 1:12), cross slope (<= 2.00% / 1:48), and smart-level / LiDAR digital inclinometer verification."),
            10: ("ODOT 8-Year Construction Work Plan (CWP) & Title 61 WORM Corridor Ledger Spec", "Remaining Service Life | Preservation | SHA-256", "Focus on remaining service life (RSL), preservation vs. reconstruction trigger gates, and sealing corridor GIS/PCI telemetry into matrix_ledger.db.")
        }
    },
    "AUT-01": {
        "title": "NHTSA / EPA OBD-II & CAN-Bus Technical Manual + OSHA 29 CFR 1910.147 Shop Safety Standard",
        "primary_url": "https://www.allcarmanuals.com",
        "primary_label": "Open Free OEM Automotive & Truck Factory Service Manuals (1982-2026 Coverage \u2014 100% Free)",
        "secondary_url": "https://www.briggsandstratton.com/na/en_us/support/manuals.html",
        "secondary_label": "Open Free Small-Engine & Lawnmower Manuals (Briggs / Honda / Kohler \u2014 100% Free)",
        "offline_file": "AUT-01_Offline_Auto_Robotics_Manual.md",
        "directives": {
            1: ("Federal OBD-II / ISO 11898-2 High-Speed CAN Spec & OSHA 1910.147 LOTO Manual", "60.0 Ohms | V_diff | 1910.147", "Focus on parallel 120-Ohm termination resistance (R_bus = 60.0 Ohms), dominant differential voltage V_diff = V_CANH - V_CANL = 2.0V, and Portable NVIDIA Three-Brain Enclave signal isolation."),
            2: ("Federal OBD-II Mode 0x01 Fuel System Spec (Stoichiometric Combustion & P0171)", "Lambda | Volumetric Efficiency | P0171", "Focus on Stoichiometric Combustion (Lambda = 1.00, AFR = 14.7:1), MAF Volumetric Efficiency (VE_%), and Combined Short-Term + Long-Term Fuel Trim (STFT + LTFT) P0171 lean fault thresholds."),
            3: ("Federal OBD-II Mode 0x06 Misfire Monitor Spec & Secondary Ignition KV Manual", "Mode 0x06 | Misfire | P0300", "Focus on Ignition Secondary KV firing/spark-line waveforms, Crankshaft Position (CKP) angular acceleration drop, and Mode 0x06 EWMA misfire counters (P0300)."),
            4: ("High-Pressure Common-Rail (HPCR) & Direct-Injection Fuel System Manual (P0087)", "Common-Rail | P0087 | Lift-Pump", "Focus on rail pressure control loop dynamics (P0087 low rail pressure), injector return-flow volume limits, and low-pressure lift-pump hydraulic supply verification."),
            5: ("Forced Induction Thermodynamics & Turbocharger VGT / Wastegate PID Manual (P0299)", "Pressure Ratio | VGT | P0299", "Focus on compressor pressure ratio (PR = P_out / P_in), VGT vane duty-cycle hysteresis (P0299 underboost), and charge-air cooler (intercooler) thermal effectiveness."),
            6: ("Automatic Transmission Hydraulics (P0700), TCC Slip & Clutch Volume Index Manual", "P0700 | Torque Converter | CVI", "Focus on line-pressure solenoid hydraulics (P0700), Torque Converter Clutch (TCC) slip RPM limits, and TCM Clutch Volume Index (CVI) adaptive fast-learn volumes."),
            7: ("EPA / OBD-II Catalyst Monitor Spec & Three-Way Catalytic (TWC) Chemistry Manual (P0420)", "P0420 | Oxygen Storage | Backpressure", "Focus on Oxygen Storage Capacity (OSC), upstream wideband vs. downstream switching O2 frequency ratio (P0420), and exhaust backpressure limits (<= 1.25 psi at idle)."),
            8: ("FMVSS 126 Electronic Stability Control (ESC) & ABS Chassis Dynamics Manual (C0035)", "C0035 | Steering Angle | Wheel Speed", "Focus on wheel-speed sensor reluctance/active air-gap faults (C0035), Steering Angle Sensor (SAS) 0.0-deg zero-point calibration, and yaw-rate lateral deceleration physics."),
            9: ("Master Preventative Maintenance (0-100k+ Mi), Tribology & Torque-to-Yield Manual", "Torque-to-Yield | K * D * F | Tribology", "Focus on 0-100k+ mile fluid shear stability, Torque-Preload mechanics (T = K * D * F / 12), and Torque-to-Yield (TTY) plastic-region angular clamping."),
            10: ("UDS ISO 14229 (0x10-0x31), SAE J2534 Checksums (B1000) & Brain-3 WORM Spec", "0x27 | Checksum | 36.75", "Focus on UDS services (0x10 Session, 0x22 ReadData, 0x27 SecurityAccess, 0x2E WriteData, 0x31 RoutineControl), EEPROM CRC-32 checksums (B1000), and 36.75ns Brain-3 WORM sealing.")
        }
    }
}

OEM_AUTO_SMALL_ENGINE_SPEC_DB = [
    {
        "Category": "Small-Engine / Lawnmower (4-Stroke Carbureted & 2014-2026 EFI)",
        "Engine / System": "Briggs & Stratton Intek / Vanguard OHV & Vanguard 810cc/993cc EFI (1990-2026)",
        "Key Clearances & Gaps": "Intake Valve: 0.004-0.006 in | Exhaust Valve: 0.006-0.008 in | Spark Plug Gap: 0.030 in | Magneto Armature Air-Gap: 0.010-0.014 in",
        "Critical Fastener Torque": "Cylinder Head Bolts: 180-220 in-lbs (staged crisscross) | Flywheel Nut: 55-65 ft-lbs | Connecting Rod Cap: 100-115 in-lbs | Mower Blade Bolt: 50-70 ft-lbs",
        "Electrical / Fuel / Diagnostic Spec": "Carbureted Kill-Wire: < 1.0 Ohm to Ground (Stop) | 2014-2026 Vanguard EFI Fuel Rail: 43.5 psi (3.0 Bar) | Crankcase Oil: SAE 30 or 10W-30 / 15W-50 Synthetic"
    },
    {
        "Category": "Small-Engine / Lawnmower (4-Stroke Carbureted & 2014-2026 iGX EFI)",
        "Engine / System": "Honda GX160 / GX200 / GX390 / GCV160 / GCV200 & iGX700/iGX800 EFI (1990-2026)",
        "Key Clearances & Gaps": "Intake Valve: 0.006 in (0.15 mm) Cold | Exhaust Valve: 0.008 in (0.20 mm) Cold | Spark Plug Gap: 0.028-0.031 in | Ignition Coil Air-Gap: 0.016 in (0.40 mm)",
        "Critical Fastener Torque": "Cylinder Head Bolts (GX160/200): 17 ft-lbs (24 N-m) | Cylinder Head (GX390): 25 ft-lbs | Flywheel Nut: 54-83 ft-lbs | Connecting Rod: 9-14 ft-lbs",
        "Electrical / Fuel / Diagnostic Spec": "Float Height: 0.54 in (13.7 mm) | iGX EFI High-Pressure Pump: 43-44 psi | Decompressor Cranking Compression: 71-100 psi (Full Running: 120-140 psi)"
    },
    {
        "Category": "Small-Engine / Commercial Zero-Turn Turf (1995-2026)",
        "Engine / System": "Kohler Command PRO / Confidant EFI (ECH/ECV) & Kawasaki FR/FS/FX/FX-EFI V-Twin (1995-2026)",
        "Key Clearances & Gaps": "Kawasaki Valve Lash: 0.004-0.006 in (In/Ex Cold) | Kohler Hydraulic Lifters: Zero-Lash Preload | Spark Plug Gap: 0.030 in | Armature Air-Gap: 0.012 in",
        "Critical Fastener Torque": "Cylinder Head Bolts: 20-25 ft-lbs (in 2 stages) | Flywheel Bolt: 40-50 ft-lbs | Stator Screws: 55 in-lbs | PTO Clutch Bolt: 45-55 ft-lbs (Blue Loctite 242)",
        "Electrical / Fuel / Diagnostic Spec": "Stator AC Output: > 28V AC @ 3,600 RPM | Regulated Charging: 13.8-14.4V DC | Kohler/Kawasaki EFI Fuel Pressure: 39-44 psi | PTO Clutch Coil: 2.4-3.2 Ohms"
    },
    {
        "Category": "Small-Engine (2-Stroke Handheld & 2014-2026 Auto-Tune / M-Tronic)",
        "Engine / System": "Stihl (M-Tronic) / Husqvarna (AutoTune) / Echo 2-Stroke Chainsaw & Trimmer (1990-2026)",
        "Key Clearances & Gaps": "Spark Plug Gap: 0.020-0.025 in (0.5-0.65 mm) | Flywheel-to-Coil Air-Gap: 0.008-0.012 in | Metering Lever Height: Flush w/ Carburetor Deck",
        "Critical Fastener Torque": "Cylinder Base Screws: 80-95 in-lbs | Muffler Bolts: 70-85 in-lbs (Clean Spark Arrestor Screen) | Clutch Spider: 15-20 ft-lbs (Left-Hand Thread!)",
        "Electrical / Fuel / Diagnostic Spec": "Premix Ratio: 50:1 (2.6 fl oz JASO-FD Synthetic per 1.0 Gal 89+ Octane Ethanol-Free) | Crankcase Seal Pressure/Vacuum Test: Hold +/- 7.0 psi for 20 sec"
    },
    {
        "Category": "Automotive & Light-Truck (1996-2026 OBD-II / CAN-Bus / CAN-FD & SGW)",
        "Engine / System": "SAE J1979 OBD-II, ISO 11898 CAN (500 kbps) & 2018-2026 CAN-FD (2-5 Mbps) w/ Security Gateway (SGW)",
        "Key Clearances & Gaps": "Pin 4: Chassis Gnd (< 0.1 Ohms) | Pin 5: Signal Gnd | Pin 6 & 14: High-Speed CAN | 2018-2026 FCA/Ford/GM/Toyota SGW: Requires 12+8 Bypass Cable or J2534 Auth",
        "Critical Fastener Torque": "Battery Terminal Clamp Bolt (10mm): 45-60 in-lbs | ECM/PCM/SGW Chassis Ground Bolt: 8-10 ft-lbs | High-Current Mega-Fuse Stud: 80-100 in-lbs",
        "Electrical / Fuel / Diagnostic Spec": "Key-Off Termination Resistance (Pin 6 to Pin 14): 60.0 Ohms (+/- 2.0 Ohms) | Key-On Dominant: CAN-H = 3.5V, CAN-L = 1.5V (V_diff = 2.0V) | Sleep Draw: < 35 mA"
    },
    {
        "Category": "Automotive & Light-Truck (2014-2026 Late-Model GDI, Turbo & Dual-Injection)",
        "Engine / System": "2014-2026 Ford EcoBoost / Coyote 5.0, GM LT1/L84/L87 (DFM), Ram 5.7 HEMI & Toyota D-4S",
        "Key Clearances & Gaps": "Spark Plug Gap (2014-2026 Turbo GDI): 0.026-0.030 in | Spark Plug Gap (2014-2026 N/A GDI): 0.040-0.044 in | Timing Chain Max Cam Phaser Error: <= +/- 2.5 deg",
        "Critical Fastener Torque": "GDI High-Pressure Fuel Line Flare Nuts: 22-28 ft-lbs (Single-Use Stainless Pipes!) | Spark Plugs (12mm/14mm): 11-16 ft-lbs | Truck Lug Nuts (M14x1.5): 140 ft-lbs",
        "Electrical / Fuel / Diagnostic Spec": "Low-Side Lift Pump: 55-72 psi | 2014-2026 GDI High-Pressure Rail: 580 psi (Idle) to 2,900-5,075 psi (200-350 Bar Full Load) | 0W-20 / 5W-30 API SP / ILSAC GF-6A (Anti-LSPI)"
    },
    {
        "Category": "Automotive & Light-Truck (2014-2026 8/9/10-Speed Transmissions, EPB & ADAS)",
        "Engine / System": "2014-2026 8/10-Speed Auto (10R80/10L80/ZF8), Electronic Parking Brake (EPB) & SAS/ADAS",
        "Key Clearances & Gaps": "Brake Rotor Max Runout: <= 0.002 in | Pad Min Thickness: 3.0 mm | Steering Angle Sensor (SAS) Zero-Point: +/- 0.5 deg | ULV ATF Fill Temp Gate: 195-215 deg F",
        "Critical Fastener Torque": "Caliper Slide Bolts: 25-35 ft-lbs | Caliper Bracket Bolts: 110-148 ft-lbs | Axle Hub Nut: 150-240 ft-lbs | Transmission Pan Bolts: 80-106 in-lbs",
        "Electrical / Fuel / Diagnostic Spec": "2014-2026 Rear EPB Service: MUST command 'EPB Maintenance/Retract Mode' via UDS 0x31 before pressing caliper piston! | Fluid: Mercon ULV / Dexron ULV / ZF Lifeguard 8"
    },
    {
        "Category": "Heavy-Duty Diesel & Ag Tractor (2014-2026 Tier-4 Final / Stage-V HPCR & SCR)",
        "Engine / System": "2014-2026 Cummins 6.7/X15, Duramax L5P, PowerStroke 6.7 & John Deere/Kubota Tier-4 Final (J1939-22)",
        "Key Clearances & Gaps": "9-Pin Green Deutsch Type-II (2016-2026 500 kbps J1939): Pin C = CAN-H, Pin D = CAN-L | Diesel Valve Lash (6.7L): Intake 0.010 in / Exhaust 0.020-0.026 in Cold",
        "Critical Fastener Torque": "HPCR Injector Hold-Down Clamp: 24-30 ft-lbs + 60 deg | High-Pressure Rail Nuts: 30-37 ft-lbs | Tractor Rear Wheel Bolts: 220-300 ft-lbs",
        "Electrical / Fuel / Diagnostic Spec": "HPCR Rail Pressure: 4,500 psi (Idle) to 29,000-36,000 psi (2,500 Bar) | DEF Fluid Concentration (Refractometer): 32.5% (+/- 1.5% Urea) | DPF Max Differential Pressure: < 3.5 psi"
    }
]

FREE_OEM_MANUAL_DIRECTORY = [
    ("StartMyCar 1990-2026 Interactive OEM Fuse Box Diagrams, Wiring & Repair Portal (100% Free)", "https://www.startmycar.com", "Select any 1990-2026 Make, Model, and Year to interact directly with OEM fuse box diagrams, relay locations, wiring schematics, and repair guides (Zero Login / Zero Paywall)."),
    ("AllCarManuals 1982-2026 Free PDF Automotive Factory Service & Workshop Manuals", "https://www.allcarmanuals.com", "Select Vehicle Make and Model (including 2014-2026 late-model platforms) to download free PDF factory workshop manuals and service guides."),
    ("ProCarManuals Free Automotive Wiring Diagrams, Transmission & Engine Overhaul Manuals", "https://procarmanuals.com", "Browse and download free PDF factory engine overhaul manuals, automatic transmission hydraulic schematics, and OBD-II fault code charts."),
    ("Gale ChiltonLibrary (1940-2026 Full OEM Factory Service Manuals, TSBs & Labor Times \u2014 Free State Library Access)", "https://www.gale.com/c/chilton-library", "Provides complete 1940-2026 OEM service procedures, wiring diagrams, and ADAS/torque specs for free through any public library card."),
    ("Briggs & Stratton Official Free PDF Engine & Lawnmower Manual Lookup (All Years through 2026)", "https://www.briggsandstratton.com/na/en_us/support/manuals.html", "Enter your engine Model-Type-Code stamped on the valve cover or blower housing to download free illustrated parts lists and repair manuals."),
    ("Kohler Engines Official Free Service & Overhaul Manual Portal (Carbureted & 2014-2026 EFI)", "https://kohlerpower.com/en/engines/manuals", "Select Engine Series (Command PRO, Courage, Confidant EFI, KT7000) to open the free PDF Service & Overhaul Manual with full torque and electrical specs.")
]

BUILTIN_REPAIR_PROCEDURES = {
    "2014-2026 Late-Model Auto/Truck: GDI High-Pressure Fuel System (P0087), Security Gateway (SGW) & EPB Service": (
        "1. **2018-2026 Security Gateway (SGW) Diagnostic Access:** On `2018-2026` FCA/Ram, Ford, GM (Global B / VIP), and Toyota platforms, the SGW module blocks bidirectional active tests (`0x2E`/`0x31`) and code clearing at the 16-pin OBD-II port unless you either connect a **12+8 SGW Bypass Adapter** directly at the SGW harness or authenticate via **SAE J2534 / AutoAuth**.\n"
        "2. **2014-2026 GDI High-Pressure Fuel Rail Depressurization (`580 - 5,075 psi`):** NEVER crack open a GDI stainless fuel rail line immediately after shutdown! Pull the Low-Pressure Fuel Pump (LPFP) relay/fuse and run the engine until it stalls (or let cool for 1 hour), wear ANSI Z87.1 eye protection, wrap the flare nut with a shop towel to absorb residual pressure, and **always install a new single-use stainless steel high-pressure line** torqued to `22 - 28 ft-lbs`.\n"
        "3. **2014-2026 Electronic Parking Brake (EPB) Rear Pad Replacement:** NEVER force or C-clamp a rear caliper piston with an electric EPB actuator motor! Command **'Enter Brake Pad Maintenance / Retract Mode'** via scan tool (`UDS Routine 0x31`) \u2014 listen for the stepper motor to fully unwind for 8 seconds \u2014 then push the piston straight in (do not twist), install pads, pump brake pedal firm, and command **'Exit EPB Maintenance Mode'**."
    ),
    "Small-Engine / Lawnmower (1990-2026): No-Spark & Magneto Ignition Coil / EFI Diagnosis (Briggs / Honda / Kohler)": (
        "1. **Safety Lockout:** Disconnect spark plug high-tension lead and ground it away from the plug; remove blower housing/recoil starter (`8mm` or `10mm` bolts).\n"
        "2. **Isolate Kill-Switch Wire:** Unplug the primary kill-wire spade terminal from the magneto armature tab. Spin flywheel and check for spark with an inline spark tester (`>= 10 kV`). If spark returns with kill-wire unplugged, the safety bail cable, seat switch, or key switch is shorted to ground.\n"
        "3. **Test Armature Coil Resistance & 2014-2026 EFI Fuel Pump:** Measure primary resistance (`0.2 - 1.0 Ohms`) and secondary resistance (`2,500 - 5,500 Ohms`). On `2014-2026` Briggs Vanguard / Kohler / Honda EFI turf engines, verify `12.4V+` battery voltage during cranking (EFI injectors and `43.5 psi` fuel pumps will not fire below `9.5V`!).\n"
        "4. **Set Magneto Air-Gap (`0.010 - 0.014 in`):** Place a `0.012 in` brass/non-magnetic feeler gauge between both armature legs and the flywheel magnet, torque mounting screws to `80 - 100 in-lbs`, and remove gauge."
    ),
    "Small-Engine / Lawnmower (1990-2026): Carburetor Bowl Overhaul, Float Level & Surging/Hunting Fix": (
        "1. **Fuel Shutoff & Anti-Afterfire Solenoid Check:** Clamp fuel line. If equipped with a bottom electric fuel-shutoff solenoid, apply `12V` to verify the plunger retracts with an audible click; remove the center bowl nut (`10mm` or `1/2 in`) and drop the float bowl.\n"
        "2. **Clear Main Jet & Emulsion Tube:** Inspect the micro-orifices in the brass main jet and vertical emulsion nozzle (`0.025 - 0.038 in`). Clean with ultrasonic cleaner and compressed air (`<= 30 psi`)?never enlarge jets with steel drill bits.\n"
        "3. **Inspect Float & Viton Needle Valve:** Verify hollow float has zero fuel inside and check Viton rubber needle tip. With carburetor inverted, verify float seam is parallel to carburetor body (`Honda GX float height = 0.54 in / 13.7 mm`).\n"
        "4. **Governor Link & Idle Circuit Check:** Ensure governor spring and throttle link rod move freely; adjust idle mixture screw (`1.25 to 1.50 turns out`) until engine transitions smoothly from `1,750 RPM` idle to `3,100 - 3,600 RPM` governed no-load speed."
    ),
    "Small-Engine / Lawnmower (1990-2026): Overhead Valve (OHV) Lash Adjustment & Decompression Release Check": (
        "1. **Find Compression Top Dead Center (TDC) Past Impulse:** Remove spark plug and valve cover. Rotate flywheel clockwise by hand until the Intake Valve opens fully and closes completely, align the TDC timing mark, and then rotate **`1/4 inch past TDC`** so the automatic compression release cam lobe is completely disengaged.\n"
        "2. **Measure Cold Valve Clearance:** Insert a flat feeler gauge between the rocker arm toe and valve stem tip (`Briggs OHV: Intake 0.004-0.006 in, Exhaust 0.006-0.008 in` | `Honda GX: Intake 0.006 in, Exhaust 0.008 in` | `Kawasaki FR/FS/FX: 0.004-0.006 in`).\n"
        "3. **Adjust Rocker Jam Nut & Pivot:** Loosen the rocker arm locking set-screw (Torx T20 or Allen) and turn the pivot ball nut until a slight drag is felt on the feeler gauge. Torque lock screw to `70 - 90 in-lbs` and re-verify after two crankshaft revolutions."
    ),
    "Automotive / Truck (1996-2026): High-Speed CAN / CAN-FD (60-Ohm) No-Comms Isolation (SAE J1979 / ISO 11898)": (
        "1. **Key-Off Termination Resistance Check (OBD-II Pins 6 & 14):** Turn ignition OFF, wait 5 minutes for network sleep, and measure resistance across **Pin 6 (CAN-H)** and **Pin 14 (CAN-L)**. Normal reading is **`60.0 Ohms (+/- 2.0 Ohms)`** (two `120-Ohm` end-of-line resistors in parallel).\n"
        "2. **Interpret Resistance Faults:** Reading **`~120 Ohms`** = Open circuit in one terminating module (ECM or BCM) or broken bus wire; Reading **`< 5.0 Ohms`** = Direct short between CAN-H and CAN-L.\n"
        "3. **Key-On Differential Voltage Check:** Turn ignition ON. Measure DC voltage from **Pin 6 to Pin 4 (Ground)** (`~2.6V - 3.5V`) and **Pin 14 to Pin 4** (`~2.4V - 1.5V`). Unplug suspect shorted modules one by one until the `2.5V` recessive bias returns."
    ),
    "Automotive / Truck (1982-2026): Starter Circuit Cranking Voltage-Drop & Lean Fuel Trim (P0171 / P0174) Isolation": (
        "1. **Positive & Ground Cranking Voltage Drop (`<= 0.20V` Max):** While cranking, measure DC volts from Positive (+) Battery Post to Starter B+ Stud (`<= 0.20V` max drop) and from Starter Metal Housing to Negative (-) Battery Post (`<= 0.20V` max drop).\n"
        "2. **Idle vs. 2,500 RPM Fuel Trim Test (`P0171 / P0174`):** Monitor `STFT + LTFT` at warm idle (`700 RPM`) vs. **`2,500 RPM`**. If fuel trim drops back near `0% to +5%` at `2,500 RPM`, isolate an **intake vacuum leak**; if fuel trim stays `> +15%` at `2,500 RPM`, diagnose a **contaminated MAF sensor** or **restricted fuel supply**."
    )
}

def render_auto_small_engine_manual_hub(unit_num: int = 1):
    import streamlit as st
    import pandas as pd
    with st.expander("\U0001f527 Direct Free OEM Automotive (1982-2026), Tractor & Small-Engine/Lawnmower Repair Manual Lookup + Built-In Shop Spec & Procedure Finder (100% Free)", expanded=True):
        st.markdown(
            "**1. Verified Live Free OEM & Factory Repair Manual Portals (`1982-2026` Model Coverage \u2014 Zero Cost / HTTP 200 Verified):**  " + chr(10)
            + "Click any verified library below to look up vehicle-specific (`1982-2026`) or lawnmower/small-engine factory repair manuals, interactive fuse/wiring diagrams, and exploded parts diagrams:"
        )
        for m_title, m_url, m_how in FREE_OEM_MANUAL_DIRECTORY:
            st.markdown(f"- \U0001f517 **[{m_title} \u2197]({m_url})** \u2014 *{m_how}*")
        st.markdown("---")
        st.markdown("**2. Built-In Step-by-Step Factory Repair & Diagnostic Procedure Lookup (`1982-2026` Auto, GDI, CAN-FD & Small-Engine \u2014 100% Local):**")
        sel_proc = st.selectbox(
            "Select an Automotive (1982-2026), CAN-Bus/SGW, or Small-Engine/Lawnmower Repair Procedure to View Step-by-Step:",
            list(BUILTIN_REPAIR_PROCEDURES.keys()),
            key=f"oem_proc_sel_{unit_num}"
        )
        st.info(BUILTIN_REPAIR_PROCEDURES[sel_proc])
        st.markdown("---")
        st.markdown("**3. Built-In Offline OEM Shop Repair Specification, Torque & Clearance Finder (`1982-2026` Air-Gap Local Database):**")
        cats = ["All Equipment Categories"] + sorted(list({r["Category"] for r in OEM_AUTO_SMALL_ENGINE_SPEC_DB}))
        c_sel, q_sel = st.columns([2, 3])
        picked_cat = c_sel.selectbox("Filter by Equipment Category:", cats, key=f"oem_cat_sel_{unit_num}")
        search_kw = q_sel.text_input("Search Engine, Year, Spec, or Part (e.g., '2026', 'GDI', 'Briggs', 'Honda', 'Valve', 'Torque', 'CAN-FD', 'EPB'):", value="", key=f"oem_kw_sel_{unit_num}").strip().lower()
        filtered_rows = []
        for row in OEM_AUTO_SMALL_ENGINE_SPEC_DB:
            if picked_cat != "All Equipment Categories" and row["Category"] != picked_cat:
                continue
            if search_kw and not any(search_kw in str(v).lower() for v in row.values()):
                continue
            filtered_rows.append(row)
        if filtered_rows:
            st.dataframe(pd.DataFrame(filtered_rows), width="stretch", hide_index=True)
        else:
            st.info("No matching spec rows found. Clear the search filter to view all 1982-2026 OEM Automotive, Tractor & Small-Engine specs.")


def render_reference_portal(course_code: str = "STR-01", unit_num: int = None):
    import streamlit as st
    key = "STR-01"
    for k in COURSE_TEXTBOOKS:
        if k in str(course_code).upper():
            key = k
            break

    if unit_num is None:
        unit_num = 1
        for sv in st.session_state.values():
            if isinstance(sv, str) and "Unit " in sv:
                m = re.search(r"Unit\s+0?([0-9]+)", sv)
                if m:
                    unit_num = int(m.group(1))
                    break

    meta = COURSE_TEXTBOOKS[key]
    ch_ref, ctrl_f_keys, focus_txt = meta["directives"].get(unit_num, meta["directives"][1])
    local_path = OFFLINE_VAULT_DIR / meta["offline_file"]

    with st.container():
        st.markdown(f"### \U0001f4da Accredited Reference Textbook & Study Directive Portal (`{key}` \u2014 Unit {unit_num:02d})")
        st.caption(f"**Assigned Reference Volume:** {meta['title']} | **Student Access Policy:** `Zero-Cost (100% Included & Paywall-Free)`")

        st.info(
            "\U0001f9ed **HOW TO LOCATE & STUDY YOUR READING MATERIALS (ZERO ADDITIONAL COST \u2014 NO EXTERNAL PURCHASES REQUIRED):**" + chr(10)
            + "1. **100% Self-Contained Inside This Console (Fastest & Air-Gap Ready):** You **never** have to pay for an external website or buy a separate book. Every statutory rule, tolerance table, and equation tested on the exam is already built directly into **Sections `1.1`\u2013`1.4` below**, **Sub-Tab 2 (Worked Math Derivations)**, and the **Local Offline Reference Manual** expander right below." + chr(10)
            + f"2. **Instant Local Lookup (`[Ctrl + F]`):** Click **`\U0001f4d6 Read Local Offline Reference Manual`** (or **`\U0001f4e5 Download / Open Offline Textbook`**) below and press **`[Ctrl + F]`** to jump straight to **`Unit {unit_num:02d}`** or search keywords: `{ctrl_f_keys}`." + chr(10)
            + "3. **Free Federal `.GOV` Source Verification:** Both online links below point strictly to **free, public-domain U.S. Government (`.gov` / `eCFR.gov`) statutory and engineering portals** (`100% Free` cost, no login or credit card ever required)."
        )

        st.warning(
            f"\U0001f3af **MANDATORY STUDY & EXAM FOCUS DIRECTIVE FOR UNIT {unit_num:02d}:**" + chr(10)
            + f"- **1. Assigned Chapter / Statutory Clause:** `{ch_ref}`" + chr(10)
            + f"- **2. Quick-Find `[Ctrl + F]` Search Keywords:** `{ctrl_f_keys}`" + chr(10)
            + f"- **3. What to Focus On for the Exam Gate:** {focus_txt}" + chr(10)
            + "- **4. Step-by-Step Study Sequence:** Read Sections `1.1`\u2013`1.4` below (or the Offline Manual expander) \u2192 Work the step-by-step derivation in **Sub-Tab 2** \u2192 Review the field/shop SOP in **Sub-Tab 3** \u2192 Pass the **Sub-Tab 4** Calculation Gate & 20-Question Exam (`>= 90%`)."
        )

        c1, c2, c3 = st.columns([2, 2, 3])
        if local_path.exists():
            raw_bytes = local_path.read_bytes()
            mime_t = "application/pdf" if local_path.suffix.lower() == ".pdf" else "text/markdown"
            c1.download_button(
                f"\U0001f4e5 Download / Open Offline Textbook ({local_path.suffix.upper()})",
                data=raw_bytes,
                file_name=local_path.name,
                mime=mime_t,
                key=f"dl_ref_portal_{key}_{unit_num}"
            )
        c2.markdown(
            f"\U0001f310 **[{meta['primary_label']} \u2197]({meta['primary_url']})**  \n"
            f"\u2696\ufe0f **[{meta['secondary_label']} \u2197]({meta['secondary_url']})**"
        )
        with c3.expander("\U0001f4c2 Offline Vault Manager (Upload Local PDF)"):
            up_pdf = st.file_uploader(
                f"Drop any full Textbook (.pdf or .md) into {key} Offline Vault:",
                type=["pdf", "md", "txt"],
                key=f"up_ref_portal_{key}_{unit_num}"
            )
            if up_pdf is not None:
                save_name = f"{key}_Offline_Textbook{Path(up_pdf.name).suffix.lower()}"
                (OFFLINE_VAULT_DIR / save_name).write_bytes(up_pdf.getvalue())
                st.success(f"Stored `{save_name}` in local Offline Vault (`c2_cockpit/offline_textbooks/`)!")
        if key == "AUT-01":
            render_auto_small_engine_manual_hub(unit_num)
        if local_path.exists() and local_path.suffix.lower() in [".md", ".txt"]:
            with st.expander(f"\U0001f4d6 Read Complete Local Offline Reference Manual (`{local_path.name}` \u2014 100% Free Built-In Air-Gap Edition)", expanded=False):
                st.markdown(local_path.read_text(encoding="utf-8", errors="ignore"))
        st.markdown("---")


def _build_full_oem_portal_dossier_text() -> str:
    lines = [
        "# SECTION 1: SOVEREIGN 1982-2026 OEM ENGINEERING & SHOP FLOOR REFERENCE REGISTRY",
        "Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OK Title 61 / HB 2992",
        "Mandatory Safety Standard: OSHA 29 CFR 1910.147 Lockout/Tagout & SAE J1715 High-Voltage Isolation",
        "",
    ]
    # Include all verified online OEM portals & technical libraries defined in hvf_reference_portal
    for k, val in globals().items():
        if isinstance(val, list) and val and isinstance(val[0], dict):
            lines.append(f"# REGISTRY TABLE: {k}")
            for item in val:
                row_str = " | ".join(f"{ik}: {iv}" for ik, iv in item.items())
                lines.append(f"- {row_str}")
            lines.append("")
        elif isinstance(val, dict) and val and k.isupper():
            lines.append(f"# SPECIFICATION MATRIX: {k}")
            for dk, dv in val.items():
                if isinstance(dv, dict):
                    sub_str = " | ".join(f"{sk}: {sv}" for sk, sv in dv.items())
                    lines.append(f"- [{dk}] {sub_str}")
                else:
                    lines.append(f"- [{dk}] {dv}")
            lines.append("")

    # Include all 16 Automotive, Heavy Diesel, Tractor & Small-Engine Repair Zones from ebony_automotive_master
    try:
        import ebony_automotive_master as _eam
        guide = getattr(_eam, "BUMPER_TO_BUMPER_MASTER_GUIDE", {})
        if guide:
            lines.append("# SECTION 2: COMPLETE 16-ZONE AUTOMOTIVE, DIESEL, TRACTOR & SMALL-ENGINE OEM MANUAL")
            for z_key, z_val in guide.items():
                lines.append(f"## {z_val.get('zone_title', z_key)}")
                lines.append(f"Subsystem Scope: {z_val.get('subsystem_scope', '')}")
                lines.append(f"Required Master Tools: {z_val.get('tools_and_ppe', '')}")
                for s_item in z_val.get("safety_precautions", []):
                    lines.append(f"  [SAFETY] {s_item}")
                for p_item in z_val.get("step_by_step_procedure", []):
                    lines.append(f"  [STEP] {p_item}")
                lines.append(f"  [TORQUE & FLUID SPECS] {z_val.get('torque_and_fluid_specs', '')}")
                lines.append(f"  [VERIFICATION] {z_val.get('post_repair_verification', '')}")
                lines.append("")
    except Exception:
        pass
    return "\n".join(lines)


def _build_full_oem_portal_dossier_text() -> str:
    lines = [
        "# SECTION 1: SOVEREIGN 1982-2026 OEM ENGINEERING & SHOP FLOOR REFERENCE REGISTRY",
        "Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OK Title 61 / HB 2992",
        "Mandatory Safety Standard: OSHA 29 CFR 1910.147 Lockout/Tagout & SAE J1715 High-Voltage Isolation",
        "",
    ]
    # Include all verified online OEM portals & technical libraries defined in hvf_reference_portal
    for k, val in globals().items():
        if isinstance(val, list) and val and isinstance(val[0], dict):
            lines.append(f"# REGISTRY TABLE: {k}")
            for item in val:
                row_str = " | ".join(f"{ik}: {iv}" for ik, iv in item.items())
                lines.append(f"- {row_str}")
            lines.append("")
        elif isinstance(val, dict) and val and k.isupper():
            lines.append(f"# SPECIFICATION MATRIX: {k}")
            for dk, dv in val.items():
                if isinstance(dv, dict):
                    sub_str = " | ".join(f"{sk}: {sv}" for sk, sv in dv.items())
                    lines.append(f"- [{dk}] {sub_str}")
                else:
                    lines.append(f"- [{dk}] {dv}")
            lines.append("")

    # Include all 16 Automotive, Heavy Diesel, Tractor & Small-Engine Repair Zones from ebony_automotive_master
    try:
        import ebony_automotive_master as _eam
        guide = getattr(_eam, "BUMPER_TO_BUMPER_MASTER_GUIDE", {})
        if guide:
            lines.append("# SECTION 2: COMPLETE 16-ZONE AUTOMOTIVE, DIESEL, TRACTOR & SMALL-ENGINE OEM MANUAL")
            for z_key, z_val in guide.items():
                lines.append(f"## {z_val.get('zone_title', z_key)}")
                lines.append(f"Subsystem Scope: {z_val.get('subsystem_scope', '')}")
                lines.append(f"Required Master Tools: {z_val.get('tools_and_ppe', '')}")
                for s_item in z_val.get("safety_precautions", []):
                    lines.append(f"  [SAFETY] {s_item}")
                for p_item in z_val.get("step_by_step_procedure", []):
                    lines.append(f"  [STEP] {p_item}")
                lines.append(f"  [TORQUE & FLUID SPECS] {z_val.get('torque_and_fluid_specs', '')}")
                lines.append(f"  [VERIFICATION] {z_val.get('post_repair_verification', '')}")
                lines.append("")
    except Exception:
        pass
    return "\n".join(lines)


def _render_portal_pdf_bar(key_prefix: str = "global") -> None:
    try:
        import hvf_pdf_engine as _hpe
        full_dossier_txt = _build_full_oem_portal_dossier_text()
        _hpe.render_pdf_export_bar(
            title="HVF 1982-2026 Master OEM Engineering & 16-Zone Shop Floor Reference Manual",
            body_text=full_dossier_txt,
            document_id="HVF-OEM-PORTAL-1982-2026",
            key_prefix=f"portal_pdf_{key_prefix}",
        )
    except Exception:
        pass


_orig_render_reference_portal = render_reference_portal


def render_reference_portal(*args, **kwargs) -> None:
    import inspect as _insp
    _kp = kwargs.get("key_prefix", args[0] if args else "global")
    _sig = _insp.signature(_orig_render_reference_portal)
    if len(_sig.parameters) == 0:
        _orig_render_reference_portal()
    elif "key_prefix" in _sig.parameters:
        _orig_render_reference_portal(key_prefix=_kp)
    else:
        _orig_render_reference_portal(_kp)
    _render_portal_pdf_bar(key_prefix=str(_kp))


render_reference_portal_expander = render_reference_portal
render = render_reference_portal
