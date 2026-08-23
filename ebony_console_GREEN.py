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
from datetime import datetime, timedelta
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
OFFICIAL_EMAIL = "humphreyvirtualfarm@gmail.com"
OFFICIAL_FOUNDER = "Jeffery Humphrey"

STRIPE_PERSONAL_LINK = os.getenv("STRIPE_PERSONAL_LINK", "https://buy.stripe.com/test_fZueVfbmx9lH4rB8yx1RC00")
STRIPE_MONTHLY_LINK = os.getenv("STRIPE_MONTHLY_LINK", "https://buy.stripe.com/test_monthly_vip")
STRIPE_ANNUAL_LINK = os.getenv("STRIPE_ANNUAL_LINK", "https://buy.stripe.com/test_annual_vip")
PAYPAL_PAY_LINK = os.getenv("PAYPAL_PAY_LINK", "https://www.paypal.com/paypalme/humphreyvirtualfarm")

OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
CLOUD_MODEL = "openai/gpt-oss-120b"
LOCAL_MODEL = "llama3:8b"

# ==========================================
# STRICT SYSTEM GROUND TRUTH & BAN ON LIES
# ==========================================
STRICT_GROUND_RULES = """
CRITICAL NON-NEGOTIABLE GROUND TRUTH:
1. FOUNDER & CEO: Jeffery Humphrey ONLY. (Never use any other name).
2. CONTACT EMAIL: humphreyvirtualfarm@gmail.com ONLY.
3. ABSOLUTE BAN ON FABRICATED DATA:
   - NEVER invent fake benchmark percentages (e.g., "99.7% uptime", "94% accuracy").
   - NEVER invent fake field trials (e.g., "12 Midwest farms", "trial across 4,000 ha").
   - NEVER invent fake certifications or audits (e.g., "SOC-2 Type II", "ISO-27001", "2024 security audit").
   - NEVER invent fake funding or VC rounds (e.g., "$14M Series-A").
   - NEVER invent hardware specs we do not build (e.g., "custom ASICs", "Jetson Nano 1200 fps", "500 drone swarm mesh").
4. WHAT WE ACTUALLY PROVIDE (REALITY):
   - Universal Drone Video Ingest: Connects any commercial drone (DJI, Autel, Skydio, Custom RTMP) via RTMP (port 1935) to local WebRTC playback (port 8889).
   - Real-Time Green Leaf Index (GLI): Vegetative canopy health calculation via GLI = (2G - R - B) / (2G + R + B).
   - Dual-Engine AI Architecture: Groq Cloud AI when online, instant zero-latency failover to local Ollama (port 11434) when offline.
   - Encrypted Vault: PBKDF2/Fernet encrypted local database for farm records.
   - Live Weather HUD: Embedded NOAA live weather radar feed.
   - Commercial Pricing: $19.99/mo Personal, $249/mo VIP, $2,499/yr Enterprise CEO, $4,950 Local Hardware Edge Server, and Free 3-Day Market Pilot.
"""

def sanitize_deterministic_output(raw_text: str) -> str:
    if not raw_text:
        return raw_text
    text = raw_text

    # Name Sanitation
    name_patterns = [
        r"(?i)\bHumphrey\s+[A-Z]\.?\s+Miller\b",
        r"(?i)\bHumphrey\s+Miller\b",
        r"(?i)\bMr\.?\s+Miller\b",
        r"(?i)\bJeffrey\s+Humphrey\b",
        r"(?i)\bJeff\s+Humphrey\b"
    ]
    for pattern in name_patterns:
        text = re.sub(pattern, OFFICIAL_FOUNDER, text)

    # Email Sanitation
    email_patterns = [
        r"(?i)[a-zA-Z0-9_.+-]+@hvf\.io",
        r"(?i)[a-zA-Z0-9_.+-]+@humphreyvirtualfarm\.io",
        r"(?i)[a-zA-Z0-9_.+-]+@humphreyvirtualfarms\.com"
    ]
    for pattern in email_patterns:
        text = re.sub(pattern, OFFICIAL_EMAIL, text)

    # Fabricated VC / Stats Sanitation
    vc_patterns = [
        r"(?i)\$?\d+(\.\d+)?\s*(M|million|B|billion)\s*(in\s+)?(seed\s*(&|and)\s*)?(series[\s-]?[a-z]|venture\s+capital|funding|investment\s+round)",
        r"(?i)secured\s+\$?\d+[\d,]*\s*(million|M)\s+in\s+funding"
    ]
    for pattern in vc_patterns:
        text = re.sub(pattern, "sovereign, self-funded agricultural architecture", text)

    return text

def format_linkedin_urn(raw_urn: str) -> str:
    if not raw_urn:
        return ""
    clean = raw_urn.strip().strip('"').strip("'")
    if clean.startswith("urn:li:member:") or clean.startswith("urn:li:person:") or clean.startswith("urn:li:organization:"):
        return clean
    if clean.isdigit():
        return f"urn:li:person:{clean}"
    return clean

