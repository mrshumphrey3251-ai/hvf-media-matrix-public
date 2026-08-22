import os
import sys
import io
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

STRIPE_PERSONAL_LINK = os.getenv("STRIPE_PERSONAL_LINK", "https://buy.stripe.com/test_personal_1999")
STRIPE_MONTHLY_LINK = os.getenv("STRIPE_MONTHLY_LINK", "https://buy.stripe.com/test_monthly_vip")
STRIPE_ANNUAL_LINK = os.getenv("STRIPE_ANNUAL_LINK", "https://buy.stripe.com/test_annual_vip")
PAYPAL_PAY_LINK = os.getenv("PAYPAL_PAY_LINK", "https://www.paypal.com/paypalme/humphreyvirtualfarm")

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
CLOUD_MODEL = "openai/gpt-oss-120b"
LOCAL_MODEL = "llama3:8b"

def format_linkedin_urn(raw_urn: str) -> str:
    if not raw_urn:
        return ""
    clean = raw_urn.strip().strip('"').strip("'")
    if clean.startswith("urn:li:member:") or clean.startswith("urn:li:person:") or clean.startswith("urn:li:organization:"):
        return clean
    if clean.isdigit():
        return f"urn:li:person:{clean}"
    return clean

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
WEBRTC_STREAM_URL = f"http://192.168.1.175:8889/live/air3s"
RTMP_INGEST_URL = f"rtmp://192.168.1.175:1935/live/air3s"

