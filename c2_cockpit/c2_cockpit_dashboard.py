# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Air-Gapped Cyber-Topological HUD
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
from pathlib import Path

class MasterCockpit:
    def __init__(self):
        self.ceo_name = "Jeffery Humphrey"
        self.clearance = "Level 5 Sovereign"
        self.telemetry_vault = Path(r"C:\HVF_Repos\HVF_Matrix_Core\telemetry_state.json")
        self._ensure_telemetry_file()
        self._init_session_state()
        self._generate_synthetic_cyber_grid()

    def _ensure_telemetry_file(self):
        if not self.telemetry_vault.parent.exists():
            self.telemetry_vault.parent.mkdir(parents=True, exist_ok=True)
        if not self.telemetry_vault.exists():
            initial_state = {"kirchhoff_current": 1.205, "optical_gli": 0.210, "matrix_throughput": 889}
            with open(self.telemetry_vault, "w") as f:
                json.dump(initial_state, f)

    def _init_session_state(self):
        if "grid_state" not in st.session_state: st.session_state.grid_state = "NORMAL"
        if "active_hazard" not in st.session_state: st.session_state.active_hazard = None
        if "hazard_gps" not in st.session_state: st.session_state.hazard_gps = ""
        if "mitigation_log" not in st.session_state: st.session_state.mitigation_log = ""
        if "alarm_active" not in st.session_state: st.session_state.alarm_active = False

    def _generate_synthetic_cyber_grid(self):
        """Generates a highly complex 120-node grid using pure offline X/Y plotting."""
        random.seed(42) # Lock generation
        self.nodes = []
        self.edges = []
        
        # Hub Centers (Y=Lat, X=Lon relative spread)
        hubs = {
            "OKC_Hub": (0, 0, 45),
            "Tulsa_Hub": (1.5, 1.5, 35),
            "Lawton_Node": (-1.5, -1.5, 15),
            "Enid_Node": (1.5, -1.5, 15),
            "Moore_Sector": (-0.5, 0, 10) # Target Zone
        }

        # Generate clustered nodes
        for hub, (y, x, count) in hubs.items():
            for i in range(count):
                n_y = y + random.uniform(-0.3, 0.3)
                n_x = x + random.uniform(-0.3, 0.3)
                self.nodes.append({"id": f"{hub}_{i}", "y": n_y, "x": n_x, "hub": hub})

        # Generate Edges (Lines) based on proximity
        for i, n1 in enumerate(self.nodes):
            connections = 0
            for j, n2 in enumerate(self.nodes):
                if i != j:
                    dist = math.hypot(n1['y'] - n2['y'], n1['x'] - n2['x'])
                    # Micro-connections within cities
                    if dist < 0.2 and connections < 3:
                        self.edges.append((i, j))
                        connections += 1
                    # Long-haul transmission corridors between cities
                    elif dist < 3.0 and random.random() < 0.005: 
                        self.edges.append((i, j))

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

    def _build_cyber_map(self, mode, progress):
        """Generates the massive 120-node offline HUD map."""
        hazard = st.session_state.active_hazard
        
        red_edges = []
        green_edges = []
        offline_nodes = set()
        standard_edges = list(self.edges)

        # Apply Hazard Logic
        if mode in ["SHOCK", "RECOVERY", "RESTORED"] and hazard:
            if "Tornado" in hazard:
                # Devastate the Moore Sector
                for i, node in enumerate(self.nodes):
                    if node['hub'] == "Moore_Sector":
                        if mode == "SHOCK" or progress < 0.5:
                            offline_nodes.add(i)
                edges_to_remove = []
                for edge in standard_edges:
                    if edge[0] in offline_nodes or edge[1] in offline_nodes:
                        edges_to_remove.append(edge)
                        if mode == "SHOCK" or progress < 0.5:
                            red_edges.append(edge)
                for e in edges_to_remove: standard_edges.remove(e)
                
                # Ebony draws a bypass around Moore
                if mode in ["RECOVERY", "RESTORED"] and progress >= 0.5:
                    for i in range(8): green_edges.append((random.randint(0, 44), random.randint(80, 119))) 

            elif "Cyber" in hazard:
                # Blackout OKC Master Hub
                for i, node in enumerate(self.nodes):
                    if node['hub'] == "OKC_Hub":
                        offline_nodes.add(i)
                edges_to_remove = [e for e in standard_edges if e[0] in offline_nodes or e[1] in offline_nodes]
                for e in edges_to_remove: standard_edges.remove(e)
                
                if mode in ["RECOVERY", "RESTORED"] and progress >= 0.5:
                    # Reroute via rural hubs
                    for i in range(12): green_edges.append((random.randint(45, 79), random.randint(80, 119)))

        fig = go.Figure()

        # Helper to plot Cartesian lines
        def plot_edges(edge_list, color, width, dash='solid'):
            if not edge_list: return
            xs = []; ys = []
            for e in edge_list:
                xs.extend([self.nodes[e[0]]['x'], self.nodes[e[1]]['x'], None])
                ys.extend([self.nodes[e[0]]['y'], self.nodes[e[1]]['y'], None])
            fig.add_trace(go.Scatter(
                x=xs, y=ys, mode='lines', line=dict(width=width, color=color, dash=dash), hoverinfo='none'
            ))

        plot_edges(standard_edges, 'rgba(0, 243, 255, 0.3)', 1) # Cyan Base Web
        plot_edges(red_edges, '#ef4444', 2) # Red Severed
        plot_edges(green_edges, '#10b981', 3) # Neon Green Routing

        # Plot Nodes
        active_x = []; active_y = []
        dead_x = []; dead_y = []
        for i, node in enumerate(self.nodes):
            if i in offline_nodes:
                dead_x.append(node['x']); dead_y.append(node['y'])
            else:
                active_x.append(node['x']); active_y.append(node['y'])

        fig.add_trace(go.Scatter(
            x=active_x, y=active_y, mode='markers',
            marker=dict(size=6, color='#00f3ff', symbol='diamond'), hoverinfo='none'
        ))
        if dead_x:
            fig.add_trace(go.Scatter(
                x=dead_x, y=dead_y, mode='markers',
                marker=dict(size=12, color='#ef4444', symbol='x'), hoverinfo='none'
            ))

        # Pure Cyber-Warfare Layout (Hidden Axes, Black Background)
        fig.update_layout(
            plot_bgcolor='#030712', paper_bgcolor='#030712',
            showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            height=450
        )
        return fig

    def _render_dashboard_frame(self, progress=1.0, mode="NORMAL"):
        cpu = psutil.cpu_percent() if mode == "NORMAL" else 98.5 + random.uniform(-1, 1)
        freq = 60.00 if mode in ["NORMAL", "RESTORED"] else 58.2 + (1.8 * progress)
        mw_load = 4250 if mode in ["NORMAL", "RESTORED"] else 3100 + (1150 * progress)
        sub_status = "120/120 NODES SECURE" if mode in ["NORMAL", "RESTORED"] else "CASCADE FAILURE IMMINENT"
        sub_color = "normal" if mode in ["NORMAL", "RESTORED"] else "inverse"

        if mode in ["RECOVERY", "RESTORED"]:
            st.markdown("<h3 style='color:#10b981; text-align:center; font-family:Orbitron;'>🟢 EBONY INITIATED: TOPOLOGICAL REROUTING IN PROGRESS</h3>", unsafe_allow_html=True)

        col_metrics, col_map, col_controls = st.columns([0.8, 2, 0.8])

        with col_metrics:
            st.markdown("#### ⚙️ TELEMETRY")
            st.metric(label="Live CPU Load", value=f"{cpu:.1f}%")
            st.metric(label="Grid Frequency", value=f"{freq:.2f} Hz", delta="Target: 60Hz", delta_color="normal" if freq>59.5 else "inverse")
            st.metric(label="Active Load", value=f"{mw_load:.0f} MW", delta=sub_status, delta_color=sub_color)

        with col_map:
            cyber_map = self._build_cyber_map(mode, progress)
            st.plotly_chart(cyber_map, use_container_width=True, config={'displayModeBar': False}, key=f"cybermap_{progress}")

        with col_controls:
            st.markdown("#### 🚨 INJECTOR")
            if mode == "NORMAL":
                log_tor = ">> EVENT: F5 Tornado. 10 Moore Substation Nodes Offline.\n>> EBONY ACTION: Severing primary OKC feeds to prevent cascade.\n>> EBONY ACTION: Establishing geographic bypass via Lawton/Enid rural hubs.\n>> GRID STATUS: Grid restabilized. Localized blackout contained.\n>> HUMAN ACTION:\n>> 1. Dispatch Heavy Infrastructure Units to I-35 Corridor.\n>> 2. Coordinate FEMA logistics."
                if st.button("🌪️ F5 Tornado", key="btn_tor", use_container_width=True):
                    self._trigger_hazard("F5 Tornado Strike", "LAT: 35.3395° N, LON: -97.4867° W (MOORE)", log_tor)
                
                log_cyb = ">> EVENT: SCADA Breach at OKC Master Hub.\n>> EBONY ACTION: Air-gapping 45 OKC Nodes.\n>> EBONY ACTION: Routing Tulsa generation directly to southern sectors.\n>> GRID STATUS: Intrusion neutralized. Power flow maintained.\n>> HUMAN ACTION:\n>> 1. Initiate forensic audit of OKC firewalls."
                if st.button("💻 SCADA Breach", key="btn_cyb", use_container_width=True):
                    self._trigger_hazard("State Cyber Breach", "LAT: 35.4676° N, LON: -97.5164° W (OKC)", log_cyb)
            else:
                st.markdown("##### ⚠ LOCKDOWN")
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
