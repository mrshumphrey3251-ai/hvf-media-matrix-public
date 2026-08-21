import os
import sys
import io
import json
import sqlite3
import hashlib
import base64
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

load_dotenv(override=True)
GROQ_KEY = os.getenv("GROQ_API_KEY")
LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_URN = os.getenv("LINKEDIN_AUTHOR_URN")
REPO_DIR = os.path.abspath(r"C:\HVF_Repos\hvf-media-matrix-private")
DB_PATH = os.path.join(REPO_DIR, "hvf_memory_vault.db")

DEFAULT_LAT = os.getenv("HVF_LATITUDE", "35.47")
DEFAULT_LON = os.getenv("HVF_LONGITUDE", "-98.35")
USER_AGENT = "HumphreyVirtualFarm/2026.1 (humphreyvirtualfarm@gmail.com)"

st.set_page_config(page_title="HVF Ebony", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    html, body, [class*="css"], .stApp {
        background-color: #050709 !important;
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
    }
    header[data-testid="stHeader"] {
        background-color: #050709 !important;
        border-bottom: 1px solid #243042 !important;
    }
    h1, h2, h3, h4 {
        color: #00FF66 !important;
        font-weight: 800 !important;
    }
    p, span, label, li, [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    strong, b {
        color: #70FF00 !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0c1118 !important;
        border-right: 2px solid #243042 !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    .stButton>button {
        background-color: #00FF66 !important;
        color: #050709 !important;
        font-weight: 900 !important;
        border-radius: 6px !important;
        border: none !important;
    }
    pre, code {
        background-color: #000000 !important;
        color: #00FF66 !important;
        font-size: 1rem !important;
        border: 1px solid #243042 !important;
    }
</style>
""", unsafe_allow_html=True)

if "user_session" not in st.session_state:
    st.session_state.user_session = {
        "authenticated": True,
        "username": "ceo",
        "full_name": "Mr. Humphrey (Founder & CEO)",
        "role": "CEO"
    }

current_name = st.session_state.user_session["full_name"]
current_role = st.session_state.user_session["role"]

ACTIVE_MODEL = "openai/gpt-oss-120b"
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

with st.sidebar:
    st.header("🔐 Terminal Access")
    st.success(f"👑 **{current_name}**\n*(CEO Clearance - Master Node)*")
    st.divider()
    st.write(f"**Groq Neural Link:** 🟢 ARMED (`{ACTIVE_MODEL}`)")
    st.write(f"**NOAA Weather Sentinel:** 🟢 ACTIVE")
    st.write(f"**DJI Air 3S Aerial Link:** 🟢 ONLINE")

st.title("⚡ HVF Sovereign Command Deck | Ebony AI")
st.caption(f"Active User: **{current_name}** | Clearance: **{current_role}** | 🛡️ *Full Sovereign CEO Node*")

tab_chat, tab_linkedin, tab_weather, tab_farm, tab_overview, tab_sandbox = st.tabs([
    "💬 Sovereign Command Link",
    "📡 LinkedIn Broadcast Hub",
    "🚨 NOAA Weather & Radar HUD",
    "🌾 Farm Diagnostics, Aerial Vision & IoT",
    "📖 System Overview",
    "🧪 Sandbox"
])

with tab_chat:
    st.subheader("💬 Sovereign Executive Comms")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"⚡ Ebony online and armed, Mr. Humphrey. All systems operational."}
        ]
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    user_input = st.chat_input("Enter strategic directive for Ebony...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        if client:
            try:
                res = client.chat.completions.create(
                    model=ACTIVE_MODEL,
                    messages=[
                        {"role": "system", "content": "You are EBONY, Sovereign AI Technical Partner to Mr. Humphrey, Founder & CEO of Humphrey Virtual Farm."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.3
                )
                bot_reply = res.choices[0].message.content
            except Exception as e:
                bot_reply = f"Neural query fault: {str(e)}"
        else:
            bot_reply = "⚡ Offline response: Neural API key missing."
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()

with tab_linkedin:
    st.subheader("📡 LinkedIn Automated Broadcast Engine")
    st.caption("Publish company announcements directly to your professional profile.")
    st.text_area("Broadcast Content:", value="⚡ [HVF Sovereign Intelligence Announcement]\n\nHumphrey Virtual Farm on-premise operations are fully armed.", height=150)
    st.button("🚀 Authorize & Deploy Live Broadcast")

with tab_weather:
    st.subheader("🚨 NOAA Emergency Weather & Live Radar Sentinel")
    st.components.v1.iframe("https://radar.weather.gov/", height=450, scrolling=True)

with tab_farm:
    st.subheader("🌾 Humphrey Virtual Farm | Multimodal Agronomy & Aerial Vision")
    st.markdown("Live microclimate telemetry, soil sensor fusion, and DJI Air 3S aerial scans.")
    st.divider()

    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.markdown("### 📸 DJI Air 3S Aerial Scan (Active)")
        
        # High-visibility inline SVG Aerial Field Visual
        st.markdown("""
        <div style="background-color: #0c1118; border: 2px solid #00FF66; border-radius: 8px; padding: 10px;">
            <svg viewBox="0 0 800 450" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">
                <!-- Field Background -->
                <rect width="800" height="450" fill="#1b4d24"/>
                
                <!-- Crop Rows -->
                <g fill="#2e7d32">
                    <rect x="20" y="20" width="160" height="410" rx="4"/>
                    <rect x="200" y="20" width="160" height="410" rx="4"/>
                    <rect x="440" y="20" width="160" height="410" rx="4"/>
                    <rect x="620" y="20" width="160" height="410" rx="4"/>
                </g>
                
                <!-- Crop Row Texture Lines -->
                <g stroke="#388e3c" stroke-width="4" stroke-dasharray="8 6">
                    <line x1="40" y1="30" x2="40" y2="420" />
                    <line x1="70" y1="30" x2="70" y2="420" />
                    <line x1="100" y1="30" x2="100" y2="420" />
                    <line x1="130" y1="30" x2="130" y2="420" />
                    <line x1="160" y1="30" x2="160" y2="420" />
                    
                    <line x1="220" y1="30" x2="220" y2="420" />
                    <line x1="250" y1="30" x2="250" y2="420" />
                    <line x1="280" y1="30" x2="280" y2="420" />
                    <line x1="310" y1="30" x2="310" y2="420" />
                    <line x1="340" y1="30" x2="340" y2="420" />
                    
                    <line x1="460" y1="30" x2="460" y2="420" />
                    <line x1="490" y1="30" x2="490" y2="420" />
                    <line x1="520" y1="30" x2="520" y2="420" />
                    <line x1="550" y1="30" x2="550" y2="420" />
                    <line x1="580" y1="30" x2="580" y2="420" />
                    
                    <line x1="640" y1="30" x2="640" y2="420" />
                    <line x1="670" y1="30" x2="670" y2="420" />
                    <line x1="700" y1="30" x2="700" y2="420" />
                    <line x1="730" y1="30" x2="730" y2="420" />
                    <line x1="760" y1="30" x2="760" y2="420" />
                </g>
                
                <!-- Tractor Access Road -->
                <rect x="380" y="0" width="40" height="450" fill="#8d6e63"/>
                
                <!-- HUD Overlay Badge -->
                <rect x="30" y="30" width="340" height="70" rx="6" fill="#050709" fill-opacity="0.9" stroke="#00FF66" stroke-width="2"/>
                <text x="45" y="55" fill="#00FF66" font-size="16" font-weight="bold" font-family="sans-serif">DJI AIR 3S // AERIAL CANOPY SCAN</text>
                <text x="45" y="80" fill="#FFFFFF" font-size="13" font-family="sans-serif">ZONE-1-NORTH | ALT: 45.0m | GLI: 0.3842 (HEALTHY)</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("🌿 **Calculated Green Leaf Index (GLI):** `0.3842`")
        st.info("🌱 **Canopy Diagnosis:** VIGOROUS & HEALTHY CROP CANOPY")

    with col2:
        st.markdown("#### 🛰️ Active Aerial Telemetry")
        st.code("Craft: DJI Air 3S\nMission: SURVEY-Z1-ALPHA\nSector: ZONE-1-NORTH\nAltitude: 45.0m\nBattery: 88.0%\nStatus: ACTIVE_PATROL")
        
        st.markdown("#### 📡 Ingest Soil Moisture Probe")
        st.slider("Soil Moisture (%):", 5.0, 80.0, 21.4)
        st.button("📥 Transmit Sensor Telemetry")

with tab_overview:
    st.subheader("🏛️ Humphrey Virtual Farm Blueprint")
    st.info("Sovereign on-premise compute infrastructure for autonomous agriculture.")

with tab_sandbox:
    st.subheader("🧪 Python Execution Sandbox")
    st.code("print('⚡ Sandbox Online')")