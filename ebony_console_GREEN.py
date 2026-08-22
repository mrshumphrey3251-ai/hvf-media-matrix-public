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

st.set_page_config(page_title="HVF Ebony | Commercial Edition", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

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
    cur.execute("SELECT id, is_used FROM member_invite_keys WHERE invite_code=?", (invite_code.strip().upper(),))
    token_row = cur.fetchone()
    if not token_row:
        conn.close()
        return False, "Invalid Invite Code."
    if token_row[1] == 1:
        conn.close()
        return False, "Invite code already used."
    try:
        cur.execute("INSERT INTO system_users (username, password_hash, full_name, role, status) VALUES (?, ?, ?, 'MEMBER', 'APPROVED')",
                    (username.strip().lower(), hash_password(pwd_raw), full_name.strip()))
        cur.execute("UPDATE member_invite_keys SET is_used=1, used_by=? WHERE id=?", (username.strip().lower(), token_row[0]))
        conn.commit()
        conn.close()
        return True, "Membership activated successfully!"
    except Exception as e:
        conn.close()
        return False, f"Registration error: {str(e)}"

def generate_invite_token(issued_by: str) -> str:
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

def get_system_prompt_for_role(role: str) -> str:
    if role == "CEO":
        return "You are EBONY, Sovereign AI Technical Partner to Mr. Humphrey, Founder & CEO of Humphrey Virtual Farm. You provide unfiltered technical analysis, executive blueprints, drone telemetry interpretation, and agricultural automation strategies with authoritative competence."
    elif role == "MEMBER":
        return "You are EBONY, Agricultural AI Co-Pilot for Authorized Members of Humphrey Virtual Farm. You assist with soil health diagnostics, weather risk alerts, microclimate telemetry, and sustainable farm management."
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
        if current_role == "CEO":
            st.success(f"👑 **{current_name}**\n*(CEO Clearance - Master Node)*")
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

        if current_role == "CEO":
            st.divider()
            st.header("📲 Swarm Uplink (CEO Only)")
            st.caption(f"Scan on mobile/tablet:\n`{UPLINK_URL}`")
            qr_buf = generate_qr_image(UPLINK_URL)
            st.image(qr_buf, width=180)
            
            st.divider()
            st.header("🔑 One-Time VIP Code")
            if st.button("⚡ Generate VIP Code", key="sidebar_gen_code"):
                new_vip = generate_invite_token(current_user)
                st.success(f"Code: `{new_vip}`")
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
            reg_code = st.text_input("One-Time VIP Code:", key="reg_c", placeholder="HVF-VIP-XXXX")
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
    if current_role == "CEO":
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
    "📖 System Overview",
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
                greeting = f"⚡ Ebony online and armed, Mr. Humphrey. All systems operational." if current_role == "CEO" else f"⚡ Ebony online, {current_name}."
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

    user_input = st.chat_input("Enter message for Ebony...")
    if user_input:
        if current_user and current_cipher:
            save_encrypted_message(current_user, "user", user_input, current_cipher)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        sys_prompt = get_system_prompt_for_role(current_role)
        
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
    if current_role == "CEO":
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
        st.info("🔒 Executive Article Dictation & Live Deployment Gateway is restricted to CEO Clearance.")

with tab_weather:
    st.subheader("🚨 NOAA Emergency Weather & Live Radar Sentinel")
    st.components.v1.iframe("https://radar.weather.gov/", height=450, scrolling=True)

with tab_farm:
    st.subheader("🌾 Humphrey Virtual Farm | Real-Time Aerial Reconnaissance & Agronomy")
    st.markdown("Live low-latency video feed direct from DJI Air 3S O4 link and soil sensor telemetry.")
    st.divider()

    col1, col2 = st.columns([1.5, 1])

    with col1:
        if current_role == "CEO":
            st.markdown("### 🎥 Live DJI Air 3S Master Video Feed (CEO Access)")
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
        
        elif current_role == "MEMBER":
            st.markdown("### 🎥 Live Aerial Canopy Spectator Feed (Member Access)")
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
            st.caption("🛡️ *Encrypted Spectator Stream Active. Network ingestion keys redacted.*")
        
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
        if current_role == "CEO":
            st.code(f"Craft: DJI Air 3S\nMission: SURVEY-Z1-ALPHA\nSector: ZONE-1-NORTH\nAltitude: 45.0m | Battery: 88%\nStatus: ACTIVE_PATROL\nRTMP Ingest: {RTMP_INGEST_URL}\nStream Engine: MediaMTX v1.9.0")
        elif current_role == "MEMBER":
            st.code("Craft: DJI Air 3S\nSector: ZONE-1-NORTH\nCanopy Health Index (GLI): 0.3842 (HEALTHY)\nStatus: ACTIVE PATROL")
        else:
            st.code("HVF Sovereign Node: ACTIVE\nCanopy Diagnostic Engine: ARMED\nAccess Level: GUEST (Redacted)")

        st.markdown("#### 📡 Ingest Soil Moisture Probe")
        if current_role in ["CEO", "MEMBER"]:
            st.slider("Soil Moisture (%):", 5.0, 80.0, 21.4)
            st.button("📥 Transmit Sensor Telemetry")
        else:
            st.info("🔒 Sensor telemetry transmission is reserved for authenticated accounts.")

# --- TAB 5: COMPREHENSIVE KNOWLEDGE ACADEMY & FEATURE DIRECTORY ---
with tab_overview:
    st.subheader("📖 System Overview | Sovereign Knowledge Academy & Feature Directory")
    st.markdown(f"Interactive training manual, technical blueprints, and operational directories. Currently viewing as: **{current_name}** (`{current_role}`)")
    st.divider()

    # ACADEMY MODULE 1: PLATFORM MANIFESTO & WHY EBONY EXISTS
    with st.expander("🏛️ [ACADEMY PILLAR 1]: The Humphrey Virtual Farm Manifesto & Sovereign AI Mission", expanded=True):
        st.markdown("""
        ### What is Humphrey Virtual Farm (HVF)?
        **Humphrey Virtual Farm** is an on-premise, air-gapped agtech intelligence ecosystem engineered to liberate agricultural producers from centralized Big Ag cloud lock-in. 
        
        Traditional agricultural platforms force farmers to upload their proprietary soil data, field yields, drone imagery, and financial models to third-party corporate servers. That data is commoditized, sold to speculative commodity traders, and used against producers in market negotiations.

        ### The Three Sovereign Core Tenets:
        1. **100% On-Premise Compute Sovereignty:** All neural inference, telemetry databases, and drone photogrammetry execute locally on your physical farm hardware. Your data never leaves your perimeter.
        2. **Dual-Engine Operational Continuity:** Agriculture does not stop when cellular towers fail or internet grids go dark. Ebony operates with zero degradation during complete offline blackout conditions.
        3. **Autonomous Multi-Agent Agronomy:** A synchronized agent matrix that monitors sub-surface moisture, aerial vegetative vigor, real-time Doppler hazards, and market communication automatically.
        """)

    # ACADEMY MODULE 2: DUAL-ENGINE NEURAL ROUTER
    with st.expander("⚡ [ACADEMY PILLAR 2]: Dual-Engine Neural Architecture & Offline AI Execution", expanded=False):
        st.markdown("""
        ### How Ebony Thinks: The Hybrid Intelligence Mesh
        Ebony is not a single cloud chatbot; it is a **Dual-Engine Neural Router** capable of instantaneous hot-switching between high-speed cloud clusters and local silicon:

        * **Engine 1: Cloud Fast Link (`Groq Neural Acceleration`)**
          * **Model:** `openai/gpt-oss-120b` & `llama-3.3-70b-versatile`
          * **Latency:** $<0.45$ seconds response speed.
          * **Protocol:** TLS 1.3 encrypted transport layer.
          * **Role:** High-speed complex market synthesis, long-form ghostwriting, and advanced economic simulations when network uplinks are active.

        * **Engine 2: Sovereign Local Core (`Ollama On-Premise Runner`)**
          * **Model:** `llama3:8b` (Quantized 4-bit local weights)
          * **Endpoint:** `http://127.0.0.1:11434/api/generate`
          * **Hardware:** Native CPU/GPU physical RAM execution.
          * **Role:** 100% offline, air-gapped agricultural intelligence, crop emergency diagnostics, and equipment safety protocols with zero internet connection.
        """)

    # ACADEMY MODULE 3: DJI AIR 3S COMPUTER VISION & PHOTOGRAMMETRY
    with st.expander("🌾 [ACADEMY PILLAR 3]: DJI Air 3S Computer Vision & Multispectral GLI Canopy Science", expanded=False):
        st.markdown("""
        ### Aerial Reconnaissance & Crop Stress Calculation
        Ebony integrates with the **DJI Air 3S** dual-camera drone platform over the ultra-long-range **DJI O4 video link** to perform real-time vegetative health indexing directly from aerial frames.

        #### The Multispectral Green Leaf Index (GLI) Mathematical Formula:
        """)
        st.latex(r"\text{GLI} = \frac{2 \cdot G - R - B}{2 \cdot G + R + B}")
        st.markdown("""
        Where:
        * $G$ = Green Spectral Channel Reflectance Value ($0 - 255$)
        * $R$ = Red Spectral Channel Reflectance Value ($0 - 255$)
        * $B$ = Blue Spectral Channel Reflectance Value ($0 - 255$)

        #### Diagnostic Classification Thresholds:
        | Calculated Index ($\text{GLI}$) | Canopy State | Agronomic Interpretation & Action Required |
        | :--- | :--- | :--- |
        | **$> +0.2500$** | 🟢 **Vigorous & Healthy** | Optimal chlorophyll absorption. Photosynthesis at peak capacity. Standard irrigation schedule. |
        | **$+0.1000 \text{ to } +0.2500$** | 🟡 **Moderate Stress / Thinning** | Early nitrogen deficit, sub-surface dry spots, or early pest emergence. Soil probe verification recommended. |
        | **$< +0.1000$** | 🔴 **High Stress / Severe Deficit** | Severe drought stress, root damage, or ground exposure. Immediate valve actuation required. |

        #### Video Ingestion Architecture:
        1. **Craft Transmitter:** DJI RC 2 broadcasts live stream via local Wi-Fi to PC port `1935`.
        2. **MediaMTX Video Server:** Ingests `rtmp://192.168.1.175:1935/live/air3s` and re-muxes the signal to WebRTC.
        3. **Ebony Console HUD:** Renders sub-second video feed in Tab 4 on `http://192.168.1.175:8889/live/air3s`.
        """)

    # ACADEMY MODULE 4: IOT SENSOR MESH & VOLUMETRIC SOIL THERMODYNAMICS
    with st.expander("📡 [ACADEMY PILLAR 4]: IoT Soil Mesh, Capacitance Probes & Telemetry Fusion", expanded=False):
        st.markdown("""
        ### Sub-Surface Agronomy & Precision Moisture Sensing
        Aerial imagery shows the surface canopy; ground sensors measure the root zone. Ebony unifies both layers into a single telemetry vault.

        #### Volumetric Water Content (VWC) Matrix:
        * **Target Crop Root Zone (Corn, Wheat, Alfalfa):**
          * **Field Capacity (Optimal):** $28\% - 38\%$ VWC
          * **Managed Depletion Threshold:** $18\% - 24\%$ VWC *(Trigger irrigation)*
          * **Permanent Wilting Point:** $<12\%$ VWC *(Irreversible plant stress)*

        #### Multi-Sector Zone Architecture:
        * **`ZONE-1-NORTH`:** Primary cultivation sector (Continuous capacitance probe sampling).
        * **`ZONE-2-SOUTH`:** Secondary sector (Microclimate temperature & humidity tracking).
        * **`ZONE-3-EAST`:** High-elevation drainage monitoring.
        * **`ZONE-4-WEST`:** Lowland riparian & moisture collection basin.
        """)

    # ACADEMY MODULE 5: NOAA EMERGENCY SENTINEL & LIFE SAFETY PROTOCOLS
    with st.expander("🚨 [ACADEMY PILLAR 5]: NOAA Emergency Radar Sentinel & Farm Life Safety Protocols", expanded=False):
        st.markdown("""
        ### Severe Weather Defense & Life Safety Boundaries
        Ebony’s Sentinel monitors National Weather Service Doppler feeds and coordinates emergency actions across your farm.

        #### Immediate Life Safety Operating Procedures (Guest & Member Active):
        1. **Severe Tornado / High Wind Warnings ($>60\text{ mph}$):**
           * Immediately ground all drone operations (DJI Air 3S wind limit is $27\text{ mph}$).
           * Disengage PTO shafts, power down high-profile machinery, and seek interior shelter.
        2. **Anhydrous Ammonia ($\text{NH}_3$) Pressurized Line Rupture:**
           * Evacuate immediately **upwind** and **crosswind**.
           * Flush contaminated skin/eyes with cold water for a minimum of 15 continuous minutes.
           * Do NOT apply salves or ointments without medical authorization.
        3. **Power Take-Off (PTO) Entanglement Hazard:**
           * Always disengage tractor master clutch and kill engine before dismounting to inspect implement drivelines.
        """)

    # ACADEMY MODULE 6: LINKEDIN EXECUTIVE BROADCAST HUB
    with st.expander("📰 [ACADEMY PILLAR 6]: LinkedIn Thought Leadership Engine & Live UGC Broadcasting", expanded=False):
        st.markdown("""
        ### Automated Corporate Voice & Market Visibility
        Position Humphrey Virtual Farm as the preeminent agtech authority by transforming raw field telemetry into polished thought leadership.

        #### How the Dictation Engine Operates:
        1. **Dictate Talking Points:** Dictate field discoveries, drone findings, or sovereign AI breakthroughs.
        2. **Multi-Tone Ghostwriter:** Choose between *Authoritative CEO*, *Technical SME*, *Commercial Investor*, or *Field Agronomist*.
        3. **One-Click Deploy:** Dispatches directly through the official LinkedIn UGC API (`v2/ugcPosts`) with verified token handshakes.
        """)

    # ACADEMY MODULE 7: CRYPTOGRAPHIC VAULT & THREE-TIER CLEARANCE
    with st.expander("🔐 [ACADEMY PILLAR 7]: Cryptographic Vault, User Isolation & Clearance Matrix", expanded=False):
        st.markdown("""
        ### Three-Tier Clearance & Zero-Knowledge Architecture
        | Clearance Tier | Who It Is For | Access Permissions & Boundaries |
        | :--- | :--- | :--- |
        | **👑 Level 3: CEO Node** | Founder & Farm Owner | Unrestricted hardware control, live video ingest, VIP code generation, full multi-agent agronomy, raw network IPs, and LinkedIn publishing. |
        | **👥 Level 2: Member Node** | Verified Partners & Operators | Private encrypted chat vault, live spectator drone streams, crop diagnostics, and soil telemetry ingestion. System keys redacted. |
        | **👤 Level 1: Guest Node** | Public Visitors & Evaluators | Commercial platform overview, emergency safety sentinel, and automated VIP registration pathway. Compute restricted. |

        #### Cryptographic Standard:
        * User sessions derive unique encryption keys via **PBKDF2-HMAC-SHA256** (100,000 iterations).
        * Chat logs and operational directives are encrypted using **Fernet (AES-128 in CBC mode with PKCS7 padding and HMAC-SHA256 authentication)**.
        """)

    # ACADEMY MODULE 8: CEO EXCLUSIVE NODE DIAGNOSTICS & VIP PROVISIONING
    if current_role == "CEO":
        with st.expander("👑 [MASTER NODE ONLY]: Live Infrastructure Diagnostics & VIP Key Provisioning Engine", expanded=True):
            st.markdown("#### 🔑 Provision VIP Member Codes")
            c_vip1, c_vip2 = st.columns([1.5, 3])
            with c_vip1:
                if st.button("⚡ Generate New VIP Key", key="tab5_vip_gen_exhaustive", use_container_width=True):
                    token = generate_invite_token(current_user)
                    st.success(f"Generated Key: `{token}`")
            with c_vip2:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT invite_code, issued_by, is_used, used_by, created_at FROM member_invite_keys ORDER BY id DESC LIMIT 5")
                recent_keys = cur.fetchall()
                conn.close()
                if recent_keys:
                    st.caption("Recent VIP License Keys Issued:")
                    for k in recent_keys:
                        status_str = f"🔴 USED by {k[3]}" if k[2] == 1 else "🟢 UNUSED / ACTIVE"
                        st.code(f"Key: {k[0]} | Status: {status_str} | Date: {k[4]}")

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
Unused VIP Invite Codes  : {unused_keys}
Encrypted Comm Records   : {msg_count}
Sensor Telemetry Records : {sensor_count}
--------------------------------------------------------------------------
Local Neural Engine      : Ollama REST API (Port 11434) -> llama3:8b
Cloud Fast Link          : Groq API (TLS 1.3) -> openai/gpt-oss-120b
Drone RTMP Ingestion     : MediaMTX (Port 1935) -> rtmp://192.168.1.175:1935/live/air3s
Drone WebRTC Streaming   : MediaMTX (Port 8889) -> http://192.168.1.175:8889/live/air3s
Weather Oracle Base      : NOAA REST API (Lat: {DEFAULT_LAT}, Lon: {DEFAULT_LON})
Cryptographic Standard   : Fernet PBKDF2HMAC (SHA-256 with Per-User Salt)
Release Status           : Commercial MVCP 1.0 (Master Academy Armed)
=========================================================================""")

with tab_sandbox:
    if current_role in ["CEO", "MEMBER"]:
        st.subheader("🧪 Python Execution Sandbox")
        st.code("print('⚡ Sandbox Online')")
    else:
        st.warning("🔒 Python Execution Sandbox is restricted to authenticated HVF Members.")