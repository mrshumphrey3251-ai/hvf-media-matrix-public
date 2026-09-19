import streamlit as st
import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(page_title="Ebony | Sovereign Empire Matrix", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050A15; }
    .stApp, p, span, div { color: #E2E8F0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3 { color: #00D2FF !important; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ HUMPHREY VIRTUAL FARMS | SOVEREIGN COMMAND DECK")
st.caption("Public Architecture Blueprint // 15-Vertical Defense & Industrial SCADA Matrix")

with st.sidebar:
    st.markdown("### 🎛️ Sovereign Modules")
    module = st.radio("Navigation", [
        "💬 Sovereign Command",
        "📡 LinkedIn Engine",
        "🚨 NOAA Radar",
        "🌾 Sensor & Drone Diagnostics",
        "📖 System Overview",
        "📡 Sovereign Comms Deck"
    ])

if module == "💬 Sovereign Command":
    st.subheader("/// EXECUTIVE COMMUNICATIONS")
    st.info("Sovereign Iron Dome Core Connected (Sanitized Architecture Baseline).")
    user_input = st.chat_input("Enter strategic directive...")
    if user_input:
        with st.chat_message("user"): st.markdown(user_input)
        with st.chat_message("assistant"): st.markdown(f"**Directive Acknowledged:** `{user_input}`. Routed through 15-Vertical Defense Matrix.")

elif module == "📡 Sovereign Comms Deck":
    st.subheader("📡 Sovereign WebRTC Comms Deck")
    st.caption("Zero-fee sovereign P2P optical feed and encrypted dispatch.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔴 LIVE SWARM OPTICAL FEED**")
        st.info("WebRTC Matrix streaming via Sovereign Tailscale Link.")
    with col2:
        st.markdown("**💬 ENCRYPTED P2P DISPATCH**")
        st.text_input("Secure message payload:")
        if st.button("Transmit Securely"):
            st.success("Encrypted payload dispatched to ledger.")

else:
    st.subheader(f"Module: {module}")
    st.info("Active in production private deployment.")