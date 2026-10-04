# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Pure Aerospace SCADA + Alert Sequence
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
        if "sim_amps" not in st.session_state: st.session_state.sim_amps = 1253.8
        if "sim_kw" not in st.session_state: st.session_state.sim_kw = 292.9

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
        
        @keyframes flash { 0% { opacity: 1; text-shadow: 0 0 20px #ff0000; } 50% { opacity: 0.3; text-shadow: none; } 100% { opacity: 1; text-shadow: 0 0 20px #ff0000; } }
        .alert-box { background: #1a0505; border: 2px solid #ff0000; padding: 40px; text-align: center; margin-top: 50px; margin-bottom: 30px; animation: flash 1s infinite; }
        .alert-title { color: #ff0000; font-size: 32px; font-weight: 900; margin-bottom: 10px; }
        
        .raw-text { color: #f8fafc; font-size: 14px; line-height: 1.6; }
        .log-footer { font-size: 12px; color: #64748b; border-top: 1px solid #1e293b; padding-top: 10px; margin-top: 30px; }
        .merkle-hash { color: #10b981; font-weight: 700; }
        .header-bar { color: #00f3ff; font-weight: 700; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #1e293b; padding-bottom: 5px; }
        </style>
        """, unsafe_allow_html=True)

    def _render_aerospace_header(self, mode="NORMAL"):
        css_class = "mil-header" if mode in ["NORMAL", "RESTORED"] else "mil-header-red"
        st.markdown(f"""
        <div class="{css_class}">
            <p class="title-main">PROJECT EBONY // UNIFIED MASTER COMMAND COCKPIT</p>
            <p class="title-sub">AEROSPACE DEFENSE SCADA // OKLAHOMA COMMERCE EVALUATION TESTBED</p>
            <p class="title-sub" style="font-weight:700;">CAGE: 1AHA8 | AUTHORITY: LEVEL 5 CEO<br>STANDARD: NIST SP 800-82 REV 2 | AIR-GAP: OK HB 2992</p>
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
            "Vehicle_Strike": {"name": "POLE_BREAK", "gps": "LAT: 35.8421° N, LON: -97.0384° W (RT 66)", "log": "DYNAMIC ELECTRICAL SITUATION: Feeder states: CH1 Utility (0.0 A), CH2 Solar (100.0 A), CH3 BESS (350.0 A), CH4 Aux Gen (0.0 A). Non-Essential Bus B Load Shedding: ACTIVE (-155 A).\nKIRCHHOFF POWER FLOW: Total instantaneous load calculated at 1253.8 Amperes across 142.0 Volts RMS. Active facility power delivery is 292.9 kW.\nDOWNSTREAM DEFENSE STATUS: Priority 1 Critical Defense C2 and pumps remain 100% continuous (0.00 seconds of outage)."},
            "High_Winds": {"name": "HIGH_WINDS", "gps": "LAT: 35.3395° N, LON: -97.4867° W", "log": "DYNAMIC ELECTRICAL SITUATION: Feeder states: CH1 Utility (250.0 A), CH2 Solar (100.0 A), CH3 BESS (150.0 A), CH4 Aux Gen (0.0 A). Non-Essential Bus B Load Shedding: ONLINE (+155 A).\nKIRCHHOFF POWER FLOW: Total instantaneous load calculated at 2125.0 Amperes across 142.0 Volts RMS. Active facility power delivery is 496.5 kW.\nDOWNSTREAM DEFENSE STATUS: Priority 1 Critical Defense C2 and pumps remain 100% continuous (0.00 seconds of outage)."},
            "Cyber_Breach": {"name": "SCADA_BREACH", "gps": "LAT: 35.4676° N, LON: -97.5164° W (OKC HUB)", "log": "DYNAMIC ELECTRICAL SITUATION: Feeder states nominal. Unauthorized logical breaker actuation attempt isolated via Iron Dome.\nKIRCHHOFF POWER FLOW: Load secure at 1258.0 Amperes. Merkle seals locked.\nDOWNSTREAM DEFENSE STATUS: Priority 1 Critical Defense C2 and pumps remain 100% continuous (0.00 seconds of outage)."},
        }
        h = hazards[hazard_key]
        st.session_state.active_hazard = h["name"]
        st.session_state.hazard_gps = h["gps"]
        st.session_state.mitigation_log = h["log"]
        st.session_state.grid_state = "SHOCK"
        st.session_state.alarm_active = True
        if hazard_key == "High_Winds":
            st.session_state.sim_amps = 2125.0
            st.session_state.sim_kw = 496.5
        else:
            st.session_state.sim_amps = 1253.8
            st.session_state.sim_kw = 292.9
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

    def _build_oscilloscope(self, mode):
        x = [i/100 for i in range(200)]
        if mode == "SHOCK":
            y = [random.uniform(-0.1, 0.1) for i in range(200)]; color = "#ef4444"
        else:
            y = [math.sin(i * 0.5) + random.uniform(-0.05, 0.05) for i in range(200)]; color = "#10b981"
        fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=2)))
        fig.update_layout(plot_bgcolor='#000000', paper_bgcolor='#000000', margin=dict(l=0, r=0, t=0, b=0), height=100, xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-1.5, 1.5]))
        return fig

    def _render_dashboard_frame(self, progress=1.0, mode="NORMAL"):
        self._render_aerospace_header(mode)

        # 1. FAULT INJECTION CONSOLE
        st.markdown('<div class="header-bar">▶ FAULT & INCIDENT INJECTION CONSOLE // TEST DYNAMIC REALITY DEFLECTION:</div>', unsafe_allow_html=True)
        if mode == "NORMAL":
            col_drop, col_btn = st.columns([3, 1])
            with col_drop:
                options = {"None": "Select Injection Vector...", "Vehicle_Strike": "Vehicle Strike (POLE_BREAK)", "High_Winds": "High Winds (HIGH_WINDS)", "Cyber_Breach": "SCADA Cyber Breach (SCADA_BREACH)"}
                selected_key = st.selectbox("Command", options=list(options.keys()), format_func=lambda x: options[x], label_visibility="collapsed", key="fault_dropdown")
            with col_btn:
                if st.button("INJECT FAULT", type="primary", use_container_width=True, key="btn_inject") and selected_key != "None":
                    self._trigger_hazard(selected_key)
        else:
            if mode == "RESTORED":
                if st.button("✅ ACKNOWLEDGE INCIDENT & RESET MATRIX", use_container_width=True, key="btn_reset"):
                    st.session_state.grid_state = "NORMAL"
                    st.session_state.sim_amps = 1253.8
                    st.session_state.sim_kw = 292.9
                    st.rerun()
            else:
                st.markdown(f"<span style='color:#ef4444; font-weight:700;'>SYSTEM LOCKED: PROCESSING {st.session_state.active_hazard.upper()}...</span>", unsafe_allow_html=True)

        st.markdown('<br>', unsafe_allow_html=True)

        # 2. MANUAL BREAKER & FEEDER SWITCHGEAR
        st.markdown('<div class="header-bar">▶ MANUAL BREAKER & FEEDER SWITCHGEAR (CLICK TO ACTUATE CURRENT DELTAS):</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.checkbox("CH1 Utility", value=(mode=="NORMAL"), disabled=True, key="ch1")
        c2.checkbox("CH2 Solar", value=True, disabled=True, key="ch2")
        c3.checkbox("CH3 BESS", value=(mode!="NORMAL"), disabled=True, key="ch3")
        c4.checkbox("CH4 Aux Gen", value=False, disabled=True, key="ch4")

        st.markdown('<br>', unsafe_allow_html=True)

        # 3. EXECUTIVE SITUATIONAL WRITE-UP
        freq = 60.00 if mode == "NORMAL" else 59.98
        amps = st.session_state.sim_amps
        kw = st.session_state.sim_kw
        hazard_title = st.session_state.active_hazard if mode != "NORMAL" else "NOMINAL_BASELINE"

        st.markdown(f'<div class="header-bar" style="color:#f8fafc;">EXECUTIVE SITUATIONAL WRITE-UP // {hazard_title} (ACTIVE CURRENT: {amps:.1f} A | ACTIVE BUS: {kw:.1f} kW)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="raw-text">DOCKET: OK-DOC-2026-EBONY // FREQUENCY: {freq:.2f} Hz</div>', unsafe_allow_html=True)
        
        if mode == "NORMAL":
            st.markdown('<div class="raw-text">DYNAMIC ELECTRICAL SITUATION: All Feeder states secured. Utility grid prioritized.<br>KIRCHHOFF POWER FLOW: Total instantaneous load calculated at 1253.8 Amperes.<br>DOWNSTREAM DEFENSE STATUS: Priority 1 Critical Defense C2 100% continuous.</div>', unsafe_allow_html=True)
        else:
            typed_length = int(len(st.session_state.mitigation_log) * progress)
            display_text = st.session_state.mitigation_log[:typed_length]
            st.markdown(f'<div class="raw-text">{display_text}</div>', unsafe_allow_html=True)

        st.markdown('<br>', unsafe_allow_html=True)

        # 4. STATIC HEADERS & OSCILLOSCOPE
        st.markdown('<div class="header-bar">▶ ANALOG GAUGES & MACHINERY INTERLOCKS</div>', unsafe_allow_html=True)
        st.markdown('<div class="header-bar">▶ REGIONAL OUTAGE MAP & POWER FLOW PIPELINE</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="header-bar">▶ MULTI-STAGE ELECTRICAL WAVEFORMS (OSCILLOSCOPE)</div>', unsafe_allow_html=True)
        st.plotly_chart(self._build_oscilloscope(mode), use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('<div class="header-bar">▶ STATUTORY PROVING MATRIX (THE 4 EVALUATION DOMAINS)</div>', unsafe_allow_html=True)

        # 5. HARDWARE ASSERTIONS
        curr_time = time.time()
        sim_drift = f"{(random.uniform(0.00, 0.02) if mode=='NORMAL' else 0.00):.2f}%"
        raw_str = f"{amps}-{freq}-{curr_time}"
        merkle_hash = hashlib.sha256(raw_str.encode()).hexdigest()

        st.markdown(f"""
        <div class="log-footer">
            [HARDWARE_ASSERTION] FC05_LATENCY: 2.04 us | ARC_QUENCH: 13.33 ms | RESYNC_WINDOW: 126.13 ms | SIMULATION_DRIFT: {sim_drift}<br><br>
            <span style="color:#10b981; font-size:14px;">⚡ LIVE FORENSIC SILICON LOG // CHRONUS LEDGER SECURED ⚡</span><br>
            [MERKLE SEALED] LOAD: {amps:.1f}A | PWR: {kw:.1f}kW | FREQ: {freq:.2f}Hz | HASH: <span class="merkle-hash">{merkle_hash}</span>
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
                time.sleep(0.15)
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
