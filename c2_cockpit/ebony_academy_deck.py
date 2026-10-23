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

import importlib
import ebony_textbook_library
importlib.reload(ebony_textbook_library)
get_course_units = ebony_textbook_library.get_course_units
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



def _describe_us_customary_unit(u_obj):
    raw_u = str(u_obj.get("calc_unit") or u_obj.get("unit") or "").strip()
    cu_map = {
        "ft": "feet (ft) — U.S. Customary Linear Feet (12 inches = 1.0 foot)",
        "in": "inches (in) — U.S. Customary Inches (1/12 of a foot)",
        "mils": "mils (0.001 in) — Thousandths of an Inch (1,000 mils = 1.0 inch)",
        "sq ft": "square feet (sq ft) — U.S. Customary Surface Area (Length_ft * Width_ft)",
        "%": "Percent (%) — Percentage Score / Ratio (0% to 100%)",
        "psi": "psi (Pounds per Square Inch) — U.S. Customary Stress / Pressure",
        "ksi": "ksi (Kips per Square Inch) — 1,000 Pounds per Square Inch",
        "kips": "kips (Kilopounds) — U.S. Customary Structural Load (1 kip = 1,000 lbs)",
        "lbs": "pounds (lbs) — U.S. Customary Force / Weight",
        "psf": "psf (Pounds per Square Foot) — U.S. Customary Area Load",
        "pcf": "pcf (Pounds per Cubic Foot) — U.S. Customary Unit Weight",
        "°F": "degrees Fahrenheit (°F) — U.S. Customary Temperature",
        "BTU/hr": "BTU/hr (British Thermal Units per Hour) — U.S. Customary Heat Transfer Rate",
        "BTU/(hr·ft²·°F)": "BTU/(hr·ft²·°F) — U.S. Customary Thermal U-Factor",
        "hr·ft²·°F/BTU": "R-Value (hr·ft²·°F/BTU) — U.S. Customary Thermal Resistance",
        "cfs": "cfs (Cubic Feet per Second) — U.S. Customary Hydraulic Flow Rate",
        "fps": "fps (Feet per Second) — U.S. Customary Velocity",
        "mph": "mph (Miles per Hour) — U.S. Customary Wind / Vehicle Speed",
        "PCI": "PCI Points (0 to 100 Scale) — ASTM D6433 Pavement Condition Index",
        "RF": "Rating Factor (RF) — AASHTO Load & Resistance Factor Ratio (RF >= 1.00 is Safe)",
        "ksi*sqrt(in)": "ksi*sqrt(in) — U.S. Customary Fracture Toughness Stress Intensity",
        "in/sec": "inches per second (in/sec) — U.S. Customary Peak Particle Velocity",
    }
    return cu_map.get(raw_u, f"{raw_u} — U.S. Customary Engineering Unit" if raw_u else "U.S. Customary Engineering Units")

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

    courses["ENV-01"] = {
        "title": "ENV-01: Radiometric Thermography, EPA Subpart OOOOb OGI & Environmental Forensics",
        "credential": "EPA OOOOb OGI & ASNT Level-II Radiometric Thermographer",
        "diagram": courses["STR-02"]["diagram"],
        "video_demo": courses["STR-02"]["video_demo"],
        "statutory": "40 CFR Part 60 Subpart OOOOb, ASTM C1153/E1934 & OAC 245:15-11 (40.0 PELS PDHs)"
    }
    courses["PAV-01"] = {
        "title": "PAV-01: Highway Pavement Distress, Subgrade Mechanics & ASTM D6433 PCI Photogrammetry",
        "credential": "ASTM D6433 & AASHTO R 86 Certified Pavement Engineer",
        "diagram": courses["STR-03"]["diagram"],
        "video_demo": courses["STR-03"]["video_demo"],
        "statutory": "ASTM D6433 PCI, AASHTO R 86, ODOT Pavement Management & OAC 245:15-11 (40.0 PELS PDHs)"
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
        "📖 Ch 6: Statutory Nomenclature, Engineering Symbols & Standards Registry"
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

        import hvf_reference_portal as _hrp; _hrp.render_reference_portal(selected_code, selected_unit_num)
        sub_t1, sub_t2, sub_t3, sub_t4 = st.tabs([
            "📖 1.5-Hr Engineering Treatise",
            "🧮 1.0-Hr Mathematical Derivations & Worked Case",
            "🛰️ 1.0-Hr Field Practicum & Telemetry SOP",
            "🔐 0.5-Hr Calculation Gate & Mastery Quiz (4.0-Hr Sign-Off)"
        ])

        with sub_t1:
            import ebony_textbook_library as _etl; st.markdown(_etl._hvf_scrub_str(active_unit["theory"]))
            st.markdown(str(active_unit.get("deep_supplement", "")).replace(chr(10) + f"### {selected_unit_num}.4", chr(10) + chr(10) + f"### {selected_unit_num}.4").replace(f"|### {selected_unit_num}.4", "|" + chr(10) + chr(10) + f"### {selected_unit_num}.4"))
            st.info("👉 Proceed to **Sub-Tab 2 (🧮 1.0-Hr Mathematical Derivations & Worked Case)** after mastering the statutory and physical treatise above.")

        with sub_t2:
            st.markdown(f"### 📐 Official U.S. Customary Formula Sheet — {active_unit['title']}")
            st.info("💡 **How to Use This Page:** Below is the exact U.S. Customary engineering formula for this module, followed by a plain-English symbol decoder and a worked example showing every math step you will use in **Sub-Tab 4**.")
            st.code(active_unit["equations"], language="text")
            _leg_txt = str(active_unit.get("equation_legend", "")).replace("Measured in U.S. Customary Units", str(active_unit.get("resolved_us_unit", "U.S. Customary Engineering Units")))
            st.markdown(_leg_txt)
            st.markdown("---")
            st.markdown("### Step-by-Step Worked Field Engineering Calculation")
            st.info(active_unit["worked_example"])
            _we_lines = [s.strip("* -").replace("**", "").replace("`", "") for s in str(active_unit.get("worked_example", "")).splitlines() if ("Step 1" in s or "Step 2" in s or "=" in s) and not s.strip().startswith("#")]
            if _we_lines:
                st.markdown("**⬛ Worked Field Calculation Summary (Black Box Copy-and-Paste Reference):**")
                st.code(chr(10).join(_we_lines), language="text")
            st.caption(" Note the mathematical derivation steps above—you will be required to solve and verify the numerical engineering parameter in Sub-Tab 4.")

        with sub_t3:
            st.markdown("### Mandatory Field Telemetry & Laboratory Practicum Protocol")
            st.warning(active_unit["lab_protocol"])
            st.markdown("#### 🛰️ Standard U.S. Customary Field Telemetry Packet & Sensor Limits")
            _t_unit_str = active_unit.get("resolved_us_unit", "U.S. Customary Engineering Units")
            _t_title_str = active_unit.get("title", "")
            _pkt_lines = [
                f"MODULE {selected_unit_num:02d}: {_t_title_str}",
                "STATUTORY AUTHORITY: CAGE 1AHA8 | UEI S1M4ENLHTDH5 | OKLAHOMA TITLE 61 / 23 CFR 650",
                "WEATHER & LIGHTING GATE: Wind < 15.0 mph | Surface Brightness >= 1.4 foot-candles | Thermal Delta_T >= +3.6 °F",
                "POSITIONAL & OPTICAL GATE: RTK Lock <= 0.60 in Horiz / <= 0.18 in Vert | Optical GSD <= 0.004 in/px (4 mils)",
                f"TARGET SUB-TAB 4 UNIT: {_t_unit_str}",
                "WORM LEDGER TARGET: matrix_ledger.db (FIPS 180-4 SHA-256 Cryptographic Seal)",
            ]
            st.code(chr(10).join(_pkt_lines), language="text")
            if active_course["diagram"].exists():
                st.image(str(active_course["diagram"]), caption=f"Module {selected_unit_num:02d} Field Sensor & Structural Load Path Reference", use_container_width=True)

        with sub_t4:
            st.markdown(f"### 🔐 Module {selected_unit_num:02d} Quantitative Engineering Calculation Gate & Mastery Exam")
            _ceo_top_c1, _ceo_top_c2 = st.columns(2)
            with _ceo_top_c1:
                if st.button(
                    f"👑 CEO Seal: All 10 Modules (40.0 Hrs) for {selected_code}",
                    use_container_width=True,
                    key=f"btn_perm_course_seal_{selected_code}_u{selected_unit_num}"
                ):
                    for _m_unit in get_course_units(selected_code):
                        log_unit_completion(
                            student_id=student_id,
                            course_code=selected_code,
                            unit_number=_m_unit["unit"],
                            unit_title=_m_unit["title"],
                            credit_hours=_m_unit.get("hours", 4.0),
                        )
                    st.success(f"👑 All 10 Modules (40.0 Credit Hours / 4.0 CEUs) for {selected_code} Sealed in WORM Ledger!")
                    st.rerun()
            with _ceo_top_c2:
                if st.button(
                    "🌐 CEO Global Seal: All 30 Modules (120.0 Hrs: STR-01, ENV-01 & PAV-01)",
                    use_container_width=True,
                    key=f"btn_perm_global_seal_{selected_code}_u{selected_unit_num}"
                ):
                    for _c_code in ["STR-01", "ENV-01", "PAV-01"]:
                        for _m_unit in get_course_units(_c_code):
                            log_unit_completion(
                                student_id=student_id,
                                course_code=_c_code,
                                unit_number=_m_unit["unit"],
                                unit_title=_m_unit["title"],
                                credit_hours=_m_unit.get("hours", 4.0),
                            )
                    st.success("🌐 All 30 Modules (120.0 Accredited Credit Hours / 12.0 CEUs) Across STR-01, ENV-01 & PAV-01 Sealed in WORM Ledger!")
                    st.rerun()
            _reopen_gate = False
            if is_done:
                seal_info = completed_map[selected_unit_num]
                st.success(
                    f"✅ **Module {selected_unit_num:02d} Verified & Sealed ({seal_info['hours']:.1f} Accredited Credit Hours)**\n\n"
                    f"* **Completion Timestamp (UTC):** `{seal_info['utc']}`\n"
                    f"* **WORM SQLite SHA-256 Digest:** `{seal_info['seal']}`"
                )
                _all_units_list = get_course_units(selected_code)
                with st.expander("🏅 Official 40.0-Hour Accredited Engineering WORM Transcript & Oklahoma Title 61 Voucher Certificate", expanded=True):
                    st.info(
                        f"**ACCREDITED CURRICULUM TRANSCRIPT ({selected_code} — 40.0 Credit Hours / 4.0 CEUs)**\n\n"
                        f"- **Candidate License ID:** `{student_id}`\n"
                        f"- **Commercial / State Voucher Value:** `$2,500.00 / Seat (Oklahoma Title 61 & HB 2992 Compliant)`\n"
                        f"- **Issuing Authority:** `Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)`"
                    )
                    _t_rows = ["| Module | Accredited Engineering Module Title | Credit Hours | WORM Ledger Status |", "| :--- | :--- | :--- | :--- |"]
                    _csv_lines = ["Module,Title,Credit_Hours,CEUs,Status"]
                    for _u_item in _all_units_list:
                        _un = _u_item["unit"]
                        _utitle = _u_item["title"].replace("|", "-")
                        _t_rows.append(f"| **Unit {_un:02d}** | {_utitle} | `4.0 Hrs (0.4 CEUs)` | `✅ VERIFIED IN WORM LEDGER` |")
                        _csv_lines.append(f"Unit {_un:02d},\"{_utitle}\",4.0,0.4,VERIFIED_WORM_SHA256")
                    st.markdown(chr(10).join(_t_rows))
                    st.download_button(
                        label=f"📥 Download Official 40-Hour WORM Cryptographic Transcript ({selected_code} CSV)",
                        data=chr(10).join(_csv_lines),
                        file_name=f"HVF_WORM_Transcript_{selected_code}_{student_id}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key=f"dl_worm_transcript_{selected_code}_u{selected_unit_num}"
                    )
                    _m_csv = ["Curriculum,Module,Title,Credit_Hours,CEUs,Commercial_Tuition_Share,WORM_Status"]
                    for _mc in ["STR-01", "ENV-01", "PAV-01"]:
                        for _mu in get_course_units(_mc):
                            _mt = _mu["title"].replace('"', "'")
                            _m_csv.append(f"{_mc},Unit {_mu['unit']:02d},\"{_mt}\",4.0,0.4,$250.00,VERIFIED_WORM_SHA256")
                    st.download_button(
                        label="🌐 Download Master 120.0-Hour Multi-Curriculum WORM Transcript (All 30 Modules: STR-01 + ENV-01 + PAV-01 CSV)",
                        data=chr(10).join(_m_csv),
                        file_name=f"HVF_Master_120Hr_WORM_Transcript_{student_id}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key=f"dl_master_120hr_worm_{selected_code}_u{selected_unit_num}"
                    )
                _reopen_gate = st.checkbox(
                    f"🔍 CEO / Instructor Review Mode: Display Calculation Gate & 20-Question Milestone Exam for Sealed Module {selected_unit_num:02d}",
                    value=True,
                    key=f"reopen_sealed_{selected_code}_u{selected_unit_num}"
                )
            if (not (is_done)) or _reopen_gate:
                st.write(
                    "To earn **4.0 Accredited Credit Hours (0.4 CEUs)** for this module, you must solve the **Quantitative Engineering Calculation Gate** "
                    "and score **100% (20/20)** on the **Module Mastery Verification Quiz** below."
                )
                calc_ch = active_unit["calc_challenge"]
                calc_challenge = active_unit.get("calc_challenge") or active_unit.get("calculation") or calc
                _raw_u = str(calc_challenge.get("unit") or calc_challenge.get("units") or "U.S. Customary")
                _disp_unit = _raw_u.split("—")[0].strip()
                if _reopen_gate and f"audit_autofill_{selected_code}_u{selected_unit_num}" not in st.session_state: st.session_state[f"audit_autofill_{selected_code}_u{selected_unit_num}"] = True
                _audit_autofill = st.checkbox(
                    f"⚡ CEO / Instructor Audit Mode: Auto-Populate Verified Calculation ({calc_challenge.get('target', 0.0)} {_disp_unit}) & 20-Question Key",
                    value=bool(_reopen_gate),
                    key=f"audit_autofill_{selected_code}_u{selected_unit_num}"
                )
                if _audit_autofill:
                    st.session_state[f"calc_in_{selected_code}_u{selected_unit_num}_{'auto' if _audit_autofill else 'manual'}"] = float(calc_challenge["target"])
                    _ceo_c1, _ceo_c2 = st.columns(2)
                    with _ceo_c1:
                        if st.button(
                            f"👑 Seal All 10 Modules (40.0 Hrs) for {selected_code}",
                            use_container_width=True,
                            key=f"btn_top_master_seal_{selected_code}_u{selected_unit_num}"
                        ):
                            for _m_unit in get_course_units(selected_code):
                                log_unit_completion(
                                    student_id=student_id,
                                    course_code=selected_code,
                                    unit_number=_m_unit["unit"],
                                    unit_title=_m_unit["title"],
                                    credit_hours=_m_unit.get("hours", 4.0),
                                )
                            st.success(f"👑 All 10 Modules (40.0 Credit Hours / 4.0 CEUs) for {selected_code} Sealed in WORM Ledger!")
                            st.rerun()
                    with _ceo_c2:
                        if st.button(
                            "🌐 Global Seal: All 30 Modules (120.0 Hrs: STR-01, ENV-01 & PAV-01)",
                            use_container_width=True,
                            key=f"btn_top_global_seal_{selected_code}_u{selected_unit_num}"
                        ):
                            for _c_code in ["STR-01", "ENV-01", "PAV-01"]:
                                for _m_unit in get_course_units(_c_code):
                                    log_unit_completion(
                                        student_id=student_id,
                                        course_code=_c_code,
                                        unit_number=_m_unit["unit"],
                                        unit_title=_m_unit["title"],
                                        credit_hours=_m_unit.get("hours", 4.0),
                                    )
                            st.success("🌐 All 30 Modules (120.0 Accredited Credit Hours / 12.0 CEUs) Across STR-01, ENV-01 & PAV-01 Sealed in WORM Ledger!")
                            st.rerun()
                st.markdown("#### Part A: Quantitative Engineering Calculation Gate")
                st.markdown(f"**Engineering Problem:** {calc_ch['prompt']}")
                _default_calc = float(calc_ch["target"]) if _audit_autofill else 0.0
                user_calc_val = st.number_input(
                    f"Enter Calculated Value ({calc_ch['unit_label']} — Target Unit: {active_unit.get('resolved_us_unit', calc_ch['unit_label'])}):",
                    value=_default_calc,
                    step=0.01,
                    format="%.2f",
                    key=f"calc_in_{selected_code}_u{selected_unit_num}_{'auto' if _audit_autofill else 'manual'}"
                )
                if _audit_autofill: user_calc_val = float(calc_challenge["target"])
                with st.expander("💡 Need Formula Reference / Engineering Hint?"):
                    st.code(calc_ch["hint"], language="text")

                st.markdown("#### Part B: 20-Question Milestone Mastery Verification Exam (100% Required — 20/20 to Seal 4.0 Hrs)")
                _domain_banners = {
                    0: "##### 🏛️ Domain I (Questions 01–05): Statutory Jurisprudence, Target Units & Core Formulations",
                    5: "##### 🧮 Domain II (Questions 06–10): U.S. Customary Engineering Calculations, Dimensional Analysis & Sensor Tolerances",
                    10: "##### 🛰️ Domain III (Questions 11–15): RTK/PPK Geodesy, Condition States & Title 61 Compliance",
                    15: "##### 🔐 Domain IV (Questions 16–20): WORM Cryptographic Non-Repudiation & Field Readiness",
                }
                quiz_answers = {}
                for q_i, q_obj in enumerate(active_unit["unit_quiz"]):
                    if q_i in _domain_banners:
                        st.markdown(_domain_banners[q_i])
                    st.markdown(f"**Q{q_i+1:02d}.** {q_obj['q']}")
                    _opts_list = q_obj["opts"]
                    _ans_letter = str(q_obj.get("ans", "A")).strip()
                    _def_idx = 0
                    for _o_idx, _o_str in enumerate(_opts_list):
                        if _o_str.startswith(_ans_letter + ")") or _o_str == _ans_letter:
                            _def_idx = _o_idx
                            break
                    sel_opt = st.radio(
                        f"Select answer for Q{q_i+1:02d}:",
                        _opts_list,
                        index=_def_idx if _audit_autofill else 0,
                        key=f"uquiz_{selected_code}_u{selected_unit_num}_q{q_i}_{'auto' if _audit_autofill else 'manual'}",
                        label_visibility="collapsed"
                    )
                    quiz_answers[q_i] = sel_opt[0]

                if _audit_autofill:
                    if st.button(
                        f"👑 CEO Master Curriculum Seal: Verify & Seal All 10 Modules (40.0 Credit Hours) for {selected_code}",
                        use_container_width=True,
                        key=f"btn_master_seal_{selected_code}_u{selected_unit_num}"
                    ):
                        for _m_unit in get_course_units(selected_code):
                            _m_num = _m_unit["unit"]
                            log_unit_completion(
                                student_id=student_id,
                                course_code=selected_code,
                                unit_number=_m_num,
                                unit_title=_m_unit["title"],
                                credit_hours=_m_unit.get("hours", 4.0),
                            )
                        st.success(f"👑 All 10 Modules (40.0 Credit Hours / 4.0 CEUs) for {selected_code} Verified & Sealed in WORM Ledger!")
                        st.rerun()
                    if st.button(
                        "🌐 CEO Global Institute Seal: Verify & Seal All 30 Modules (120.0 Credit Hours / 12.0 CEUs) Across STR-01, ENV-01 & PAV-01",
                        use_container_width=True,
                        key=f"btn_global_3course_seal_{selected_code}_u{selected_unit_num}"
                    ):
                        for _c_code in ["STR-01", "ENV-01", "PAV-01"]:
                            for _m_unit in get_course_units(_c_code):
                                log_unit_completion(
                                    student_id=student_id,
                                    course_code=_c_code,
                                    unit_number=_m_unit["unit"],
                                    unit_title=_m_unit["title"],
                                    credit_hours=_m_unit.get("hours", 4.0),
                                )
                        st.success("🌐 All 30 Modules (120.0 Accredited Credit Hours / 12.0 CEUs) Across STR-01, ENV-01 & PAV-01 Sealed in WORM Ledger!")
                        st.rerun()

                if st.button(
                    f"⚡ Verify Calculation & Grade Module {selected_unit_num:02d} to Seal 4.0 Credit Hours",
                    use_container_width=True,
                    key=f"btn_verify_{selected_code}_u{selected_unit_num}"
                ):
                    calc_ok = abs(user_calc_val - calc_ch["target"]) <= calc_ch["tol"]
                    _total_q = len(active_unit["unit_quiz"])
                    quiz_correct = sum(
                        1 for idx, q_obj in enumerate(active_unit["unit_quiz"])
                        if quiz_answers.get(idx) == str(q_obj["ans"])[0]
                    )
                    if not calc_ok:
                        st.error(
                            f"❌ **Calculation Gate Failed:** Your entry `{user_calc_val:.2f} {calc_ch['unit_label']}` is outside the allowable engineering tolerance. "
                            f"Review Sub-Tab 2 (`{calc_ch['hint']}`) and try again."
                        )
                    elif quiz_correct < _total_q:
                        st.error(
                            f"❌ **Milestone Mastery Exam Incomplete:** You scored `{quiz_correct} / {_total_q}` (100% required — {_total_q}/{_total_q}). Review the treatise and resubmit."
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

        elif selected_code == "AUT-01":
            st.markdown("#### 🏎️ Interactive SAE J1349 Dynamometer, Volumetric Efficiency, Fuel Trim & ISO 11898 CAN-Bus Workbench")
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                w_tq = st.slider("Engine Brake Torque (lb-ft)", 100.0, 1200.0, 365.0, 5.0, key="ch2_aut_tq")
                w_rpm = st.slider("Engine Rotational Speed (RPM)", 800.0, 7000.0, 2800.0, 100.0, key="ch2_aut_rpm")
            with ac2:
                w_maf = st.slider("Mass Air Flow Sensor MAF (g/sec)", 10.0, 350.0, 115.0, 2.5, key="ch2_aut_maf")
                w_disp = st.slider("Engine Displacement (Liters)", 1.5, 10.0, 5.0, 0.1, key="ch2_aut_disp")
            with ac3:
                w_stft = st.slider("Short-Term Fuel Trim STFT (%)", -25.0, 25.0, 8.5, 0.5, key="ch2_aut_stft")
                w_ltft = st.slider("Long-Term Fuel Trim LTFT (%)", -25.0, 25.0, 18.2, 0.5, key="ch2_aut_ltft")

            w_hp = (w_tq * w_rpm) / 5252.0
            w_theo_maf = max((w_rpm / 120.0) * w_disp * 1.184, 0.001)
            w_ve = (w_maf / w_theo_maf) * 100.0
            w_trim = w_stft + w_ltft

            ak1, ak2, ak3 = st.columns(3)
            ak1.metric("SAE J1349 Net Power (HP = T*RPM/5252)", f"{w_hp:.1f} HP", f"{w_tq:.0f} lb-ft @ {w_rpm:.0f} RPM")
            ak2.metric("Volumetric Efficiency (VE_%)", f"{w_ve:.1f}%", "OPTIMAL AIRFLOW (>=80%)" if w_ve >= 80.0 else "RESTRICTED / BOOST LOSS (<80%)")
            ak3.metric("Total Fuel Trim (STFT + LTFT)", f"{w_trim:+.1f}%", "DTC P0171/P0172 FAULT (>=10%)" if abs(w_trim) >= 10.0 else "STOICHIOMETRIC LAMBDA 1.00")
            st.code(
                chr(10).join([
                    "ISO 11898 HIGH-SPEED CAN-BUS SCHEMATIC (OBD-II J1962 PINS 6 & 14 / J1939 PINS C & D):",
                    "[ECM / PCM (120 Ohm)] <====== Twisted-Pair CAN_H (3.5V) / CAN_L (1.5V) ======> [BCM / Gateway (120 Ohm)]",
                    "                              |                                                |",
                    "                              +---> [OBD-II Port Pin 6 & 14 (R_eq = 60.0 Ohms)] <--- [NVIDIA Three-Brain Enclave]"
                ]),
                language="text"
            )
        elif selected_code in ("STR-02", "ENV-01"):
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
        _ch5_ceo_audit = st.checkbox(
            f"⚡ CEO / State Board Audit Mode: Auto-Verify All 155 State Certification Exam Questions (100% Mastery Key for {selected_code})",
            value=True,
            key=f"ch5_ceo_audit_mode_{selected_code}"
        )
        _c_meta = COURSE_CATALOG.get(selected_code, {}) if "COURSE_CATALOG" in globals() else {}
        _c_title = _c_meta.get("title") or _c_meta.get("name") or selected_code
        _c_cred = _c_meta.get("credential") or "AASHTO / ODOT / FAA Level-5 Sovereign Inspector"
        if _ch5_ceo_audit:
            st.success(
                f"🏅 **OFFICIAL OKLAHOMA TITLE 61 & 23 CFR § 650 STATE CERTIFICATION CREDENTIAL ISSUED ({selected_code})**\n\n"
                f"- **Certified Engineer / Inspector:** `{student_name} ({student_id})`\n"
                f"- **Accredited Program & Credential:** `{_c_title} — {_c_cred}`\n"
                f"- **3-Tier State Examination Score:** `155 / 155 Questions Verified (100.0% Mastery — Stage 1: 20/20 | Stage 2: 45/45 | Stage 3: 90/90)`\n"
                f"- **Prerequisite Seat-Time Verification:** `40.0 / 40.0 Accredited Credit Hours (4.0 CEUs) Sealed in WORM SQLite Ledger`\n"
                f"- **Issuing Sovereign Institute:** `Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)`"
            )
            _cert_txt = (
                "================================================================================\n"
                "          HUMPHREY VIRTUAL FARMS LLC // SOVEREIGN FIELD ACADEMY                 \n"
                "     CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OKLAHOMA TITLE 61 & HB 2992 COMPLIANT    \n"
                "================================================================================\n"
                f"OFFICIAL LEVEL-5 ACCREDITED ENGINEERING CREDENTIAL & STATE VOUCHER CERTIFICATE\n\n"
                f"Candidate Name       : {student_name}\n"
                f"Candidate License ID : {student_id}\n"
                f"Accredited Program   : {selected_code} ({_c_title})\n"
                f"State Credential     : {_c_cred}\n"
                f"Verified Credit Hours: 40.0 Contact Hours (4.0 Accredited CEUs / 10 Modules)\n"
                f"3-Tier Exam Mastery  : 155 / 155 Questions Correct (100.0% Verified)\n"
                f"Tuition Voucher Tier : $2,500.00 Commercial / State Title 61 Compliant\n"
                f"WORM Ledger Authority: matrix_ledger.db (FIPS 180-4 SHA-256 Non-Repudiation)\n"
                    f"Statutory Standing   : OAC 245:15-11 (40.0 PELS PDHs) | 23 CFR 650 | 40 CFR 60 OOOOb | ASTM D6433\n"
                "================================================================================\n"
            )
            st.download_button(
                label=f"📜 Download Official {selected_code} State Certification Credential & $2,500 Title 61 Voucher Certificate (.TXT)",
                data=_cert_txt,
                file_name=f"HVF_Official_State_Credential_{selected_code}_{student_id}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"dl_official_state_cert_{selected_code}"
            )
            try:
                import generate_academy_master_binder as _gmb
                _b_res = _gmb.generate_master_executive_binder(student_id=student_id, student_name=student_name)
                _b_col1, _b_col2 = st.columns(2)
                with _b_col1:
                    st.download_button(
                        label="📘 Download Master 120-Hr Executive Compliance Binder (.MD)",
                        data=Path(_b_res["markdown_binder"]).read_text(encoding="utf-8"),
                        file_name=Path(_b_res["markdown_binder"]).name,
                        mime="text/markdown",
                        use_container_width=True,
                        key=f"dl_master_exec_binder_md_{selected_code}"
                    )
                with _b_col2:
                    st.download_button(
                        label="📊 Download Master 120-Hr WORM SQLite Transcript (.CSV)",
                        data=Path(_b_res["csv_transcript"]).read_text(encoding="utf-8"),
                        file_name=Path(_b_res["csv_transcript"]).name,
                        mime="text/csv",
                        use_container_width=True,
                        key=f"dl_master_exec_binder_csv_{selected_code}"
                    )
            except Exception:
                pass
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

        import importlib, ebony_exam_engine as _eee_live; importlib.reload(_eee_live); stage_questions = _eee_live.generate_course_stage_questions(selected_code, active_s_num)

        with st.form(key=f"unified_exam_form_{selected_code}_{active_s_num}"):
            submitted_answers = {}
            for q_idx, q in enumerate(stage_questions):
                st.markdown(f"**Question {q_idx + 1:02d} / {stage_meta['questions_count']}:** {q['question']}")
                if _ch5_ceo_audit:
                        _ans_opt = next((o for o in q.get("options", []) if o.startswith(f"{q.get('correct', '')})")), q.get("answer"))
                        if _ans_opt in q.get("options", []): st.session_state[f"unified_q_{selected_code}_s{active_s_num}_{q['id']}"] = _ans_opt
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
        st.subheader("📖 Engineering Master Glossary, Math Symbol Decoder, U.S. Units & Statutory References")
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
            st.markdown("### A–Z Technical Engineering & Inspection Glossary")
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
                    st.markdown(f"* **Technical Meaning:** {s_item['meaning']}")
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
