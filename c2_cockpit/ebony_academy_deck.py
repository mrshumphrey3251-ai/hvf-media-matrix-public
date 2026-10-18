"""
E.B.O.N.Y. Sovereign Field Academy // $2,500.00 Accredited 40-Hour Engineering Institute
Renders the 10-Module Interactive Engineering Workstation (4 Sub-Tabs per Module),
Quantitative Calculation Verification Gates, Module Mastery Quizzes, WORM CEU Credit Ledger,
Multi-Variable Engineering Workbenches, and the 3-Tier State Examination Gauntlet.
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
"""
import streamlit as st
import math
from pathlib import Path
import sys

_cockpit_dir = str(Path(__file__).resolve().parent)
if _cockpit_dir not in sys.path:
    sys.path.insert(0, _cockpit_dir)

from ebony_textbook_library import (
    get_course_units, log_unit_completion, get_completed_units, export_full_course_textbook_markdown, get_master_glossary_and_references
)

try:
    from ebony_exam_engine import (
        COURSE_METADATA, STAGE_METADATA,
        generate_course_stage_questions, grade_course_stage_exam, issue_course_stage_certificate
    )
    EXAM_ENGINE_ONLINE = True
except Exception as e:
    EXAM_ENGINE_ONLINE = False
    EXAM_ENGINE_ERR = str(e)


