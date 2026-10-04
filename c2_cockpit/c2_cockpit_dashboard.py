# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Kinetic Threat Simulator (Audio Enhanced)
Authority: CEO Jeffery Humphrey (Level 5 Authority)
"""
import streamlit as st
import streamlit.components.v1 as components
import psutil
import time
import random
from pathlib import Path

class MasterCockpit:
    def __init__(self):
        self.ceo_name = "Jeffery Humphrey"
        self.clearance = "Level 5 Sovereign"
        self._init_session_state()

    def _init_session_state(self):
        if "grid_state" not in st.session_state:
            st.session_state.grid_state = "NORMAL" # NORMAL, SHOCK, MITIGATION
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
        
        .c2-header {
            background: #090e17;
            border: 1px solid #1e293b;
            border-left: 4px solid #00f3ff;
            padding: 10px 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'JetBrains Mono', monospace;
        }
        .c2-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 18px;
            color: #f8fafc;
            margin: 0;
            letter-spacing: 2px;
        }
        .c2-badge {
            color: #00f3ff;
            font-size: 12px;
            font-weight: 700;
        }
        
        /* Flashing Red Alert */
        @keyframes flash {
            0% { opacity: 1; text-shadow: 0 0 20px #ff0000; }
            50% { opacity: 0.3; text-shadow: none; }
            100% { opacity: 1; text-shadow: 0 0 20px #ff0000; }
        }
        .alert-box {
            background: #1a0505;
            border: 2px solid #ff0000;
            padding: 40px;
            text-align: center;
            margin-top: 50px;
            border-radius: 5px;
            animation: flash 1s infinite;
        }
        .alert-title {
            color: #ff0000;
            font-family: 'Orbitron', sans-serif;
            font-size: 32px;
            font-weight: 900;
            margin-bottom: 10px;
        }
        .alert-gps {
            color: #f8fafc;
            font-family: 'JetBrains Mono', monospace;
            font-size: 20px;
            letter-spacing: 2px;
        }
        
        /* Terminal */
        .ebony-terminal {
            background: #000000;
            border: 1px solid #00f3ff;
            padding: 15px;
            color: #00f3ff;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            height: 150px;
            overflow-y: auto;
        }
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

    def _trigger_hazard(self, hazard_name, gps, log_msg):
        st.session_state.active_hazard = hazard_name
        st.session_state.hazard_gps = gps
        st.session_state.mitigation_log = log_msg
        st.session_state.grid_state = "SHOCK"
        st.rerun()

    def _trigger_audio_alarm(self):
        """Synthesizes a bare-metal dual-tone SCADA alarm."""
        alarm_js = """
        <script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        function playAlarm() {
            const osc1 = ctx.createOscillator();
            const osc2 = ctx.createOscillator();
            const gain = ctx.createGain();
            osc1.connect(gain);
            osc2.connect(gain);
            gain.connect(ctx.destination);
            osc1.type = "square";
            osc2.type = "square";
            osc1.frequency.value = 853; // EAS Tone 1
            osc2.frequency.value = 960; // EAS Tone 2
            gain.gain.value = 0.15; // Volume
            osc1.start();
            osc2.start();
            setTimeout(() => { osc1.stop(); osc2.stop(); }, 2000); // 2-second klaxon
        }
        playAlarm();
        </script>
        """
        components.html(alarm_js, height=0)

    def _render_shock_screen(self):
        """Phase 2: The 3-Second Shock and Awe + Audio Alarm"""
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
        
        time.sleep(3.5) # Force the room to watch the red alert and hear the klaxon
        
        st.session_state.grid_state = "MITIGATION"
        st.rerun()

    def _render_dashboard(self, mode="NORMAL"):
        """Phase 1 & 3: Standard and Mitigation Dashboard"""
        
        if mode == "NORMAL":
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory().percent
            freq = f"{random.uniform(59.98, 60.02):.2f} Hz"
            freq_delta = "Stable"
            mw_load = f"{random.uniform(4200, 4300):.0f} MW"
            mw_delta = "Nominal"
            sub_status = "100% ONLINE"
            sub_delta = "All Sectors Secure"
            sub_color = "normal"
        else:
            cpu = 98.5
            ram = psutil.virtual_memory().percent + 15
            freq = f"{random.uniform(58.10, 58.90):.2f} Hz"
            freq_delta = "-1.8 Hz (CRITICAL DROP)"
            mw_load = f"{random.uniform(3100, 3200):.0f} MW"
            mw_delta = "-1100 MW (LOSS OF LOAD)"
            sub_status = "88% ONLINE"
            sub_delta = "SECTOR BREACH DETECTED"
            sub_color = "inverse"

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown("#### 🖥️ BARE-METAL C2 NODE")
            st.metric(label="Live CPU Core Load", value=f"{cpu}%", delta="Hardware Monitored")
            st.metric(label="Physical Memory (RAM)", value=f"{ram}%", delta="Hardware Monitored")

        with col2:
            st.markdown("#### ⚡ OKLAHOMA GRID STATUS")
            st.metric(label="Grid Frequency Target", value=freq, delta=freq_delta, delta_color="normal" if mode=="NORMAL" else "inverse")
            st.metric(label="Active State MW Load", value=mw_load, delta=mw_delta, delta_color="normal" if mode=="NORMAL" else "inverse")
            st.metric(label="Substation Integrity", value=sub_status, delta=sub_delta, delta_color=sub_color)

        with col3:
            st.markdown("#### 🚨 KINETIC THREAT SIMULATOR")
            if st.button("🚗 Vehicle Strike (Powerline)", use_container_width=True):
                self._trigger_hazard("Vehicle Strike", "LAT: 35.8421° N, LON: -97.0384° W (RURAL RT 66)", ">> SENSOR TRIP: Distribution pole severed.\n>> ACTION: Isolating line. Rerouting via automated feeder switches.\n>> STATUS: Power restored to 94% of affected block in 1.2s.")
            if st.button("🌪️ F5 Tornado Strike", use_container_width=True):
                self._trigger_hazard("F5 Tornado Strike", "LAT: 35.3395° N, LON: -97.4867° W (MOORE, OK)", ">> SENSOR TRIP: Massive transmission failure in Sector 4.\n>> ACTION: Air-gapping Sector 4. Backfeeding 400MW to local hospitals.\n>> STATUS: Grid restabilized. Casualties minimized.")
            if st.button("💻 SCADA Cyber Breach", use_container_width=True):
                self._trigger_hazard("State-Sponsored Cyber Breach", "LAT: 35.4676° N, LON: -97.5164° W (OKC HUB)", ">> SENSOR TRIP: Unauthorized breaker actuation attempt.\n>> ACTION: Iron Dome deployed. Node air-gapped. Malware hunted.\n>> STATUS: Intrusion neutralized. Zero loss of load.")
            if st.button("❄️ Winter Freeze-Off", use_container_width=True):
                self._trigger_hazard("Generation Shortfall", "STATEWIDE ALERT", ">> SENSOR TRIP: Natural gas line freeze. -1200MW generation loss.\n>> ACTION: Initiating micro-load shedding. Purchasing SPP reserve power.\n>> STATUS: Total grid collapse averted. Rolling blackouts optimized.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if mode == "MITIGATION":
                if st.button("✅ CLEAR HAZARD & RESET", use_container_width=True, type="primary"):
                    st.session_state.grid_state = "NORMAL"
                    st.rerun()

        if mode == "MITIGATION":
            st.markdown("#### 👑 EBONY AI: AUTONOMOUS MITIGATION TERMINAL")
            st.markdown(f'<div class="ebony-terminal">> INITIATING SOVEREIGN RESPONSE...<br>{st.session_state.mitigation_log}</div>', unsafe_allow_html=True)

    def render_cockpit(self):
        self._inject_css()
        self._render_header()
        
        if st.session_state.grid_state == "SHOCK":
            self._render_shock_screen()
        elif st.session_state.grid_state == "MITIGATION":
            self._render_dashboard(mode="MITIGATION")
        else:
            self._render_dashboard(mode="NORMAL")

# === EXPORTED RENDER HOOK FOR MAIN DISPATCHER ===
def render():
    cockpit = MasterCockpit()
    cockpit.render_cockpit()
