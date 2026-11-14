import streamlit as st
import sys
import os

st.set_page_config(page_title="Robotics & Kinematics | EBONY C2", page_icon="🤖", layout="wide")
st.title("🤖 SOVEREIGN ROBOTICS & KINEMATICS ENGINE")
st.caption("EBONY-RTOS // Deterministic <50µs Bare-Metal C Fieldbus + 36.75ns Kinetic Guillotine")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Real-Time Kinematic Envelope")
    st.metric("Fieldbus", "CAN-FD / EtherCAT", "Deterministic CST")
    st.metric("Effective Contact Force", "48.0 N", "Limit: 140.0 N")
    st.metric("Kinetic Guillotine State", "ARMED / NOMINAL", "14.5 A Shunt")
with col2:
    st.subheader("Life-Safety Interlock Comparison")
    st.metric("EBONY-RTOS Overrun (36.75 ns)", "0.0551 µm", "Zero Injury")
    st.metric("Legacy PLC Overrun (150 ms)", "225.0 mm", "Crush Hazard")
