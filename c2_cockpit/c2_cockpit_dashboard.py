# -*- coding: utf-8 -*-
"""
PROJECT EBONY: UNIFIED MASTER COMMAND COCKPIT
Object-Oriented Sovereign Architecture - Glass Cockpit Integration
Authority: CEO Jeffery Humphrey (Level 5 Authority)
"""
import streamlit as st
import random
import time

class MasterCockpit:
    def __init__(self):
        self.ceo_name = "Jeffery Humphrey"
        self.clearance = "Level 5 Sovereign"

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

    def _render_telemetry_grid(self):
        st.markdown("### 🌐 LIVE SYSTEM TELEMETRY")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🖥️ CORE INFRASTRUCTURE")
            st.metric(label="Neural Core Temp", value=f"{random.uniform(45.0, 48.5):.1f} °C", delta="-0.2 °C (Cooling)")
            st.metric(label="Iron Dome DB Latency", value=f"{random.uniform(8, 12):.0f} ms", delta="-2 ms (Optimized)")
            st.metric(label="Active Network Nodes", value="16 / 16 ONLINE", delta="100% Sovereign", delta_color="normal")

        with col2:
            st.markdown("#### ⚡ KINETIC PROCESSING")
            st.metric(label="Kirchhoff Current Vector", value=f"{random.uniform(1.15, 1.25):.3f} A", delta="+0.01 A (Nominal)")
            st.metric(label="Optical GLI Average", value=f"{random.uniform(0.18, 0.22):.3f}", delta="Optimal Vigor", delta_color="normal")
            st.metric(label="Matrix Throughput", value=f"{random.uniform(850, 950):.0f} Mbps", delta="Peak Flow", delta_color="normal")

        with col3:
            st.markdown("#### 🛡️ EXECUTIVE OVERRIDES")
            if st.button("🔄 Force Core Resync", use_container_width=True, type="primary"):
                st.toast("Core Resync Initiated. Aligning Sub-Nodes...", icon="🔄")
            if st.button("🔒 Lock All External Ports", use_container_width=True):
                st.toast("External Ports Locked. Air-Gap Verified.", icon="🔒")
            if st.button("⚠️ Run Diagnostic Sweep", use_container_width=True):
                st.toast("Diagnostic Sweep Dispatched across all 16 modules.", icon="⚠️")

    def render_cockpit(self):
        self._inject_css()
        self._render_header()
        self._render_telemetry_grid()

# === EXPORTED RENDER HOOK FOR MAIN DISPATCHER ===
def render():
    cockpit = MasterCockpit()
    cockpit.render_cockpit()
