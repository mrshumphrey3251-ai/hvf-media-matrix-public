"""
E.B.O.N.Y. Sovereign Field Academy // Dedicated Academic & Engineering Deck
Provides Exhaustive Multi-Chapter Textbooks, Interactive Formula Workbenches,
and the Seamless 3-Tier Examination Certification Gauntlet.
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Framework: Oklahoma Title 61, Title 74 & OK HB 2992
"""
import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import sys

_cockpit_dir = str(Path(__file__).resolve().parent)
if _cockpit_dir not in sys.path:
    sys.path.insert(0, _cockpit_dir)

try:
    from ebony_exam_engine import (
        COURSE_METADATA, STAGE_METADATA,
        generate_course_stage_questions, grade_course_stage_exam, issue_course_stage_certificate
    )
except Exception as e:
    st.error(f"Engine import error: {e}")

def render_academy_deck():
    st.header("🎓 Sovereign Field Academy // Master Engineering Institute")
    st.info("**Statutory & Copyright Attribution:** Technical standards, formulations, and condition states referenced herein are the intellectual property of their respective governing bodies (AASHTO, ASTM International, FAA, and ODOT). Materials are utilized under Fair Use strictly for state compliance, workforce training, and infrastructure certification under Oklahoma Title 61.")
    st.markdown("---")

    assets_img_dir = Path(r"C:\hvf_c2\assets\images")
    courses_dir = Path(r"C:\hvf_c2\courses")

    courses = {
        "STR-01": {
            "title": "STR-01: Bridge Deck, Pier & Fracture-Critical Member Inspection",
            "hours": "40 Hours (16 Hrs Theory | 24 Hrs Practicum)",
            "framework": "Oklahoma Title 61, Title 74 & ODOT National Bridge Inventory",
            "badge": "AASHTO / ODOT Level-5 Bridge Inspector",
            "diagram": assets_img_dir / "bridge_girder_diagram.svg",
            "video_demo": "https://www.w3schools.com/html/mov_bbb.mp4",
            "manual": courses_dir / "STR_01_BRIDGE_INSPECTION_COURSEWARE.md"
        },
        "STR-02": {
            "title": "STR-02: Commercial Building Envelope, Roof Membrane Moisture & Facade NDT",
            "hours": "40 Hours (16 Hrs Theory | 24 Hrs Practicum)",
            "framework": "Oklahoma Title 61 Public Facilities & ASTM C1153 Standards",
            "badge": "Title 61 Commercial Building Diagnostic Specialist",
            "diagram": assets_img_dir / "roof_thermal_moisture.svg",
            "video_demo": "https://www.w3schools.com/html/mov_bbb.mp4",
            "manual": courses_dir / "STR_02_BUILDING_ENVELOPE_COURSEWARE.md"
        },
        "STR-03": {
            "title": "STR-03: Roadway Pavement Distress, Rutting & ASTM D6433 PCI Survey",
            "hours": "40 Hours (16 Hrs Theory | 24 Hrs Practicum)",
            "framework": "Oklahoma Title 61, ODOT & ASTM D6433 Pavement Standards",
            "badge": "ASTM D6433 Certified Roadway & Drainage Inspector",
            "diagram": assets_img_dir / "roadway_pavement_rutting.svg",
            "video_demo": "https://www.w3schools.com/html/mov_bbb.mp4",
            "manual": courses_dir / "STR_03_ROADWAY_PCI_COURSEWARE.md"
        }
    }

    c_sel_col1, c_sel_col2 = st.columns([3, 1])
    with c_sel_col1:
        selected_code = st.selectbox(
            "Select Accredited Engineering Curriculum:",
            list(courses.keys()),
            format_func=lambda x: courses[x]["title"],
            key="sel_main_academy_course"
        )
    with c_sel_col2:
        st.write("")
        st.metric("Accredited Duration", "40.0 Hours", courses[selected_code]["badge"])

    active_course = courses[selected_code]
    st.info(f"**Curriculum Target:** `{active_course['title']}` | **Statutory Authority:** `{active_course['framework']}`")

    tab_ch1, tab_ch2, tab_ch3, tab_ch4, tab_exam = st.tabs([
        "📖 Ch 1: Statutory Law & Manual",
        "⚙️ Ch 2: Physics & Schematics",
        "💥 Ch 3: Forensic Case Studies",
        "🎬 Ch 4: Flight Videos & Field SOPs",
        "📝 Ch 5: 3-Tier Certification Exam"
    ])

    with tab_ch1:
        st.subheader(f"Chapter 1: Statutory Governance & Master Textbook // {selected_code}")
        if active_course["manual"].exists():
            with st.container(height=420):
                st.markdown(active_course["manual"].read_text(encoding="utf-8"))
        else:
            st.warning("Master course manual not found on disk.")

    with tab_ch2:
        st.subheader("Chapter 2: Structural Mechanics & Technical Schematics")
        if active_course["diagram"].exists():
            st.image(str(active_course["diagram"]), caption=f"Figure: {active_course['title']} Engineering Schematic", use_container_width=True)
        if selected_code == "STR-01":
            st.markdown("### Interactive Delamination Calculator (D_%)")
            gc1, gc2 = st.columns(2)
            with gc1:
                gross = st.number_input("Gross Deck Span Area (sq ft):", value=15000, step=500, key="gc_deck")
            with gc2:
                delam = st.number_input("Detected Delamination Area (sq ft):", value=1800, step=50, key="gc_delam")
            dpct = (delam / gross) * 100.0 if gross > 0 else 0.0
            st.metric("Delamination Percentage", f"{dpct:.2f}%", "MANDATES HYDRODEMOLITION" if dpct >= 10.0 else "Monitoring Permitted")
        elif selected_code == "STR-02":
            st.markdown("### ASTM C1153 Roof Thermal Anomaly Formulation")
            st.code("Delta_T >= 2.0 degrees C", language="text")
            st.markdown("### Conductive Heat Loss Equation")
            st.code("Q = U * A * Delta_T", language="text")
        else:
            st.markdown("### ASTM D6433 Pavement Condition Index Formulation")
            st.code("PCI = 100 - SUM(CDV)", language="text")
            st.markdown("### Transverse Rut Depth Threshold")
            st.code("d_rut = y_straightedge - y_pavement >= 0.25 in", language="text")

    with tab_ch3:
        st.subheader("Chapter 3: Forensic Engineering Failure Case Studies")
        if selected_code == "STR-01":
            st.markdown("""
            * **Silver Bridge Collapse (1967):** Single 0.1-inch stress corrosion fracture in Eyebar 330 caused total progressive collapse in <60s (46 fatalities). Mandates 100% inspection of FCM tension nodes.
            * **I-35W Mississippi River Bridge Disaster (2007):** Undersized 0.5-inch steel gusset plates bowed and fractured under dead load. Mandates 3D point-cloud distortion measurement.
            """)
        elif selected_code == "STR-02":
            st.markdown("""
            * **Champlain Towers South Collapse (2021):** Decades of unmitigated water penetration through failed pool deck waterproofing corroded structural support column rebar, leading to catastrophic failure.
            * **High-Rise Masonry Rust-Jacking:** Moisture penetrating behind brick facades oxidizes structural steel shelf angles, generating expansive tensile stresses exceeding 10,000 psi.
            """)
        else:
            st.markdown("""
            * **US Route 66 Embankment Shear Failure:** Failed RCB culvert separated at internal barrel joints, piping pressurized water into highway subgrade and causing a 30-foot slope blowout.
            * **Wheel-Path Hydroplaning Catastrophe:** Rut depth >=0.25 inches creates water pooling, causing dynamic hydroplaning and multi-vehicle roadway crossover crashes.
            """)

    with tab_ch4:
        st.subheader("Chapter 4: Operational Flight Videos & Field SOPs")
        st.video(active_course["video_demo"])
        st.caption("Operational Flight Telemetry & Sensor Deployment Sortie Demonstration")
        if selected_code == "STR-01":
            st.markdown("""
            1. **Optical Flow Navigation:** Minimum 15 lux surface illumination required.
            2. **Ingress Speed:** Abutment entry speed <= 1.5 m/s.
            3. **LiDAR Rangefinding:** Downward TF02-i altitude hold maintained within +/- 0.1m.
            """)
        elif selected_code == "STR-02":
            st.markdown("""
            1. **Window:** 45-90 minutes post-sunset during clear sky conditions.
            2. **Emissivity:** Set thermal camera emissivity to 0.92 for single-ply membranes.
            3. **Standoff:** Maintain 10-foot minimum standoff from parapet edge.
            """)
        else:
            st.markdown("""
            1. **Traffic Escort:** Moving roadway escort vehicle maintaining continuous visual line of sight.
            2. **No Hover Over Moving Traffic:** Sustained hovering over moving vehicles prohibited under FAA Part 107.
            3. **LiDAR Scan Rate:** Maintain 300,000 pts/sec rate across corridor sweeps.
            """)

    with tab_exam:
        st.subheader(f"Chapter 5: Official {selected_code} State Certification Exam")
        st.write("Candidates must conquer all three progressive examination stages (Stage 1: 20 Qs, Stage 2: 45 Qs, Stage 3: 90 Qs) to earn official state credentials under Oklahoma Title 61.")

        e_col1, e_col2, e_col3 = st.columns([2, 2, 2])
        with e_col1:
            active_s_num = st.selectbox(
                "Select Qualification Stage:",
                [1, 2, 3],
                format_func=lambda x: f"Stage {x}: {STAGE_METADATA[x]['name']}",
                key="unified_stage_sel"
            )
        with e_col2:
            cand_name = st.text_input("Candidate Full Name:", value="Jeffery Humphrey", key="unified_name")
        with e_col3:
            cand_id = st.text_input("Candidate ID:", value="HVF-TECH-001", key="unified_id")

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
                st.error("Candidate did not achieve the required passing threshold. Review Chapters 1-4 and resubmit.")

            with st.expander("🔍 View Technical Question Feedback & Explanations", expanded=False):
                for fb in grade_res["detailed_feedback"]:
                    if fb["status"] == "CORRECT":
                        st.write(f":green[**{fb['id']} (Correct):**] {fb['explanation']}")
                    else:
                        st.write(f":red[**{fb['id']} (Incorrect):**] Selected: `{fb['your_answer']}` | Correct: `{fb['correct_answer']}` — {fb['explanation']}")