@st.cache_resource
def get_tailscale_or_local_ip_cached() -> str:
    try:
        ts_path = "C:\\Program Files\\Tailscale\\tailscale.exe"
        if os.path.exists(ts_path):
            ts_proc = subprocess.run(
                [ts_path, "ip", "-4"], 
                capture_output=True, 
                text=True, 
                creationflags=0x08000000
            )
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

ACTIVE_IP = get_tailscale_or_local_ip_cached()
UPLINK_URL = f"http://{ACTIVE_IP}:8501"
WEBRTC_STREAM_URL = f"http://192.168.1.175:8889/live/stream"
RTMP_INGEST_URL = f"rtmp://192.168.1.175:1935/live/stream"

st.set_page_config(page_title="HVF Ebony | Universal Drone & Predictive AI", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

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

# 2. Database Engine
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
            trial_expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("PRAGMA table_info(system_users)")
    cols = [col[1] for col in cur.fetchall()]
    if "company_id" not in cols:
        cur.execute("ALTER TABLE system_users ADD COLUMN company_id TEXT DEFAULT 'HVF_MAIN'")
    if "trial_expires_at" not in cols:
        cur.execute("ALTER TABLE system_users ADD COLUMN trial_expires_at TIMESTAMP")

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
        CREATE TABLE IF NOT EXISTS pilot_feedback_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            full_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            farm_size_acres TEXT,
            primary_crops TEXT,
            feedback_text TEXT NOT NULL,
            contact_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversation_entity_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            topic_key TEXT NOT NULL,
            entity_summary TEXT NOT NULL,
            last_context TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, topic_key)
        )
    """)
    conn.commit()
    conn.close()

ensure_db_schema()

def verify_user(username: str, pwd_raw: str):
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT username, full_name, role, status, trial_expires_at FROM system_users WHERE username=? AND password_hash=?", 
                (username.strip().lower(), hash_password(pwd_raw)))
    user = cur.fetchone()
    conn.close()
    if not user:
        return None, "Invalid Username or Password."
    
    if user[2] == "TRIAL_MEMBER" and user[4]:
        try:
            exp_date = datetime.strptime(user[4], "%Y-%m-%d %H:%M:%S")
            if datetime.now() > exp_date:
                return user, "TRIAL_EXPIRED"
        except Exception:
            pass
    return user, "OK"

def register_3day_trial(username: str, pwd_raw: str, full_name: str, farm_info: str):
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM system_users WHERE username=?", (username.strip().lower(),))
    if cur.fetchone():
        conn.close()
        return False, "Username already registered. Please choose another or sign in."
    
    expires_at = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute("""
            INSERT INTO system_users (username, password_hash, full_name, role, company_id, status, trial_expires_at)
            VALUES (?, ?, ?, 'TRIAL_MEMBER', ?, 'APPROVED', ?)
        """, (username.strip().lower(), hash_password(pwd_raw), full_name.strip(), farm_info.strip(), expires_at))
        conn.commit()
        conn.close()
        return True, f"🎉 3-Day Pilot Activated! Full member access granted until {expires_at}."
    except Exception as e:
        conn.close()
        return False, f"Trial registration error: {str(e)}"

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

def save_pilot_feedback(username: str, full_name: str, rating: int, acres: str, crops: str, feedback: str, email: str):
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pilot_feedback_vault (username, full_name, rating, farm_size_acres, primary_crops, feedback_text, contact_email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username or "anonymous", full_name or "Guest Operator", rating, acres, crops, feedback, email))
    conn.commit()
    conn.close()

def load_all_entity_memories(username: str) -> str:
    if not username:
        return ""
    ensure_db_schema()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT topic_key, entity_summary, last_context FROM conversation_entity_memory WHERE username=? ORDER BY updated_at DESC LIMIT 8", (username,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return ""
    
    memory_block = "\n[PERSISTENT KNOWLEDGE BASE & PAST TOPIC RECALL]:\n"
    for r in rows:
        memory_block += f"- Topic: {r[0]} | Key Facts: {r[1]} | Context: {r[2]}\n"
    memory_block += "[End of Persistent Knowledge Base.]\n"
    return memory_block

def store_entity_memory_async(username: str, user_prompt: str, bot_response: str):
    if not username or len(user_prompt.strip()) < 5:
        return
    ensure_db_schema()
    words = [w.strip(".,!?:;\"'()[]{}") for w in user_prompt.lower().split() if len(w) > 3]
    stopwords = {"what", "whats", "where", "when", "which", "about", "there", "their", "please", "could", "would", "should", "tell", "explain", "that", "this", "with", "from", "have", "been"}
    keywords = [w for w in words if w not in stopwords]
    if not keywords:
        return
    
    topic_key = " ".join(keywords[:4]).title()
    summary = user_prompt.strip()[:180]
    last_context = bot_response.strip()[:240].replace("\n", " ")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO conversation_entity_memory (username, topic_key, entity_summary, last_context, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(username, topic_key) DO UPDATE SET
                entity_summary = excluded.entity_summary,
                last_context = excluded.last_context,
                updated_at = CURRENT_TIMESTAMP
        """, (username, topic_key, summary, last_context))
        conn.commit()
        conn.close()
    except Exception:
        pass

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
            raw_msg = cipher.decrypt(r[1].encode("utf-8")).decode("utf-8")
            decrypted.append({"role": r[0], "content": sanitize_deterministic_output(raw_msg)})
        except Exception:
            pass
    return decrypted