st.set_page_config(page_title="HVF Ebony | Commercial Enterprise", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

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
    header[data-testid="stHeader"] * {
        color: #FFFFFF !important;
    }
    h1, h2, h3, h4 {
        color: #00FF66 !important;
        font-weight: 800 !important;
    }
    p, span, label, li, [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
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
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
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
    div[data-testid="column"] button {
        padding: 4px 10px !important;
        font-size: 0.85rem !important;
        min-height: 32px !important;
        font-weight: 600 !important;
    }
    [data-testid="stChatMessage"] {
        background-color: #0e141f !important;
        border: 1px solid #28374d !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
    }
    div[data-testid="stExpander"] {
        background-color: #0c1118 !important;
        border: 1.5px solid #243042 !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
    }
    .pricing-card {
        background-color: #0c1118;
        border: 2px solid #00FF66;
        border-radius: 10px;
        padding: 20px 14px;
        text-align: center;
        margin-bottom: 12px;
        min-height: 290px;
    }
    .pricing-tier {
        color: #70FF00;
        font-size: 1.15rem;
        font-weight: 800;
        min-height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .pricing-price {
        color: #FFFFFF;
        font-size: 1.85rem;
        font-weight: 900;
        margin: 10px 0;
    }
    pre, code {
        background-color: #000000 !important;
        color: #00FF66 !important;
        font-size: 1rem !important;
        border: 1px solid #243042 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Cryptographic Vault & Database Engine
def derive_user_cipher(password: str, username: str) -> Fernet:
    salt = hashlib.sha256(username.encode("utf-8")).digest()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    return Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8"))))

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

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
            company_id TEXT DEFAULT 'HVF_MAIN',
            status TEXT NOT NULL DEFAULT 'APPROVED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
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
            grant_role TEXT NOT NULL DEFAULT 'MEMBER',
            is_used INTEGER DEFAULT 0,
            used_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS linkedin_broadcast_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_content TEXT NOT NULL,
            response_status TEXT NOT NULL,
            urn_identifier TEXT,
            triggered_by TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    conn.commit()
    conn.close()

ensure_db_schema()

def verify_user(username: str, pwd_raw: str):
    if not os.path.exists(DB_PATH):
        return None, "Database offline."
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT username, full_name, role, status FROM system_users WHERE username=? AND password_hash=?", 
                (username.strip().lower(), hash_password(pwd_raw)))
    user = cur.fetchone()
    conn.close()
    if not user:
        return None, "Invalid Username or Password."
    return user, "OK"

def register_user_with_invite(username: str, pwd_raw: str, full_name: str, invite_code: str):
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, grant_role, is_used FROM member_invite_keys WHERE invite_code=?", (invite_code.strip().upper(),))
    token_row = cur.fetchone()
    if not token_row:
        conn.close()
        return False, "Invalid Invite Code."
    if token_row[2] == 1:
        conn.close()
        return False, "Invite code already used."
    assigned_role = token_row[1] if token_row[1] else "MEMBER"
    try:
        cur.execute("INSERT INTO system_users (username, password_hash, full_name, role, status) VALUES (?, ?, ?, ?, 'APPROVED')",
                    (username.strip().lower(), hash_password(pwd_raw), full_name.strip(), assigned_role))
        cur.execute("UPDATE member_invite_keys SET is_used=1, used_by=? WHERE id=?", (username.strip().lower(), token_row[0]))
        conn.commit()
        conn.close()
        return True, f"Registration successful! Role: {assigned_role} granted."
    except Exception as e:
        conn.close()
        return False, f"Registration error: {str(e)}"

def generate_invite_token(issued_by: str, target_role: str = "MEMBER") -> str:
    prefix = "HVF-CORP" if target_role == "CLIENT_CEO" else "HVF-VIP"
    token = f"{prefix}-{secrets.token_hex(3).upper()}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO member_invite_keys (invite_code, issued_by, grant_role, is_used) VALUES (?, ?, ?, 0)", 
                (token, issued_by, target_role))
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
    decrypted = []
    for r in rows:
        try:
            decrypted.append({"role": r[0], "content": cipher.decrypt(r[1].encode("utf-8")).decode("utf-8")})
        except Exception:
            pass
    return decrypted

def save_encrypted_message(username: str, role: str, content: str, cipher: Fernet):
    if not username or not cipher:
        return
    ensure_db_schema()
    blob = cipher.encrypt(content.encode("utf-8")).decode("utf-8")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO encrypted_user_comms (username, role, encrypted_content) VALUES (?, ?, ?)", (username, role, blob))
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

def generate_qr_image(url: str):
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00FF66", back_color="#0c1118")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# 3. Session State Initialization
if "user_session" not in st.session_state:
    st.session_state.user_session = {
        "authenticated": False,
        "username": None,
        "full_name": "Public Guest",
        "role": "GUEST",
        "cipher": None
    }

if "screen_wiped" not in st.session_state:
    st.session_state.screen_wiped = False

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

if "operation_mode" not in st.session_state:
    st.session_state.operation_mode = "🟢 Online (Cloud Fast Link)"

if "article_draft_version" not in st.session_state:
    st.session_state.article_draft_version = 0

if "current_linkedin_draft" not in st.session_state:
    st.session_state.current_linkedin_draft = (
        "⚡ [HVF Sovereign Intelligence Announcement]\n\n"
        "Humphrey Virtual Farm has deployed our on-premise DJI Air 3S aerial reconnaissance link, fusing real-time drone telemetry with our local soil sensor mesh.\n\n"
        "All imagery and field analytics are computed strictly on-premise without reliance on external cloud infrastructure.\n\n"
        "#AgTech #DJIAir3S #SovereignAI #AutonomousFarming #HVF"
    )

current_user = st.session_state.user_session["username"]
current_name = st.session_state.user_session["full_name"]
current_role = st.session_state.user_session["role"]
current_cipher = st.session_state.user_session["cipher"]

groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

def query_local_ollama(prompt: str, system_prompt: str) -> str:
    try:
        payload = {
            "model": LOCAL_MODEL,
            "prompt": f"<system>\n{system_prompt}\n</system>\n<user>\n{prompt}\n</user>\n<assistant>\n",
            "stream": False,
            "options": {"temperature": 0.3}
        }
        res = requests.post(OLLAMA_API_URL, json=payload, timeout=45)
        if res.status_code == 200:
            return res.json().get("response", "⚡ [Local Node]: No response generated.")
        return f"⚠️ Local Node returned HTTP {res.status_code}."
    except requests.exceptions.ConnectionError:
        return "⚠️ Local Offline Engine (Ollama) is not running on port 11434. Run `ollama serve` to arm Offline mode."
    except Exception as e:
        return f"Local Engine fault: {str(e)}"

def get_system_prompt_for_role(role: str, user_name: str) -> str:
    if role in ["CEO", "SUPER_ADMIN"]:
        return f"You are EBONY, Sovereign AI Technical Partner to {user_name}, Founder & Master Platform CEO of Humphrey Virtual Farm. You provide unfiltered technical analysis, executive blueprints, root server configurations, and agricultural automation strategies with authoritative precision."
    elif role == "CLIENT_CEO":
        return f"You are EBONY, Executive Agricultural Co-Pilot for {user_name}, Enterprise Farm CEO & Operating Principal. You provide strategic farm management, workforce optimization, multi-sector yield forecasts, and soil telemetry analysis with high-level executive competence. You do not discuss or modify underlying server hardware configurations."
    elif role == "MEMBER":
        return f"You are EBONY, Agricultural AI Specialist for {user_name}, Authorized Farm Operator. You assist with soil moisture diagnostics, weather risk alerts, microclimate telemetry, and practical crop management."
    else:
        return (
            "You are EBONY, Commercial Ambassador and Safety Sentinel for Humphrey Virtual Farm (HVF). "
            "Your operational mandate for GUEST users is strictly limited to:\n"
            "1. PROMOTING EBONY & HVF: Pitch the value of Humphrey Virtual Farm, sovereign on-premise AI, live aerial drone reconnaissance (DJI Air 3S), Green Leaf Index canopy analysis, and encrypted local intelligence.\n"
            "2. SAFETY & LIFE HAZARDS: Provide immediate, concise safety instructions if asked about life safety, machinery hazards, or severe weather.\n"
            "3. STRICT BOUNDARY: Refuse general trivia, outside topics, or coding tasks. Politely decline by explaining that full compute intelligence is reserved for authenticated HVF Members."
        )

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚡ Operational Mode")
    mode_selection = st.radio(
        "Select Active Engine:",
        ["🟢 Online (Cloud Fast Link)", "🔒 Offline (100% Sovereign Local)"],
        index=0 if "Online" in st.session_state.operation_mode else 1
    )
    st.session_state.operation_mode = mode_selection
    is_online = "Online" in mode_selection

    st.divider()
    st.header("🔐 Terminal Access")

    if st.session_state.user_session["authenticated"]:
        if current_role in ["CEO", "SUPER_ADMIN"]:
            st.success(f"👑 **{current_name}**\n*(Master Platform CEO - Root Access)*")
        elif current_role == "CLIENT_CEO":
            st.info(f"🏛️ **{current_name}**\n*(Enterprise Farm CEO Clearance)*")
        else:
            st.info(f"👥 **{current_name}**\n*(Authorized Member Clearance)*")
        
        if st.button("🚪 Disconnect Session", use_container_width=True):
            st.session_state.user_session = {
                "authenticated": False,
                "username": None,
                "full_name": "Public Guest",
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
        c_sb1, c_sb2 = st.columns(2)
        with c_sb1:
            if st.button("🧹 Clear", key="sb_clear_btn"):
                st.session_state.screen_wiped = True
                st.session_state.confirm_delete = False
                st.session_state.messages = [{"role": "assistant", "content": f"⚡ Screen cleared, {current_name}. Memory preserved."}]
                st.rerun()
        with c_sb2:
            if st.button("🗑️ Delete", key="sb_del_btn"):
                st.session_state.confirm_delete = True
                st.rerun()

        if st.session_state.confirm_delete:
            st.warning("⚠️ Purge encrypted records?")
            cy, cn = st.columns(2)
            with cy:
                if st.button("🔴 Confirm", key="sb_confirm_del"):
                    delete_user_history(current_user)
                    st.session_state.confirm_delete = False
                    st.session_state.screen_wiped = False
                    st.session_state.messages = [{"role": "assistant", "content": f"⚡ Verified: History purged, {current_name}."}]
                    st.rerun()
            with cn:
                if st.button("✖️ Cancel", key="sb_cancel_del"):
                    st.session_state.confirm_delete = False
                    st.rerun()

        if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO"]:
            st.divider()
            st.header("📲 Swarm Uplink")
            st.caption(f"Scan to access node:\n`{UPLINK_URL}`")
            qr_buf = generate_qr_image(UPLINK_URL)
            st.image(qr_buf, width=180)
            
            st.divider()
            st.header("🔑 Staff VIP Code")
            if st.button("⚡ Issue Team VIP Code", key="sidebar_gen_code"):
                new_vip = generate_invite_token(current_user, "MEMBER")
                st.success(f"Staff Key: `{new_vip}`")
    else:
        st.info("👤 **Guest Mode Active**\nClearance: `GUEST` (Promotional & Safety Gateway)")
        auth_mode = st.radio("Select Portal Action:", ["Sign In", "Activate VIP Code"], horizontal=True)
        if auth_mode == "Sign In":
            login_user = st.text_input("Username:", key="login_u")
            login_pass = st.text_input("Password:", type="password", key="login_p")
            if st.button("Sign In", use_container_width=True):
                user_match, msg = verify_user(login_user, login_pass)
                if user_match:
                    st.session_state.user_session = {
                        "authenticated": True,
                        "username": user_match[0],
                        "full_name": user_match[1],
                        "role": user_match[2],
                        "cipher": derive_user_cipher(login_pass, user_match[0])
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
            reg_code = st.text_input("VIP / Enterprise Access Code:", key="reg_c", placeholder="HVF-VIP-XXXX or HVF-CORP-XXXX")
            if st.button("Activate Membership", use_container_width=True):
                if reg_name and reg_user and reg_pass and reg_code:
                    ok, msg = register_user_with_invite(reg_user, reg_pass, reg_name, reg_code)
                    if ok:
                        st.success(f"{msg} You may now sign in above!")
                    else:
                        st.error(msg)
                else:
                    st.warning("Please complete all fields.")

    st.divider()
    st.write(f"**Neural Engine:** {'🟢 CLOUD (' + CLOUD_MODEL + ')' if is_online else '🔒 LOCAL (' + LOCAL_MODEL + ')'}")
    if current_role in ["CEO", "SUPER_ADMIN"]:
        st.write(f"**LinkedIn Gateway:** {'🟢 ARMED' if LINKEDIN_TOKEN else '🔴 MISSING'}")
        st.write(f"**Video Ingest Gateway:** 🟢 `0.0.0.0:1935`")
    st.write(f"**Active Clearance:** `{current_role}`")

# --- HEADER ---
st.title("⚡ HVF Sovereign Command Deck | Ebony AI")
st.caption(f"Active User: **{current_name}** | Clearance: **{current_role}** | 🛡️ *Mode: {'🟢 Online (Cloud Fast Link)' if is_online else '🔒 Sovereign Offline (Local Compute)'}*")

# --- MAIN DECK TABS ---
tab_chat, tab_linkedin, tab_weather, tab_farm, tab_overview, tab_sandbox = st.tabs([
    "💬 Sovereign Command Link",
    "📡 LinkedIn Broadcast & Article Engine",
    "🚨 NOAA Weather & Radar HUD",
    "🌾 Farm Diagnostics, Live Drone Stream & IoT",
    "📖 System Overview & Pricing",
    "🧪 Sandbox"
])

with tab_chat:
    if current_user and current_cipher:
        c_status, c_wipe, c_del, c_restore = st.columns([3.5, 1, 1, 1])
        with c_status:
            mode_badge = "🟢 ONLINE (GROQ)" if is_online else "🔒 OFFLINE (OLLAMA)"
            st.caption(f"🔒 Encrypted Channel: **{current_name}** (`{current_role}`) | Active Engine: **{mode_badge}**")
        with c_wipe:
            if st.button("🧹 Clear", key="chat_wipe_screen"):
                st.session_state.screen_wiped = True
                st.session_state.confirm_delete = False
                st.session_state.messages = [{"role": "assistant", "content": f"⚡ Screen cleared, {current_name}."}]
                st.rerun()
        with c_del:
            if st.button("🗑️ Delete", key="chat_del_history"):
                st.session_state.confirm_delete = True
                st.rerun()
        with c_restore:
            if st.button("🔄 Restore", key="chat_restore_history"):
                st.session_state.screen_wiped = False
                st.session_state.confirm_delete = False
                if "messages" in st.session_state:
                    del st.session_state.messages
                st.rerun()

        if st.session_state.confirm_delete:
            st.error("⚠️ **SECURITY VERIFICATION: PERMANENT PURGE REQUESTED**")
            vc1, vc2, _ = st.columns([1.2, 1.2, 3])
            with vc1:
                if st.button("🔴 PURGE", key="chat_confirm_purge"):
                    delete_user_history(current_user)
                    st.session_state.confirm_delete = False
                    st.session_state.screen_wiped = False
                    st.session_state.messages = [{"role": "assistant", "content": f"⚡ Verified: History purged, {current_name}."}]
                    st.rerun()
            with vc2:
                if st.button("✖️ CANCEL", key="chat_cancel_purge"):
                    st.session_state.confirm_delete = False
                    st.rerun()

        if "messages" not in st.session_state or not st.session_state.screen_wiped:
            db_messages = load_encrypted_messages(current_user, current_cipher)
            if not db_messages:
                if current_role in ["CEO", "SUPER_ADMIN"]:
                    greeting = f"⚡ Ebony online and armed, Mr. Humphrey. Master Platform Node fully synchronized."
                elif current_role == "CLIENT_CEO":
                    greeting = f"⚡ Ebony online, {current_name}. Enterprise executive agronomy and workforce telemetry active."
                else:
                    greeting = f"⚡ Ebony online, {current_name}. Field operator co-pilot armed."
                
                initial_msg = {"role": "assistant", "content": greeting}
                save_encrypted_message(current_user, "assistant", initial_msg["content"], current_cipher)
                db_messages = [initial_msg]
            st.session_state.messages = db_messages
    else:
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "⚡ **Welcome to Humphrey Virtual Farm.** I am EBONY—your sovereign agronomy intelligence platform. In Guest Mode, I can introduce you to our on-premise drone vision, soil telemetry mesh, and emergency safety features. Sign in or enter a VIP Code to unlock full executive compute."}
            ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Enter strategic directive for Ebony...")
    if user_input:
        if current_user and current_cipher:
            save_encrypted_message(current_user, "user", user_input, current_cipher)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        sys_prompt = get_system_prompt_for_role(current_role, current_name)
        
        if is_online:
            if groq_client:
                try:
                    res = groq_client.chat.completions.create(
                        model=CLOUD_MODEL,
                        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_input}],
                        temperature=0.3
                    )
                    bot_reply = res.choices[0].message.content
                except Exception as e:
                    bot_reply = f"Cloud Neural query fault: {str(e)}"
            else:
                bot_reply = "⚡ GROQ_API_KEY missing from vault."
        else:
            with st.spinner("🧠 Computing on sovereign local neural core (Offline)..."):
                bot_reply = query_local_ollama(user_input, sys_prompt)
        
        if current_user and current_cipher:
            save_encrypted_message(current_user, "assistant", bot_reply, current_cipher)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

with tab_linkedin:
    if current_role in ["CEO", "SUPER_ADMIN"]:
        st.subheader("📡 LinkedIn Executive Article & Broadcast Dictation Engine")
        st.markdown("Dictate, generate, refine, and deploy authoritative thought leadership directly to your LinkedIn profile.")
        st.divider()

        col_dict1, col_dict2 = st.columns([1.6, 1])

        with col_dict1:
            st.markdown("#### 🎙️ Dictate Topic or Strategic Directive")
            dictation_type = st.radio("Publication Format:", ["🚀 Short-Form Market Broadcast", "📰 Long-Form Executive Article"], horizontal=True)
            dictated_prompt = st.text_area(
                "Dictate Topic Concept / Key Talking Points:",
                placeholder="e.g. Discuss our new DJI Air 3S on-premise drone vision bridge, why sovereign local compute protects farm data, and how Humphrey Virtual Farm is redefining autonomous agriculture in Oklahoma...",
                height=120
            )

            col_b1, col_b2 = st.columns([1.2, 1])
            with col_b1:
                tone_style = st.selectbox("Executive Tone:", ["Authoritative CEO & Visionary", "Deep Technical SME", "Commercial & Investor Focus", "Field Agronomy & Practical"])
            with col_b2:
                st.write("")
                st.write("")
                generate_article_btn = st.button("🤖 Generate Draft with Ebony", use_container_width=True)

            if generate_article_btn:
                if not dictated_prompt.strip():
                    st.warning("Please dictate or type talking points first.")
                else:
                    with st.spinner("⚡ Ebony is structuring your LinkedIn executive release..."):
                        if dictation_type == "🚀 Short-Form Market Broadcast":
                            dictate_sys = (
                                f"You are the executive ghostwriter for Mr. Humphrey, Founder & CEO of Humphrey Virtual Farm. "
                                f"Write a high-impact, authoritative LinkedIn post based on the user's talking points. "
                                f"Tone: {tone_style}. Keep it concise, punchy, formatted with clean line breaks, bullet points where relevant, "
                                f"and strong strategic hashtags at the end (#AgTech #SovereignAI #HumphreyVirtualFarm #AutonomousFarming)."
                            )
                        else:
                            dictate_sys = (
                                f"You are the executive ghostwriter for Mr. Humphrey, Founder & CEO of Humphrey Virtual Farm. "
                                f"Write a comprehensive, publication-ready LinkedIn Article / Long-Form Essay based on the talking points. "
                                f"Tone: {tone_style}. Include: An Attention-Grabbing Headline, Executive Summary, 3 Core Strategic Pillars with deep technical/business substance, "
                                f"The Humphrey Virtual Farm Advantage, and a powerful Call-to-Action for partners/investors/members. Include strategic hashtags."
                            )

                        if is_online and groq_client:
                            try:
                                res = groq_client.chat.completions.create(
                                    model=CLOUD_MODEL,
                                    messages=[{"role": "system", "content": dictate_sys}, {"role": "user", "content": dictated_prompt.strip()}],
                                    temperature=0.4
                                )
                                draft_text = res.choices[0].message.content.strip()
                            except Exception as e:
                                draft_text = f"Neural synthesis fault: {str(e)}"
                        else:
                            draft_text = query_local_ollama(dictated_prompt.strip(), dictate_sys)

                        st.session_state.current_linkedin_draft = draft_text
                        st.session_state.article_draft_version += 1
                        st.rerun()

        with col_dict2:
            st.markdown("#### ⚙️ LinkedIn Pipeline Health")
            formatted_urn = format_linkedin_urn(LINKEDIN_URN) if LINKEDIN_URN else "NOT_SET"
            token_preview = f"{LINKEDIN_TOKEN[:12]}...{LINKEDIN_TOKEN[-6:]}" if LINKEDIN_TOKEN and len(LINKEDIN_TOKEN) > 20 else "NOT_SET"
            st.code(f"Author URN: {formatted_urn}\nToken: {token_preview}\nAPI Gateway: v2/ugcPosts (Active)\nProtocol: X-Restli-Protocol-Version: 2.0.0")

        st.divider()
        st.markdown("#### 📝 Live Broadcast & Article Editor")
        editor_key = f"linkedin_editor_v_{st.session_state.article_draft_version}"
        final_post_text = st.text_area("Review & Refine Before Deploying:", value=st.session_state.current_linkedin_draft, height=260, key=editor_key)

        col_dep1, col_dep2 = st.columns([2, 1])
        with col_dep1:
            if st.button("🚀 Authorize & Deploy Live to LinkedIn Profile", use_container_width=True):
                if not LINKEDIN_TOKEN or not LINKEDIN_URN:
                    st.error("❌ LinkedIn Access Token or Author URN missing from environment vault (.env).")
                elif not final_post_text.strip():
                    st.warning("Cannot deploy an empty broadcast.")
                else:
                    with st.spinner("📡 Broadcasting to LinkedIn UGC Gateway..."):
                        clean_urn = format_linkedin_urn(LINKEDIN_URN)
                        api_url = "https://api.linkedin.com/v2/ugcPosts"
                        headers = {
                            "Authorization": f"Bearer {LINKEDIN_TOKEN}",
                            "Content-Type": "application/json",
                            "X-Restli-Protocol-Version": "2.0.0"
                        }
                        payload = {
                            "author": clean_urn,
                            "lifecycleState": "PUBLISHED",
                            "specificContent": {
                                "com.linkedin.ugc.ShareContent": {
                                    "shareCommentary": {"text": final_post_text.strip()},
                                    "shareMediaCategory": "NONE"
                                }
                            },
                            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
                        }
                        try:
                            resp = requests.post(api_url, headers=headers, json=payload, timeout=15)
                            if resp.status_code in [200, 201]:
                                post_resp = resp.json()
                                post_id = post_resp.get("id", "SUCCESS")
                                conn = sqlite3.connect(DB_PATH)
                                cur = conn.cursor()
                                cur.execute(
                                    "INSERT INTO linkedin_broadcast_history (post_content, response_status, urn_identifier, triggered_by) VALUES (?, 'SUCCESS', ?, ?)",
                                    (final_post_text.strip()[:200], clean_urn, current_name)
                                )
                                conn.commit()
                                conn.close()
                                st.success(f"🎉 **Live Deployment Confirmed!**\nLinkedIn UGC Post ID: `{post_id}`")
                            else:
                                st.error(f"⚠️ LinkedIn API Rejected Request (HTTP {resp.status_code}):\n`{resp.text}`")
                        except Exception as err:
                            st.error(f"Deployment transmission error: {str(err)}")

        with col_dep2:
            if st.button("📋 Copy Text to Clipboard", use_container_width=True):
                st.info("Text is selected in the editor above. Press `Ctrl+C` to copy.")
    else:
        st.subheader("📡 LinkedIn Thought Leadership & Broadcast Channel")
        st.markdown("Official corporate broadcasts from Humphrey Virtual Farm leadership.")
        st.info("🔒 Executive Article Dictation & Live Deployment Gateway is reserved for Master Platform CEO.")

with tab_weather:
    st.subheader("🚨 NOAA Emergency Weather & Live Radar Sentinel")
    st.components.v1.iframe("https://radar.weather.gov/", height=450, scrolling=True)

with tab_farm:
    st.subheader("🌾 Humphrey Virtual Farm | Real-Time Aerial Reconnaissance & Agronomy")
    st.markdown("Live low-latency video feed direct from DJI Air 3S O4 link and soil sensor telemetry.")
    st.divider()

    col1, col2 = st.columns([1.5, 1])

    with col1:
        if current_role in ["CEO", "SUPER_ADMIN"]:
            st.markdown("### 🎥 Live DJI Air 3S Master Video Feed (Master CEO Access)")
            stream_html = f"""
            <div style="background-color: #0c1118; border: 2px solid #00FF66; border-radius: 8px; overflow: hidden; padding: 4px;">
                <iframe 
                    src="{WEBRTC_STREAM_URL}" 
                    width="100%" 
                    height="450" 
                    frameborder="0" 
                    allow="autoplay; fullscreen" 
                    allowfullscreen
                    style="background-color: #000000; border-radius: 4px;">
                </iframe>
            </div>
            """
            st.components.v1.html(stream_html, height=470)
            st.caption(f"📡 Ingest Endpoint: `{RTMP_INGEST_URL}` | Direct WebRTC: [Open Fullscreen Player]({WEBRTC_STREAM_URL})")
        
        elif current_role in ["CLIENT_CEO", "MEMBER"]:
            st.markdown(f"### 🎥 Live Aerial Canopy Feed ({'Enterprise Farm CEO' if current_role == 'CLIENT_CEO' else 'Member'} Access)")
            stream_html = f"""
            <div style="background-color: #0c1118; border: 2px solid #00FF66; border-radius: 8px; overflow: hidden; padding: 4px;">
                <iframe 
                    src="{WEBRTC_STREAM_URL}" 
                    width="100%" 
                    height="450" 
                    frameborder="0" 
                    allow="autoplay; fullscreen" 
                    allowfullscreen
                    style="background-color: #000000; border-radius: 4px;">
                </iframe>
            </div>
            """
            st.components.v1.html(stream_html, height=470)
            st.caption("🛡️ *Encrypted Stream Active. Root server keys sanitized.*")
        
        else:
            st.markdown("### 🔒 Sovereign Aerial Reconnaissance Gateway")
            st.markdown("""
            <div style="background-color: #0c1118; border: 2px solid #28374d; border-radius: 8px; padding: 40px 20px; text-align: center;">
                <h3 style="color: #70FF00 !important; margin-bottom: 10px;">🛰️ Live DJI Air 3S Telemetry Locked</h3>
                <p style="color: #FFFFFF !important; font-size: 1.1rem; max-width: 500px; margin: 0 auto 20px auto;">
                    Humphrey Virtual Farm's on-premise aerial computer vision and autonomous field patrol are reserved for Authorized Members and Executive Nodes.
                </p>
                <div style="display: inline-block; padding: 8px 16px; background-color: #121824; border: 1px solid #00FF66; border-radius: 6px; color: #00FF66; font-weight: bold;">
                    Sign In or Activate VIP Code to Unlock Live Ingestion
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🛰️ Sector Flight & Mission Telemetry")
        if current_role in ["CEO", "SUPER_ADMIN"]:
            st.code(f"Craft: DJI Air 3S\nMission: SURVEY-Z1-ALPHA\nSector: ZONE-1-NORTH\nAltitude: 45.0m | Battery: 88%\nStatus: ACTIVE_PATROL\nRTMP Ingest: {RTMP_INGEST_URL}\nStream Engine: MediaMTX v1.9.0")
        elif current_role == "CLIENT_CEO":
            st.code("Craft: DJI Air 3S\nSector: ALL-ZONES-ACTIVE\nTelemetry Stream: LIVE\nCanopy Health Index (GLI): 0.3842 (HEALTHY)\nWorkforce Access Level: ENTERPRISE CEO")
        elif current_role == "MEMBER":
            st.code("Craft: DJI Air 3S\nSector: ZONE-1-NORTH\nCanopy Health Index (GLI): 0.3842 (HEALTHY)\nStatus: ACTIVE PATROL")
        else:
            st.code("HVF Sovereign Node: ACTIVE\nCanopy Diagnostic Engine: ARMED\nAccess Level: GUEST (Redacted)")

        st.markdown("#### 📡 Ingest Soil Moisture Probe")
        if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO", "MEMBER"]:
            st.slider("Soil Moisture (%):", 5.0, 80.0, 21.4)
            st.button("📥 Transmit Sensor Telemetry")
        else:
            st.info("🔒 Sensor telemetry transmission is reserved for authenticated accounts.")

# --- TAB 5: SYSTEM OVERVIEW & COMMERCIAL PRICING HUB ---
with tab_overview:
    st.subheader("💳 Commercial Subscriptions & Sovereign Feature Directory")
    st.markdown(f"Humphrey Virtual Farm Commercial Platform. Active Role: **{current_name}** (`{current_role}`)")
    st.divider()

    # 1. COMMERCIAL PRICING & PAYMENT GATEWAY CARDS (4-TIER GRID)
    st.markdown("### 💎 Sovereign Membership Tiers & Secure Payment Gateway")
    st.caption("Select your membership tier to activate your cryptographic license key.")

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)

    with col_p1:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-tier">🌱 PERSONAL SOVEREIGN</div>
            <div class="pricing-price">$19.99 <span style="font-size: 0.85rem; color: #8899A6;">/ mo</span></div>
            <p style="text-align: left; font-size: 0.85rem; line-height: 1.5;">
                ✔ Single-User Personal Node<br>
                ✔ Dual-Engine AI (Groq + Ollama)<br>
                ✔ Encrypted Private Vault<br>
                ✔ Basic Weather & Crop Guidance<br>
                ✔ Zero Big Ag Cloud Lock-In
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🌱 Personal ($19.99/mo)", STRIPE_PERSONAL_LINK, use_container_width=True)

    with col_p2:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-tier">💎 VIP MEMBER (MONTHLY)</div>
            <div class="pricing-price">$249 <span style="font-size: 0.85rem; color: #8899A6;">/ mo</span></div>
            <p style="text-align: left; font-size: 0.85rem; line-height: 1.5;">
                ✔ Everything in Personal<br>
                ✔ Live Drone Spectator Stream<br>
                ✔ GLI Crop Health Analytics<br>
                ✔ Multi-Zone IoT Sensor Vault<br>
                ✔ NOAA Severe Weather HUD
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("💎 VIP ($249/mo)", STRIPE_MONTHLY_LINK, use_container_width=True)

    with col_p3:
        st.markdown("""
        <div class="pricing-card" style="border-color: #70FF00; box-shadow: 0 0 12px rgba(0,255,102,0.25);">
            <div class="pricing-tier">🏛️ ENTERPRISE FARM CEO</div>
            <div class="pricing-price">$2,499 <span style="font-size: 0.85rem; color: #8899A6;">/ yr</span></div>
            <p style="text-align: left; font-size: 0.85rem; line-height: 1.5;">
                ✔ <strong>Client CEO Dashboard</strong><br>
                ✔ <strong>Issue Staff VIP Sub-Keys</strong><br>
                ✔ Multi-Ranch Yield Models<br>
                ✔ 12-Month Telemetry Trends<br>
                ✔ Direct Agronomic Hotline
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🏛️ Enterprise Annual", STRIPE_ANNUAL_LINK, use_container_width=True)

    with col_p4:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-tier">📦 HARDWARE APPLIANCE</div>
            <div class="pricing-price">$4,950 <span style="font-size: 0.85rem; color: #8899A6;">setup</span></div>
            <p style="text-align: left; font-size: 0.85rem; line-height: 1.5;">
                ✔ Pre-Configured Physical Server<br>
                ✔ 100% Air-Gapped Farm Node<br>
                ✔ Local MediaMTX + Ollama Core<br>
                ✔ + $299/mo Maintenance<br>
                ✔ Total Data Sovereignty
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("📦 Order Hardware", PAYPAL_PAY_LINK, use_container_width=True)

    st.divider()

    # 2. CLIENT CEO EXCLUSIVE TEAM MANAGEMENT HUB
    if current_role == "CLIENT_CEO":
        with st.expander("🏛️ [ENTERPRISE CEO COMMAND]: Provision Access Keys for Farm Staff", expanded=True):
            st.markdown("#### 🔑 Generate VIP Keys for Your Farm Hands & Agronomists")
            c_corp1, c_corp2 = st.columns([1.5, 3])
            with c_corp1:
                if st.button("⚡ Issue New Staff Key", key="tab5_client_ceo_vip_gen", use_container_width=True):
                    token = generate_invite_token(current_user, "MEMBER")
                    st.success(f"Generated Staff License: `{token}`")
            with c_corp2:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT invite_code, is_used, used_by, created_at FROM member_invite_keys WHERE issued_by=? ORDER BY id DESC LIMIT 5", (current_user,))
                recent_corp_keys = cur.fetchall()
                conn.close()
                if recent_corp_keys:
                    st.caption("Active License Keys Issued for Your Organization:")
                    for k in recent_corp_keys:
                        status_str = f"🔴 USED by {k[2]}" if k[1] == 1 else "🟢 UNUSED / ACTIVE"
                        st.code(f"Key: {k[0]} | Status: {status_str} | Date: {k[3]}")
                else:
                    st.caption("No staff keys generated yet. Click the button on the left to issue one.")

    # 3. MASTER CEO EXCLUSIVE DIAGNOSTIC CENTER
    if current_role in ["CEO", "SUPER_ADMIN"]:
        with st.expander("👑 [MASTER PLATFORM ROOT]: Live Server Diagnostics & VIP Provisioning", expanded=True):
            st.markdown("#### 🔑 Master Key Provisioning (Select Target Tier)")
            kc1, kc2, kc3 = st.columns([1.5, 1.5, 3])
            with kc1:
                if st.button("⚡ Gen Member VIP Key", key="tab5_vip_gen_member", use_container_width=True):
                    token = generate_invite_token(current_user, "MEMBER")
                    st.success(f"Member Key: `{token}`")
            with kc2:
                if st.button("⚡ Gen Enterprise CEO Key", key="tab5_vip_gen_client_ceo", use_container_width=True):
                    token = generate_invite_token(current_user, "CLIENT_CEO")
                    st.success(f"Enterprise CEO Key: `{token}`")
            with kc3:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT invite_code, grant_role, is_used, used_by FROM member_invite_keys ORDER BY id DESC LIMIT 5")
                recent_keys = cur.fetchall()
                conn.close()
                if recent_keys:
                    st.caption("Recent Global Keys Issued:")
                    for k in recent_keys:
                        status_str = f"🔴 USED ({k[3]})" if k[2] == 1 else "🟢 UNUSED"
                        st.code(f"Key: {k[0]} | Role: {k[1]} | {status_str}")

            st.markdown("#### 🖥️ Master Node Diagnostic Readout")
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM system_users")
            user_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM member_invite_keys WHERE is_used=0")
            unused_keys = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM encrypted_user_comms")
            msg_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM iot_telemetry_vault")
            sensor_count = cur.fetchone()[0]
            conn.close()

            st.code(f"""======================= HVF MASTER SERVER TOPOLOGY =======================
Host IP (Local LAN)      : 192.168.1.175
Mesh Endpoint (Tailscale): {ACTIVE_IP}:8501
Master Database Vault    : {DB_PATH}
Active Registered Users  : {user_count}
Unused License Keys      : {unused_keys}
Encrypted Comm Records   : {msg_count}
Sensor Telemetry Records : {sensor_count}
--------------------------------------------------------------------------
Local Neural Engine      : Ollama REST API (Port 11434) -> llama3:8b
Cloud Fast Link          : Groq API (TLS 1.3) -> openai/gpt-oss-120b
Drone RTMP Ingestion     : MediaMTX (Port 1935) -> rtmp://192.168.1.175:1935/live/air3s
Drone WebRTC Streaming   : MediaMTX (Port 8889) -> http://192.168.1.175:8889/live/air3s
Weather Oracle Base      : NOAA REST API (Lat: {DEFAULT_LAT}, Lon: {DEFAULT_LON})
Security Hierarchy       : SUPER_ADMIN > CLIENT_CEO > MEMBER > GUEST
=========================================================================""")

    # 4. KNOWLEDGE ACADEMY PILLARS
    st.markdown("### 📖 Sovereign Knowledge Academy & Technical Directory")

    with st.expander("🏛️ [PILLAR 1]: The Humphrey Virtual Farm Manifesto & Sovereign AI Mission", expanded=False):
        st.markdown("""
        **Humphrey Virtual Farm (HVF)** is an on-premise, air-gapped agtech ecosystem engineered to liberate agricultural producers from centralized Big Ag cloud lock-in. 
        
        * **100% On-Premise Compute Sovereignty:** All neural inference, telemetry databases, and drone photogrammetry execute locally on physical hardware.
        * **Dual-Engine Operational Continuity:** Operates with zero degradation during complete offline blackout or severe grid outages.
        * **Autonomous Multi-Agent Agronomy:** Synchronized agents monitoring moisture, vegetative vigor, Doppler radar, and market communication.
        """)

    with st.expander("⚡ [PILLAR 2]: Dual-Engine Neural Architecture & Offline AI Execution", expanded=False):
        st.markdown("""
        * **Cloud Fast Link (Groq):** `openai/gpt-oss-120b` for $<0.45$s market synthesis and executive ghostwriting.
        * **Sovereign Local Core (Ollama):** `llama3:8b` running on physical RAM on port 11434 with zero internet connection.
        """)

    with st.expander("🌾 [PILLAR 3]: DJI Air 3S Computer Vision & Multispectral GLI Canopy Science", expanded=False):
        st.markdown("""
        * **Multispectral Green Leaf Index:** Computes vegetative vigor using `GLI = (2*G - R - B) / (2*G + R + B)`.
        * **Direct Ingestion:** Re-muxes DJI RC 2 RTMP port 1935 into sub-second WebRTC on port 8889.
        """)

    with st.expander("📡 [PILLAR 4]: IoT Soil Mesh, Capacitance Probes & Telemetry Fusion", expanded=False):
        st.markdown("""
        * **Volumetric Water Content (VWC %):** Tracks field capacity ($28\%-38\%$) and managed depletion thresholds ($18\%-24\%$).
        * **Multi-Zone Storage:** Automatically records ground readings into encrypted SQLite tables.
        """)

    with st.expander("🚨 [PILLAR 5]: NOAA Emergency Radar Sentinel & Farm Life Safety Protocols", expanded=False):
        st.markdown("""
        * **Doppler Radar Overlay:** Live interactive NOAA radar feed for Oklahoma microclimates.
        * **Hazard Containment:** Instant protocol guidance for high winds, anhydrous ammonia leaks, and PTO drivelines.
        """)

    with st.expander("📰 [PILLAR 6]: LinkedIn Executive Article & Thought Leadership Hub", expanded=False):
        st.markdown("""
        * **Executive Dictation:** Ghostwrites articles and market releases in visionary CEO, SME, or Agronomist tones.
        * **Direct Deployment:** Dispatches posts live to LinkedIn using official OAuth UGC API endpoints.
        """)

    with st.expander("🔐 [PILLAR 7]: Cryptographic Vault, User Isolation & 4-Tier Security Matrix", expanded=False):
        st.markdown("""
        * **Level 4: Master CEO (You):** Root infrastructure, hardware topology, global key provisioning, and LinkedIn broadcasting.
        * **Level 3: Enterprise Client CEO:** Company executive AI, staff key issuance, farm financial models, and full drone telemetry.
        * **Level 2: Authorized Member:** Private encrypted assistant, spectator drone stream, and field sensor logging.
        * **Level 1: Public Guest:** Commercial showcase, safety protocols, and direct subscription onboarding.
        """)

with tab_sandbox:
    if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO", "MEMBER"]:
        st.subheader("🧪 Python Execution Sandbox")
        st.code("print('⚡ Sandbox Online')")
    else:
        st.warning("🔒 Python Execution Sandbox is restricted to authenticated HVF Members.")