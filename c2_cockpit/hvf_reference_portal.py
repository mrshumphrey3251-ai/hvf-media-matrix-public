"""
HVF Sovereign Reference Textbook & Study Directive Portal (Online & Air-Gap Offline Vault)
Standalone modular architecture ? zero coupling or mutation risk to legacy files.
"""
import json
import re
from pathlib import Path

OFFLINE_VAULT_DIR = Path(__file__).resolve().parent / "offline_textbooks"
OFFLINE_VAULT_DIR.mkdir(parents=True, exist_ok=True)
TEXTBOOK_LINKS_FILE = Path(__file__).resolve().parent / "hvf_textbook_links.json"

COURSE_TEXTBOOKS = {
    "STR-01": {
        "title": "Non-Destructive Evaluation of Reinforced Concrete and Timber Structures & FHWA/NHI Bridge Inspection Reference Manual (BIRM, FHWA-NHI-12-049)",
        "primary_url": "https://www.fhwa.dot.gov/bridge/nbis.cfm",
        "secondary_url": "https://www.astm.org/products-services/standards-and-publications.html",
        "offline_file": "STR-01_Offline_NDE_Master_Manual.md",
        "directives": {
            1: ("FHWA BIRM Ch. 1-2 & 23 CFR Part 650 Subpart C", "Focus on the 20.0-ft NBI bridge span rule, 24-month Routine vs. FCM inspection intervals, Sufficiency Rating (S1+S2+S3-S4) weights, and 18 U.S.C. 1001 criminal attestation."),
            2: ("NDE Treatise Ch. 9 & AASHTO MBEI Section 3 (Condition States)", "Focus on optical Ground Sampling Distance (GSD <= 0.004 in/px for FCMs), focal-length standoff equations, and Condition States CS-1 through CS-4."),
            3: ("NDE Treatise Ch. 1 (Half-Cell, LPR & Resistivity) & Ch. 3 (Impact-Echo)", "Focus on ASTM C876 Cu/CuSO4 thresholds (-200 mV / -350 mV CSE), Stern-Geary icorr, and P-wave delamination depth D = (C_p * delta_t) / 2."),
            4: ("FHWA BIRM Ch. 7 (Steel Superstructures) & AASHTO LRFD Sec. 6", "Focus on Mode I Stress Intensity Factor K_I = Y * sigma * sqrt(pi * a), fracture toughness K_Ic limits, and ultrasonic thickness gauging of pack-rust gusset plates."),
            5: ("FHWA HEC-18 (Evaluating Scour at Bridges) Ch. 5-7", "Focus on the CSU Pier Scour Equation, Froude number Fr_1 calculation, and 200 kHz bathymetric sonar draft compensation."),
            6: ("FHWA BIRM Ch. 6 (Reinforced & Prestressed Concrete) & ACI 318", "Focus on concrete modulus of rupture f_r = 7.5 * sqrt(f'_c), shear-crack inclination angles, and prestressed strand corrosion limits."),
            7: ("FHWA BIRM Ch. 10 (Bearings & Substructures) & AASHTO LRFD Sec. 14", "Focus on elastomeric bearing pad shear strain gamma = Delta_T / h_rt (<= 0.50 limit), thermal deck expansion Delta_L = alpha * L * Delta_T, and anchor-bolt shear."),
            8: ("ASPRS Positional Accuracy Standards & NDE Treatise Ch. 11 (LiDAR/Photogrammetry)", "Focus on GPS-denied 3D LiDAR SLAM drift bounds, EKF3 covariance limits, and point-cloud vertical deflection measurement (L/800 limit)."),
            9: ("NDE Treatise Ch. 2 (ASR) & ASTM C1153 (Infrared Deck Thermography)", "Focus on diurnal solar loading windows, minimum thermal contrast Delta_T >= +3.6 deg F (+2.0 deg C), and convective wind abort thresholds (< 15 mph)."),
            10: ("Oklahoma Title 61 / HB 2992 & FIPS 180-4 Cryptographic Standards", "Focus on compiling the PE-stamped Emergency Closure Docket, Benefit-Cost Ratio (BCR), and verifying the 64-character SHA-256 WORM ledger seal.")
        }
    },
    "ENV-01": {
        "title": "ASTM C1153 / D7954 Building Envelope Thermography, ASHRAE 90.1 & OMES Title 61 Facility Audit Manual",
        "primary_url": "https://www.astm.org",
        "secondary_url": "https://omes.ok.gov/services/construction-and-properties",
        "offline_file": "ENV-01_Offline_Envelope_Manual.md",
        "directives": {
            i: (f"ASTM C1153 / ASHRAE 90.1 Section {i:02d}", f"Focus on the quantitative radiometric, psychrometric, and U.S. Customary heat-transfer tolerances for Module {i:02d}.")
            for i in range(1, 11)
        }
    },
    "PAV-01": {
        "title": "ASTM D6433 Pavement Condition Index (PCI), AASHTO R 86 & ODOT TAMP Corridor Profilometry Manual",
        "primary_url": "https://www.fhwa.dot.gov/pavement/",
        "secondary_url": "https://oklahoma.gov/odot.html",
        "offline_file": "PAV-01_Offline_Pavement_Manual.md",
        "directives": {
            i: (f"ASTM D6433 / ODOT TAMP Section {i:02d}", f"Focus on PCI distress deduct curves, IRI quarter-car profilometry, and structural number calculations for Module {i:02d}.")
            for i in range(1, 11)
        }
    },
    "AUT-01": {
        "title": "SAE J1979 / J1939 CAN-Bus Diagnostics, ASE Master Technician Series & ANSI B71.1 Small-Engine Service Manual",
        "primary_url": "https://www.sae.org/standards",
        "secondary_url": "https://www.osha.gov/control-hazardous-energy",
        "offline_file": "AUT-01_Offline_Auto_Robotics_Manual.md",
        "directives": {
            1: ("ISO 11898-2 High-Speed CAN Spec & SAE J1979 / J1939 Physical Layer Manual", "Focus on parallel 120-Ohm termination resistance (R_bus = 60.0 Ohms), dominant differential voltage V_diff = V_CANH - V_CANL = 2.0V, and OSHA 1910.147 LOTO stabilization."),
            2: ("ASE A1/A2 Engine Repair Manual & Heywood ICE Fundamentals Ch. 2", "Focus on Swept Displacement V_d = (pi/4)*B^2*S*N, Static Compression Ratio CR = (V_d + V_c)/V_c, and cylinder differential leakdown limits (<= 10-12%)."),
            3: ("SAE J1979 OBD-II Mode $01/$06 Fuel Spec & Bosch Automotive Handbook", "Focus on Stoichiometric Air-Fuel Ratio (14.7:1 gasoline / 14.5:1 diesel), Lambda equivalence ratio, and combined STFT + LTFT fault thresholds (+/- 8.0% normal, > +/- 15% fault)."),
            4: ("SAE J537 Storage Battery Standards & Starting/Charging Diagnostics Manual", "Focus on Ohm's Law parasitic draw (< 50 mA), starter-circuit maximum voltage drop (<= 0.50V under cranking load), and alternator diode ripple (< 50 mV AC)."),
            5: ("ISO 4413 Hydraulic Fluid Power & Agricultural Tractor Hydraulics Manual", "Focus on Pascal's Law actuator force F = P * A, hydraulic pump volumetric efficiency, and high-pressure pinhole fluid-injection lockout."),
            6: ("ANSI/OPEI B71.1 Commercial Turf Safety & 2-Stroke/4-Stroke Service Manual", "Focus on magneto ignition air-gap (0.010-0.014 in), 2-stroke fuel-to-oil mixing ratios (50:1 = 2.6 fl oz oil/gal), and blade tip speed limits (<= 19,000 ft/min)."),
            7: ("FMVSS 105 / 121 Hydraulic & Air Brake Systems Manual", "Focus on rotor minimum machine-to/discard thickness tolerances, lateral runout (<= 0.002 in), and master cylinder hydraulic pressure ratios."),
            8: ("SAE J639 Mobile Air Conditioning & EPA Section 609 Recovery Manual", "Focus on R-134a / R-1234yf pressure-temperature saturation relationships, superheat/subcooling diagnostics, and manifold gauge fault isolation."),
            9: ("SAE J429 / ISO 898-1 Fastener Metallurgy & Torque-Tension Manual", "Focus on the Torque-Preload equation T = K * D * F / 12, dry vs. lubricated K-factor reductions, and broken fastener extraction."),
            10: ("EBONY-RTOS Hardware Guillotine Spec & ISO 26262 ASIL-D Functional Safety", "Focus on the 36.75 ns hardware safety interlock, CAN-Bus command authentication, and WORM cryptographic shop sign-off.")
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

    # Auto-detect active unit (1..10) from st.session_state if not explicitly passed
    if unit_num is None:
        unit_num = 1
        for sv in st.session_state.values():
            if isinstance(sv, str) and "Unit " in sv:
                m = re.search(r"Unit\s+0?([0-9]+)", sv)
                if m:
                    unit_num = int(m.group(1))
                    break

    meta = COURSE_TEXTBOOKS[key]
    ch_ref, focus_txt = meta["directives"].get(unit_num, meta["directives"][1])
    local_path = OFFLINE_VAULT_DIR / meta["offline_file"]

    with st.container():
        st.markdown(f"### \U0001f4da Accredited Reference Textbook & Study Directive Portal (`{key}` \u2014 Unit {unit_num:02d})")
        st.caption(f"**Assigned Reference Volume:** {meta['title']}")
        st.warning(
            f"\U0001f3af **MANDATORY STUDY & EXAM FOCUS DIRECTIVE FOR UNIT {unit_num:02d}:**" + chr(10)
            + f"- **1. Exact Textbook Chapters / Standards to Read:** `{ch_ref}`" + chr(10)
            + f"- **2. What to Focus On for the Exam Gate:** {focus_txt}" + chr(10)
            + "- **3. Study Sequence:** Read the assigned textbook chapter above + Sections `1.1`\u2013`1.4` below \u2192 Review the derivation in **Sub-Tab 2** \u2192 Execute the SOP in **Sub-Tab 3** \u2192 Pass the **Sub-Tab 4** Calculation Gate & Exam (`>= 90%`)."
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
        c2.markdown(f"\U0001f310 **[Open Online Reference Manual \u2197]({meta['primary_url']})**  \n\U0001f517 **[Open Standards Library \u2197]({meta['secondary_url']})**")
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
            with st.expander(f"\U0001f4d6 Read Local Offline Reference Manual (`{local_path.name}` \u2014 100% Air-Gap Local Disk)", expanded=False):
                st.markdown(local_path.read_text(encoding="utf-8", errors="ignore"))
        st.markdown("---")