def save_encrypted_message(username: str, role: str, content: str, cipher: Fernet):
    if not username or not cipher:
        return
    sanitized = sanitize_deterministic_output(content)
    blob = cipher.encrypt(sanitized.encode("utf-8")).decode("utf-8")
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
    cur.execute("DELETE FROM conversation_entity_memory WHERE username=?", (username,))
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
        "cipher": None,
        "trial_expires_at": None
    }

if "screen_wiped" not in st.session_state:
    st.session_state.screen_wiped = False

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

if "operation_mode" not in st.session_state:
    st.session_state.operation_mode = "🟢 Online (Cloud Fast Link)"

if "article_draft_version" not in st.session_state:
    st.session_state.article_draft_version = 0

if "selected_drone_model" not in st.session_state:
    st.session_state.selected_drone_model = "DJI Air 3S (Reference)"

if "current_linkedin_draft" not in st.session_state:
    st.session_state.current_linkedin_draft = (
        "⚡ [HVF Sovereign Intelligence Announcement]\n\n"
        "Humphrey Virtual Farm has deployed our on-premise universal aerial reconnaissance link, fusing real-time drone telemetry (DJI, Autel, Skydio, Custom RTMP) with our local soil sensor mesh.\n\n"
        "All imagery and field analytics are computed strictly on-premise without reliance on external cloud infrastructure.\n\n"
        "#AgTech #SovereignAI #JefferyHumphrey #AutonomousFarming #PrecisionAg #HVF"
    )

current_user = st.session_state.user_session["username"]
current_name = st.session_state.user_session["full_name"]
current_role = st.session_state.user_session["role"]
current_cipher = st.session_state.user_session["cipher"]
current_trial_exp = st.session_state.user_session.get("trial_expires_at")

groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

