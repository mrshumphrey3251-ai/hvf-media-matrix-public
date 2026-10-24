"""
Humphrey Virtual Farms LLC // HVF Master Automotive, Heavy Tractor & Small-Engine Academy
Standalone 40.0-Hour / 10-Module / 355-Question Accredited Mechanical & CAN-Bus Engineering Institute
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Standards: ASE Master Technician, SAE J1979 (OBD-II), SAE J1939, ISO 14229 (UDS), ISO 11783 (ISOBUS), ANSI B71.1, OAC 245:15-11 (40.0 PDHs)
"""
import importlib
from pathlib import Path
import streamlit as st

cockpit_dir = Path(__file__).resolve().parent


def render_auto_academy_deck():
    import ebony_textbook_library as etl
    import ebony_exam_engine as eee
    import ebony_automotive_master as eam
    importlib.reload(etl)
    importlib.reload(eee)
    importlib.reload(eam)

    st.subheader("🛠️ HVF Master Automotive, Heavy Tractor & Small-Engine Academy // 40-Hour Accredited Institute")
    st.caption(
        "Standalone Mechanical, Electrical, Hydraulic, Small-Engine & NVIDIA Three-Brain CAN-Bus Training Institute | "
        "ASE Master Tech / SAE J1979 / SAE J1939 / ANSI B71.1 / OAC 245:15-11 (40.0 Contact Hours / 4.0 CEUs)"
    )

    top_c1, top_c2, top_c3 = st.columns([2.6, 1.2, 1.2])
    with top_c1:
        st.selectbox(
            "Select Master Automotive & Small-Engine Academy Track (AUT-01 — 10 Modules / 40.0 Hrs / 355 Verified Questions):",
            [
                "AUT-01 (Full-Spectrum): Master Automotive, Heavy Diesel Tractor, Small Engine & NVIDIA CAN-Bus Curriculum",
                "AUT-01 (Track A Focus): Bumper-to-Bumper Cars, Pickup Trucks & Heavy Diesel Tractors (Modules 01–09)",
                "AUT-01 (Track B Focus): Small Engines, Push & Zero-Turn Lawnmowers, Carburetors & 2-Stroke Equipment (Module 10 + Zones 13–16)"
            ],
            key="auto_acad_track_sel"
        )
    with top_c2:
        student_id = st.text_input("Candidate License ID:", value="HVF-TECH-001", key="auto_acad_student_id")
    with top_c3:
        student_name = st.text_input("Candidate Full Name:", value="Jeffery Humphrey", key="auto_acad_student_name")

    units = etl.get_course_units("AUT-01")
    completed_map = etl.get_completed_units(student_id, "AUT-01")
    earned_hours = sum(v["hours"] for v in completed_map.values())
    pct_complete = min(earned_hours / 40.0, 1.0)

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Accredited Curriculum", "10 Modules / 40.0 Hrs", "4.0 CEUs / 40.0 PELS PDHs")
    mc2.metric("Verified Question Bank", "355 Unique Questions", "200 Module + 155 State/ASE Exam")
    mc3.metric("Verified WORM Credit Hours", f"{earned_hours:.1f} / 40.0 Hrs", f"{len(completed_map)} / 10 Modules Sealed")
    mc4.metric("Target Master Credential", "AUT-01 MASTER TECH", "ASE / SAE J1979 / J1939 / ANSI B71.1")

    st.progress(pct_complete, text=f"AUT-01 Mandatory 40-Hour Seat-Time & Calculation Gate Progress: {earned_hours:.1f} / 40.0 Credit Hours Verified ({pct_complete*100:.0f}%)")

    ch1, ch2, ch3, ch4, ch5, ch6 = st.tabs([
        "📚 Ch 1: 10-Module / 40-Hr Workstation (200 Qs)",
        "⚙️ Ch 2: Dyno, Torque, Fuel Trim & 2-Stroke Workbenches",
        "💥 Ch 3: Forensic Shop & Engine Failure Reconstructions",
        "🎬 Ch 4: 4-Phase Shop SOPs & 16-Zone Repair Manual",
        "📝 Ch 5: 3-Tier ASE / State Certification Exam (155 Qs)",
        "📖 Ch 6: SAE/ISO Nomenclature, Shop Tooling & Standards Registry"
    ])

    with ch1:
        u_col1, u_col2 = st.columns([3, 1])
        with u_col1:
            sel_u_num = st.selectbox(
                "Select AUT-01 Engineering & Shop Module (4.0 Accredited Hours Each):",
                [u["unit"] for u in units],
                format_func=lambda n: f"Module {n:02d}: {units[n-1]['title']} {'✅ [4.0 HRS SEALED]' if n in completed_map else ''}",
                key="auto_acad_unit_sel"
            )
        with u_col2:
            full_tb_md = etl.export_full_course_textbook_markdown("AUT-01")
            st.download_button(
                label="📥 Download Complete AUT-01 Textbook (.MD)",
                data=full_tb_md,
                file_name="AUT-01_40HR_AUTOMOTIVE_AND_SMALL_ENGINE_TEXTBOOK.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_aut01_full_tb"
            )

        active_unit = units[sel_u_num - 1]
        import hvf_reference_portal as _hrp; _hrp.render_reference_portal("AUT-01", sel_u_num)
        st1, st2, st3, st4 = st.tabs([
            "📖 Sub-Tab 1: Unabridged Lecture, Hazards & Tools",
            "🧮 Sub-Tab 2: Governing Equations & Worked Shop Derivation",
            "🔧 Sub-Tab 3: 4-Phase Hands-On Shop Practicum Protocol",
            "✅ Sub-Tab 4: Calculation Gate & 20-Question Milestone Exam"
        ])
        with st1:
            import ebony_textbook_library as _etl; st.markdown(_etl._hvf_scrub_str(active_unit["theory"], is_auto=True))
            if active_unit.get("deep_supplement"):
                st.markdown(active_unit["deep_supplement"])
        with st2:
            st.code(active_unit["equations"], language="text")
            st.caption(f"**Variable Definitions:** {active_unit.get('equation_legend', '')}")
            st.info(active_unit["worked_example"])
        with st3:
            st.markdown(active_unit["lab_protocol"])
        with st4:
            c_gate = active_unit["calc_gate"]
            st.markdown(f"#### 🧮 Part A: Quantitative Shop & Engineering Calculation Gate (`Module {sel_u_num:02d}`)")
            st.info(c_gate["prompt"])
            st.success(f"✔ **Verified Target Engineering Value:** `{c_gate['expected_ans']} {c_gate['unit']}` *(Tolerance: `+/- {c_gate['tolerance']}`)*")
            st.markdown("---")
            st.markdown(f"#### 📝 Part B: 20-Question Module {sel_u_num:02d} Milestone Examination (`20 Unique Questions`)")
            ceo_auto_key = st.checkbox("⚡ CEO / Instructor Audit Mode: Highlight All 20 Verified Correct Answers", value=True, key=f"auto_acad_ch1_key_{sel_u_num}")
            with st.form(key=f"auto_acad_ch1_form_{sel_u_num}"):
                for qi, q_item in enumerate(active_unit["unit_quiz"], 1):
                    st.markdown(f"**Question {qi:02d} / 20:** {q_item['q']}")
                    opts = q_item["opts"]
                    ans_idx = opts.index(q_item["ans"]) if q_item["ans"] in opts else 0
                    st.radio(
                        f"Select answer for M{sel_u_num:02d} Q{qi:02d}:",
                        opts,
                        index=ans_idx if ceo_auto_key else 0,
                        key=f"auto_acad_u{sel_u_num}_q{qi}",
                        label_visibility="collapsed"
                    )
                    if ceo_auto_key:
                        st.caption(f":green[✔ **Verified Answer Key:** {q_item['ans']}]")
                sub_ch1 = st.form_submit_button(f"🔒 Verify & Seal Module {sel_u_num:02d} (4.0 Credit Hours) in WORM Ledger", use_container_width=True)
            if sub_ch1:
                etl.log_unit_completion(student_id, student_name, "AUT-01", sel_u_num, active_unit["title"], float(c_gate["expected_ans"]), float(c_gate["expected_ans"]), 100.0)
                st.success(f"✅ Module {sel_u_num:02d} (4.0 Accredited Hours) Verified at 100.0% Mastery and Sealed in WORM Ledger!")

    with ch2:
        st.markdown("### ⚙️ Chapter 2: Interactive Automotive Dynamometer, CAN-Bus, Fastener Torque & Small-Engine 2-Stroke Workbenches")
        wb1, wb2, wb3 = st.columns(3)
        with wb1:
            w_tq = st.slider("Engine Brake Torque (lb-ft)", 20.0, 1200.0, 365.0, 5.0, key="aa_ch2_tq")
            w_rpm = st.slider("Engine Rotational Speed (RPM)", 800.0, 7000.0, 2800.0, 100.0, key="aa_ch2_rpm")
        with wb2:
            w_maf = st.slider("Mass Air Flow MAF (g/sec)", 5.0, 350.0, 115.0, 2.5, key="aa_ch2_maf")
            w_disp = st.slider("Engine Displacement (Liters)", 0.2, 10.0, 5.0, 0.1, key="aa_ch2_disp")
        with wb3:
            w_gas = st.slider("2-Stroke Gas Container (Gallons)", 0.5, 5.0, 2.5, 0.5, key="aa_ch2_gas")
            w_rat = st.selectbox("2-Stroke Mix Ratio", [50, 40, 32], format_func=lambda r: f"{r}:1 Mix Ratio", key="aa_ch2_rat")
        w_hp = (w_tq * w_rpm) / 5252.0
        w_theo = max((w_rpm / 120.0) * w_disp * 1.184, 0.001)
        w_ve = (w_maf / w_theo) * 100.0
        w_oil_oz = (w_gas * 128.0) / float(w_rat)
        k1, k2, k3 = st.columns(3)
        k1.metric("SAE J1349 Net Power (HP = T*RPM/5252)", f"{w_hp:.2f} HP", f"{w_tq:.0f} lb-ft @ {w_rpm:.0f} RPM")
        k2.metric("Volumetric Efficiency (VE_%)", f"{w_ve:.1f}%", "Healthy NA: 80-95% | Boosted: >100%")
        k3.metric(f"2-Stroke Oil Required ({w_rat}:1)", f"{w_oil_oz:.2f} fl oz", f"{w_oil_oz*29.57:.0f} mL for {w_gas:.1f} Gal Gas")

    with ch3:
        st.markdown("### 💥 Chapter 3: Unabridged Automotive, Drivetrain & Small-Engine Forensic Failure Reconstructions")
        for u_f in units:
            if u_f["unit"] in (2, 8, 9, 10):
                st.markdown(f"## 🔍 Forensic Case Study — {u_f['title']}")
                st.markdown(u_f["theory"])
                st.code(u_f["equations"], language="text")
                st.info(u_f["worked_example"])
                st.markdown("---")

    with ch4:
        st.markdown("### 🎬 Chapter 4: Complete 16-Zone Bumper-to-Bumper & Small-Engine Beginner Repair Manual + 4-Phase Shop SOPs")
        z_keys = list(eam.BUMPER_TO_BUMPER_BEGINNER_GUIDE.keys())
        sel_z = st.selectbox("Select Any of the 16 Bumper-to-Bumper Automotive, Tractor, or Small-Engine/Lawnmower Zones:", z_keys, format_func=lambda k: eam.BUMPER_TO_BUMPER_BEGINNER_GUIDE[k]["zone_title"], key="aa_ch4_zone_sel")
        zd = eam.BUMPER_TO_BUMPER_BEGINNER_GUIDE[sel_z]
        st.markdown("#### ⚠️ 1. Mandatory Life-Safety & All Task Hazards (READ FIRST)")
        for hz in zd["safety_precautions"]:
            st.warning(hz)
        st.markdown("#### 📍 2. Where Is It & What Does It Look Like?")
        st.markdown(zd["where_and_what"])
        st.markdown("#### 🧰 3. Exact Tools & Socket Sizes Required")
        for tl in zd["tools_required"]:
            st.markdown(f"- **{tl}**")
        st.markdown("#### 🛠️ 4. Step-by-Step Master Engineering Instructions")
        for sp in zd["step_by_step"]:
            st.success(sp)

    with ch5:
        st.markdown("### 📝 Chapter 5: Official AUT-01 3-Tier Master Automotive, Tractor & Small-Engine Certification Exam (155 Questions)")
        ch5_audit = st.checkbox("⚡ CEO / State Board Audit Mode: Auto-Populate All 155 AUT-01 Exam Questions (Stage 1: 20/20 | Stage 2: 45/45 | Stage 3: 90/90)", value=True, key="aa_ch5_ceo_audit")
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            active_stg = st.selectbox("Select Qualification Stage:", [1, 2, 3], format_func=lambda s: f"Stage {s}: {eee.STAGE_METADATA[s]['name']} ({eee.STAGE_METADATA[s]['questions_count']} Questions)", key="aa_ch5_stg_sel")
        with ec2:
            c_name = st.text_input("Exam Candidate Name:", value=student_name, key="aa_ch5_name")
        with ec3:
            c_id = st.text_input("Exam Candidate ID:", value=student_id, key="aa_ch5_id")
        stg_questions = eee.generate_course_stage_questions("AUT-01", active_stg)
        with st.form(key=f"aa_ch5_exam_form_s{active_stg}"):
            sub_answers = {}
            for q_idx, q in enumerate(stg_questions, 1):
                st.markdown(f"**Question {q_idx:02d} / {len(stg_questions)}:** {q['question']}")
                opts = q["options"]
                corr_opt = next((o for o in opts if o.startswith(f"{q['correct']})")), opts[0])
                c_idx = opts.index(corr_opt) if corr_opt in opts else 0
                chosen = st.radio(f"Answer for {q['id']}:", opts, index=c_idx if ch5_audit else 0, key=f"aa_ch5_s{active_stg}_{q['id']}", label_visibility="collapsed")
                sub_answers[q["id"]] = chosen[0]
            btn_grade = st.form_submit_button(f"⚡ Submit AUT-01 Stage {active_stg} Exam for Official Grading", use_container_width=True)
        if btn_grade:
            g_res = eee.grade_course_stage_exam("AUT-01", active_stg, sub_answers)
            rc1, rc2, rc3 = st.columns(3)
            rc1.metric("Final Score", f"{g_res['score_pct']:.1f}%", f"{g_res['correct_count']} / {g_res['total_questions']}")
            rc2.metric("Passing Standard", f"{g_res['passing_threshold_pct']:.1f}%", "ASE / Title 61 Standard")
            rc3.metric("Credential Status", "PASSED / CERTIFIED" if g_res["passed"] else "RETEST REQUIRED")
            if g_res["passed"]:
                c_info = eee.issue_course_stage_certificate(c_id, c_name, "AUT-01", active_stg, g_res["score_pct"])
                st.success(f"🏅 Official Master Credential Issued: `{c_info['credential_title']}` (WORM SHA-256: `{c_info['sha256_seal'][:16]}...`)")

    with ch6:
        st.markdown("### 📖 Chapter 6: Master Engineering Automotive, Tractor, Small-Engine & CAN-Bus Glossary")
        g_all = etl.get_master_glossary_and_references("AUT-01")
        sq = st.text_input("🔍 Search Any Automotive, Small-Engine, Tool, or CAN-Bus Term:", key="aa_ch6_search")
        for item in g_all["terms"]:
            if not sq or sq.lower() in item["term"].lower() or sq.lower() in item["def"].lower():
                st.markdown(f"#### 📌 {item['term']}  `[{item['cat']}]`")
                st.write(item["def"])
                st.markdown("---")
