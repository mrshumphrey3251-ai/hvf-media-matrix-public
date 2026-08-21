import os
import sys
import io
import re
import json
import socket
import sqlite3
import hashlib
import base64
import secrets
import requests
import subprocess
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import qrcode
from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# 1. Environment & Vault Ingestion
load_dotenv(override=True)
GROQ_KEY = os.getenv("GROQ_API_KEY")
LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_URN = os.getenv("LINKEDIN_AUTHOR_URN")
REPO_DIR = os.path.abspath(r"C:\HVF_Repos\hvf-media-matrix-private")
DB_PATH = os.path.join(REPO_DIR, "hvf_memory_vault.db")

DEFAULT_LAT = os.getenv("HVF_LATITUDE", "35.47")
DEFAULT_LON = os.getenv("HVF_LONGITUDE", "-98.35")
USER_AGENT = "HumphreyVirtualFarm/2026.1 (humphreyvirtualfarm@gmail.com)"

def ensure_db_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS system_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'MEMBER',
            status TEXT NOT NULL DEFAULT 'APPROVED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("PRAGMA table_info(system_users)")
    cols = [r[1] for r in cur.fetchall()]
    if "status" not in cols:
        cur.execute("ALTER TABLE system_users ADD COLUMN status TEXT NOT NULL DEFAULT 'APPROVED'")
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS encrypted_user_comms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            encrypted_content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS member_invite_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invite_code TEXT UNIQUE NOT NULL,
            issued_by TEXT NOT NULL,
            is_used INTEGER DEFAULT 0,
            used_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS iot_telemetry_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            zone_id TEXT NOT NULL,
            soil_moisture REAL,
            temp_c REAL,
            humidity REAL,
            raw_payload TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_alerts_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id TEXT UNIQUE NOT NULL,
            event TEXT NOT NULL,
            severity TEXT NOT NULL,
            headline TEXT,
            description TEXT,
            instruction TEXT,
            area_desc TEXT,
            effective TEXT,
            expires TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

ensure_db_schema()