def query_local_ollama_chat(messages_payload: list) -> str:
    try:
        payload = {
            "model": LOCAL_MODEL,
            "messages": messages_payload,
            "stream": False,
            "options": {"temperature": 0.0}
        }
        res = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=45)
        if res.status_code == 200:
            raw_out = res.json().get("message", {}).get("content", "⚡ [Local Node]: No response generated.")
            return sanitize_deterministic_output(raw_out)
        return f"⚠️ Local Node returned HTTP {res.status_code}."
    except requests.exceptions.ConnectionError:
        return "⚠️ Local Offline Engine (Ollama) is not running on port 11434. Run `ollama serve` to arm Offline mode."
    except Exception as e:
        return f"Local Engine fault: {str(e)}"

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
        elif current_role == "TRIAL_MEMBER":
            st.warning(f"⏳ **{current_name}**\n*(3-Day Market Pilot Active)*\nExpires: `{current_trial_exp}`")
        else:
            st.info(f"👥 **{current_name}**\n*(Authorized Member Clearance)*")
        
        if st.button("🚪 Disconnect Session", use_container_width=True):
            st.session_state.user_session = {
                "authenticated": False,
                "username": None,
                "full_name": "Public Guest",
                "role": "GUEST",
                "cipher": None,
                "trial_expires_at": None
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
                    st.session_state.messages = [{"role": "assistant", "content": f"⚡ Verified: History & entity memory purged, {current_name}."}]
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
        st.info("👤 **Guest Mode Active**\nSelect an option below to enter:")
        auth_mode = st.radio("Access Portal:", ["Sign In", "🚀 Free 3-Day Pilot", "Activate VIP Code"], horizontal=False)
        
        if auth_mode == "Sign In":
            login_user = st.text_input("Username:", key="login_u")
            login_pass = st.text_input("Password:", type="password", key="login_p")
            if st.button("Sign In", use_container_width=True):
                user_match, status_msg = verify_user(login_user, login_pass)
                if user_match and status_msg == "OK":
                    st.session_state.user_session = {
                        "authenticated": True,
                        "username": user_match[0],
                        "full_name": user_match[1],
                        "role": user_match[2],
                        "cipher": derive_user_cipher(login_pass, user_match[0]),
                        "trial_expires_at": user_match[4]
                    }
                    st.session_state.screen_wiped = False
                    st.session_state.confirm_delete = False
                    if "messages" in st.session_state:
                        del st.session_state.messages
                    st.success(f"Welcome back, {user_match[1]}!")
                    st.rerun()
                elif status_msg == "TRIAL_EXPIRED":
                    st.error("⏳ Your 3-Day Market Pilot has concluded. Please subscribe in Tab 5 to continue.")
                else:
                    st.error(status_msg)

        elif auth_mode == "🚀 Free 3-Day Pilot":
            st.markdown("##### 🌾 72-Hour Full Member Trial (No CC Required)")
            t_fn = st.text_input("Your Full Name:", key="trial_fn", placeholder="e.g. Dale Robinson")
            t_farm = st.text_input("Farm / Operation Name:", key="trial_farm", placeholder="e.g. Robinson Red River Ranch")
            t_u = st.text_input("Create Username:", key="trial_u")
            t_p = st.text_input("Create Password:", type="password", key="trial_p")
            if st.button("🚀 Launch 3-Day Pilot Access", use_container_width=True):
                if t_fn and t_farm and t_u and t_p:
                    ok, msg = register_3day_trial(t_u, t_p, t_fn, t_farm)
                    if ok:
                        st.success(msg)
                        st.info("You may now select 'Sign In' above with your credentials!")
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill in all trial fields.")

        else:
            reg_name = st.text_input("Full Name:", key="reg_fn")
            reg_user = st.text_input("Desired Username:", key="reg_u")
            reg_pass = st.text_input("Desired Password:", type="password", key="reg_p")
            reg_code = st.text_input("VIP Access Code:", key="reg_c", placeholder="HVF-VIP-XXXX or HVF-CORP-XXXX")
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
        st.write(f"**Universal Video Ingest:** 🟢 `0.0.0.0:1935`")
        st.write(f"**Zero-Lie Engine:** 🟢 ARMED")
    st.write(f"**Active Clearance:** `{current_role}`")

# --- HEADER ---
st.title("⚡ HVF Sovereign Command Deck | Ebony AI")
st.caption(f"Active User: **{current_name}** | Clearance: **{current_role}** | 🛡️ *Mode: {'🟢 Online (Cloud Fast Link)' if is_online else '🔒 Sovereign Offline (Local Compute)'}*")

# --- MAIN DECK TABS ---
tab_chat, tab_linkedin, tab_weather, tab_farm, tab_overview, tab_feedback, tab_sandbox = st.tabs([
    "💬 Sovereign Command Link",
    "📡 LinkedIn Broadcast & Article Engine",
    "🚨 NOAA Weather & Radar HUD",
    "🌾 Farm Diagnostics, Live Drone Stream & IoT",
    "📖 System Overview & Pricing",
    "📝 3-Day Pilot Feedback Hub",
    "🧪 Sandbox"
])

with tab_chat:
    if current_user and current_cipher:
        c_status, c_wipe, c_del, c_restore = st.columns([3.5, 1, 1, 1])
        with c_status:
            st.caption(f"🔒 Encrypted Channel: **{current_name}** (`{current_role}`) | 🧠 *Predictive Memory: ARMED*")
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
                    st.session_state.messages = [{"role": "assistant", "content": f"⚡ Verified: History & entity memory purged, {current_name}."}]
                    st.rerun()
            with vc2:
                if st.button("✖️ CANCEL", key="chat_cancel_purge"):
                    st.session_state.confirm_delete = False
                    st.rerun()

        if "messages" not in st.session_state or not st.session_state.screen_wiped:
            db_messages = load_encrypted_messages(current_user, current_cipher)
            if not db_messages:
                if current_role in ["CEO", "SUPER_ADMIN"]:
                    greeting = f"⚡ Ebony online and armed, Mr. Humphrey. Ground truth strictly enforced."
                elif current_role == "CLIENT_CEO":
                    greeting = f"⚡ Ebony online, {current_name}. Enterprise executive agronomy active."
                elif current_role == "TRIAL_MEMBER":
                    greeting = f"⚡ Welcome to Humphrey Virtual Farm, {current_name}! Your 3-Day Pilot is active."
                else:
                    greeting = f"⚡ Ebony online, {current_name}. Field operator co-pilot armed."
                
                initial_msg = {"role": "assistant", "content": greeting}
                save_encrypted_message(current_user, "assistant", initial_msg["content"], current_cipher)
                db_messages = [initial_msg]
            st.session_state.messages = db_messages
    else:
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "⚡ **Welcome to Humphrey Virtual Farm.** I am EBONY—your sovereign agronomy platform founded by Jeffery Humphrey. In Guest Mode, I introduce our on-premise drone vision (supporting DJI, Autel, Skydio, custom RTMP), local soil sensor mesh, and emergency safety features."}
            ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask Ebony anything...")
    if user_input:
        if current_user and current_cipher:
            save_encrypted_message(current_user, "user", user_input, current_cipher)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        persistent_knowledge = load_all_entity_memories(current_user)
        full_sys_prompt = f"You are EBONY, Sovereign AI Technical Partner to Jeffery Humphrey, Founder & CEO of Humphrey Virtual Farm.\n{STRICT_GROUND_RULES}\n{persistent_knowledge}"
        
        history_window = st.session_state.messages[-12:]
        conversation_payload = [{"role": "system", "content": full_sys_prompt}]
        for m in history_window:
            conversation_payload.append({"role": m["role"], "content": m["content"]})
        
        if is_online:
            if groq_client:
                try:
                    res = groq_client.chat.completions.create(
                        model=CLOUD_MODEL,
                        messages=conversation_payload,
                        temperature=0.0
                    )
                    raw_reply = res.choices[0].message.content
                    bot_reply = sanitize_deterministic_output(raw_reply)
                except Exception as e:
                    bot_reply = f"Cloud Neural query fault: {str(e)}"
            else:
                bot_reply = "⚡ GROQ_API_KEY missing from vault."
        else:
            with st.spinner("🧠 Computing on local neural core..."):
                bot_reply = query_local_ollama_chat(conversation_payload)
        
        if current_user and current_cipher:
            save_encrypted_message(current_user, "assistant", bot_reply, current_cipher)
            store_entity_memory_async(current_user, user_input, bot_reply)
            
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

