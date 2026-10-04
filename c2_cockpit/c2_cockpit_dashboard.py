# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture
Authority: CEO Jeffery Humphrey (Level 5 Authority)
"""
import streamlit as st

class MasterCockpit:
    def __init__(self):
        self.ceo_name = "Jeffery Humphrey"
        self.clearance = "Level 5 Sovereign"

    def _inject_css(self):
        """Isolates all UI styling away from the core logic."""
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700;900&display=swap');
        
        .c2-header {
            background: #090e17;
            border: 1px solid #1e293b;
            border-left: 4px solid #00f3ff;
            padding: 10px 15px;
            margin-bottom: 15px;
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
        </style>
        """, unsafe_allow_html=True)

    def _render_header(self):
        """Renders the top-level executive HUD."""
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

    def _render_telemetry_grid(self):
        """Placeholder for the telemetry and data feeds (To be injected next)"""
        st.info("📡 Telemetry Grid: Foundation Secure. Awaiting Data Payloads.")

    def render_cockpit(self):
        """The single master execution trigger for the Command Deck."""
        self._inject_css()
        self._render_header()
        self._render_telemetry_grid()

# === EXPORTED RENDER HOOK FOR MAIN DISPATCHER ===
def render():
    cockpit = MasterCockpit()
    cockpit.render_cockpit()
