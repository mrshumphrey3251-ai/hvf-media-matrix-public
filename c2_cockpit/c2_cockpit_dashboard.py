# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Man-in-the-Loop Mitigation & Typewriter
Authority: CEO Jeffery Humphrey (Level 5 Authority)
"""
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import psutil
import time
import random
import json
from pathlib import Path

class MasterCockpit:
    def __init__(self):
        self.ceo_name = "Jeffery Humphrey"
        self.clearance = "Level 5 Sovereign"
        self.telemetry_vault = Path(r"C:\HVF_Repos\HVF_Matrix_Core\telemetry_state.json")
        self._ensure_telemetry_file()
        self._init_session_state()

    def _ensure_telemetry_file(self):
        if not self.telemetry_vault.parent.exists():
            self.telemetry_vault.parent.mkdir(parents=True, exist_ok=True)
        if not self.telemetry_vault.exists():
            initial_state = {"kirchhoff_current": 1.205, "optical_gli": 0.210, "matrix_throughput": 889}
            with open(self.telemetry_vault, "w") as f:
                json.dump(initial_state, f)

    def _read_live_sensors(self):
        try:
            with open(self.telemetry_vault, "r") as f:
                return json.load(f)
        except:
            return {"kirchhoff_current": 1.2, "optical_gli": 0.2, "matrix_throughput": 850}

    def _init_session_state(self):
        if "grid_state" not in st.session_state:
            st.session_state.grid_state = "NORMAL"
        if "active_hazard" not in st.session_state:
            st.session_state.active_hazard = None
        if "hazard_gps" not in st.session_state:
            st.session_state.hazard_gps = ""
        if "mitigation_log" not in st.session_state:
            st.session_state.mitigation_log = ""
        if "alarm_active" not in st.session_state:
            st.session_state.alarm_active = False

    def _inject_css(self):
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700;900&display=swap');
        .c2-header { background: #090e17; border: 1px solid #1e293b; border-left: 4px solid #00f3ff; padding: 10px 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace; }
        .c2-title { font-family: 'Orbitron', sans-serif; font-size: 18px; color: #f8fafc; margin: 0; letter-spacing: 2px; }
        .c2-badge { color: #00f3ff; font-size: 12px; font-weight: 700; }
        @keyframes flash { 0% { opacity: 1; text-shadow: 0 0 20px #ff0000; } 50% { opacity: 0.3; text-shadow: none; } 100% { opacity: 1; text-shadow: 0 0 20px #ff0000; } }
        .alert-box { background: #1a0505; border: 2px solid #ff0000; padding: 40px; text-align: center; margin-top: 50px; border-radius: 5px; animation: flash 1s infinite; margin-bottom: 30px; }
        .alert-title { color: #ff0000; font-family: 'Orbitron', sans-serif; font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        .alert-gps { color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-size: 20px; letter-spacing: 2px; }
        .ebony-modal { border: 2px solid #00f3ff; background: #030712; padding: 25px; margin-top: 20px; box-shadow: 0 0 20px rgba(0, 243, 255, 0.2); }
        </style>
        """, unsafe_allow_html=True)

    def _render_header(self):
        st.markdown(f"""
        <div class="c2-header">
            <div>
                <p class="c2-title">HVF OMNI-INDUSTRIAL COMMAND MATRIX</p>
                <p style="margin:0; font-size:10px; color:#64748b;">ACTIVE ENGINE: EBONY AI // KERNEL: SECURE</p>
            </div>
            <div style="text-align: right;">
                <p style="margin:0; font-size:10px; color:#64748b;">COMMANDER</p>
                <p class="c2-badge">{self.ceo_name} | {self.clearance}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _create_gauge(self, title, val, min_v, max_v, safe_low, safe_high, suffix=""):
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = val,
            number = {'suffix': suffix, 'font': {'color': '#f8fafc', 'size': 30}},
            title = {'text': title, 'font': {'color': '#00f3ff', 'size': 14, 'family': 'JetBrains Mono'}},
            gauge = {
                'axis': {'range': [min_v, max_v], 'tickwidth': 1, 'tickcolor': "#1e293b"},
                'bar': {'color': "#f8fafc", 'thickness': 0.2},
                'bgcolor': "#090e17",
                'borderwidth': 2,
                'bordercolor': "#1e293b",
                'steps': [
                    {'range': [min_v, safe_low], 'color': '#ef4444'},
                    {'range': [safe_low, safe_high], 'color': '#10b981'},
                    {'range': [safe_high, max_v], 'color': '#ef4444'}
                ],
            }
        ))
        fig.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'family': "JetBrains Mono"})
        return fig

    def _trigger_hazard(self, hazard_name, gps, log_msg):
        st.session_state.active_hazard = hazard_name
        st.session_state.hazard_gps = gps
        st.session_state.mitigation_log = log_msg
        st.session_state.grid_state = "SHOCK"
        st.session_state.alarm_active = True
        st.rerun()

    def _manage_audio_alarm(self):
        cmd = "START" if st.session_state.alarm_active else "STOP"
        alarm_js = f"""
        <script>
        if (!window.scadaAudioCtx) {{ window.scadaAudioCtx = new (window.AudioContext || window.webkitAudioContext)(); }}
        function manageAlarm(command) {{
            if (command === "START") {{
                if (!window.scadaOsc1) {{
                    window.scadaOsc1 = window.scadaAudioCtx.createOscillator();
                    window.scadaOsc2 = window.scadaAudioCtx.createOscillator();
                    window.scadaGain = window.scadaAudioCtx.createGain();
                    window.scadaOsc1.connect(window.scadaGain); window.scadaOsc2.connect(window.scadaGain);
                    window.scadaGain.connect(window.scadaAudioCtx.destination);
                    window.scadaOsc1.type = "square"; window.scadaOsc2.type = "square";
                    window.scadaOsc1.frequency.value = 853; window.scadaOsc2.frequency.value = 960;
                    window.scadaGain.gain.value = 0.15;
                    window.scadaOsc1.start(); window.scadaOsc2.start();
                }}
            }} else {{
                if (window.scadaOsc1) {{ window.scadaOsc1.stop(); window.scadaOsc1 = null; }}
                if (window.scadaOsc2) {{ window.scadaOsc2.stop(); window.scadaOsc2 = null; }}
            }}
        }}
        manageAlarm("{cmd}");
        </script>
        """
        components.html(alarm_js, height=0)

    def _render_shock_screen(self):
        st.markdown(f"""
        <div class="alert-box">
            <div class="alert-title">⚠ CRITICAL INFRASTRUCTURE FAILURE ⚠</div>
            <div class="alert-title">{st.session_state.active_hazard.upper()} DETECTED</div>
            <div class="alert-gps">IMPACT COORDINATES: {st.session_state.hazard_gps}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ INITIATE EBONY PROTOCOL ⚡", key="init_ebony", type="primary", use_container_width=True):
            st.session_state.alarm_active = False
            st.session_state.grid_state = "MITIGATION_ANIMATION"
            st.rerun()

    def _render_dashboard_frame(self, progress=1.0, mode="NORMAL"):
        base_freq = 60.0; base_mw = 4250.0; base_kirchhoff = 1.2
        crash_freq = 58.2; crash_mw = 3100.0; crash_kirchhoff = 3.5
        
        current_freq = crash_freq + ((base_freq - crash_freq) * progress) + random.uniform(-0.02, 0.02)
        current_mw = crash_mw + ((base_mw - crash_mw) * progress) + random.uniform(-10, 10)
        current_k = crash_kirchhoff + ((base_kirchhoff - crash_kirchhoff) * progress) + random.uniform(-0.05, 0.05)

        cpu = psutil.cpu_percent() if mode == "NORMAL" else 95.0 + random.uniform(-2, 2)
        ram = psutil.virtual_memory().percent
        sub_status = "100% ONLINE" if progress > 0.8 else "88% ONLINE (SECTOR BREACH)"
        sub_color = "normal" if progress > 0.8 else "inverse"

        if mode in ["RECOVERY", "RESTORED"]:
            st.markdown("<h3 style='color:#10b981; text-align:center; font-family:Orbitron;'>🟢 EBONY INITIATED: SYSTEM RECOVERY IN PROGRESS</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([0.8, 1.2, 1.2, 1.1])

        with col1:
            st.markdown("#### 🖥️ BARE-METAL")
            st.metric(label="Live CPU Load", value=f"{cpu:.1f}%", delta="Hardware")
            st.metric(label="Physical RAM", value=f"{ram}%", delta="Hardware")
            st.metric(label="Substation Net", value=sub_status, delta="Status", delta_color=sub_color)

        with col2:
            st.markdown("#### ⚡ SENSOR CORE")
            gauge_k = self._create_gauge("Kirchhoff Vector", current_k, 0, 5, 0.5, 1.8, "A")
            st.plotly_chart(gauge_k, use_container_width=True, config={'displayModeBar': False}, key=f"gk_{progress}")

        with col3:
            st.markdown("#### 🌐 OKLAHOMA GRID")
            gauge_f = self._create_gauge("Grid Frequency", current_freq, 55, 65, 59.5, 60.5, "Hz")
            st.plotly_chart(gauge_f, use_container_width=True, config={'displayModeBar': False}, key=f"gf_{progress}")
            
            gauge_mw = self._create_gauge("Active MW Load", current_mw, 0, 5000, 3800, 4800, "MW")
            st.plotly_chart(gauge_mw, use_container_width=True, config={'displayModeBar': False}, key=f"gmw_{progress}")

        with col4:
            st.markdown("#### 🚨 THREAT SIMULATOR")
            if mode == "NORMAL":
                log_veh = ">> EVENT: Loss of 12kV Distribution Line.\n>> EBONY ACTION: Isolating Line 4. Activating automated feeder switches.\n>> GRID STATUS: Load restored to 94% of affected block.\n>> ---------------------------------------------------\n>> REQUIRED HUMAN ACTION:\n>> 1. Dispatch physical Line Crew to RT 66.\n>> 2. Notify Highway Patrol of pole debris in roadway.\n>> 3. Schedule replacement transformer installation."
                if st.button("🚗 Vehicle Strike", key="btn_veh", use_container_width=True):
                    self._trigger_hazard("Vehicle Strike", "LAT: 35.8421° N, LON: -97.0384° W (RT 66)", log_veh)
                
                log_tor = ">> EVENT: Massive transmission failure in Sector 4.\n>> EBONY ACTION: Air-gapping Sector 4 to prevent cascade failure.\n>> GRID STATUS: Backfeeding 400MW to local hospitals. Frequency stable.\n>> ---------------------------------------------------\n>> REQUIRED HUMAN ACTION:\n>> 1. Dispatch Heavy Infrastructure Units to Moore.\n>> 2. Coordinate emergency logistics with FEMA/State Police.\n>> 3. Authorize emergency budget release for tower reconstruction."
                if st.button("🌪️ F5 Tornado", key="btn_tor", use_container_width=True):
                    self._trigger_hazard("F5 Tornado Strike", "LAT: 35.3395° N, LON: -97.4867° W (MOORE)", log_tor)
                
                log_cyb = ">> EVENT: Unauthorized breaker actuation attempt via State Actor.\n>> EBONY ACTION: Iron Dome deployed. Node air-gapped from C2.\n>> GRID STATUS: Intrusion neutralized. Zero loss of load.\n>> ---------------------------------------------------\n>> REQUIRED HUMAN ACTION:\n>> 1. Initiate forensic audit of OKC Hub firewalls.\n>> 2. Rotate all cryptographic keys network-wide.\n>> 3. Dispatch Threat Intelligence report to DHS."
                if st.button("💻 SCADA Breach", key="btn_cyb", use_container_width=True):
                    self._trigger_hazard("State Cyber Breach", "LAT: 35.4676° N, LON: -97.5164° W (OKC)", log_cyb)
                
                log_frz = ">> EVENT: Natural gas freeze off. Rapid -1200MW generation loss.\n>> EBONY ACTION: Micro-load shedding engaged. Purchasing SPP reserve.\n>> GRID STATUS: Total grid collapse averted. Rolling blackouts active.\n>> ---------------------------------------------------\n>> REQUIRED HUMAN ACTION:\n>> 1. Issue emergency conservation alerts via SMS/Broadcast.\n>> 2. Dispatch crews to winterize failing wellheads.\n>> 3. Prepare political brief for Governor's office."
                if st.button("❄️ Freeze-Off", key="btn_frz", use_container_width=True):
                    self._trigger_hazard("Generation Shortfall", "STATEWIDE ALERT", log_frz)

        # The Middle-Screen Typewriter Popup
        if mode in ["RECOVERY", "RESTORED"]:
            typed_length = int(len(st.session_state.mitigation_log) * progress)
            display_text = st.session_state.mitigation_log[:typed_length]
            
            st.markdown(f'''
            <div class="ebony-modal">
                <h3 style="color: #00f3ff; font-family: 'Orbitron', sans-serif; margin-top: 0;">👑 EBONY AUTONOMOUS MITIGATION LOG</h3>
                <p style="color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-size: 15px; white-space: pre-wrap; line-height: 1.5;">{display_text}</p>
            </div>
            ''', unsafe_allow_html=True)
            
            if mode == "RESTORED":
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✅ ACKNOWLEDGE ACTIONS & RESET BOARD", key="btn_reset", use_container_width=True, type="primary"):
                    st.session_state.grid_state = "NORMAL"
                    st.rerun()

    def render_cockpit(self):
        self._inject_css()
        self._manage_audio_alarm()
        self._render_header()
        
        if st.session_state.grid_state == "SHOCK":
            self._render_shock_screen()
        elif st.session_state.grid_state == "MITIGATION_ANIMATION":
            ui_placeholder = st.empty()
            steps = 20 # Slower, smoother typing and dial animation
            for i in range(steps + 1):
                progress = i / float(steps)
                with ui_placeholder.container():
                    self._render_dashboard_frame(progress=progress, mode="RECOVERY")
                time.sleep(0.2)
            st.session_state.grid_state = "MITIGATION_STABLE"
            st.rerun()
        elif st.session_state.grid_state == "MITIGATION_STABLE":
            self._render_dashboard_frame(progress=1.0, mode="RESTORED")
        else:
            self._render_dashboard_frame(progress=1.0, mode="NORMAL")

# === EXPORTED RENDER HOOK ===
def render():
    cockpit = MasterCockpit()
    cockpit.render_cockpit()
