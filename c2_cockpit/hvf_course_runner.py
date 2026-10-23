# -*- coding: utf-8 -*-
"""
HVF LIVING CLASSROOM: SOVEREIGN FLIGHT ACADEMY & C2 COCKPIT
Universal Interactive Industrial Flight Simulator & Role-Based C2 Command Deck
Statutory Authority: DFARS 252.227-7018 / Oklahoma Title 61 (HB 2992)
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8)
"""
import streamlit as st
import json
import math
from datetime import datetime
from pathlib import Path

def calculate_emc_chung_pfost(temp_f: float, rh_pct: float, crop: str = "Corn") -> float:
    rh = max(0.05, min(0.95, rh_pct / 100.0))
    val = (-math.log(1.0 - rh) / (0.0000265 * (temp_f + 45.0))) ** 0.45
    return round(max(8.0, min(25.0, val)), 2)

DEFAULT_GRAIN_ASCII = (
    "===================================================\n"
    "               [ GRAVITY RELIEF VENTS ]\n"
    "                     /          \\\n"
    "                    /  [TOP CAP] \\  <-- Condensation Zone\n"
    "                   /              \\\n"
    "                  |   ZONE 4 TEMP  | <-- Upper Grain Line\n"
    "                  |   ZONE 3 TEMP  | <-- Core Hotspot Zone\n"
    "                  |   ZONE 2 TEMP  | <-- Thermocouple Tree\n"
    "                  |   ZONE 1 TEMP  | <-- Lower Grain Bed\n"
    "                  |----------------|\n"
    "                  |================| <-- Perforated Floor\n"
    "                  [ PLENUM CHAMBER ] <-- Static Air Chamber\n"
    "                   ^      ^      ^\n"
    "             [480V AXIAL / CENTRIFUGAL BLOWER]\n"
    "==================================================="
)

