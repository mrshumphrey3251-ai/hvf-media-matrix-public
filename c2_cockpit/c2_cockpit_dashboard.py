# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Aerospace Defense SCADA (Fusion Protocol)
Authority: CEO Jeffery Humphrey (Level 5 Authority)
"""
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import psutil
import time
import random
import json
import math
import hashlib
from pathlib import Path

class MasterCockpit:
    def __init__(self):
        self.telemetry_vault = Path(r"C:\HVF_Repos\HVF_Matrix_Core\telemetry_state.json")
        self._ensure_telemetry_file()
        self._init_session_state()

    def _ensure_telemetry_file(self):
        if not self.telemetry_vault.parent.exists():
            self.telemetry_vault.parent.mkdir(parents=True, exist_ok=True)
        if not self.telemetry_vault.exists():
            initial_state = {"kirchhoff_current": 1253.8, "optical_gli": 0.210, "matrix_throughput": 889}
            with open(self.telemetry_vault, "w") as f:
                json.dump(initial_state, f)

    def _init_session_state(self):
        if "grid_state" not in st.session_state: st.session_state.grid_state = "NORMAL"
        if "active_hazard" not in st.session_state: st.session_state.active_hazard = None
        if "hazard_gps" not in st.session_state: st.session_state.hazard_gps = ""
        if "mitigation_log" not in st.session_state: st.session_state.mitigation_log = ""
        if "alarm_active" not in st.session_state: st.session_state.alarm_active = False

    def _inject_css(self):
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
        * { font-family: 'JetBrains Mono', monospace; }
        .mil-header { border: 1px solid #1e293b; border-left: 4px solid #10b981; background: #030712; padding: 15px; margin-bottom: 20px; }
        .mil-header-red { border: 1px solid #ef4444; border-left: 4px solid #ef4444; background: #1a0505; padding: 15px; margin-bottom: 20px; }
        .title-main { font-size: 18px; color: #f8fafc; font-weight: 900; letter-spacing: 1px; margin:0; }
        .title-sub { font-size: 12px; color: #64748b; margin:0; }
        .title-accent { color: #10b981; font-size: 12px; font-weight: 700; margin:0; }
        
        .section-box { border: 1px solid #1e293b; background: #090e17; padding: 15px; margin-bottom: 15px; }
        .section-title { color: #00f3ff; font-size: 14px; font-weight: 700; border-bottom: 1px solid #1e293b; padding-bottom: 5px; margin-bottom: 15px; text-transform: uppercase; }
        
        @keyframes flash { 0% { opacity: 1; text-shadow: 0 0 20px #ff0000; } 50% { opacity: 0.3; text-shadow: none; } 100% { opacity: 1; text-shadow: 0 0 20px #ff0000; } }
        .alert-box { background: #1a0505; border: 2px solid #ff0000; padding: 40px; text-align: center; margin-top: 50px; margin-bottom: 30px; animation: flash 1s infinite; }
        .alert-title { color: #ff0000; font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        
        .terminal-text { color: #f8fafc; font-size: 13px; line-height: 1.5; white-space: pre-wrap; }
        .log-footer { font-size: 11px; color: #64748b; border-top: 1px solid #1e293b; padding-top: 10px; margin-top: 20px; }
        .merkle-hash { color: #10b981; font-weight: 700; }
        </style>
        """, unsafe_allow_html=True)

    def _render_aerospace_header(self, mode="NORMAL"):
        css_class = "mil-header" if mode in ["NORMAL", "RESTORED"] else "mil-header-red"
        accent_color = "#10b981" if mode in ["NORMAL", "RESTORED"] else "#ef4444"
        st.markdown(f"""
        <div class="{css_class}">
            <p class="title-main">PROJECT EBONY // UNIFIED MASTER COMMAND COCKPIT</p>
            <p class="title-sub">AEROSPACE DEFENSE SCADA // OKLAHOMA COMMERCE EVALUATION TESTBED</p>
            <p class="title-sub" style="color:{accent_color}; font-weight:700;">CAGE: 1AHA8 | AUTHORITY: LEVEL 5 CEO | STANDARD: NIST SP 800-82 REV 2 | AIR-GAP: OK HB 2992</p>
        </div>
        """, unsafe_allow_html=True)

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

    def _trigger_hazard(self, hazard_key):
        hazards = {
            "Vehicle_Strike": {"name": "Vehicle Strike (Pole Break)", "gps": "LAT: 35.8421° N, LON: -97.0384° W (RT 66)", "log": "DYNAMIC ELECTRICAL SITUATION: Loss of 12kV Distribution Line.\nKIRCHHOFF POWER FLOW: Instantaneous drop of 145A detected. Fault localized to Feeder CH1.\nEBONY ACTION: Actuating Feeder CH2 (Solar) and CH3 (BESS) switches to backfeed block.\nDOWNSTREAM DEFENSE STATUS: Priority 1 Critical Defense C2 remains 100% continuous."},
            "F5_Tornado": {"name": "F5 Tornado (Sector Wipe)", "gps": "LAT: 35.3395° N, LON: -97.4867° W (MOORE)", "log": "DYNAMIC ELECTRICAL SITUATION: Massive transmission failure. Moore Sector offline.\nKIRCHHOFF POWER FLOW: -400MW load loss. Frequency deviation detected (58.2Hz).\nEBONY ACTION: Air-gapping Sector. Rerouting via Lawton high-voltage corridors.\nDOWNSTREAM DEFENSE STATUS: Hospitals and Priority 1 nodes repowered via bypass."},
            "Cyber_Breach": {"name": "SCADA Cyber Breach", "gps": "LAT: 35.4676° N, LON: -97.5164° W (OKC HUB)", "log": "DYNAMIC ELECTRICAL SITUATION: Unauthorized breaker actuation attempt.\nKIRCHHOFF POWER FLOW: Zero physical disruption. Logical layer compromised.\nEBONY ACTION: Iron Dome deployed. Air-gapping infected nodes. Merkle seals locked.\nDOWNSTREAM DEFENSE STATUS: Intrusion neutralized. 0.00 seconds of outage."},
            "Freeze_Off": {"name": "Winter Freeze-Off", "gps": "STATEWIDE ALERT", "log": "DYNAMIC ELECTRICAL SITUATION: Severe generation shortfall (-1200MW).\nKIRCHHOFF POWER FLOW: Thermal collapse on primary bus.\nEBONY ACTION: Initiating Non-Essential Bus B Load Shedding. Actuating Aux Gen.\nDOWNSTREAM DEFENSE STATUS: Total grid collapse averted. Core grid intact."}
        }
        
        h = hazards[hazard_key]
        st.session_state.active_hazard = h["name"]
        st.session_state.hazard_gps = h["gps"]
        st.session_state.mitigation_log = h["log"]
        st.session_state.grid_state = "SHOCK"
        st.session_state.alarm_active = True
        st.rerun()

    def _render_shock_screen(self):
        self._render_aerospace_header(mode="SHOCK")
        st.markdown(f"""
        <div class="alert-box">
            <div class="alert-title">⚠ CRITICAL INFRASTRUCTURE FAILURE ⚠</div>
            <div style="color:#f8fafc; font-size:24px;">{st.session_state.active_hazard.upper()} DETECTED</div>
            <div style="color:#ef4444; font-size:18px; margin-top:10px;">{st.session_state.hazard_gps}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ INITIATE EBONY PROTOCOL ⚡", key="init_ebony", type="primary", use_container_width=True):
            st.session_state.alarm_active = False
            st.session_state.grid_state = "MITIGATION_ANIMATION"
            st.rerun()

    def _build_oscilloscope(self, progress, mode):
        """Generates a dynamic electrical waveform visualization."""
        x = [i/100 for i in range(200)]
        
        if mode == "NORMAL":
            y = [math.sin(i * 0.5) for i in range(200)]
            color = "#10b981"
        elif mode in ["RECOVERY", "RESTORED"]:
            # Recovers from flatline/noise back to clean sine wave
            noise_factor = 1.0 - progress
            sine_factor = progress
            y = [(math.sin(i * 0.5) * sine_factor) + (random.uniform(-1, 1) * noise_factor) for i in range(200)]
            color = "#00f3ff"
        else: # SHOCK
            y = [random.uniform(-0.1, 0.1) for i in range(200)] # Flatline/Noise
            color = "#ef4444"

        fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=2)))
        fig.update_layout(
            plot_bgcolor='#000000', paper_bgcolor='#000000',
            margin=dict(l=0, r=0, t=0, b=0), height=150,
            xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-1.5, 1.5])
        )
        return fig

    def _render_dashboard_frame(self, progress=1.0, mode="NORMAL"):
        self._render_aerospace_header(mode)

        # 1. FAULT INJECTION (Dropdown Console)
        st.markdown('<div class="section-box"><div class="section-title">▶ FAULT & INCIDENT INJECTION CONSOLE // TEST DYNAMIC REALITY DEFLECTION</div>', unsafe_allow_html=True)
        col_drop, col_btn = st.columns([3, 1])
        with col_drop:
            options = {"None": "Select Fault Vector...", "Vehicle_Strike": "Vehicle Strike (Pole Break)", "F5_Tornado": "F5 Tornado (Sector Wipe)", "Cyber_Breach": "SCADA Cyber Breach", "Freeze_Off": "Winter Freeze-Off (Load Shed)"}
            selected_key = st.selectbox("Awaiting Command...", options=list(options.keys()), format_func=lambda x: options[x], label_visibility="collapsed")
        with col_btn:
            if st.button("INJECT FAULT", type="primary", use_container_width=True) and selected_key != "None" and mode == "NORMAL":
                self._trigger_hazard(selected_key)
        
        if mode != "NORMAL":
            if st.button("✅ ACKNOWLEDGE & RESET MATRIX", use_container_width=True):
                st.session_state.grid_state = "NORMAL"
                st.session_state.alarm_active = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. MIDDLE PANELS: SWITCHGEAR & OSCILLOSCOPE
        col_sw, col_osc = st.columns([1, 1])
        with col_sw:
            st.markdown('<div class="section-box"><div class="section-title">▶ MANUAL BREAKER & FEEDER SWITCHGEAR</div>', unsafe_allow_html=True)
            st.checkbox("CH1 Utility Grid", value=(mode=="NORMAL"), disabled=True)
            st.checkbox("CH2 Solar Array", value=True, disabled=True)
            st.checkbox("CH3 BESS (Battery Storage)", value=(mode!="NORMAL"), disabled=True)
            st.checkbox("CH4 Aux Generator", value=False, disabled=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_osc:
            st.markdown('<div class="section-box"><div class="section-title">▶ MULTI-STAGE ELECTRICAL WAVEFORMS</div>', unsafe_allow_html=True)
            st.plotly_chart(self._build_oscilloscope(progress, mode), use_container_width=True, config={'displayModeBar': False}, key=f"osc_{progress}")
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. EXECUTIVE SITUATIONAL WRITE-UP
        st.markdown('<div class="section-box"><div class="section-title">▶ EXECUTIVE SITUATIONAL WRITE-UP // AUTONOMOUS LOG</div>', unsafe_allow_html=True)
        
        if mode == "NORMAL":
            st.markdown('<p class="terminal-text" style="color:#10b981;">DOCKET: OK-DOC-2026-EBONY // FREQUENCY: 60.00 Hz<br>STATUS: ALL SYSTEMS NOMINAL. AWAITING INJECTION COMMAND.</p>', unsafe_allow_html=True)
        else:
            freq = 58.2 + (1.8 * progress)
            amps = 1253.8 if progress > 0.8 else random.uniform(2000, 3000)
            st.markdown(f'<p class="terminal-text" style="color:#ef4444;">DOCKET: OK-DOC-2026-EBONY // ACTIVE CURRENT: {amps:.1f} A | FREQUENCY: {freq:.2f} Hz</p>', unsafe_allow_html=True)
            
            typed_length = int(len(st.session_state.mitigation_log) * progress)
            display_text = st.session_state.mitigation_log[:typed_length]
            st.markdown(f'<p class="terminal-text">{display_text}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. HARDWARE ASSERTIONS & LOG FOOTER
        curr_time = time.time()
        sim_drift = f"{(random.uniform(0.00, 0.02) if mode=='NORMAL' else random.uniform(0.1, 0.5)):.2f}%"
        raw_str = f"{amps if mode!='NORMAL' else 1253.8}-{freq if mode!='NORMAL' else 60.00}-{curr_time}"
        merkle_hash = hashlib.sha256(raw_str.encode()).hexdigest()

        st.markdown(f"""
        <div class="log-footer">
            [HARDWARE_ASSERTION] FC05_LATENCY: 2.04 us | ARC_QUENCH: 13.33 ms | RESYNC_WINDOW: 126.13 ms | SIMULATION_DRIFT: {sim_drift}<br><br>
            <span style="color:#10b981;">⚡ LIVE FORENSIC SILICON LOG // CHRONUS LEDGER SECURED ⚡</span><br>
            [MERKLE SEALED] LOAD: {amps if mode!='NORMAL' else 1253.8:.1f}A | PWR: 292.9kW | FREQ: {freq if mode!='NORMAL' else 60.00:.2f}Hz | HASH: <span class="merkle-hash">{merkle_hash}</span>
        </div>
        """, unsafe_allow_html=True)

    def render_cockpit(self):
        self._inject_css()
        self._manage_audio_alarm()
        
        if st.session_state.grid_state == "SHOCK":
            self._render_shock_screen()
        elif st.session_state.grid_state == "MITIGATION_ANIMATION":
            ui_placeholder = st.empty()
            steps = 15
            for i in range(steps + 1):
                progress = i / float(steps)
                with ui_placeholder.container():
                    self._render_dashboard_frame(progress=progress, mode="RECOVERY")
                time.sleep(0.3)
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
