# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Full Telemetry & Simulator Integration
Authority: CEO Jeffery Humphrey (Level 5 Authority)
"""
import streamlit as st
import streamlit.components.v1 as components
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
        """Creates a real local file that physical sensors will push data into."""
        if not self.telemetry_vault.parent.exists():
            self.telemetry_vault.parent.mkdir(parents=True, exist_ok=True)
        if not self.telemetry_vault.exists():
            initial_state = {
                "kirchhoff_current": 1.205,
                "optical_gli": 0.210,
                "matrix_throughput": 889
            }
            with open(self.telemetry_vault, "w") as f:
                json.dump(initial_state, f)

    def _read_live_sensors(self):
        """Reads the actual sensor data from the local vault."""
        try:
            with open(self.telemetry_vault, "r") as f:
                return json.load(f)
        except:
            return {"kirchhoff_current": 0.0, "optical_gli": 0.0, "matrix_throughput": 0}

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
            osc1.frequency.value = 853; 
            osc2.frequency.value = 960; 
            gain.gain.value = 0.15; 
            osc1.start();
            osc2.start();
            setTimeout(() => { osc1.stop(); osc2.stop(); }, 2000); 
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
        st.session_state.grid_state = "MITIGATION"
        st.rerun()

    def _render_dashboard(self, mode="NORMAL"):
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('C:\\').percent
        sensors = self._read_live_sensors()
        
        if mode == "NORMAL":
            freq = f"{random.uniform(59.98, 60.02):.2f} Hz"
            freq_delta = "Stable"
            mw_load = f"{random.uniform(4200, 4300):.0f} MW"
            mw_delta = "Nominal"
            sub_status = "100% ONLINE"
            sub_delta = "All Sectors Secure"
            sub_color = "normal"
            
            k_val = f"{sensors.get('kirchhoff_current', 1.205):.3f} A"
            k_delta = "Live Stream"
            gli_val = f"{sensors.get('optical_gli', 0.210):.3f}"
            gli_delta = "Live Stream"
            tp_val = f"{sensors.get('matrix_throughput', 889)} Mbps"
            tp_delta = "Live Stream"
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
            
            k_val = f"{sensors.get('kirchhoff_current', 1.205) * 2.4:.3f} A"
            k_delta = "SPIKE (OVERLOAD)"
            gli_val = f"{sensors.get('optical_gli', 0.210) * 0.4:.3f}"
            gli_delta = "DEGRADED"
            tp_val = f"{sensors.get('matrix_throughput', 889) + 400} Mbps"
            tp_delta = "DATA FLOOD"

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])

        with col1:
            st.markdown("#### 🖥️ BARE-METAL")
            st.metric(label="Live CPU Load", value=f"{cpu}%", delta="Hardware Monitored")
            st.metric(label="Physical RAM", value=f"{ram}%", delta="Hardware Monitored")
            st.metric(label="C: Drive Capacity", value=f"{disk}%", delta="Hardware Monitored")

        with col2:
            st.markdown("#### ⚡ SENSOR CORE")
            st.metric(label="Kirchhoff Vector", value=k_val, delta=k_delta, delta_color="normal" if mode=="NORMAL" else "inverse")
            st.metric(label="Optical GLI", value=gli_val, delta=gli_delta, delta_color="normal" if mode=="NORMAL" else "inverse")
            st.metric(label="Matrix Throughput", value=tp_val, delta=tp_delta, delta_color="normal" if mode=="NORMAL" else "inverse")

        with col3:
            st.markdown("#### 🌐 OKLAHOMA GRID")
            st.metric(label="Grid Frequency", value=freq, delta=freq_delta, delta_color="normal" if mode=="NORMAL" else "inverse")
            st.metric(label="Active MW Load", value=mw_load, delta=mw_delta, delta_color="normal" if mode=="NORMAL" else "inverse")
            st.metric(label="Substation Integrity", value=sub_status, delta=sub_delta, delta_color=sub_color)

        with col4:
            st.markdown("#### 🚨 THREAT SIMULATOR")
            if st.button("🚗 Vehicle Strike", use_container_width=True):
                self._trigger_hazard("Vehicle Strike", "LAT: 35.8421° N, LON: -97.0384° W (RT 66)", ">> SENSOR TRIP: Distribution pole severed.\n>> ACTION: Isolating line. Rerouting via automated switches.\n>> STATUS: Power restored to 94% of affected block in 1.2s.")
            if st.button("🌪️ F5 Tornado", use_container_width=True):
                self._trigger_hazard("F5 Tornado Strike", "LAT: 35.3395° N, LON: -97.4867° W (MOORE)", ">> SENSOR TRIP: Massive transmission failure in Sector 4.\n>> ACTION: Air-gapping Sector 4. Backfeeding 400MW to hospitals.\n>> STATUS: Grid restabilized. Casualties minimized.")
            if st.button("💻 SCADA Breach", use_container_width=True):
                self._trigger_hazard("State Cyber Breach", "LAT: 35.4676° N, LON: -97.5164° W (OKC)", ">> SENSOR TRIP: Unauthorized breaker actuation attempt.\n>> ACTION: Iron Dome deployed. Node air-gapped. Malware hunted.\n>> STATUS: Intrusion neutralized. Zero loss of load.")
            if st.button("❄️ Freeze-Off", use_container_width=True):
                self._trigger_hazard("Generation Shortfall", "STATEWIDE ALERT", ">> SENSOR TRIP: Natural gas freeze. -1200MW generation loss.\n>> ACTION: Initiating load shedding. Purchasing SPP reserve.\n>> STATUS: Grid collapse averted. Blackouts optimized.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if mode == "MITIGATION":
                if st.button("✅ CLEAR HAZARD", use_container_width=True, type="primary"):
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