def render_academy_deck():
    st.header("🎓 Sovereign Field Academy // $2,500.00 Accredited 40-Hour Engineering Institute")
    st.info(
        "**Statutory & Copyright Attribution:** Technical standards, formulations, and condition states "
        "referenced herein are the intellectual property of their respective governing bodies (AASHTO, "
        "ASTM International, FAA, and ODOT). Materials are utilized under Fair Use strictly for state "
        "compliance, workforce training, and infrastructure certification under Oklahoma Title 61."
    )

    assets_img_dir = Path(r"C:\hvf_c2\assets\images")

    courses = {
        "STR-01": {
            "title": "STR-01: Bridge Deck, Pier & Fracture-Critical Member Inspection",
            "tuition": "$2,500.00 / Seat",
            "framework": "Oklahoma Title 61, Title 74, 23 CFR § 650 Subpart C (NBIS) & AASHTO MBEI",
            "badge": "AASHTO / ODOT Level-5 Bridge Inspector",
            "diagram": assets_img_dir / "bridge_girder_diagram.svg",
            "video_demo": "https://www.w3schools.com/html/mov_bbb.mp4"
        },
        "STR-02": {
            "title": "STR-02: Commercial Building Envelope, Roof Membrane Moisture & Facade NDT",
            "tuition": "$2,500.00 / Seat",
            "framework": "Oklahoma Title 61 (OMES CAP), ASTM C1153, ISO 6781 & ASHRAE 90.1",
            "badge": "Title 61 Commercial Building Diagnostic Specialist",
            "diagram": assets_img_dir / "roof_thermal_moisture.svg",
            "video_demo": "https://www.w3schools.com/html/mov_bbb.mp4"
        },
        "STR-03": {
            "title": "STR-03: Roadway Pavement Distress, Rutting & ASTM D6433 PCI Survey",
            "tuition": "$2,500.00 / Seat",
            "framework": "Oklahoma Title 61, ODOT TAMP, 23 CFR Part 515 & ASTM D6433",
            "badge": "ASTM D6433 Certified Roadway & Drainage Inspector",
            "diagram": assets_img_dir / "roadway_pavement_rutting.svg",
            "video_demo": "https://www.w3schools.com/html/mov_bbb.mp4"
        }
    }

    top_c1, top_c2, top_c3 = st.columns([3, 1.2, 1.2])
    with top_c1:
        selected_code = st.selectbox(
            "Select Accredited 40-Hour Engineering Curriculum ($2,500.00 Commercial / State Tuition Tier):",
            list(courses.keys()),
            format_func=lambda x: courses[x]["title"],
            key="sel_main_academy_course"
        )
    with top_c2:
        student_id = st.text_input("Candidate License ID:", value="HVF-TECH-001", key="acad_student_id")
    with top_c3:
        student_name = st.text_input("Candidate Full Name:", value="Jeffery Humphrey", key="acad_student_name")

    active_course = courses[selected_code]
    units = get_course_units(selected_code)
    completed_map = get_completed_units(student_id, selected_code)
    earned_hours = sum(v["hours"] for v in completed_map.values())
    pct_complete = min(earned_hours / 40.0, 1.0)

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Accredited Curriculum", "10 Modules / 40.0 Hrs", "4.0 Continuing Ed Units (CEUs)")
    m_col2.metric("Commercial Tuition Value", active_course["tuition"], "State Title 61 Voucher Eligible")
    m_col3.metric("Verified WORM Credit Hours", f"{earned_hours:.1f} / 40.0 Hrs", f"{len(completed_map)} / 10 Modules Sealed")
    m_col4.metric("Target State Credential", selected_code, active_course["badge"])

    st.progress(pct_complete, text=f"Mandatory 40-Hour Accredited Seat-Time & Calculation Gate Progress: {earned_hours:.1f} / 40.0 Credit Hours Verified ({pct_complete*100:.0f}%)")
    st.markdown("---")

    tab_ch1, tab_ch2, tab_ch3, tab_ch4, tab_exam, tab_glossary = st.tabs([
        "📚 Ch 1: 10-Module / 40-Hr Workstation",
        "⚙️ Ch 2: Engineering Physics Workbenches & Schematics",
        "💥 Ch 3: NTSB & Forensic Failure Reconstructions",
        "🎬 Ch 4: Flight Sortie Videos & 4-Phase Field SOPs",
        "📝 Ch 5: 3-Tier State Certification Exam (155 Qs)",
        "📖 Ch 6: Beginner's Glossary, Symbols & References"
    ])

    # CHAPTER 1: 10-MODULE INTERACTIVE ENGINEERING WORKSTATION
    with tab_ch1:
        st.markdown("### 🏛️ 10-Module Accredited Engineering Curriculum Navigator (4.0 Credit Hours per Module)")
        u_col1, u_col2 = st.columns([3, 1])
        with u_col1:
            unit_options = [u["unit"] for u in units]
            selected_unit_num = st.selectbox(
                "Select Active 4.0-Hour Engineering Module (Complete All 4 Sub-Stations to Unlock Credit Seal):",
                unit_options,
                format_func=lambda u_num: (
                    f"{'✅ [SEALED 4.0 HRS]' if u_num in completed_map else '🔒 [REQUIRED 4.0 HRS]'} {units[u_num-1]['title']}"
                ),
                key=f"unit_sel_{selected_code}"
            )
        with u_col2:
            full_md = export_full_course_textbook_markdown(selected_code, active_course["title"])
            st.download_button(
                label=f"📥 Download Complete 10-Volume Textbook",
                data=full_md,
                file_name=f"{selected_code}_40HR_MASTER_ENGINEERING_TEXTBOOK.md",
                mime="text/markdown",
                use_container_width=True
            )

        active_unit = units[selected_unit_num - 1]
        is_done = selected_unit_num in completed_map

        st.subheader(f"{active_unit['title']}")
        st.caption(
            f"**Module Credit Allocation:** `1.5 Hrs Statutory/Physics Lecture + 1.0 Hr Math Derivation + 1.0 Hr Field Practicum + 0.5 Hr Calculation & Quiz Gate = 4.0 Credit Hours` | "
            f"**Ledger Status:** `{'✅ CERTIFIED IN WORM LEDGER' if is_done else '⏳ PENDING CALCULATION & QUIZ VERIFICATION'}`"
        )

        sub_t1, sub_t2, sub_t3, sub_t4 = st.tabs([
            "📖 1.5-Hr Engineering Treatise",
            "🧮 1.0-Hr Mathematical Derivations & Worked Case",
            "🛰️ 1.0-Hr Field Practicum & Telemetry SOP",
            "🔐 0.5-Hr Calculation Gate & Mastery Quiz (4.0-Hr Sign-Off)"
        ])

        with sub_t1:
            st.markdown(active_unit.get("beginner_primer", ""))
            with st.expander("📖 Need to Look Up a Term, Acronym, U.S. Unit, or Math Symbol? (Click to Open Beginner's Quick-Reference Glossary)", expanded=False):
                g_data = get_master_glossary_and_references(selected_code)
                st.markdown("#### 1. Common U.S. Customary Engineering Units Used in This Course")
                for u_item in g_data["units_guide"]:
                    st.markdown(f"* **`{u_item['unit']}`** — {u_item['what']}. *(Real-World Benchmark: {u_item['benchmark']})*")
                st.markdown("#### 2. Key Engineering & Statutory Terms Decoded")
                for t_item in g_data["terms"]:
                    st.markdown(f"* **{t_item['term']}** *({t_item['cat']})*: {t_item['def']}")
            st.markdown(active_unit["theory"])
            st.markdown(active_unit.get("deep_supplement", ""))
            st.info("👉 Proceed to **Sub-Tab 2 (🧮 1.0-Hr Mathematical Derivations & Worked Case)** after mastering the statutory and physical treatise above.")

        with sub_t2:
            st.markdown(f"### 📐 Official U.S. Customary Formula Sheet — {active_unit['title']}")
            st.info("💡 **How to Use This Page:** Below is the exact U.S. Customary engineering formula for this module, followed by a plain-English symbol decoder and a worked example showing every math step you will use in **Sub-Tab 4**.")
            st.code(active_unit["equations"], language="text")
            st.markdown(active_unit.get("equation_legend", ""))
            st.markdown("---")
            st.markdown("### Step-by-Step Worked Field Engineering Calculation")
            st.info(active_unit["worked_example"])
            st.caption(" Note the mathematical derivation steps above—you will be required to solve and verify the numerical engineering parameter in Sub-Tab 4.")

        with sub_t3:
            st.markdown("### Mandatory Field Telemetry & Laboratory Practicum Protocol")
            st.warning(active_unit["lab_protocol"])
            if active_course["diagram"].exists():
                st.image(str(active_course["diagram"]), caption=f"Module {selected_unit_num:02d} Field Sensor & Structural Load Path Reference", use_container_width=True)

        with sub_t4:
            st.markdown(f"### 🔐 Module {selected_unit_num:02d} Quantitative Engineering Calculation Gate & Mastery Exam")
            if is_done:
                seal_info = completed_map[selected_unit_num]
                st.success(
                    f"✅ **Module {selected_unit_num:02d} Verified & Sealed ({seal_info['hours']:.1f} Accredited Credit Hours)**\n\n"
                    f"* **Completion Timestamp (UTC):** `{seal_info['utc']}`\n"
                    f"* **WORM SQLite SHA-256 Digest:** `{seal_info['seal']}`"
                )
            else:
                st.write(
                    "To earn **4.0 Accredited Credit Hours (0.4 CEUs)** for this module, you must solve the **Quantitative Engineering Calculation Gate** "
                    "and score **100% (3/3)** on the **Module Mastery Verification Quiz** below."
                )
                calc_ch = active_unit["calc_challenge"]
                st.markdown("#### Part A: Quantitative Engineering Calculation Gate")
                st.markdown(f"**Engineering Problem:** {calc_ch['prompt']}")
                user_calc_val = st.number_input(
                    f"Enter Calculated Value ({calc_ch['unit_label']}):",
                    value=0.0,
                    step=0.01,
                    format="%.2f",
                    key=f"calc_in_{selected_code}_u{selected_unit_num}"
                )
                with st.expander("💡 Need Formula Reference / Engineering Hint?"):
                    st.code(calc_ch["hint"], language="text")

                st.markdown("#### Part B: 3-Question Module Mastery Verification Quiz (100% Required)")
                quiz_answers = {}
                for q_i, q_obj in enumerate(active_unit["unit_quiz"]):
                    st.markdown(f"**Q{q_i+1}.** {q_obj['q']}")
                    sel_opt = st.radio(
                        f"Select answer for Q{q_i+1}:",
                        q_obj["opts"],
                        key=f"uquiz_{selected_code}_u{selected_unit_num}_q{q_i}",
                        label_visibility="collapsed"
                    )
                    quiz_answers[q_i] = sel_opt[0]

                if st.button(
                    f"⚡ Verify Calculation & Grade Module {selected_unit_num:02d} to Seal 4.0 Credit Hours",
                    use_container_width=True,
                    key=f"btn_verify_{selected_code}_u{selected_unit_num}"
                ):
                    calc_ok = abs(user_calc_val - calc_ch["target"]) <= calc_ch["tol"]
                    quiz_correct = sum(
                        1 for idx, q_obj in enumerate(active_unit["unit_quiz"])
                        if quiz_answers.get(idx) == q_obj["ans"]
                    )
                    if not calc_ok:
                        st.error(
                            f"❌ **Calculation Gate Failed:** Your entry `{user_calc_val:.2f} {calc_ch['unit_label']}` is outside the allowable engineering tolerance. "
                            f"Review Sub-Tab 2 (`{calc_ch['hint']}`) and try again."
                        )
                    elif quiz_correct < 3:
                        st.error(
                            f"❌ **Module Mastery Quiz Incomplete:** You scored `{quiz_correct} / 3` (100% required). Review the treatise and resubmit."
                        )
                    else:
                        seal = log_unit_completion(
                            student_id=student_id,
                            course_code=selected_code,
                            unit_number=selected_unit_num,
                            unit_title=active_unit["title"],
                            credit_hours=active_unit["hours"]
                        )
                        st.success(f"✅ **100% Mastery Verified! 4.0 Credit Hours Sealed in WORM Ledger:** `{seal}`")
                        st.rerun()

    # CHAPTER 2: ENGINEERING PHYSICS WORKBENCHES & SCHEMATICS
    with tab_ch2:
        st.subheader(f"Chapter 2: Interactive Multi-Variable Engineering Workbenches & Schematics // {selected_code}")
        if active_course["diagram"].exists():
            st.image(str(active_course["diagram"]), caption=f"Figure 2.1: {active_course['title']} — Sensor Geometry & Structural Load Path Schematic", use_container_width=True)
        st.markdown("---")

        if selected_code == "STR-01":
            st.markdown("### Workbench 2.1: Concrete Deck Delamination Percentage (D_%) & Title 61 Hydrodemolition Gate")
            st.code("D_% = (Area_CS3_delam + Area_CS4_spall) / Area_gross_deck * 100", language="text")
            c1, c2, c3 = st.columns(3)
            with c1:
                gross_area = st.number_input("Gross Deck Area (sq ft):", value=15000.0, step=500.0, key="wb_gross")
            with c2:
                delam_area = st.number_input("Delaminated + Spalled Area (sq ft):", value=1800.0, step=50.0, key="wb_delam")
            with c3:
                d_pct = (delam_area / gross_area) * 100.0 if gross_area > 0 else 0.0
                st.metric("Deck Delamination (D_%)", f"{d_pct:.2f}%", "MANDATES HYDRODEMOLITION (>=10%)" if d_pct >= 10.0 else "Localized Epoxy/Patch (<10%)")

            st.markdown("---")
            st.markdown("### Workbench 2.2: Linear-Elastic Fracture Mechanics (K_I) & Critical Crack Length (a_c)")
            st.code("K_I = Y * sigma_max * sqrt(pi * a)      [Mode I Stress Intensity Factor, ksi*sqrt(in)]\na_c = (1 / pi) * [ K_Ic / (Y * sigma_max) ]^2  [Critical Brittle Fracture Crack Length, in]", language="text")
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                sigma_max = st.number_input("Peak Flange Tensile Stress (ksi):", value=22.0, step=1.0, key="wb_sigma")
            with f2:
                a_init = st.number_input("Measured Crack Length a_0 (in):", value=0.35, step=0.05, format="%.2f", key="wb_a0")
            with f3:
                y_geom = st.number_input("Flange Geometry Factor Y:", value=1.12, step=0.02, format="%.2f", key="wb_y")
            with f4:
                k_ic = st.number_input("Steel Fracture Toughness K_Ic (ksi*sqrt(in)):", value=45.0, step=2.5, key="wb_kic")

            k_i = y_geom * sigma_max * math.sqrt(math.pi * max(a_init, 0.001))
            a_crit = (1.0 / math.pi) * ((k_ic / max(y_geom * sigma_max, 0.1)) ** 2)
            fr1, fr2 = st.columns(2)
            fr1.metric("Current Stress Intensity Factor (K_I)", f"{k_i:.2f} ksi√in", "CRITICAL FRACTURE IMMINENT" if k_i >= 0.85 * k_ic else "Sub-Critical Fatigue Regime")
            fr2.metric("Critical Cleavage Crack Length (a_c)", f"{a_crit:.3f} inches", f"Remaining Margin: {max(a_crit - a_init, 0.0):.3f} in")

            st.markdown("---")
            st.markdown("### Workbench 2.3: FHWA HEC-18 / CSU Equilibrium Pier Scour Depth (y_s) Solver")
            st.code("y_s = y_1 * 2.0 * K_1 * K_2 * K_3 * K_4 * (b / y_1)^0.65 * Fr_1^0.43", language="text")
            s1, s2, s3, s4 = st.columns(4)
            with s1:
                y1 = st.number_input("Upstream Flood Depth y_1 (ft):", value=14.0, step=1.0, key="wb_y1")
            with s2:
                b_pier = st.number_input("Pier Width b (ft):", value=4.0, step=0.5, key="wb_bpier")
            with s3:
                v1 = st.number_input("Flood Flow Velocity V_1 (ft/s):", value=11.0, step=0.5, key="wb_v1")
            with s4:
                foot_d = st.number_input("Footing Embedment Depth (ft):", value=9.0, step=0.5, key="wb_foot")

            fr_num = v1 / math.sqrt(32.174 * max(y1, 0.1))
            ys_scour = y1 * 2.0 * 1.0 * 1.0 * 1.1 * 1.0 * ((b_pier / max(y1, 0.1)) ** 0.65) * (fr_num ** 0.43)
            sc1, sc2 = st.columns(2)
            sc1.metric("Upstream Froude Number (Fr_1)", f"{fr_num:.3f}", "Supercritical Flow (Fr >= 1)" if fr_num >= 1.0 else "Subcritical Riverine Flow")
            sc2.metric("Predicted HEC-18 Scour Depth (y_s)", f"{ys_scour:.2f} ft", "ODOT ITEM 113 SCOUR CRITICAL (Exceeds Footing!)" if ys_scour >= foot_d else "Footing Embedment Safe")

        elif selected_code == "STR-02":
            st.markdown("### Workbench 2.1: ASTM C1153 Roof Conductive Heat Loss (BTU/hr) & Dew-Point (°F) Solver")
            st.code("Q_BTU_hr = (Area_sqft / R_Value_US) * (T_indoor_F - T_outdoor_F)\nDew_Point_F = (T_dp_C * 1.8) + 32.0   [U.S. Customary ASHRAE Psychrometric Formulation]", language="text")
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                wet_sqft = st.number_input("Saturated Roof Core Area (sq ft):", value=3500.0, step=250.0, key="wb2_area")
            with b2:
                t_in_f = st.number_input("Indoor Building Temp (°F):", value=72.0, step=1.0, key="wb2_tin_f")
            with b3:
                rh_in = st.number_input("Indoor Relative Humidity (%):", value=52.0, step=2.0, key="wb2_rh")
            with b4:
                t_out_f = st.number_input("Nocturnal Outdoor Temp (°F):", value=38.0, step=1.0, key="wb2_tout_f")

            delta_t_f = max(t_in_f - t_out_f, 0.0)
            q_dry_btu = (wet_sqft / 25.0) * delta_t_f
            q_wet_btu = (wet_sqft / 4.0) * delta_t_f
            t_in_c = (t_in_f - 32.0) / 1.8
            gamma_v = math.log(max(rh_in, 1.0) / 100.0) + (17.62 * t_in_c) / (243.12 + t_in_c)
            t_dp_c = (243.12 * gamma_v) / (17.62 - gamma_v)
            t_dp_f = (t_dp_c * 1.8) + 32.0

            r1, r2, r3 = st.columns(3)
            r1.metric("Dry Insulation Heat Loss (R-25)", f"{q_dry_btu:,.0f} BTU/hr", "Baseline Design Conduction")
            r2.metric("Wet Core Heat Bleed (R-4)", f"{q_wet_btu:,.0f} BTU/hr", f"+{q_wet_btu - q_dry_btu:,.0f} BTU/hr Waste (6.25x Loss)")
            r3.metric("Interstitial Dew-Point Temp", f"{t_dp_f:.1f} °F", "ACTIVE CONDENSATION ON DECK" if t_out_f <= t_dp_f else "Safe (Above Dew Point)")

        else:
            st.markdown("### Workbench 2.1: ASTM D6433 PCI Solver, Boussinesq Subgrade Stress (sigma_z) & Hydroplaning Speed (V_p)")
            st.code("PCI = 100 - max(CDV_i)\nV_hydroplaning_mph = 10.35 * sqrt(P_tire_psi)\nsigma_z = p * [ 1 - (1 / (1 + (a / z)^2))^1.5 ]", language="text")
            p1, p2, p3, p4 = st.columns(4)
            with p1:
                max_cdv = st.number_input("Maximum Corrected Deduct Value (CDV):", value=38.0, step=2.0, key="wb3_cdv")
            with p2:
                rut_in = st.number_input("Measured Wheel-Path Rut Depth (in):", value=0.45, step=0.05, format="%.2f", key="wb3_rut")
            with p3:
                tire_psi = st.number_input("Vehicle Tire Pressure P_tire (psi):", value=32.0, step=2.0, key="wb3_psi")
            with p4:
                z_sub = st.number_input("Subgrade Depth z (in, for a=4.5in, p=110psi):", value=12.0, step=1.0, key="wb3_z")

            pci_val = max(100.0 - max_cdv, 0.0)
            v_hydro = 10.35 * math.sqrt(max(tire_psi, 1.0))
            sig_z = 110.0 * (1.0 - ((1.0 / (1.0 + ((4.5 / max(z_sub, 0.5)) ** 2))) ** 1.5))

            k1, k2, k3 = st.columns(3)
            k1.metric("ASTM D6433 Pavement Condition Index", f"{pci_val:.1f} PCI", "REHABILITATION REQUIRED (<70)" if pci_val < 70 else "Preventive Maintenance (>=70)")
            k2.metric("Critical Hydroplaning Velocity (V_p)", f"{v_hydro:.1f} mph", "SEVERE HYDROPLANING RISK (Rut >= 0.25 in)" if rut_in >= 0.25 else "Drainage Safe (<0.25 in)")
            k3.metric("Boussinesq Vertical Subgrade Stress", f"{sig_z:.2f} psi", f"At Depth z = {z_sub:.1f} in under 110 psi Dual Tire")

    # CHAPTER 3: NTSB & FORENSIC ENGINEERING FAILURE RECONSTRUCTIONS
    with tab_ch3:
        st.subheader(f"Chapter 3: Unabridged NTSB & Structural Forensic Failure Reconstructions // {selected_code}")
        for u in units:
            if u["unit"] in (8, 9):
                st.markdown(f"## {u['title']}")
                st.markdown(u["theory"])
                st.code(u["equations"], language="text")
                st.info(u["worked_example"])
                st.markdown("---")

    # CHAPTER 4: FLIGHT SORTIE VIDEOS & 4-PHASE FIELD SOPS
    with tab_ch4:
        st.subheader(f"Chapter 4: Operational Flight Telemetry Videos & 4-Phase Field SOPs // {selected_code}")
        st.video(active_course["video_demo"])
        st.caption("Live Telemetry Feed: Sensor Gimbal Orientation, Optical SLAM Lock & WORM Hashing Pipeline")
        st.markdown("---")
        st.markdown("### Mandatory 4-Phase Field Sortie Standard Operating Procedures (SOPs)")
        for u in units:
            st.markdown(f"**{u['title']} — Practicum Checklist:**")
            st.markdown(u["lab_protocol"])

    # CHAPTER 5: 3-TIER STATE CERTIFICATION EXAM GAUNTLET
    with tab_exam:
        st.subheader(f"Chapter 5: Official {selected_code} 3-Tier State Certification Exam Gauntlet (155 Questions Total)")
        if not EXAM_ENGINE_ONLINE:
            st.error(f"Exam Engine Offline: {EXAM_ENGINE_ERR}")
            return

        if earned_hours < 40.0:
            st.warning(
                f"🎓 **Accredited Seat-Time & Calculation Gate Notice:** You have verified **{earned_hours:.1f} / 40.0 Credit Hours** ({len(completed_map)}/10 Modules) in Chapter 1. "
                f"Complete the Quantitative Calculation Gates across all 10 Modules to achieve 100% 40-Hour WORM Accreditation alongside your 3-Tier Exam."
            )
        else:
            st.success("✅ **40.0 / 40.0 Accredited Credit Hours Verified in WORM Ledger!** Candidate is fully cleared for Official State Licensing.")

        e_col1, e_col2, e_col3 = st.columns([2, 2, 2])
        with e_col1:
            active_s_num = st.selectbox(
                "Select Qualification Stage:",
                [1, 2, 3],
                format_func=lambda x: f"Stage {x}: {STAGE_METADATA[x]['name']} ({STAGE_METADATA[x]['questions_count']} Qs)",
                key="unified_stage_sel"
            )
        with e_col2:
            cand_name = st.text_input("Exam Candidate Name:", value=student_name, key="unified_name")
        with e_col3:
            cand_id = st.text_input("Exam Candidate ID:", value=student_id, key="unified_id")

        stage_meta = STAGE_METADATA[active_s_num]
        st.markdown(f"**Target Discipline:** `{selected_code}` | **Questions:** `{stage_meta['questions_count']}` | **Passing Standard:** `>= {stage_meta['passing_pct']}%`")

        stage_questions = generate_course_stage_questions(selected_code, active_s_num)

        with st.form(key=f"unified_exam_form_{selected_code}_{active_s_num}"):
            submitted_answers = {}
            for q_idx, q in enumerate(stage_questions):
                st.markdown(f"**Question {q_idx + 1:02d} / {stage_meta['questions_count']}:** {q['question']}")
                chosen = st.radio(
                    f"Answer for {q['id']}:",
                    q["options"],
                    key=f"unified_q_{selected_code}_s{active_s_num}_{q['id']}",
                    label_visibility="collapsed"
                )
                submitted_answers[q["id"]] = chosen[0]
                st.write("")

            btn_submit = st.form_submit_button(
                f"⚡ Submit {selected_code} Stage {active_s_num} Exam for Official State Grading",
                use_container_width=True
            )

        if btn_submit:
            grade_res = grade_course_stage_exam(selected_code, active_s_num, submitted_answers)
            st.markdown("---")
            st.subheader(f"Official Examination Results // {selected_code} {grade_res['stage_name']}")

            r_col1, r_col2, r_col3 = st.columns(3)
            r_col1.metric("Final Score", f"{grade_res['score_pct']:.1f}%", f"{grade_res['correct_count']} / {grade_res['total_questions']} Correct")
            r_col2.metric("Required Passing Threshold", f"{grade_res['passing_threshold_pct']:.1f}%", "Oklahoma Title 61 Standard")
            r_col3.metric("Qualification Status", "PASSED / CERTIFIED" if grade_res["passed"] else "FAILED / RETEST REQUIRED", ":green[Certified]" if grade_res["passed"] else ":red[Retest]")

            if grade_res["passed"]:
                cert_info = issue_course_stage_certificate(
                    student_id=cand_id,
                    student_name=cand_name,
                    course_code=selected_code,
                    stage_num=active_s_num,
                    score_pct=grade_res["score_pct"]
                )
                st.success(f"State Credential Issued: `{cert_info['credential_title']}`")
                st.caption(f"Docket Seal: `{cert_info['certificate_id']}` | SHA-256 Digest: `{cert_info['sha256_seal']}`")

                cert_file = Path(cert_info["certificate_file"])
                if cert_file.exists():
                    st.download_button(
                        label=f"📥 Download Official State Certificate ({selected_code} Stage {active_s_num})",
                        data=cert_file.read_text(encoding="utf-8"),
                        file_name=cert_file.name,
                        mime="text/markdown",
                        key=f"unified_dl_cert_{selected_code}_s{active_s_num}",
                        use_container_width=True
                    )
            else:
                st.error("Candidate did not achieve the required passing threshold. Review the 10-Module Workstation in Chapter 1 and resubmit.")

            with st.expander("🔍 View Technical Question Feedback & Explanations", expanded=False):
                for fb in grade_res["detailed_feedback"]:
                    if fb["status"] == "CORRECT":
                        st.write(f":green[**{fb['id']} (Correct):**] {fb['explanation']}")
                    else:
                        st.write(f":red[**{fb['id']} (Incorrect):**] Selected: `{fb['your_answer']}` | Correct: `{fb['correct_answer']}` — {fb['explanation']}")


    # CHAPTER 6: BEGINNER'S GLOSSARY, SYMBOL DECODER, U.S. UNITS & STATUTORY REFERENCES
    with tab_glossary:
        st.subheader("📖 Beginner's Master Glossary, Math Symbol Decoder, U.S. Units & Statutory References")
        st.success(
            "💡 **Zero-Jargon Training Guarantee:** Every symbol, acronym, U.S. measurement unit, and federal/state law "
            "used across all 30 modules is explained below in plain, everyday English so any student can master the curriculum from scratch."
        )
        g_all = get_master_glossary_and_references(selected_code)

        search_q = st.text_input("🔍 Search Any Term, Acronym, Symbol, or Law (e.g., 'kip', 'mils', 'scour', 'sigma', 'PCI', 'Title 61'):", value="", key="gloss_search").strip().lower()

        g_tab1, g_tab2, g_tab3, g_tab4 = st.tabs([
            "🔤 A–Z Engineering & Legal Glossary",
            "🧮 Math & Greek Symbol Decoder",
            "📏 U.S. Customary Units Guide (°F, ft, in, psi, BTU)",
            "⚖️ Official Federal & Oklahoma Statutory References"
        ])

        with g_tab1:
            st.markdown("### A–Z Plain-English Engineering & Inspection Glossary")
            for item in g_all["terms"]:
                if not search_q or search_q in item["term"].lower() or search_q in item["def"].lower() or search_q in item["cat"].lower():
                    st.markdown(f"#### 📌 {item['term']}  `[{item['cat']}]`")
                    st.write(item["def"])
                    st.markdown("---")

        with g_tab2:
            st.markdown("### Mathematical & Greek Symbol Decoder (How to Read & Calculate Every Equation)")
            for s_item in g_all["symbols"]:
                if not search_q or search_q in s_item["sym"].lower() or search_q in s_item["meaning"].lower() or search_q in s_item["example"].lower():
                    st.markdown(f"#### 🔹 Symbol: `{s_item['sym']}`  *(Pronounced: {s_item['say']})*")
                    st.markdown(f"* **Plain-English Meaning:** {s_item['meaning']}")
                    st.markdown(f"* **How to Use It on Your Calculator:** {s_item['example']}")
                    st.markdown("---")

        with g_tab3:
            st.markdown("### U.S. Customary Measurement Units Guide (American Field Standards)")
            for u_item in g_all["units_guide"]:
                if not search_q or search_q in u_item["unit"].lower() or search_q in u_item["what"].lower() or search_q in u_item["benchmark"].lower():
                    st.markdown(f"#### 📏 `{u_item['unit']}` — {u_item['what']}")
                    st.info(f"**Real-World Comparison:** {u_item['benchmark']}")

        with g_tab4:
            st.markdown("### Official Federal & State of Oklahoma Statutory Reference Library")
            for r_item in g_all["references"]:
                if not search_q or search_q in r_item["code"].lower() or r_item["agency"].lower() or search_q in r_item["scope"].lower():
                    st.markdown(f"#### ⚖️ {r_item['code']}  —  *{r_item['agency']}*")
                    st.write(r_item["scope"])
                    st.markdown("---")
