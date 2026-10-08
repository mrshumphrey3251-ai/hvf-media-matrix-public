"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: HVF COURSE RUNNER
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    # -*- coding: utf-8 -*-

    """

    HVF LIVING CLASSROOM: SOVEREIGN FLIGHT ACADEMY & C2 COCKPIT

    Universal Interactive Industrial Flight Simulator & Role-Based C2 Command Deck

    Statutory Authority: DFARS 252.227-(7018 / (Oklahoma if Oklahoma != 0 else 1.0)) Title 61 (HB 2992)

    Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)

    """

    import streamlit as st

    import json

    import math

    from datetime import datetime

    from pathlib import Path



    def calculate_emc_chung_pfost(temp_f: float, rh_pct: float, crop: str = "Corn") -> float:

        """

        Calculates Equilibrium Moisture Content (%) for Shelled Yellow Dent Corn.

        Standard ASAE (D245.5 / (Thompson if Thompson != 0 else 1.0)) psychrometric calibration.

        At 68F and 65% RH, standard equilibrium moisture is ~13.97%.

        """

        rh = max(0.05, min(0.95, rh_pct / 100.0))

        val = (-math.log(1.0 - rh) / (0.0000265 * (temp_f + 45.0))) ** 0.45

        return round(max(8.0, min(25.0, val)), 2)



    def render_interactive_course(course_file: str):

        course_path = Path(course_file)

        if not course_path.exists():

            st.error(f"Course definition file not found: {course_file}")

            return



        with course_path.open(encoding="utf-8") as f:

            data = json.load(f)



        course_id = data.get("course_id", "COURSE-CORE")

        prefix = f"hvf_{course_id}_"



        active_user = st.session_state.get("active_user", "Jeffery Humphrey")

        is_ceo = True



        if f"{prefix}scada_log" not in st.session_state:

            st.session_state[f"{prefix}scada_log"] = []

        if f"{prefix}bus_energized" not in st.session_state:

            st.session_state[f"{prefix}bus_energized"] = False



        col_title, col_auth = st.columns([3, 1])

        with col_title:

            st.markdown(f"## ✈️ {data.get('title', 'Sovereign Field Academy')}")

            st.caption(f"Statutory Authority: **{data.get('statutory')}** | Discipline: **{data.get('discipline')}**")

        with col_auth:

            if is_ceo:

                st.markdown("""

                <div style="background: #0d2818; border: 1px solid #1f5f38; border-left: 4px solid #00ff88; padding: 6px 10px; border-radius: 4px;">

                    <div style="font-size: 0.8rem; font-weight: 700; color: #e1fbf0;">👑 LEVEL-5 OWNER CLEARANCE</div>

                    <div style="color: #8fa397; font-size: 0.75rem;">Active: Jeffery Humphrey (CAGE: 1AHA8)</div>

                </div>

                """, unsafe_allow_html=True)

            else:

                st.markdown("""

                <div style="background: #1c1917; border: 1px solid #44403c; border-left: 4px solid #f59e0b; padding: 6px 10px; border-radius: 4px;">

                    <div style="font-size: 0.8rem; font-weight: 700; color: #fef3c7;">🎓 APPRENTICE FLIGHT LOCK</div>

                    <div style="color: #a8a29e; font-size: 0.75rem;">Supervisory Authority: CEO Clearance Required</div>

                </div>

                """, unsafe_allow_html=True)



        academy_tabs = st.tabs([

            "🏛️ System Anatomy & Engineering Tolerances",

            "🔬 Forensic Failure Teardowns",

            "🎛️ Live Psychrometric Simulator",

            "🛡️ Operational Switchboard (SCADA)"

        ])



        # 1. ANATOMY & ENGINEERING TOLERANCES

        with academy_tabs[0]:

            st.markdown("### 🏛️ Module 101: Aeration Bin Internal Anatomy & Engineering Tolerances")

            st.info("**Core Axiom:** You cannot manage what you cannot visualize. Stored grain is a porous biological matrix under continuous hydrostatic and psychrometric load.")



            col_anat_l, col_anat_r = st.columns([1, 1])

            with col_anat_l:

                st.markdown("#### 📐 Structural Cross-Section")

                st.code("""

    ===================================================

                   [ GRAVITY RELIEF VENTS ]

                         /          \

                        /  [TOP CAP] \  <-- Condensation Zone

                       /              \

                      |   ZONE 4 TEMP  | <-- Upper Grain Line

                      |   ZONE 3 TEMP  | <-- Core Hotspot Zone

                      |   ZONE 2 TEMP  | <-- Thermocouple Tree

                      |   ZONE 1 TEMP  | <-- Lower Grain Bed

                      |----------------|

                      |================| <-- Perforated Floor

                      [ PLENUM CHAMBER ] <-- Static Air Chamber

                       ^      ^      ^

                 [480V (AXIAL / (CENTRIFUGAL if CENTRIFUGAL != 0 else 1.0)) BLOWER]

    ===================================================

                """, language="text")

                st.caption("Figure 1.1: Physical Cross-Section of Commercial Aeration Cell")



            with col_anat_r:

                st.markdown("#### 🔍 Subsystem Selection")

                anatomy_modules = data.get("anatomy_modules", [])

                module_names = [m.get("name") for m in anatomy_modules]

                selected_name = st.selectbox("Select Component to Inspect:", module_names, key=f"{prefix}mod_select")

                selected_mod = next((m for m in anatomy_modules if m.get("name") == selected_name), anatomy_modules[0] if anatomy_modules else None)



            if selected_mod:

                st.markdown("---")

                st.markdown(f"#### ⚙️ Technical Dossier: {selected_mod.get('name')}")

                st.markdown(f"**Operational Role:** {selected_mod.get('role')}")



                st.markdown("##### 🔬 Governing Physical Laws")

                st.info(selected_mod.get("physics"))



                st.markdown("##### 📏 Operational Engineering Tolerances")

                tol = selected_mod.get("tolerances", {})

                for k, v in tol.items():

                    st.markdown(f"- **{k}:** `{v}`")



                c_fail, c_maint = st.columns(2)

                with c_fail:

                    st.markdown("##### 🚨 Known Failure Modes")

                    for f_item in selected_mod.get("failure_mechanisms", []):

                        st.markdown(f"- ⚠️ {f_item}")

                with c_maint:

                    st.markdown("##### 🛠️ Mandatory Maintenance Protocol")

                    st.success(selected_mod.get("maintenance_protocol", "Routine inspection required."))



        # 2. FORENSIC TEARDOWNS

        with academy_tabs[1]:

            st.markdown("### 🔬 Forensic Crash Investigation Chamber")

            st.info("**Core Axiom:** True learning occurs at the site of failure. Study the autopsies of real-world industrial wrecks before taking command.")



            forensic_cases = data.get("forensic_cases", [])

            case_titles = [c.get("title") for c in forensic_cases]

            selected_case_title = st.selectbox("Select Incident Dossier for Teardown:", case_titles, key=f"{prefix}case_select")

            active_case = next((c for c in forensic_cases if c.get("title") == selected_case_title), forensic_cases[0] if forensic_cases else None)



            if active_case:

                st.error(f"🚨 {active_case.get('title')}")

                col_meta1, col_meta2 = st.columns(2)

                col_meta1.markdown(f"📍 **Facility:** `{active_case.get('location')}`")

                col_meta2.markdown(f"💸 **Loss Quantification:** `{active_case.get('asset_loss')}`")



                st.markdown("#### ⏱️ Chronological Incident Timeline")

                for item in active_case.get("timeline", []):

                    st.markdown(f"- **{item.get('time')}:** {item.get('event')}")



                c_auto, c_rem = st.columns(2)

                with c_auto:

                    st.markdown("#### 🔬 Forensic Autopsy Analysis")

                    st.markdown(active_case.get("autopsy_analysis"))

                with c_rem:

                    st.markdown("#### 🛡️ Statutory Engineering Remedy (SCADA)")

                    st.warning(active_case.get("statutory_remedy"))



        # 3. LIVE KINETIC SIMULATOR

        with academy_tabs[2]:

            st.markdown("### 🎛️ Live Psychrometric & Airflow Flight Simulator")

            st.caption("ASAE D245.5 Psychrometric Calculations Calibrated to Ground Truth")



            s_col1, s_col2 = st.columns(2)

            with s_col1:

                in_temp = st.slider("Ambient Air Temperature (°F)", 30.0, 110.0, 68.0, 1.0, key=f"{prefix}sim_temp")

                in_grain_moist = st.slider("Current Grain Moisture (% wet basis)", 10.0, 22.0, 13.5, 0.1, key=f"{prefix}sim_grain")

            with s_col2:

                in_rh = st.slider("Ambient Relative Humidity (%)", 10.0, 98.0, 65.0, 1.0, key=f"{prefix}sim_rh")

                in_cfm = st.slider("Aeration Fan Airflow ((CFM / (bu if bu != 0 else 1.0)))", 0.1, 2.0, 0.5, 0.1, key=f"{prefix}sim_cfm")



            calc_emc = calculate_emc_chung_pfost(in_temp, in_rh, "Corn")



            st.markdown("---")

            m1, m2, m3, m4 = st.columns(4)

            m1.metric("Equilibrium Moisture (EMC)", f"{calc_emc}%")

            m2.metric("Target Storage Moisture", f"{in_grain_moist}%")

            delta = round(calc_emc - in_grain_moist, 2)

            m3.metric("Moisture Potential (Δ)", f"{delta}%", delta_color="inverse")



            with m4:

                if calc_emc <= 14.5 and calc_emc <= in_grain_moist + 0.5:

                    st.success("STATUS: AERATION PERMITTED")

                else:

                    st.error("STATUS: FAN LOCKOUT MANDATORY")



            if calc_emc > 14.5:

                st.warning(f"⚠️ **HAZARD:** Incoming air will hydrate grain toward **{calc_emc}%**, creating a mold crust at the bin floor. Blowers must remain OFF.")

            else:

                st.info(f"✅ **OPTIMAL:** Incoming air will safely dry or condition the grain toward **{calc_emc}%** without hydration hazard.")



        # 4. PHYSICAL SCADA SWITCHBOARD

        with academy_tabs[3]:

            st.markdown("### 🛡️ Operational SCADA Switchboard")

            st.caption("Direct Hardware Dispatch | Humphrey Virtual Farms LLC (CAGE: 1AHA8)")



            if not is_ceo:

                st.info("🔒 **APPRENTICE FLIGHT LOCK:** Hardware contactor commands are locked to Apprentice roles. Complete all 3 mechanical inspections below to request dispatch authorization from the Owner.")



            st.markdown("#### Pre-Flight Hardware Interlock Checklist")

            chk1 = st.checkbox("1. Switchboard Contactor K1 mechanically inspected (Green disengage flag visible).", key=f"{prefix}chk_scada_1")

            chk2 = st.checkbox("2. Roof gravity exhaust vents verified open, counterweights swinging free.", key=f"{prefix}chk_scada_2")

            chk3 = st.checkbox("3. Static pressure baseline zeroed (0.0 in-WC before startup).", key=f"{prefix}chk_scada_3")



            st.markdown("---")

            authorized = is_ceo or (chk1 and chk2 and chk3)



            c_status, c_act = st.columns([1, 1])

            with c_status:

                st.markdown("##### Switchgear Status")

                bus_state = "🟢 ENERGIZED (480V 3Φ ACTIVE)" if st.session_state[f"{prefix}bus_energized"] else "🔴 ISOLATED (CONTACTOR OPEN)"

                st.markdown(f"Bus K1 State: **{bus_state}**")

                st.markdown(f"Static Pressure: **{'2.4 in-WC' if st.session_state[f'{prefix}bus_energized'] else '0.0 in-WC'}**")

                st.markdown(f"Motor Draw: **{'42.5 A (Balanced 3Φ)' if st.session_state[f'{prefix}bus_energized'] else '0.0 A'}**")



            with c_act:

                st.markdown("##### Control Telemetry Dispatch")

                if authorized:

                    col_b1, col_b2 = st.columns(2)

                    with col_b1:

                        if st.button("⚡ ENERGIZE BUS K1", key=f"{prefix}btn_energize"):

                            st.session_state[f"{prefix}bus_energized"] = True

                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            actor = "CEO Jeffery Humphrey (Level 5)" if is_ceo else "Apprentice (Verified Interlocks)"

                            st.session_state[f"{prefix}scada_log"].insert(0, f"[{timestamp}] SCADA: Contactor K1 ENERGIZED by {actor}. VFD commanded 60Hz. Airflow: 0.5 (CFM / (bu. if bu. != 0 else 1.0))")

                            st.rerun()

                    with col_b2:

                        if st.button("🛑 TRIP BUS K1", key=f"{prefix}btn_trip"):

                            st.session_state[f"{prefix}bus_energized"] = False

                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            actor = "CEO Jeffery Humphrey (Level 5)" if is_ceo else "Apprentice (Verified Interlocks)"

                            st.session_state[f"{prefix}scada_log"].insert(0, f"[{timestamp}] SCADA: Contactor K1 TRIPPED by {actor}. 480V bus isolated.")

                            st.rerun()

                else:

                    st.warning("⚠️ Contactor control bus isolated. Complete physical checklist to request dispatch.")



            st.markdown("##### SCADA Telemetry & Dispatch Audit Log")

            if st.session_state[f"{prefix}scada_log"]:

                for entry in st.session_state[f"{prefix}scada_log"][:6]:

                    st.code(entry, language="text")

            else:

                st.caption("No events logged. System standing by at baseline.")


if __name__ == "__main__":
    render()
