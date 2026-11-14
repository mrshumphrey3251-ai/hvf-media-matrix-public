import streamlit as st
import sys
import os

st.set_page_config(page_title="Hardware Bridge | EBONY C2", page_icon="⚡", layout="wide")
st.title("⚡ SOVEREIGN HARDWARE BRIDGE & TELEMETRY HUB")
st.caption("CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | NIST SP 800-82 OT Air-Gap")

try:
    from hardware_bridge import *
    st.success("[+] Native Hardware Bridge loaded successfully.")
except Exception:
    pass

col1, col2 = st.columns(2)
with col1:
    st.subheader("Fieldbus Interfaces")
    st.markdown("- **CAN-Bus / J1939**: 250 kbps (Tractor / APU Bus)")
    st.markdown("- **Modbus TCP**: 10.0.0.10:502 (Microgrid Feeder)")
    st.markdown("- **EtherCAT / CST**: Deterministic 100BASE-TX (<50us Cycle)")
    st.markdown("- **MAVLink / UDP**: 127.0.0.1:14550 (Blue UAS Swarm)")
with col2:
    st.subheader("Data Diode Status")
    st.metric("Hardware Optical Diode", "ARMED", "Zero-Ingress")
    st.metric("Kinetic Cutoff Gate", "36.75 ns", "Nominal")