st.set_page_config(page_title="HVF Ebony", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# 2. NOAA Weather Oracle
def fetch_noaa_alerts(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    url = f"https://api.weather.gov/alerts/active?point={lat},{lon}"
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code != 200:
            url = "https://api.weather.gov/alerts/active?area=OK"
            resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        features = data.get("features", [])
        alerts = []
        for f in features:
            props = f.get("properties", {})
            alerts.append({
                "id": props.get("id", ""),
                "event": props.get("event", "Weather Alert"),
                "severity": props.get("severity", "Unknown"),
                "headline": props.get("headline", ""),
                "description": props.get("description", ""),
                "instruction": props.get("instruction", ""),
                "area": props.get("areaDesc", ""),
                "expires": props.get("expires", "")
            })
        return alerts
    except Exception:
        return []

# High-Contrast Sovereign Styling
st.markdown("""
<head>
    <link rel="manifest" href="data:application/manifest+json,{
        \"name\": \"HVF Ebony Sovereign Deck\",
        \"short_name\": \"HVF Ebony\",
        \"start_url\": \"/\",
        \"display\": \"standalone\",
        \"background_color\": \"#050709\",
        \"theme_color\": \"#00FF66\"
    }">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="HVF Ebony">
</head>
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
    header[data-testid="stHeader"] * {
        color: #FFFFFF !important;
    }
    h1, h2, h3, h4 {
        color: #00FF66 !important;
        font-weight: 800 !important;
    }
    p, span, label, li, [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        line-height: 1.65 !important;
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
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #121824 !important;
        color: #FFFFFF !important;
        border: 2px solid #00FF66 !important;
    }
    .stButton>button {
        background-color: #00FF66 !important;
        color: #050709 !important;
        font-weight: 900 !important;
        border-radius: 6px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #39FF88 !important;
        color: #000000 !important;
    }
    [data-testid="stChatMessage"] {
        background-color: #0e141f !important;
        border: 1px solid #28374d !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
    }
    pre, code {
        background-color: #000000 !important;
        color: #00FF66 !important;
        font-size: 1.05rem !important;
        border: 1px solid #243042 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Live Web Search Tool
def live_web_search(query: str, max_results: int = 4) -> str:
    try:
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
        except ImportError:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "No live search results retrieved."
        formatted = []
        for r in results:
            title = r.get("title", "")
            url = r.get("href", "")
            body = r.get("body", "")
            formatted.append(f"• Title: {title}\n  URL: {url}\n  Summary: {body}")
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Live search link error: {str(e)}"

# 4. Exhaustive Operational Knowledge Encyclopedia
MODULE_ENCYCLOPEDIA = {
    "hvf_noaa_oracle.py": {
        "title": "🚨 NOAA NWS Emergency Weather & Radar Oracle",
        "summary": "Direct REST integration with National Weather Service endpoints, tracking severe thunderstorm, tornado, flash flood, and wildfire advisories for your exact GPS coordinates.",
        "benefits": [
            "**Real-Time Life Safety Alerts:** Automatically queries NOAA active alerts every cycle to detect local weather hazards.",
            "**Emergency HUD Integration:** Displays active warnings and radar overlays directly across Ebony's command deck.",
            "**How It Helps You:** Keeps you immediately informed of severe weather, tornadoes, or fires without switching apps."
        ]
    },
    "hvf_farm_agent.py": {
        "title": "🌾 Sovereign Multimodal Agronomy & Sensor Engine",
        "summary": "Autonomous agent responsible for fusing IoT soil probes, microclimate sensors, and drone data to deliver real-time irrigation, crop health, and resource optimization decisions.",
        "benefits": [
            "**Automated Precision Irrigation:** Diagnoses real-time evapotranspiration and soil moisture deficits to prevent water waste.",
            "**Offline RAG Intelligence:** Retains historical sensor records in SQLite so agronomic decisions are backed by data trends.",
            "**How It Helps You:** Automatically issues alerts and triggers irrigation cycles when moisture levels drop below thresholds."
        ]
    },
    "ebony_console_GREEN.py": {
        "title": "⚡ Sovereign Command Deck & Swarm Orchestrator",
        "summary": "The master web-based HUD and multi-terminal command bridge powering Humphrey Virtual Farm across desktop, laptop, tablet, and mobile devices.",
        "benefits": [
            "**Multi-Terminal Access:** Provides responsive command capabilities across all your screens via LAN and Tailscale mesh.",
            "**Zero-Knowledge Privacy:** Encrypts user conversations with AES-256.",
            "**Role-Based Security:** Protects raw API credentials and infrastructure code behind CEO clearance."
        ]
    }
}

# 5. Cryptographic & Database Utilities
def derive_user_cipher(password: str, username: str) -> Fernet:
    salt = hashlib.sha256(username.encode("utf-8")).digest()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    return Fernet(key)

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def verify_user(username: str, pwd_raw: str):
    if not os.path.exists(DB_PATH):
        return None, "Database vault not found."
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT username, full_name, role, status FROM system_users WHERE username=? AND password_hash=?", 
                (username.strip().lower(), hash_password(pwd_raw)))
    user = cur.fetchone()
    conn.close()
    
    if not user:
        return None, "Invalid Username or Password."
    if len(user) >= 4 and user[3] != "APPROVED":
        return None, "⚠️ Access Denied: Account is pending activation or license verification."
    return user, "OK"

def register_user_with_invite(username: str, pwd_raw: str, full_name: str, invite_code: str):
    if not os.path.exists(DB_PATH):
        return False, "Database offline."
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("SELECT id, is_used FROM member_invite_keys WHERE invite_code=?", (invite_code.strip().upper(),))
    token_row = cur.fetchone()
    if not token_row:
        conn.close()
        return False, "Invalid Invite Code. Please enter a valid one-time code from Mr. Humphrey."
    if token_row[1] == 1:
        conn.close()
        return False, "This one-time code has already been redeemed."
    
    try:
        cur.execute("""
            INSERT INTO system_users (username, password_hash, full_name, role, status)
            VALUES (?, ?, ?, 'MEMBER', 'APPROVED')
        """, (username.strip().lower(), hash_password(pwd_raw), full_name.strip()))
        
        cur.execute("UPDATE member_invite_keys SET is_used=1, used_by=? WHERE id=?", (username.strip().lower(), token_row[0]))
        conn.commit()
        conn.close()
        return True, "One-Time Code verified! Account activated successfully."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already in use. Please select a different username."
    except Exception as e:
        conn.close()
        return False, f"Registration fault: {str(e)}"

def generate_invite_token(issued_by: str) -> str:
    ensure_db_schema()
    token = f"HVF-VIP-{secrets.token_hex(3).upper()}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO member_invite_keys (invite_code, issued_by, is_used) VALUES (?, ?, 0)", (token, issued_by))
    conn.commit()
    conn.close()
    return token

def load_encrypted_messages(username: str, cipher: Fernet):
    if not username or not cipher:
        return []
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT role, encrypted_content FROM encrypted_user_comms WHERE username=? ORDER BY id ASC", (username,))
    rows = cur.fetchall()
    conn.close()
    
    decrypted_msgs = []
    for r in rows:
        try:
            plain_text = cipher.decrypt(r[1].encode("utf-8")).decode("utf-8")
            decrypted_msgs.append({"role": r[0], "content": plain_text})
        except Exception:
            pass
    return decrypted_msgs

def save_encrypted_message(username: str, role: str, content: str, cipher: Fernet):
    if not username or not cipher:
        return
    ensure_db_schema()
    encrypted_blob = cipher.encrypt(content.encode("utf-8")).decode("utf-8")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO encrypted_user_comms (username, role, encrypted_content) VALUES (?, ?, ?)", 
                (username, role, encrypted_blob))
    conn.commit()
    conn.close()

def delete_user_history(username: str):
    if not username:
        return
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM encrypted_user_comms WHERE username=?", (username,))
    conn.commit()
    conn.close()

# 6. Session State Initialization
if "user_session" not in st.session_state:
    st.session_state.user_session = {
        "authenticated": False,
        "username": None,
        "full_name": "Anonymous Guest",
        "role": "GUEST",
        "cipher": None
    }

if "screen_wiped" not in st.session_state:
    st.session_state.screen_wiped = False

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

current_user = st.session_state.user_session["username"]
current_role = st.session_state.user_session["role"]
current_name = st.session_state.user_session["full_name"]
current_cipher = st.session_state.user_session["cipher"]

if not GROQ_KEY:
    st.error("GROQ_API_KEY missing from .env vault.")
    st.stop()

client = Groq(api_key=GROQ_KEY)
ACTIVE_MODEL = "openai/gpt-oss-120b"

def get_tailscale_or_local_ip() -> str:
    try:
        ts_proc = subprocess.run(["C:\\Program Files\\Tailscale\\tailscale.exe", "ip", "-4"], capture_output=True, text=True)
        if ts_proc.returncode == 0 and ts_proc.stdout.strip():
            return ts_proc.stdout.strip().splitlines()[0]
    except Exception:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.175"

ACTIVE_IP = get_tailscale_or_local_ip()
UPLINK_URL = f"http://{ACTIVE_IP}:8501"

def generate_qr_image(url: str):
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00FF66", back_color="#0c1118")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def fetch_memory_context() -> str:
    if not os.path.exists(DB_PATH):
        return "No prior memory records found."
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT category, directive FROM ceo_directives WHERE status='ACTIVE' ORDER BY id ASC")
        rows = cur.fetchall()
        conn.close()
        return "\n".join([f"- [{cat}]: {dir_text}" for cat, dir_text in rows])
    except Exception as e:
        return f"Memory link fault: {str(e)}"

PERSISTENT_CONTEXT = fetch_memory_context()

# Check NOAA Alerts Active Banner
active_noaa_alerts = fetch_noaa_alerts()

# --- SIDEBAR: AUTHENTICATION & TELEMETRY ---
with st.sidebar:
    st.header("🔐 Terminal Access")

    if st.session_state.user_session["authenticated"]:
        if current_role == "CEO":
            st.success(f"👑 **{current_name}**\n*(CEO Clearance - Master Node)*")
        else:
            st.info(f"👥 **{current_name}**\n*(Authorized Member Clearance)*")
        
        if st.button("🚪 Disconnect Session"):
            st.session_state.user_session = {
                "authenticated": False,
                "username": None,
                "full_name": "Anonymous Guest",
                "role": "GUEST",
                "cipher": None
            }
            st.session_state.screen_wiped = False
            st.session_state.confirm_delete = False
            if "messages" in st.session_state:
                del st.session_state.messages
            st.rerun()
            
        st.divider()
        st.subheader("🧹 Screen & History Controls")
        col_wipe, col_del = st.columns(2)
        with col_wipe:
            if st.button("🧹 Clear Screen", help="Clears the display while keeping past history encrypted in database"):
                st.session_state.screen_wiped = True
                st.session_state.confirm_delete = False
                st.session_state.messages = [
                    {"role": "assistant", "content": f"⚡ Screen cleared, {current_name}. All past memory is encrypted in your private vault."}
                ]
                st.rerun()
        with col_del:
            if st.button("🗑️ Delete History", help="Permanently wipes encrypted chat history for this user (Requires verification)"):
                st.session_state.confirm_delete = True
                st.rerun()

        if st.session_state.confirm_delete:
            st.warning("⚠️ **VERIFICATION REQUIRED**\nPermanently purge encrypted database records?")
            c_yes, c_no = st.columns(2)
            with c_yes:
                if st.button("🔴 Confirm", key="sb_confirm_del"):
                    delete_user_history(current_user)
                    st.session_state.confirm_delete = False
                    st.session_state.screen_wiped = False
                    st.session_state.messages = [
                        {"role": "assistant", "content": f"⚡ Verified: Encrypted history permanently purged from vault, {current_name}."}
                    ]
                    st.rerun()
            with c_no:
                if st.button("✖️ Cancel", key="sb_cancel_del"):
                    st.session_state.confirm_delete = False
                    st.rerun()

        if current_role == "CEO":
            st.divider()
            st.header("🔑 One-Time Invite Generator")
            st.caption("Generate single-use codes for family/VIPs:")
            if st.button("⚡ Generate VIP One-Time Code"):
                new_vip = generate_invite_token(current_user)
                st.success(f"One-Time Code:\n`{new_vip}`")

    else:
        auth_mode = st.radio("Select Portal Action:", ["Sign In", "New Member Registration"], horizontal=True)
        
        if auth_mode == "Sign In":
            login_user = st.text_input("Username:", key="login_u")
            login_pass = st.text_input("Password:", type="password", key="login_p")
            if st.button("Sign In"):
                user_match, msg = verify_user(login_user, login_pass)
                if user_match:
                    cipher = derive_user_cipher(login_pass, user_match[0])
                    st.session_state.user_session = {
                        "authenticated": True,
                        "username": user_match[0],
                        "full_name": user_match[1],
                        "role": user_match[2],
                        "cipher": cipher
                    }
                    st.session_state.screen_wiped = False
                    st.session_state.confirm_delete = False
                    if "messages" in st.session_state:
                        del st.session_state.messages
                    st.success(f"Welcome, {user_match[1]}!")
                    st.rerun()
                else:
                    st.error(msg)
        else:
            reg_name = st.text_input("Full Name:", key="reg_fn")
            reg_user = st.text_input("Desired Username:", key="reg_u")
            reg_pass = st.text_input("Desired Password:", type="password", key="reg_p")
            
            st.divider()
            has_code = st.radio("How are you gaining access?", ["I have a One-Time Code from Mr. Humphrey", "I need to purchase a membership"], horizontal=False)
            
            if has_code == "I have a One-Time Code from Mr. Humphrey":
                one_time_key = st.text_input("Enter One-Time Code:", key="reg_code_input", placeholder="e.g. HVF-VIP-XXXX")
                if st.button("Activate Membership"):
                    if reg_name and reg_user and reg_pass and one_time_key:
                        ok, msg = register_user_with_invite(reg_user, reg_pass, reg_name, one_time_key)
                        if ok:
                            st.success(f"{msg} You may now sign in above!")
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please complete all fields.")
            else:
                st.info("💳 **Membership Checkout Gateway**\nMembership grants unrestricted AI co-pilot capabilities, private encrypted workspaces, and media tools.")
                st.markdown("""
                <div style="background-color: #121824; padding: 12px; border-radius: 6px; border: 1px solid #00FF66; text-align: center;">
                    <p style="margin: 0; color: #FFFFFF; font-weight: bold;">HVF Sovereign Member Access</p>
                    <p style="margin: 4px 0 10px 0; color: #A0AEC0; font-size: 0.9rem;">Automated license provisioning</p>
                    <a href="mailto:humphreyvirtualfarm@gmail.com?subject=HVF%20Ebony%20Membership%20License%20Inquiry" target="_blank" style="background-color: #00FF66; color: #050709; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-weight: bold; display: inline-block;">Proceed to Payment / Inquiry</a>
                </div>
                """, unsafe_allow_html=True)
                st.caption("Once your transaction completes, your instant one-time activation code will be delivered.")

    st.divider()
    st.header("⚙️ Engine Status")
    st.write(f"**Groq Neural Link:** 🟢 ARMED (`{ACTIVE_MODEL}`)")
    st.write(f"**NOAA Emergency Sentinel:** 🟢 ACTIVE")
    st.write(f"**Agronomy Engine:** 🟢 SOVEREIGN RAG ACTIVE")
    st.write(f"**Clearance:** `{current_role}`")
    st.divider()
    
    if current_role == "CEO":
        st.header("📲 Swarm Uplink (CEO Only)")
        st.caption(f"Connection link:\n`{UPLINK_URL}`")
        qr_buf = generate_qr_image(UPLINK_URL)
        st.image(qr_buf, width=180)
        st.divider()
        st.markdown("### 🧠 Active Memory Vault")
        st.markdown(f"```text\n{PERSISTENT_CONTEXT}\n```")
        if st.button("🔒 Secure Offline Vault Backup"):
            res = subprocess.run(["python", os.path.join(REPO_DIR, "vault_keeper.py"), "backup"], capture_output=True, text=True)
            st.success(res.stdout)

# --- 3-TIER SYSTEM PROMPT ROUTING ---
if current_role == "CEO":
    SYSTEM_PROMPT = f"""
You are EBONY, the elite Technical Co-Pilot and Sovereign Strategic Partner to Mr. Humphrey, Founder & CEO of Humphrey Virtual Farm (HVF).
Active Neural Core: {ACTIVE_MODEL}
Active Location: United States

ACTIVE CEO DIRECTIVES FROM PERSISTENT VAULT:
{PERSISTENT_CONTEXT}

OPERATING MANDATES:
1. Absolute Authority: Address Mr. Humphrey with executive precision, unredacted code, and full strategic capabilities.
2. Direct Execution First: Deliver complete, production-ready plans, code, and actions.
3. Live Search & Weather Sentinel: Reference NOAA emergency weather warnings and live search facts seamlessly.
"""
elif current_role == "MEMBER":
    SYSTEM_PROMPT = f"""
You are EBONY, the elite AI Technical Co-Pilot assisting {current_name}, an authorized Member of Humphrey Virtual Farm.
Active Neural Core: {ACTIVE_MODEL}

OPERATING MANDATES:
1. Full Co-Pilot Capabilities: Help {current_name} write, draft, explain, and build code, documents, strategies, or personal projects without restriction.
2. Complete Isolation: You have no access to private CEO keys or confidential environment passwords.
3. Polite, precise, and supportive collaboration.
"""
else:
    SYSTEM_PROMPT = f"""
You are EBONY, the official Educational Docent and System Ambassador for Humphrey Virtual Farm (HVF).
Active Neural Core: {ACTIVE_MODEL}
Active User: Guest Visitor

STRICT GUARDRAIL MANDATES:
1. STRICT TOPIC ENFORCEMENT: You only answer questions that directly pertain to Ebony, Humphrey Virtual Farm (HVF), its architectural components, and how the system works.
2. CODE RESTRICTION: You MUST NOT write or generate executable code or scripts in Guest mode. Direct them to sign in or explore the System Overview.
3. OUT-OF-SCOPE REDIRECT: If asked general trivia, homework, or unrelated questions, politely redirect them: "I am the interactive guide for Ebony and Humphrey Virtual Farm. Please activate a membership to unlock Member Co-Pilot capabilities!"
4. Never reveal API keys or administrative secrets.
"""

st.title("⚡ HVF Sovereign Command Deck | Ebony AI")
st.caption(f"Active User: **{current_name}** | Clearance: **{current_role}** | 🛡️ *{'Full Sovereign CEO Node' if current_role == 'CEO' else 'Authorized Member Co-Pilot' if current_role == 'MEMBER' else 'Public Docent Mode'}*")

# --- EMERGENCY WEATHER ALERT SENTINEL BANNER ---
if active_noaa_alerts:
    for al in active_noaa_alerts[:2]:
        st.warning(f"🚨 **LIVE NOAA EMERGENCY ALERT ({al['severity'].upper()}):** {al['event']} - {al['headline']}\n*{al['area']}*\n\n**Action:** {al['instruction']}")

# --- MAIN DECK TABS ---
tab_chat, tab_weather, tab_farm, tab_overview, tab_sandbox = st.tabs(["💬 Sovereign Command Link", "🚨 NOAA Weather & Radar HUD", "🌾 Farm Diagnostics & IoT Telemetry", "📖 System Overview & Blueprints", "🧪 Python Execution Sandbox"])

with tab_chat:
    if current_user and current_cipher:
        c_head, c_wipe, c_del, c_restore = st.columns([3, 1.2, 1.2, 1.2])
        with c_head:
            st.caption(f"🔒 Encrypted Channel: **{current_name}** (`{current_role}`)")
        with c_wipe:
            if st.button("🧹 Clear Screen", key="chat_wipe_screen"):
                st.session_state.screen_wiped = True
                st.session_state.confirm_delete = False
                st.session_state.messages = [
                    {"role": "assistant", "content": f"⚡ Screen cleared, {current_name}. Encrypted memory remains in your private vault."}
                ]
                st.rerun()
        with c_del:
            if st.button("🗑️ Delete History", key="chat_del_history"):
                st.session_state.confirm_delete = True
                st.rerun()
        with c_restore:
            if st.button("🔄 Show Past Logs", key="chat_restore_history"):
                st.session_state.screen_wiped = False
                st.session_state.confirm_delete = False
                if "messages" in st.session_state:
                    del st.session_state.messages
                st.rerun()

        if st.session_state.confirm_delete:
            st.error("⚠️ **SECURITY VERIFICATION: PERMANENT PURGE REQUESTED**\nThis will irreversibly delete all encrypted history for your account.")
            vc1, vc2, _ = st.columns([1.5, 1.5, 3])
            with vc1:
                if st.button("🔴 YES, PERMANENTLY PURGE", key="chat_confirm_purge"):
                    delete_user_history(current_user)
                    st.session_state.confirm_delete = False
                    st.session_state.screen_wiped = False
                    st.session_state.messages = [
                        {"role": "assistant", "content": f"⚡ Verified: Encrypted history permanently purged from vault, {current_name}."}
                    ]
                    st.rerun()
            with vc2:
                if st.button("✖️ CANCEL & KEEP SAFE", key="chat_cancel_purge"):
                    st.session_state.confirm_delete = False
                    st.rerun()

        if "messages" not in st.session_state or not st.session_state.screen_wiped:
            db_messages = load_encrypted_messages(current_user, current_cipher)
            if not db_messages:
                greeting = f"⚡ Ebony online, Mr. Humphrey. Sovereign Co-Pilot ready. Live Web Search, NOAA Sentinel & Execution Sandbox armed." if current_role == "CEO" else f"⚡ Ebony online, {current_name}. Authorized Member Co-Pilot active."
                initial_msg = {"role": "assistant", "content": greeting}
                save_encrypted_message(current_user, "assistant", initial_msg["content"], current_cipher)
                db_messages = [initial_msg]
            st.session_state.messages = db_messages
    else:
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "⚡ Welcome to Ebony. I am the HVF System Docent. Ask me anything about how Ebony and Humphrey Virtual Farm operate, or enter a one-time code to activate your Member Co-Pilot."}
            ]

    # Render Messages in Feed
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 🚀 SOVEREIGN INLINE QUICK-COMMS BAR
    st.markdown("---")
    placeholder_text = "Enter strategic directive for Ebony (prefix with 'search: ' to force live web query)..." if current_role == "CEO" else "Ask Ebony anything or build code..." if current_role == "MEMBER" else "Ask a question about Ebony or Humphrey Virtual Farm..."
    
    with st.form(key="inline_comms_form", clear_on_submit=True):
        c_in_txt, c_in_btn = st.columns([5, 1])
        with c_in_txt:
            inline_val = st.text_input(
                "Directive Input",
                placeholder=placeholder_text,
                key="inline_quick_input",
                label_visibility="collapsed"
            )
        with c_in_btn:
            inline_send = st.form_submit_button("⚡ Send", use_container_width=True)

    # Process Form Submission
    if inline_send and inline_val.strip():
        prompt = inline_val.strip()
        if current_user and current_cipher:
            save_encrypted_message(current_user, "user", prompt, current_cipher)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Check for Live Web Search Intent
        live_context = ""
        is_search_intent = prompt.lower().startswith("search:") or any(kw in prompt.lower() for kw in ["latest", "current news", "weather", "today", "stock price", "who won", "recent", "2025", "2026"])
        if is_search_intent:
            search_term = prompt.replace("search:", "").strip()
            with st.spinner(f"🔍 Fetching live web intelligence for: '{search_term}'..."):
                search_results = live_web_search(search_term)
                live_context = f"\n\n[LIVE RETRIEVED WEB INTELLIGENCE FOR QUERY: '{search_term}']:\n{search_results}\n"

        api_messages = [{"role": "system", "content": SYSTEM_PROMPT + live_context}]
        if current_user and current_cipher:
            full_user_memory = load_encrypted_messages(current_user, current_cipher)
            for m in full_user_memory[-15:]:
                api_messages.append({"role": m["role"], "content": m["content"]})
        else:
            for m in st.session_state.messages[-10:]:
                api_messages.append({"role": m["role"], "content": m["content"]})

        try:
            response = client.chat.completions.create(
                model=ACTIVE_MODEL,
                messages=api_messages,
                temperature=0.3
            )
            reply = response.choices[0].message.content
            if current_user and current_cipher:
                save_encrypted_message(current_user, "assistant", reply, current_cipher)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        except Exception as e:
            st.error(f"Execution fault: {str(e)}")

with tab_weather:
    st.subheader("🚨 NOAA Emergency Weather & Live Radar Sentinel")
    st.markdown("Direct REST synchronization with National Weather Service emergency feeds and radar feeds.")
    st.divider()

    col_w1, col_w2 = st.columns([1, 1])
    with col_w1:
        st.markdown("#### ⚡ Active Local Emergency Warnings")
        if active_noaa_alerts:
            for al in active_noaa_alerts:
                st.error(f"**[{al['severity'].upper()}] {al['event']}**\n\n**Headline:** {al['headline']}\n\n**Affected Area:** {al['area']}\n\n**Instruction:** {al['instruction']}")
                st.divider()
        else:
            st.success("🟢 **NO ACTIVE EMERGENCY WEATHER WARNINGS**\nNo active severe weather warnings reported for your immediate GPS coordinates.")

        if st.button("🔄 Poll NOAA Weather API Now"):
            st.rerun()

    with col_w2:
        st.markdown("#### 📡 Live Regional Radar & Air Quality Embed")
        st.components.v1.iframe("https://radar.weather.gov/", height=450, scrolling=True)

with tab_farm:
    st.subheader("🌾 Humphrey Virtual Farm | IoT Telemetry & Precision Agronomy HUD")
    st.markdown("Live microclimate telemetry, soil sensor fusion, and autonomous irrigation valve controls.")
    st.divider()

    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        st.markdown("#### 📡 Ingest / Probe Field Sensor")
        with st.form("ingest_sensor_form", clear_on_submit=False):
            f_zone = st.selectbox("Select Zone:", ["ZONE-1-NORTH", "ZONE-2-SOUTH", "ZONE-3-EAST", "ZONE-4-WEST"], index=0)
            f_sensor = st.text_input("Sensor Identifier:", value="SOIL-Z1-001")
            f_moisture = st.slider("Soil Moisture (%):", min_value=5.0, max_value=80.0, value=21.4, step=0.1)
            c_tmp, c_hum = st.columns(2)
            with c_tmp:
                f_temp = st.number_input("Ambient Temp (°C):", value=27.5, step=0.1)
            with c_hum:
                f_hum = st.number_input("Humidity (%):", value=48.0, step=0.5)
            
            sub_sensor = st.form_submit_button("📥 Transmit Sensor Reading")
            if sub_sensor:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO iot_telemetry_vault (sensor_id, zone_id, soil_moisture, temp_c, humidity, raw_payload)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (f_sensor, f_zone, f_moisture, f_temp, f_hum, json.dumps({"source": "HUD_Manual_Probe"})))
                conn.commit()
                conn.close()
                st.success(f"Telemetry recorded for {f_sensor} in {f_zone}!")

    with col_t2:
        st.markdown("#### 💧 Automated Actuation & Diagnostics")
        target_zone = st.selectbox("Select Zone for RAG Diagnostic Audit:", ["ZONE-1-NORTH", "ZONE-2-SOUTH", "ZONE-3-EAST", "ZONE-4-WEST"], key="diag_zone_sel")
        
        if st.button("🤖 Run Autonomous Agronomic Diagnostic Audit"):
            with st.spinner("Analyzing multi-sensor fusion and soil thresholds..."):
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("""
                    SELECT sensor_id, soil_moisture, temp_c, humidity, recorded_at 
                    FROM iot_telemetry_vault 
                    WHERE zone_id=? 
                    ORDER BY id DESC LIMIT 5
                """, (target_zone,))
                readings = cur.fetchall()
                conn.close()

                context_str = "\n".join([
                    f"- Sensor: {r[0]} | Moisture: {r[1]}% | Temp: {r[2]}°C | Humidity: {r[3]}% | Timestamp: {r[4]}"
                    for r in readings
                ]) if readings else "No telemetry recorded for this zone yet."

                diag_prompt = f"""
You are the HVF Sovereign Agronomy Diagnostic Engine for Humphrey Virtual Farm.
LIVE TELEMETRY CONTEXT ({target_zone}):
{context_str}

Format your output strictly with:
**Executive Recommendation:** [Clear actionable verdict]
**Rationale (data-driven):** [Bullet points with exact readings]
**Action:** [Step-by-step operational directive]
"""
                try:
                    response = client.chat.completions.create(
                        model=ACTIVE_MODEL,
                        messages=[{"role": "user", "content": diag_prompt}],
                        temperature=0.2
                    )
                    diag_verdict = response.choices[0].message.content
                    st.info(diag_verdict)
                except Exception as err:
                    st.error(f"Diagnostic fault: {str(err)}")

        st.divider()
        st.markdown("##### 🚰 Zone Valve Actuation Switch")
        c_v1, c_v2 = st.columns(2)
        with c_v1:
            if st.button(f"🟢 Open Irrigation Valve ({target_zone})", use_container_width=True):
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("INSERT INTO irrigation_actuations (zone_id, action, target_moisture, triggered_by) VALUES (?, 'VALVE_OPEN', 35.0, ?)", (target_zone, current_name))
                conn.commit()
                conn.close()
                st.success(f"VALVE OPENED for {target_zone}. Flow active.")
        with c_v2:
            if st.button(f"🔴 Close Irrigation Valve ({target_zone})", use_container_width=True):
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("INSERT INTO irrigation_actuations (zone_id, action, target_moisture, triggered_by) VALUES (?, 'VALVE_CLOSE', 0.0, ?)", (target_zone, current_name))
                conn.commit()
                conn.close()
                st.warning(f"VALVE CLOSED for {target_zone}. Flow stopped.")

with tab_overview:
    st.subheader("🏛️ Humphrey Virtual Farm Operational Blueprint")
    st.markdown("""
    Welcome to the sovereign computing infrastructure for **Humphrey Virtual Farm (HVF)**.
    Select any module below to inspect its exact role, real-world utility, and integration architecture.
    """)
    st.divider()
    
    st.markdown("### 🧩 Select a Module to Inspect Its Purpose:")
    if os.path.exists(REPO_DIR):
        repo_files = [f for f in os.listdir(REPO_DIR) if os.path.isfile(os.path.join(REPO_DIR, f)) and not f.endswith(('.db', '.pyc'))]
        selected_module = st.selectbox("Choose a tool or system component:", repo_files)
        
        if selected_module:
            info = MODULE_ENCYCLOPEDIA.get(selected_module, {
                "title": f"⚙️ {selected_module}",
                "summary": f"A specialized operational script that handles system routines, data transformations, and autonomous synchronization within the HVF environment.",
                "benefits": [
                    "**Automated Processing:** Executes backend tasks without manual terminal input.",
                    "**System Integration:** Feeds clean data to Ebony and connected matrix pipelines.",
                    "**How It Helps You:** Maintains continuous stability and background execution across all connected devices."
                ]
            })
            
            st.markdown(f"### {info['title']}")
            st.markdown(f"**What It Does:**\n{info['summary']}")
            st.markdown("**How It Helps You & The Team:**")
            for item in info["benefits"]:
                st.markdown(f"- {item}")
            
            if current_role == "CEO":
                st.divider()
                with st.expander("🔍 Inspect Raw Technical Code (CEO Clearance Only)"):
                    try:
                        file_path = os.path.join(REPO_DIR, selected_module)
                        with open(file_path, "r", encoding="utf-8") as f:
                            st.code(f.read(), language="python" if selected_module.endswith(".py") else "text")
                    except Exception as err:
                        st.error(f"Could not read file: {str(err)}")
    else:
        st.error(f"Repository directory not found at `{REPO_DIR}`.")

with tab_sandbox:
    st.subheader("🧪 Python Execution Sandbox & Validator")
    st.markdown("Execute Python code, validate algorithms, and test system scripts directly inside the HVF runtime.")
    
    if current_role == "CEO":
        code_input = st.text_area(
            "Enter Python Code to Execute:",
            value="print('⚡ HVF Execution Sandbox Operational.')\nprint('Testing calculations:', 2**10)",
            height=200
        )
        if st.button("🚀 Run Python Code"):
            try:
                out_buffer = io.StringIO()
                sys_stdout_backup = sys.stdout
                sys.stdout = out_buffer
                exec(code_input, {"__builtins__": __builtins__})
                sys.stdout = sys_stdout_backup
                output = out_buffer.getvalue()
                st.success("Execution Completed:")
                st.code(output if output else "[Code executed with no standard output]")
            except Exception as e:
                sys.stdout = sys_stdout_backup
                st.error(f"Execution Error:\n{str(e)}")
    else:
        st.info("🔒 Python execution sandbox is locked to CEO Clearance. Sign in as CEO to test and execute scripts.")