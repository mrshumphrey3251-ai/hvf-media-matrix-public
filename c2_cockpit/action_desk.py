import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="HVF Actionable Dashboard", layout="wide")

st.title("🦅 HVF Omni-Industrial Matrix - Action Desk")

# Retire static widgets, introduce Actionable Heatmap & Alerts
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Current GLI Heatmap (Active Field)")
    # Simulated GLI Heatmap array (Grid of vegetative vigor)
    gli_data = np.random.uniform(low=-0.1, high=0.8, size=(10, 10))
    st.image(gli_data, use_column_width=True, clamp=True, caption="Green Leaf Index (Darker = Higher Vigor)")

    st.subheader("Soil Moisture Trend (Last 24h)")
    moisture_trend = pd.DataFrame(
        np.random.normal(loc=18.0, scale=2.0, size=(24, 1)),
        columns=['Moisture %']
    )
    st.line_chart(moisture_trend)

with col2:
    st.subheader("Active Alerts - Resolve/Assign")
    
    st.error("🚨 Critical Soil Moisture Drop - Sector 4 (Duration: > 30m)")
    if st.button("Schedule Irrigation - Sector 4"):
        st.success("Irrigation Node Activated.")
    
    st.warning("⚠️ Sudden GLI Vigor Drop - Sector 7 (Immediate)")
    if st.button("Deploy Drone - Sector 7 Recon"):
        st.success("Recon Drone Dispatched.")

st.sidebar.info("HVF Governance: UI audited to guarantee ≤ 3 clicks to action.")

