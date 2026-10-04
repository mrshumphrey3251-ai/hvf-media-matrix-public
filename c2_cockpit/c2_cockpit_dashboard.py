# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - SCADA Topological Interface
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

        # Oklahoma Grid Coordinates for SCADA Map
        self.nodes = {
            "Enid Node": (-1.5, 1.5),
            "Tulsa Hub": (1.5, 1.5),
            "OKC Master Hub": (0, 0),
            "Moore Sub": (0, -1.0),
            "Lawton Node": (-1.5, -1.5),
            "McAlester Sub": (1.5, -1.5)
        }

    def _ensure_telemetry_file(self):
        if not self.telemetry_vault.parent.exists():
            self.telemetry_vault.parent.mkdir(parents=True, exist_ok=True)
        if not self.telemetry_vault.exists():
            initial_state = {"kirchhoff_current": 1.205, "optical_gli": 0.210, "matrix_throughput": 889}
            with open(self.telemetry_vault, "w") as f:
                json.dump(initial_state, f)

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
        div[data-testid="metric-container"] { background: #090e17; border: 1px solid #1e293b; padding: 10px; border-radius: 4px; }
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

    def _build_scada_map(self, mode, progress):
        """Generates the single-line topological SCADA network map."""
        hazard = st.session_state.active_hazard
        
        # Base Edges
        standard_edges = [
            ("OKC Master Hub", "Enid Node"), ("OKC Master Hub", "Tulsa Hub"),
            ("OKC Master Hub", "Moore Sub"), ("OKC Master Hub", "Lawton Node"),
            ("Tulsa Hub", "McAlester Sub")
        ]
        
        red_edges = []
        green_edges = []
        offline_nodes = []

        # Hazard Topological Modifications
        if mode in ["SHOCK", "RECOVERY", "RESTORED"] and hazard:
            if "Tornado" in hazard:
                standard_edges.remove(("OKC Master Hub", "Moore Sub"))
                if mode == "SHOCK" or progress < 0.5:
                    red_edges.append(("OKC Master Hub", "Moore Sub"))
                    offline_nodes.append("Moore Sub")
                if mode in ["RECOVERY", "RESTORED"] and progress >= 0.5:
                    green_edges.append(("Lawton Node", "Moore Sub")) # Ebony Reroute
            
            elif "Vehicle" in hazard:
                standard_edges.remove(("OKC Master Hub", "Tulsa Hub"))
                if mode == "SHOCK" or progress < 0.5:
                    red_edges.append(("OKC Master Hub", "Tulsa Hub"))
                if mode in ["RECOVERY", "RESTORED"] and progress >= 0.5:
                    green_edges.append(("Enid Node", "Tulsa Hub")) # Ebony Reroute

            elif "Cyber" in hazard:
                # Isolate OKC Hub
                standard_edges.clear()
                if mode == "SHOCK" or progress < 0.5:
                    offline_nodes.append("OKC Master Hub")
                if mode in ["RECOVERY", "RESTORED"] and progress >= 0.5:
                    # Ebony builds an outer ring to bypass OKC
                    green_edges = [("Enid Node", "Tulsa Hub"), ("Tulsa Hub", "McAlester Sub"), 
                                   ("McAlester Sub", "Lawton Node"), ("Lawton Node", "Enid Node")]

            elif "Freeze" in hazard:
                # Load Shedding
                if ("OKC Master Hub", "Enid Node") in standard_edges: standard_edges.remove(("OKC Master Hub", "Enid Node"))
                if ("Tulsa Hub", "McAlester Sub") in standard_edges: standard_edges.remove(("Tulsa Hub", "McAlester Sub"))
                if mode == "SHOCK" or progress < 0.5:
                    offline_nodes.extend(["Enid Node", "McAlester Sub"])

        # Plotly Figure Setup
        fig = go.Figure()

        # Helper to add lines
        def add_lines(edges, color, width, dash='solid'):
            for edge in edges:
                x0, y0 = self.nodes[edge[0]]; x1, y1 = self.nodes[edge[1]]
                fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines', 
                                         line=dict(color=color, width=width, dash=dash), hoverinfo='none'))

        # Draw Lines
        add_lines(standard_edges, '#00f3ff', 2) # Cyan Standard
        add_lines(red_edges, '#ef4444', 3, 'dot') # Red Flashing Failed
        add_lines(green_edges, '#10b981', 4) # Neon Green Reroutes

        # Draw Nodes
        node_x = []; node_y = []; node_colors = []; node_texts = []
        for name, coords in self.nodes.items():
            node_x.append(coords[0])
            node_y.append(coords[1])
            node_texts.append(name)
            if name in offline_nodes:
                node_colors.append('#ef4444') # Red Offline
            else:
                node_colors.append('#00f3ff') # Cyan Online

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            marker=dict(size=25, color=node_colors, line=dict(width=2, color='#ffffff')),
            text=node_texts, textposition="top center",
            textfont=dict(color='#f8fafc', family="JetBrains Mono", size=12),
            hoverinfo='text'
        ))

        fig.update_layout(
            title=dict(text="SOVEREIGN TOPOLOGICAL GRID VIEW", font=dict(color="#64748b", family="JetBrains Mono")),
            plot_bgcolor='#030712', paper_bgcolor='#030712',
            showlegend=False, margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            height=400
        )
        return fig

    def _render_dashboard_frame(self, progress=1.0, mode="NORMAL"):
        cpu = psutil.cpu_percent() if mode == "NORMAL" else 98.5 + random.uniform(-1, 1)
        freq = 60.00 if mode in ["NORMAL", "RESTORED"] else 58.2 + (1.8 * progress)
        mw_load = 4250 if mode in ["NORMAL", "RESTORED"] else 3100 + (1150 * progress)
        sub_status = "100% SECURE" if mode in ["NORMAL", "RESTORED"] else "SECTOR BREACH"
        sub_color = "normal" if mode in ["NORMAL", "RESTORED"] else "inverse"

        if mode in ["RECOVERY", "RESTORED"]:
            st.markdown("<h3 style='color:#10b981; text-align:center; font-family:Orbitron;'>🟢 EBONY INITIATED: TOPOLOGICAL REROUTING IN PROGRESS</h3>", unsafe_allow_html=True)

        col_metrics, col_map, col_controls = st.columns([1, 2, 1])

        with col_metrics:
            st.markdown("#### ⚙️ TELEMETRY")
            st.metric(label="Live CPU Load", value=f"{cpu:.1f}%")
            st.metric(label="Grid Frequency", value=f"{freq:.2f} Hz", delta="Target: 60Hz", delta_color="normal" if freq>59.5 else "inverse")
            st.metric(label="Active Load", value=f"{mw_load:.0f} MW", delta=sub_status, delta_color=sub_color)

        with col_map:
            scada_map = self._build_scada_map(mode, progress)
            st.plotly_chart(scada_map, use_container_width=True, config={'displayModeBar': False}, key=f"map_{progress}")

        with col_controls:
            st.markdown("#### 🚨 THREAT INJECTOR")
            if mode == "NORMAL":
                log_veh = ">> EVENT: 12kV Line Severed on RT 66.\n>> EBONY ACTION: Isolating Tulsa Hub feed. Rerouting via Enid Node switches.\n>> GRID STATUS: Load restored. Zero cascade failure.\n>> ---------------------------------------------------\n>> HUMAN ACTION:\n>> 1. Dispatch Line Crew.\n>> 2. Schedule pole replacement."
                if st.button("🚗 Vehicle Strike", key="btn_veh", use_container_width=True):
                    self._trigger_hazard("Vehicle Strike", "LAT: 35.8421° N, LON: -97.0384° W (RT 66)", log_veh)
                
                log_tor = ">> EVENT: F5 Tornado - Moore Substation offline.\n>> EBONY ACTION: Severing primary OKC feed. Backfeeding 400MW from Lawton Node.\n>> GRID STATUS: Grid restabilized. Hospitals powered.\n>> ---------------------------------------------------\n>> HUMAN ACTION:\n>> 1. Dispatch Heavy Infrastructure Units.\n>> 2. Coordinate FEMA logistics."
                if st.button("🌪️ F5 Tornado", key="btn_tor", use_container_width=True):
                    self._trigger_hazard("F5 Tornado Strike", "LAT: 35.3395° N, LON: -97.4867° W (MOORE)", log_tor)
                
                log_cyb = ">> EVENT: SCADA Breach at OKC Master Hub.\n>> EBONY ACTION: Air-gapping OKC Hub. Constructing decentralized outer ring.\n>> GRID STATUS: Intrusion neutralized. Power flow maintained.\n>> ---------------------------------------------------\n>> HUMAN ACTION:\n>> 1. Initiate forensic audit of OKC firewalls.\n>> 2. Rotate crypto keys."
                if st.button("💻 SCADA Breach", key="btn_cyb", use_container_width=True):
                    self._trigger_hazard("State Cyber Breach", "LAT: 35.4676° N, LON: -97.5164° W (OKC)", log_cyb)
                
                log_frz = ">> EVENT: Natural gas freeze. -1200MW generation loss.\n>> EBONY ACTION: Shedding peripheral nodes (Enid, McAlester). Preserving core triangle.\n>> GRID STATUS: Total grid collapse averted.\n>> ---------------------------------------------------\n>> HUMAN ACTION:\n>> 1. Issue emergency conservation alerts.\n>> 2. Winterize wellheads."
                if st.button("❄️ Freeze-Off", key="btn_frz", use_container_width=True):
                    self._trigger_hazard("Generation Shortfall", "STATEWIDE ALERT", log_frz)
            else:
                st.markdown("##### ⚠️ CRISIS LOCKDOWN")
                if st.button("✅ ACKNOWLEDGE & RESET", key=f"btn_reset_{progress}", use_container_width=True, type="primary"):
                    st.session_state.grid_state = "NORMAL"
                    st.session_state.alarm_active = False
                    st.rerun()

        if mode in ["RECOVERY", "RESTORED"]:
            typed_length = int(len(st.session_state.mitigation_log) * progress)
            display_text = st.session_state.mitigation_log[:typed_length]
            st.markdown(f'''
            <div class="ebony-modal">
                <h3 style="color: #00f3ff; font-family: 'Orbitron', sans-serif; margin-top: 0;">👑 EBONY AUTONOMOUS MITIGATION LOG</h3>
                <p style="color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-size: 14px; white-space: pre-wrap;">{display_text}</p>
            </div>
            ''', unsafe_allow_html=True)

    def render_cockpit(self):
        self._inject_css()
        self._manage_audio_alarm()
        self._render_header()
        
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
