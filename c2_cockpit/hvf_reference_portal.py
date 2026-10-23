"""
HVF Sovereign Reference Textbook & Study Directive Portal (100% Free Public-Domain & Air-Gap Offline Vault)
Zero external paywalls ($0.00 student cost) + exact step-by-step navigation & [Ctrl+F] lookup instructions.
"""
import re
from pathlib import Path

OFFLINE_VAULT_DIR = Path(__file__).resolve().parent / "offline_textbooks"
OFFLINE_VAULT_DIR.mkdir(parents=True, exist_ok=True)

COURSE_TEXTBOOKS = {
    "STR-01": {
        "title": "FHWA Bridge Inspector's Reference Manual (BIRM, FHWA-NHI-12-049) & 23 CFR Part 650 (NBIS)",
        "primary_url": "https://www.fhwa.dot.gov/bridge/nbis.cfm",
        "primary_label": "Open Free FHWA Bridge Inspection Manual Portal (.GOV ? $0.00 Free)",
        "secondary_url": "https://www.ecfr.gov/current/title-23/chapter-I/subchapter-G/part-650/subpart-C",
        "secondary_label": "Open 23 CFR Part 650 NBIS Federal Law Text (eCFR.gov ? $0.00 Free)",
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
        "primary_label": "Open Free U.S. DOE Building Envelope Design Guide (.GOV ? $0.00 Free)",
        "secondary_url": "https://omes.ok.gov/services/construction-and-properties",
        "secondary_label": "Open Free Oklahoma OMES CAP Title 61 Portal (.GOV ? $0.00 Free)",
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
        "primary_label": "Open Free FHWA Pavement & Profilometry Portal (.GOV ? $0.00 Free)",
        "secondary_url": "https://www.ecfr.gov/current/title-23/chapter-I/subchapter-F/part-515",
        "secondary_label": "Open Free 23 CFR Part 515 TAMP Law Text (eCFR.gov ? $0.00 Free)",
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
        "primary_url": "https://www.osha.gov/control-hazardous-energy",
        "primary_label": "Open Free OSHA 1910.147 LOTO & Shop Safety Standard (.GOV ? $0.00 Free)",
        "secondary_url": "https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-86/subpart-S/section-86.1806-17",
        "secondary_label": "Open Free Federal OBD-II / SAE J1979/J1939 Mandate Text (eCFR.gov ? $0.00 Free)",
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
        st.caption(f"**Assigned Reference Volume:** {meta['title']} | **Student Access Policy:** `$0.00 Cost ? 100% Included & Paywall-Free`")

        st.info(
            "\U0001f9ed **HOW TO LOCATE & STUDY YOUR READING MATERIALS ($0.00 COST \u2014 NO EXTERNAL PURCHASES REQUIRED):**" + chr(10)
            + "1. **100% Self-Contained Inside This Console (Fastest & Air-Gap Ready):** You **never** have to pay for an external website or buy a separate book. Every statutory rule, tolerance table, and equation tested on the exam is already built directly into **Sections `1.1`\u2013`1.4` below**, **Sub-Tab 2 (Worked Math Derivations)**, and the **Local Offline Reference Manual** expander right below." + chr(10)
            + f"2. **Instant Local Lookup (`[Ctrl + F]`):** Click **`\U0001f4d6 Read Local Offline Reference Manual`** (or **`\U0001f4e5 Download / Open Offline Textbook`**) below and press **`[Ctrl + F]`** to jump straight to **`Unit {unit_num:02d}`** or search keywords: `{ctrl_f_keys}`." + chr(10)
            + "3. **Free Federal `.GOV` Source Verification:** Both online links below point strictly to **free, public-domain U.S. Government (`.gov` / `eCFR.gov`) statutory and engineering portals** (`$0.00` cost, no login or credit card ever required)."
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
        if local_path.exists() and local_path.suffix.lower() in [".md", ".txt"]:
            with st.expander(f"\U0001f4d6 Read Complete Local Offline Reference Manual (`{local_path.name}` \u2014 $0.00 Built-In Air-Gap Edition)", expanded=False):
                st.markdown(local_path.read_text(encoding="utf-8", errors="ignore"))
        st.markdown("---")