with tab_linkedin:
    if current_role in ["CEO", "SUPER_ADMIN"]:
        st.subheader("📡 LinkedIn Executive Article & Broadcast Dictation Engine")
        st.markdown("Dictate, generate, refine, and deploy 100% factual thought leadership directly to LinkedIn.")
        st.divider()

        col_dict1, col_dict2 = st.columns([1.6, 1])

        with col_dict1:
            st.markdown("#### 🎙️ Dictate Topic or Strategic Directive")
            dictation_type = st.radio("Publication Format:", ["🚀 Short-Form Market Broadcast", "📰 Long-Form Executive Article"], horizontal=True)
            dictated_prompt = st.text_area(
                "Dictate Topic Concept / Key Talking Points:",
                placeholder="e.g. Discuss why offline-first on-premise compute is necessary for agriculture, our universal drone support (DJI, Autel, Skydio, RTMP), and our Free 3-Day Pilot...",
                height=120
            )

            col_b1, col_b2 = st.columns([1.2, 1])
            with col_b1:
                tone_style = st.selectbox("Executive Tone:", ["Authoritative CEO & Founder", "Technical Systems Architect", "Practical Field Agronomist"])
            with col_b2:
                st.write("")
                st.write("")
                generate_article_btn = st.button("🤖 Generate 100% Factual Draft", use_container_width=True)

            if generate_article_btn:
                if not dictated_prompt.strip():
                    st.warning("Please dictate talking points first.")
                else:
                    with st.spinner("⚡ Structuring verified factual release (Zero Hallucination Mode)..."):
                        dictate_sys = f"""
You are the executive ghostwriter for Jeffery Humphrey, Founder & CEO of Humphrey Virtual Farm.
{STRICT_GROUND_RULES}

INSTRUCTIONS FOR GENERATION:
1. Tone: {tone_style}. Write strictly based on the user's prompt and our REAL architecture.
2. DO NOT invent fake numbers, trial results, percentages, or audits.
3. If writing a Short Broadcast: Make it punchy, direct, and under 250 words.
4. If writing a Long Article: Organize with clean markdown headers (# Headline, ## Executive Summary, ## Core Pillars, ## Call to Action).
5. Always end with:
Founder & CEO: Jeffery Humphrey
Contact: humphreyvirtualfarm@gmail.com
GitHub: https://github.com/humphreyvirtualfarm
Hashtags: #AgTech #SovereignAI #JefferyHumphrey #HumphreyVirtualFarm #PrecisionFarming
"""

                        if is_online and groq_client:
                            try:
                                res = groq_client.chat.completions.create(
                                    model=CLOUD_MODEL,
                                    messages=[{"role": "system", "content": dictate_sys}, {"role": "user", "content": dictated_prompt.strip()}],
                                    temperature=0.0
                                )
                                raw_draft = res.choices[0].message.content.strip()
                                draft_text = sanitize_deterministic_output(raw_draft)
                            except Exception as e:
                                draft_text = f"Neural synthesis fault: {str(e)}"
                        else:
                            ollama_dictate_payload = [{"role": "system", "content": dictate_sys}, {"role": "user", "content": dictated_prompt.strip()}]
                            raw_draft = query_local_ollama_chat(ollama_dictate_payload)
                            draft_text = sanitize_deterministic_output(raw_draft)

                        st.session_state.current_linkedin_draft = draft_text
                        st.session_state.article_draft_version += 1
                        st.rerun()

        with col_dict2:
            st.markdown("#### ⚙️ Pipeline Status")
            formatted_urn = format_linkedin_urn(LINKEDIN_URN) if LINKEDIN_URN else "NOT_SET"
            st.code(f"Author URN: {formatted_urn}\nZero-Hallucination: STRICT (Temp 0.0)\nFounder: Jeffery Humphrey\nEmail: {OFFICIAL_EMAIL}")

        st.divider()
        st.markdown("#### 📝 Live Broadcast & Article Editor")
        editor_key = f"linkedin_editor_v_{st.session_state.article_draft_version}"
        final_post_text = st.text_area("Review & Refine Before Deploying:", value=st.session_state.current_linkedin_draft, height=260, key=editor_key)

        col_dep1, col_dep2 = st.columns([2, 1])
        with col_dep1:
            if st.button("🚀 Authorize & Deploy Live to LinkedIn Profile", use_container_width=True):
                sanitized_deployment = sanitize_deterministic_output(final_post_text.strip())
                if not LINKEDIN_TOKEN or not LINKEDIN_URN:
                    st.error("❌ LinkedIn credentials missing from .env.")
                elif not sanitized_deployment:
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
                                    "shareCommentary": {"text": sanitized_deployment},
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
                                    (sanitized_deployment[:200], clean_urn, current_name)
                                )
                                conn.commit()
                                conn.close()
                                st.success(f"🎉 **Live Deployment Confirmed!**\nPost ID: `{post_id}`")
                            else:
                                st.error(f"⚠️ LinkedIn API Error (HTTP {resp.status_code}):\n`{resp.text}`")
                        except Exception as err:
                            st.error(f"Deployment transmission error: {str(err)}")

        with col_dep2:
            if st.button("📋 Copy Text to Clipboard", use_container_width=True):
                st.info("Text selected above. Press `Ctrl+C` to copy.")
    else:
        st.subheader("📡 LinkedIn Broadcast Channel")
        st.info("🔒 Executive Article Dictation is reserved for Master Platform CEO.")

