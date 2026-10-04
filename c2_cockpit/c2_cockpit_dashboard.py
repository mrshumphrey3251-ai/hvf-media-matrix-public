# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Industrial Gauges & Dynamic Recovery
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

    def _inject_css(self):
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700;900&display=swap');
        .c2-header { background: #090e17; border: 1px solid #1e293b; border-left: 4px solid #00f3ff; padding: 10px 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace; }
        .c2-title { font-family: 'Orbitron', sans-serif; font-size: 18px; color: #f8fafc; margin: 0; letter-spacing: 2px; }
        .c2-badge { color: #00f3ff; font-size: 12px; font-weight: 700; }
        @keyframes flash { 0% { opacity: 1; text-shadow: 0 0 20px #ff0000; } 50% { opacity: 0.3; text-shadow: none; } 100% { opacity: 1; text-shadow: 0 0 20px #ff0000; } }
        .alert-box { background: #1a0505; border: 2px solid #ff0000; padding: 40px; text-align: center; margin-top: 50px; border-radius: 5px; animation: flash 1s infinite; }
        .alert-title { color: #ff0000; font-family: 'Orbitron', sans-serif; font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        .alert-gps { color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-size: 20px; letter-spacing: 2px; }
        .ebony-terminal { background: #000000; border: 1px solid #00f3ff; padding: 15px; color: #00f3ff; font-family: 'JetBrains Mono', monospace; font-size: 13px; height: 160px; overflow-y: auto; }
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
                    {'range': [min_v, safe_low], 'color': '#ef4444'}, # RED
                    {'range': [safe_low, safe_high], 'color': '#10b981'}, # GREEN
                    {'range': [safe_high, max_v], 'color': '#ef4444'}  # RED
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
        st.rerun()

    def _trigger_audio_alarm(self):
        alarm_js = """
        <script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        function playAlarm() {
            const osc1 = ctx.createOscillator(); const osc2 = ctx.createOscillator(); const gain = ctx.createGain();
            osc1.connect(gain); osc2.connect(gain); gain.connect(ctx.destination);
            osc1.type = "square"; osc2.type = "square";
            osc1.frequency.value = 853; osc2.frequency.value = 960; 
            gain.gain.value = 0.15; 
            osc1.start(); osc2.start(); setTimeout(() => { osc1.stop(); osc2.stop(); }, 2000); 
        }
        playAlarm();
        </script>
        """
        components.html(alarm_js, height=0)

    def _render_shock_screen(self):
        self._trigger_audio_alarm()
        placeholder = st.empty()
        with placeholder.container():
            st.markdown(f"""
            <div class="alert-box">
                <div class="alert-title">⚠ CRITICAL INFRASTRUCTURE FAILURE ⚠</div>
                <div class="alert-title">{st.session_state.active_hazard.upper()} DETECTED</div>
                <div class="alert-gps">IMPACT COORDINATES: {st.session_state.hazard_gps}</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(3.5)
        st.session_state.grid_state = "MITIGATION_ANIMATION"
        st.rerun()

    def _render_dashboard_frame(self, progress=1.0, mode="NORMAL"):
        """Progress 0.0 = CRASHED, 1.0 = FULLY RESTORED"""
        
        # Base/Restored values
        base_freq = 60.0
        base_mw = 4250.0
        base_kirchhoff = 1.2
        
        # Crashed values
        crash_freq = 58.2
        crash_mw = 3100.0
        crash_kirchhoff = 3.5
        
        # Interpolate based on progress
        current_freq = crash_freq + ((base_freq - crash_freq) * progress) + random.uniform(-0.02, 0.02)
        current_mw = crash_mw + ((base_mw - crash_mw) * progress) + random.uniform(-10, 10)
        current_k = crash_kirchhoff + ((base_kirchhoff - crash_kirchhoff) * progress) + random.uniform(-0.05, 0.05)

        cpu = psutil.cpu_percent() if mode == "NORMAL" else 95.0 + random.uniform(-2, 2)
        ram = psutil.virtual_memory().percent
        sub_status = "100% ONLINE" if progress > 0.8 else "88% ONLINE (SECTOR BREACH)"
        sub_color = "normal" if progress > 0.8 else "inverse"

        col1, col2, col3, col4 = st.columns([0.8, 1.2, 1.2, 1.1])

        with col1:
            st.markdown("#### 🖥️ BARE-METAL")
            st.metric(label="Live CPU Load", value=f"{cpu:.1f}%", delta="Hardware")
            st.metric(label="Physical RAM", value=f"{ram}%", delta="Hardware")
            st.metric(label="Substation Net", value=sub_status, delta="Status", delta_color=sub_color)

        with col2:
            st.markdown("#### ⚡ SENSOR CORE")
            gauge_k = self._create_gauge("Kirchhoff Vector", current_k, 0, 5, 0.5, 1.8, "A")
            st.plotly_chart(gauge_k, use_container_width=True, config={'displayModeBar': False})

        with col3:
            st.markdown("#### 🌐 OKLAHOMA GRID")
            gauge_f = self._create_gauge("Grid Frequency", current_freq, 55, 65, 59.5, 60.5, "Hz")
            st.plotly_chart(gauge_f, use_container_width=True, config={'displayModeBar': False})
            
            gauge_mw = self._create_gauge("Active MW Load", current_mw, 0, 5000, 3800, 4800, "MW")
            st.plotly_chart(gauge_mw, use_container_width=True, config={'displayModeBar': False})

        with col4:
            st.markdown("#### 🚨 THREAT SIMULATOR")
            if st.button("🚗 Vehicle Strike", use_container_width=True):
                self._trigger_hazard("Vehicle Strike", "LAT: 35.8421° N, LON: -97.0384° W (RT 66)", ">> SENSOR TRIP: Distribution pole severed.\n>> ACTION: Isolating line. Rerouting via automated switches.\n>> STATUS: Power restored to 94% of affected block.")
            if st.button("🌪️ F5 Tornado", use_container_width=True):
                self._trigger_hazard("F5 Tornado Strike", "LAT: 35.3395° N, LON: -97.4867° W (MOORE)", ">> SENSOR TRIP: Massive transmission failure in Sector 4.\n>> ACTION: Air-gapping Sector 4.\n>> ACTION: Backfeeding 400MW to hospitals.\n>> STATUS: Grid restabilized.")
            if st.button("💻 SCADA Breach", use_container_width=True):
                self._trigger_hazard("State Cyber Breach", "LAT: 35.4676° N, LON: -97.5164° W (OKC)", ">> SENSOR TRIP: Unauthorized breaker actuation attempt.\n>> ACTION: Iron Dome deployed. Node air-gapped.\n>> STATUS: Intrusion neutralized.")
            
            if mode != "NORMAL":
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✅ CLEAR HAZARD", use_container_width=True, type="primary"):
                    st.session_state.grid_state = "NORMAL"
                    st.rerun()

        if mode != "NORMAL":
            st.markdown("#### 👑 EBONY AI: AUTONOMOUS MITIGATION TERMINAL")
            st.markdown(f'<div class="ebony-terminal">> INITIATING SOVEREIGN RESPONSE...<br>{st.session_state.mitigation_log}</div>', unsafe_allow_html=True)

    def render_cockpit(self):
        self._inject_css()
        self._render_header()
        
        if st.session_state.grid_state == "SHOCK":
            self._render_shock_screen()
        elif st.session_state.grid_state == "MITIGATION_ANIMATION":
            # Live Recovery Animation Loop
            ui_placeholder = st.empty()
            steps = 15
            for i in range(steps + 1):
                progress = i / float(steps)
                with ui_placeholder.container():
                    self._render_dashboard_frame(progress=progress, mode="RECOVERY")
                time.sleep(0.3) # Wait between frames to animate the needle
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
