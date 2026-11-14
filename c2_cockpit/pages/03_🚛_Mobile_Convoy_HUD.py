"""
================================================================================
PROPRIETARY AND CONFIDENTIAL -- HUMPHREY VIRTUAL FARMS LLC
PROTECTED UNDER 10 U.S.C. § 4022 OTHER TRANSACTION AGREEMENT
================================================================================
CONTRACTOR NAME: Humphrey Virtual Farms LLC
CONTRACTOR ADDRESS: Oklahoma, USA
CAGE CODE: 1AHA8 | UEI: S1M4ENLHTDH5
AGREEMENT / OTA IDENTIFIER: PROTOTYPE OTA 10 U.S.C. § 4022

RESTRICTIVE LEGEND -- COMMERCIAL COMPUTER SOFTWARE & PROPRIETARY TECHNICAL DATA:
The software, firmware, algorithms, architectural structures, and underlying 
source code contained herein are proprietary commercial items developed entirely 
at private expense by Humphrey Virtual Farms LLC. 

The Government's rights to use, modify, reproduce, release, perform, display, 
or disclose this computer software and technical data are restricted as set forth 
in the governing 10 U.S.C. § 4022 Prototype Agreement. Any reproduction of this 
software, in whole or in part, or disclosure to unauthorized third parties or 
commercial competitors without the express written permission of Humphrey 
Virtual Farms LLC is strictly prohibited.
================================================================================
"""
import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Mobile Convoy HUD", page_icon="🚛", layout="wide")
st.markdown("<h1 style='color: #00ffcc; border-bottom: 2px solid #00ffcc;'>MOBILE COMMAND CONVOY TACTICAL HUD</h1>", unsafe_allow_html=True)
st.markdown("**SYSTEM: E.B.O.N.Y. v8.0.0 | CAGE: 1AHA8 | CLEARANCE: LEVEL-5**")
st.markdown("---")

# 3-Pillar Hardware Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚛 PRIME MOVER (CAN-Bus)")
    st.markdown("*Asset: Class-8 Electric Semi (GFE)*")
    st.metric(label="600V Traction Inverter", value="NOMINAL", delta="0 Faults")
    st.metric(label="Drive-by-Wire Speed", value="0 mph", delta="PARKED", delta_color="off")
    st.metric(label="J1939 Override State", value="STANDBY")

with col2:
    st.subheader("⚡ 18kW MICROGRID (Modbus)")
    st.markdown("*Asset: EMP-Hardened Trailer*")
    st.metric(label="LFP Battery Bank (500kWh)", value="94.5%", delta="-0.5% Drain")
    st.progress(0.94)
    st.metric(label="Active DC Bus Voltage", value="482.4 V")
    st.metric(label="Solar Generation", value="14.2 kW")

with col3:
    st.subheader("🚁 AIRSPACE (MAVLink)")
    st.markdown("*Asset: Blue UAS Swarm*")
    st.metric(label="Swarm Status", value="DOCKED", delta="3/3 Nodes Charging")
    st.metric(label="Telemetry Link", value="SECURE (UDP)")
    st.metric(label="Airspace Veto Lock", value="ACTIVE")

st.markdown("---")
st.subheader("🛡️ SOVEREIGN KINETIC GUILLOTINE STATUS")
k_col1, k_col2 = st.columns([1, 1])

with k_col1:
    st.info("ACTIVE GLI CONFIDENCE SCORE: **0.948** (Threshold: 0.85)")
with k_col2:
    st.error("SiC MOSFET GATE CUTOFF TARGET: **36.75 ns** (ARMED)")

st.success("WORM LEDGER: 52 Tables Locked | Hardware Data Diode: VERIFIED")