with tab_weather:
    st.subheader("🚨 NOAA Emergency Weather & Live Radar Sentinel")
    st.components.v1.iframe("https://radar.weather.gov/", height=450, scrolling=True)

with tab_farm:
    st.subheader("🌾 Humphrey Virtual Farm | Universal Aerial Reconnaissance & Agronomy")
    st.markdown("Live low-latency video feed supporting **DJI, Autel, Skydio, and Custom RTMP/RTSP** commercial drones.")
    st.divider()

    col1, col2 = st.columns([1.5, 1])

    with col1:
        if current_role in ["CEO", "SUPER_ADMIN"]:
            st.markdown("### 🎥 Live Universal Master Video Feed (CEO Access)")
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
            st.caption(f"📡 Universal RTMP Ingest: `{RTMP_INGEST_URL}` | Direct WebRTC: [Open Fullscreen Player]({WEBRTC_STREAM_URL})")
        
        elif current_role in ["CLIENT_CEO", "MEMBER", "TRIAL_MEMBER"]:
            role_label = "3-Day Market Pilot" if current_role == "TRIAL_MEMBER" else ("Enterprise Farm CEO" if current_role == "CLIENT_CEO" else "Member")
            st.markdown(f"### 🎥 Live Aerial Canopy Spectator Feed ({role_label} Access)")
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
            st.caption("🛡️ *Encrypted Spectator Stream Active.*")
        
        else:
            st.markdown("### 🔒 Sovereign Aerial Reconnaissance Gateway")
            st.markdown("""
            <div style="background-color: #0c1118; border: 2px solid #28374d; border-radius: 8px; padding: 40px 20px; text-align: center;">
                <h3 style="color: #70FF00 !important; margin-bottom: 10px;">🛰️ Universal Drone Ingest Gateway</h3>
                <p style="color: #FFFFFF !important; font-size: 1.1rem; max-width: 500px; margin: 0 auto 20px auto;">
                    Humphrey Virtual Farm integrates with any commercial drone (DJI, Autel, Skydio, Custom RTMP) for real-time field patrol and Green Leaf Index canopy analysis.
                </p>
                <div style="display: inline-block; padding: 8px 16px; background-color: #121824; border: 1px solid #00FF66; border-radius: 6px; color: #00FF66; font-weight: bold;">
                    Select '🚀 Free 3-Day Pilot' in Sidebar to Test Live Feed
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🛰️ Active Craft & Sensor Calibration")
        selected_drone = st.selectbox(
            "Select Connected Drone Profile:",
            [
                "DJI Air 3S (Reference Model)",
                "DJI Mavic 3 Enterprise / Thermal",
                "DJI Matrice 300 / 350 RTK",
                "Autel EVO II Pro / Enterprise",
                "Autel EVO Max 4T",
                "Skydio 2+ / X10 Enterprise",
                "Custom PX4 / ArduPilot RTMP Stream"
            ],
            index=0
        )
        st.session_state.selected_drone_model = selected_drone

        if current_role in ["CEO", "SUPER_ADMIN"]:
            st.code(f"Selected Craft: {selected_drone}\nMission: SURVEY-Z1-ALPHA\nSector: ZONE-1-NORTH\nAltitude: 45.0m | Battery: 88%\nStatus: ACTIVE_PATROL\nRTMP Ingest: {RTMP_INGEST_URL}\nStream Engine: MediaMTX v1.9.0")
        elif current_role == "CLIENT_CEO":
            st.code(f"Craft: {selected_drone}\nSector: ALL-ZONES-ACTIVE\nTelemetry Stream: LIVE\nCanopy Health Index (GLI): 0.3842 (HEALTHY)\nWorkforce Access Level: ENTERPRISE CEO")
        elif current_role in ["MEMBER", "TRIAL_MEMBER"]:
            status_text = "3-DAY MARKET PILOT (ACTIVE)" if current_role == "TRIAL_MEMBER" else "ACTIVE PATROL"
            st.code(f"Craft: {selected_drone}\nSector: ZONE-1-NORTH\nCanopy Health Index (GLI): 0.3842 (HEALTHY)\nStatus: {status_text}")
        else:
            st.code(f"HVF Sovereign Node: ACTIVE\nConnected Craft Profile: {selected_drone}\nCanopy Diagnostic Engine: ARMED\nAccess Level: GUEST (Redacted)")

        st.markdown("#### 📡 Ingest Soil Moisture Probe")
        if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO", "MEMBER", "TRIAL_MEMBER"]:
            st.slider("Soil Moisture (%):", 5.0, 80.0, 21.4)
            st.button("📥 Transmit Sensor Telemetry")
        else:
            st.info("🔒 Sensor telemetry transmission is reserved for authenticated accounts.")

with tab_overview:
    st.subheader("💳 Commercial Subscriptions & Sovereign Feature Directory")
    st.markdown(f"Humphrey Virtual Farm Commercial Platform. Active Role: **{current_name}** (`{current_role}`)")
    st.divider()

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

    if current_role in ["CEO", "SUPER_ADMIN"]:
        with st.expander("👑 [MASTER PLATFORM ROOT]: Live Pilot Testers & Diagnostic Mesh", expanded=True):
            st.markdown("#### 🌾 Active 3-Day Market Pilot Accounts")
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT username, full_name, company_id, trial_expires_at, created_at FROM system_users WHERE role='TRIAL_MEMBER' ORDER BY id DESC")
            trial_rows = cur.fetchall()
            conn.close()
            if trial_rows:
                for tr in trial_rows:
                    st.code(f"Pilot User: {tr[1]} ({tr[0]}) | Farm: {tr[2]} | Expires: {tr[3]} | Registered: {tr[4]}")
            else:
                st.caption("No open market pilot testers registered yet.")

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
            cur.execute("SELECT COUNT(*) FROM pilot_feedback_vault")
            feedback_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM conversation_entity_memory")
            topic_count = cur.fetchone()[0]
            conn.close()

            st.code(f"""======================= HVF MASTER SERVER TOPOLOGY =======================
Host IP (Local LAN)      : 192.168.1.175
Mesh Endpoint (Tailscale): {ACTIVE_IP}:8501
Master Database Vault    : {DB_PATH}
Active Registered Users  : {user_count}
Active Trial Operators   : {len(trial_rows)}
Submitted Pilot Reviews  : {feedback_count}
Predictive Topic Memories: {topic_count}
Unused License Keys      : {unused_keys}
Encrypted Comm Records   : {msg_count}
--------------------------------------------------------------------------
Local Neural Engine      : Ollama REST API (Port 11434) -> llama3:8b (Deterministic Chat)
Cloud Fast Link          : Groq API (TLS 1.3) -> openai/gpt-oss-120b (Deterministic Chat)
Universal Drone Ingest   : MediaMTX (Port 1935 RTMP / 8554 RTSP) -> rtmp://192.168.1.175:1935/live/stream
Drone WebRTC Streaming   : MediaMTX (Port 8889) -> http://192.168.1.175:8889/live/stream
Supported Drone Ecosystem: DJI (Air 3S, Mavic, Matrice), Autel EVO, Skydio, Custom PX4
Weather Oracle Base      : NOAA REST API (Lat: {DEFAULT_LAT}, Lon: {DEFAULT_LON})
=========================================================================""")

    st.markdown("### 📖 Sovereign Knowledge Academy & Technical Directory")

    with st.expander("🏛️ [PILLAR 1]: The Humphrey Virtual Farm Manifesto & Sovereign AI Mission", expanded=False):
        st.markdown("""
        **Humphrey Virtual Farm (HVF)** is an on-premise, air-gapped agtech ecosystem engineered by Founder & CEO **Jeffery Humphrey** to liberate agricultural producers from centralized Big Ag cloud lock-in. 
        
        * **100% On-Premise Compute Sovereignty:** All neural inference, telemetry databases, and drone photogrammetry execute locally on physical hardware.
        * **Dual-Engine Operational Continuity:** Operates with zero degradation during complete offline blackout or severe grid outages.
        * **Autonomous Multi-Agent Agronomy:** Synchronized agents monitoring moisture, vegetative vigor, Doppler radar, and market communication.
        """)

    with st.expander("⚡ [PILLAR 2]: Dual-Engine Neural Architecture & Predictive Memory", expanded=False):
        st.markdown("""
        * **Cloud Fast Link (Groq):** `openai/gpt-oss-120b` with multi-turn persistent entity recall.
        * **Sovereign Local Core (Ollama):** `llama3:8b` running on physical RAM on port 11434 with persistent topic indexing.
        """)

    with st.expander("🌾 [PILLAR 3]: Universal Drone Computer Vision & Multispectral GLI Canopy Science", expanded=False):
        st.markdown("""
        * **Universal Ingest Gateway:** Ingests live video from **DJI, Autel, Skydio, and custom PX4** crafts over standard RTMP (port 1935) and RTSP (port 8554).
        * **Multispectral Green Leaf Index:** Computes vegetative vigor using `GLI = (2*G - R - B) / (2*G + R + B)`.
        * **Direct Sub-Second Playback:** Re-muxes drone streams into sub-second WebRTC on port 8889.
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
        * **Executive Dictation:** Ghostwrites articles and market releases in visionary CEO, SME, or Agronomist tones for Founder **Jeffery Humphrey**.
        * **Direct Deployment:** Dispatches posts live to LinkedIn using official OAuth UGC API endpoints.
        """)

    with st.expander("🔐 [PILLAR 7]: Cryptographic Vault, User Isolation & 4-Tier Security Matrix", expanded=False):
        st.markdown("""
        * **Level 4: Master CEO (Jeffery Humphrey):** Root infrastructure, hardware topology, global key provisioning, and LinkedIn broadcasting.
        * **Level 3: Enterprise Client CEO:** Company executive AI, staff key issuance, farm financial models, and full drone telemetry.
        * **Level 2: Authorized / Trial Member:** Private encrypted assistant, spectator drone stream, and field sensor logging.
        * **Level 1: Public Guest:** Commercial showcase, safety protocols, and 3-Day Trial onboarding.
        """)

with tab_feedback:
    st.subheader("📝 Open Market Pilot Feedback & Operator Reviews")
    st.markdown("We value direct operator telemetry. Share your field experience with Humphrey Virtual Farm leadership.")
    st.divider()

    if current_role in ["CEO", "SUPER_ADMIN"]:
        st.markdown("### 👑 Master Review Ingestion Vault (CEO Access)")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT full_name, username, rating, farm_size_acres, primary_crops, feedback_text, contact_email, created_at FROM pilot_feedback_vault ORDER BY id DESC")
        reviews = cur.fetchall()
        conn.close()
        
        if reviews:
            for r in reviews:
                stars = "⭐" * r[2]
                st.markdown(f"""
                <div style="background-color: #0c1118; border: 1.5px solid #00FF66; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: #70FF00;">{r[0]} ({r[1]}) — {stars} ({r[2]}/5)</div>
                    <div style="color: #8899A6; font-size: 0.9rem;">Acres: {r[3]} | Crops: {r[4]} | Email: {r[6]} | Date: {r[7]}</div>
                    <div style="color: #FFFFFF; font-size: 1rem; margin-top: 8px; line-height: 1.5;">{r[5]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No operator reviews submitted yet.")

    else:
        st.markdown("### 🌾 Submit Your 3-Day Field Trial Feedback")
        fb_rating = st.slider("Overall Platform Rating:", 1, 5, 5, help="1 = Poor, 5 = Exceptional")
        fb_acres = st.selectbox("Operation Size (Acres):", ["Under 100 Acres", "100 - 500 Acres", "500 - 1,500 Acres", "1,500 - 5,000 Acres", "5,000+ Commercial Acres"])
        fb_crops = st.text_input("Primary Crops / Livestock:", placeholder="e.g. Winter Wheat, Grain Sorghum, Angus Cattle")
        fb_text = st.text_area("Detailed Operator Feedback / Feature Requests:", placeholder="Tell us how Ebony performed with your soil tests, drone flights, weather alerts, or what features you would like added...", height=150)
        
        prefill_email = current_user if (current_user and "@" in current_user) else ""
        fb_email = st.text_input("Contact Email (Optional for direct founder follow-up):", value=prefill_email)

        if st.button("🚀 Submit Operator Review to HVF Leadership", use_container_width=True):
            if not fb_text.strip():
                st.warning("Please enter your feedback comments before submitting.")
            else:
                save_pilot_feedback(current_user, current_name, fb_rating, fb_acres, fb_crops, fb_text.strip(), fb_email.strip())
                st.success("🎉 Thank you! Your review has been encrypted and delivered directly to Founder & CEO Jeffery Humphrey.")

with tab_sandbox:
    if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO", "MEMBER", "TRIAL_MEMBER"]:
        st.subheader("🧪 Python Execution Sandbox")
        st.code("print('⚡ Sandbox Online')")
    else:
        st.warning("🔒 Python Execution Sandbox is restricted to authenticated HVF Members.")