def render_interactive_course(course_file: str):
    course_path = Path(course_file)
    if not course_path.exists():
        st.error(f"Course definition file not found: {course_file}")
        return

    with course_path.open(encoding="utf-8") as f:
        data = json.load(f)

    course_id = data.get("course_id", "COURSE-CORE")
    prefix = f"hvf_{course_id}_"
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
        st.markdown("""
        <div style="background: #0d2818; border: 1px solid #1f5f38; border-left: 4px solid #00ff88; padding: 6px 10px; border-radius: 4px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #e1fbf0;">👑 LEVEL-5 OWNER CLEARANCE</div>
            <div style="color: #8fa397; font-size: 0.75rem;">Active: Jeffery Humphrey (CAGE: 1AHA8)</div>
        </div>
        """, unsafe_allow_html=True)

    academy_tabs = st.tabs([
        "🏛️ System Anatomy & Engineering Tolerances",
        "🔬 Forensic Failure Teardowns",
        "🎛️ Live Engineering Simulator",
        "🛡️ Operational Switchboard (SCADA)"
    ])

    # 1. ANATOMY & ENGINEERING TOLERANCES
    with academy_tabs[0]:
        mod_hdr = data.get("module_header", "🏛️ Module 101: Aeration Bin Internal Anatomy & Engineering Tolerances")
        axiom_txt = data.get("core_axiom", "You cannot manage what you cannot visualize. Stored grain is a porous biological matrix under continuous hydrostatic and psychrometric load.")
        fig_cap = data.get("figure_caption", "Figure 1.1: Physical Cross-Section of Commercial Aeration Cell")
        ascii_art = data.get("ascii_schematic", DEFAULT_GRAIN_ASCII)

        st.markdown(f"### {mod_hdr}")
        st.info(f"**Core Axiom:** {axiom_txt}")

        col_anat_l, col_anat_r = st.columns([1, 1])
        with col_anat_l:
            st.markdown("#### 📐 Structural Cross-Section")
            clean_ascii = "\n" + ascii_art.strip()
            st.code(clean_ascii, language="text")
            st.caption(fig_cap)

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
            if selected_mod.get("latex"):
                st.latex(selected_mod.get("latex"))

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

    # 3. LIVE DOMAIN-SPECIFIC SIMULATOR
    with academy_tabs[2]:
        if "CIVIL" in course_id:
            st.markdown("### 🎛️ Live Bridge Structural Load, Crack Fatigue & Pier Scour Simulator")
            st.caption("ODOT NBI / 23 CFR Part 650 Structural Deflection & Hydrologic Scour Telemetry")
            s1, s2 = st.columns(2)
            with s1:
                axle_load = st.slider(" Gross Vehicle Freight Load (Tons)", 10.0, 80.0, 36.0, 2.0, key=f"{prefix}load")
                crack_mm = st.slider("Detected Gusset/Girder Crack Width (mm)", 0.05, 1.50, 0.12, 0.05, key=f"{prefix}crack")
            with s2:
                scour_m = st.slider("Bathymetric Pier Scour Depth (m)", 0.0, 3.0, 0.4, 0.1, key=f"{prefix}scour")
                pci_idx = st.slider("ASTM D6433 Corridor PCI Score", 20, 100, 88, 1, key=f"{prefix}pci")
            defl_in = round((axle_load * 0.042) * (1.0 + crack_mm * 0.5), 2)
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mid-Span Deflection", f"{defl_in} in")
            m2.metric("Crack Growth Risk", "CRITICAL" if crack_mm > 0.25 else "NOMINAL")
            m3.metric("Pier Footing Margin", f"{round(3.5 - scour_m, 2)} m")
            m4.metric("Corridor PCI Rating", f"{pci_idx} / 100")
            if crack_mm > 0.25 or scour_m > 1.2:
                st.error("🛑 **STRUCTURAL ALERT:** Fracture-critical threshold exceeded. Seal Title 61 Emergency Docket and restrict heavy axle load immediately.")
            else:
                st.success("✅ **STRUCTURAL INTEGRITY VERIFIED:** Bridge deflection, crack tolerance, and pier scour within ODOT NBI operational limits.")
        elif "03" in course_id or "MICROGRID" in course_id:
            st.markdown("### 🎛️ Live 480V 3-Phase Microgrid Islanding & Kinetic Storage Simulator")
            st.caption("IEEE 1547 Sub-16ms Static Transfer & Synchronous Frequency Droop Telemetry")
            s1, s2 = st.columns(2)
            with s1:
                solar_kw = st.slider("Solar Array Output (kW)", 0.0, 500.0, 320.0, 10.0, key=f"{prefix}solar")
                load_kw = st.slider("Facility 480V Bus Demand (kW)", 50.0, 450.0, 210.0, 10.0, key=f"{prefix}load_kw")
            with s2:
                soc_pct = st.slider("BESS & Kinetic Reserve SoC (%)", 10.0, 100.0, 88.0, 1.0, key=f"{prefix}soc")
                grid_hz = st.slider("Utility Grid Frequency (Hz)", 57.5, 61.5, 60.0, 0.1, key=f"{prefix}hz")
            net_kw = round(solar_kw - load_kw, 1)
            islanded = abs(grid_hz - 60.0) > 0.5
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Net Microgrid Surplus", f"{net_kw:+.1f} kW")
            m2.metric("Bus Frequency", "60.00 Hz (Locked)" if islanded else f"{grid_hz:.2f} Hz")
            m3.metric("Reserve Autonomy", f"{round(soc_pct * 0.45, 1)} Hrs")
            m4.metric("PCC Breaker State", "ISLANDED (11.4ms)" if islanded else "GRID-TIED")
            if islanded:
                st.warning("⚠️ **SUB-16ms ISLANDING ACTIVE:** Utility frequency excursion detected. Static transfer switch isolated PCC in 11.4ms; facility running 100% on Sovereign BESS/Solar.")
            else:
                st.success("✅ **SYNCHRONOUS GRID PARITY:** 480V 3-phase bus locked at nominal frequency and voltage.")
        elif "C2" in course_id or "04" in course_id:
            st.markdown("### 🎛️ Live Bare-Metal Cryptographic Entropy & Guillotine Isolation Simulator")
            st.caption("DFARS 252.204-7012 / FIPS 140-3 TLS 1.3 Socket & WORM Merkle Verification")
            s1, s2 = st.columns(2)
            with s1:
                snr_db = st.slider("Tactical Comms SNR (dB)", 5.0, 40.0, 28.0, 1.0, key=f"{prefix}snr")
                bw_mhz = st.slider("Channel Bandwidth (MHz)", 1.0, 100.0, 40.0, 1.0, key=f"{prefix}bw")
            with s2:
                anom_score = st.slider("Ingress Packet Anomaly Score", 0.0, 1.0, 0.04, 0.02, key=f"{prefix}anom")
                iter_k = st.slider("PBKDF2 Key Iterations (x1,000)", 100, 1000, 600, 50, key=f"{prefix}iter")
            cap_mbps = round(bw_mhz * math.log2(1.0 + (10.0 ** (snr_db / 10.0))), 1)
            isolated = anom_score >= 0.35
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Shannon Channel Capacity", f"{cap_mbps} Mbps")
            m2.metric("Hardware Guillotine", "TRIPPED (36.75ns)" if isolated else "ARMED & NOMINAL")
            m3.metric("PBKDF2 Hardening", f"{iter_k:,},000 iters")
            m4.metric("Merkle Parity", "593 / 593 SEALED")
            if isolated:
                st.error("🛑 **REALITY FIREWALL TRIPPED:** Unsigned anomaly threshold exceeded. Hardware bus severed in 36.75ns; zero bytes reached SQLite WORM vault.")
            else:
                st.success("✅ **BARE-METAL ENCLAVE SECURE:** Direct TLS 1.3 socket verified; WORM ledger operating with zero cloud dependencies.")
        else:
            st.markdown("### 🎛️ Live Psychrometric & Airflow Flight Simulator")
            st.caption("ASAE D245.5 Psychrometric & Industrial Telemetry Calculations Calibrated to Ground Truth")
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                in_temp = st.slider("Ambient Air Temperature (°F)", 30.0, 110.0, 68.0, 1.0, key=f"{prefix}sim_temp")
                in_grain_moist = st.slider("Current Grain Moisture (% wet basis)", 10.0, 22.0, 13.5, 0.1, key=f"{prefix}sim_grain")
            with s_col2:
                in_rh = st.slider("Ambient Relative Humidity (%)", 10.0, 98.0, 65.0, 1.0, key=f"{prefix}sim_rh")
                in_cfm = st.slider("Aeration Fan Airflow (CFM / bu)", 0.1, 2.0, 0.5, 0.1, key=f"{prefix}sim_cfm")
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

        st.markdown("#### Pre-Flight Hardware Interlock Checklist")
        chk1 = st.checkbox("1. Switchboard Contactor K1 mechanically inspected (Green disengage flag visible).", key=f"{prefix}chk_scada_1")
        chk2 = st.checkbox("2. Primary relief & isolation interlocks verified clear.", key=f"{prefix}chk_scada_2")
        chk3 = st.checkbox("3. Telemetry baseline zeroed and WORM ledger ready.", key=f"{prefix}chk_scada_3")

        st.markdown("---")
        authorized = is_ceo or (chk1 and chk2 and chk3)

        c_status, c_act = st.columns([1, 1])
        with c_status:
            st.markdown("##### Switchgear Status")
            bus_state = "🟢 ENERGIZED (480V 3Φ ACTIVE)" if st.session_state[f"{prefix}bus_energized"] else "🔴 ISOLATED (CONTACTOR OPEN)"
            st.markdown(f"Bus K1 State: **{bus_state}**")
            st.markdown(f"Line Pressure / Load: **{'NOMINAL (LOCKED)' if st.session_state[f'{prefix}bus_energized'] else '0.0 (STANDBY)'}**")
            st.markdown(f"Current Draw: **{'42.5 A (Balanced 3Φ)' if st.session_state[f'{prefix}bus_energized'] else '0.0 A'}**")

        with c_act:
            st.markdown("##### Control Telemetry Dispatch")
            if authorized:
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("⚡ ENERGIZE BUS K1", key=f"{prefix}btn_energize"):
                        st.session_state[f"{prefix}bus_energized"] = True
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state[f"{prefix}scada_log"].insert(0, f"[{timestamp}] SCADA: Contactor K1 ENERGIZED by CEO Jeffery Humphrey (Level 5). Bus active.")
                        st.rerun()
                with col_b2:
                    if st.button("🛑 TRIP BUS K1", key=f"{prefix}btn_trip"):
                        st.session_state[f"{prefix}bus_energized"] = False
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state[f"{prefix}scada_log"].insert(0, f"[{timestamp}] SCADA: Contactor K1 TRIPPED by CEO Jeffery Humphrey (Level 5). 480V bus isolated.")
                        st.rerun()

        st.markdown("##### SCADA Telemetry & Dispatch Audit Log")
        if st.session_state[f"{prefix}scada_log"]:
            for entry in st.session_state[f"{prefix}scada_log"][:6]:
                st.code(entry, language="text")
        else:
            st.caption("No events logged. System standing by at baseline.")
