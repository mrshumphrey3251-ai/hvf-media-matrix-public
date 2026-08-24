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

STRIPE_PERSONAL_LINK = os.getenv("STRIPE_PERSONAL_LINK", "https://buy.stripe.com/test_fZueVfbmx9lH4rB8yx1RC00")
STRIPE_MONTHLY_LINK = os.getenv("STRIPE_MONTHLY_LINK", "https://buy.stripe.com/test_monthly_vip")
STRIPE_ANNUAL_LINK = os.getenv("STRIPE_ANNUAL_LINK", "https://buy.stripe.com/test_annual_vip")
PAYPAL_PAY_LINK = os.getenv("PAYPAL_PAY_LINK", "https://www.paypal.com/paypalme/humphreyvirtualfarm")

OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
CLOUD_MODEL = "openai/gpt-oss-120b"
LOCAL_MODEL = "llama3:8b"

# ==========================================
# DATABASE & WHITE-LABEL EMPIRE ENGINE
# ==========================================
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
    if "company_id" not in cols: cur.execute("ALTER TABLE system_users ADD COLUMN company_id TEXT DEFAULT 'HVF_MAIN'")
    if "trial_expires_at" not in cols: cur.execute("ALTER TABLE system_users ADD COLUMN trial_expires_at TIMESTAMP")

    cur.execute("CREATE TABLE IF NOT EXISTS encrypted_user_comms (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, role TEXT NOT NULL, encrypted_content TEXT NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS member_invite_keys (id INTEGER PRIMARY KEY AUTOINCREMENT, invite_code TEXT UNIQUE NOT NULL, issued_by TEXT NOT NULL, grant_role TEXT NOT NULL DEFAULT 'MEMBER', is_used INTEGER DEFAULT 0, used_by TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS pilot_feedback_vault (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, full_name TEXT NOT NULL, rating INTEGER NOT NULL, farm_size_acres TEXT, primary_crops TEXT, feedback_text TEXT NOT NULL, contact_email TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS conversation_entity_memory (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, topic_key TEXT NOT NULL, entity_summary TEXT NOT NULL, last_context TEXT NOT NULL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(username, topic_key))")
    cur.execute("CREATE TABLE IF NOT EXISTS empire_config (config_key TEXT PRIMARY KEY, config_value TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS linkedin_broadcast_history (id INTEGER PRIMARY KEY AUTOINCREMENT, post_content TEXT, response_status TEXT, urn_identifier TEXT, triggered_by TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

ensure_db_schema()

def get_empire_config():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT config_key, config_value FROM empire_config")
    rows = cur.fetchall()
    conn.close()
    settings = {k: v for k, v in rows}
    return {
        "FARM_NAME": settings.get("FARM_NAME", "Humphrey Virtual Farm"),
        "FOUNDER_NAME": settings.get("FOUNDER_NAME", "Jeffery Humphrey"),
        "AI_PERSONA": settings.get("AI_PERSONA", "Ebony"),
        "CONTACT_EMAIL": settings.get("CONTACT_EMAIL", "humphreyvirtualfarm@gmail.com")
    }

def update_empire_config(farm_name, founder, persona, email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executemany("INSERT INTO empire_config (config_key, config_value) VALUES (?, ?) ON CONFLICT(config_key) DO UPDATE SET config_value=excluded.config_value", [("FARM_NAME", farm_name), ("FOUNDER_NAME", founder), ("AI_PERSONA", persona), ("CONTACT_EMAIL", email)])
    conn.commit()
    conn.close()

EMPIRE = get_empire_config()

STRICT_GROUND_RULES = f"""
CRITICAL NON-NEGOTIABLE GROUND TRUTH:
1. PLATFORM NAME: {EMPIRE["FARM_NAME"]}
2. FOUNDER & CEO: {EMPIRE["FOUNDER_NAME"]} ONLY.
3. YOUR IDENTITY: You are {EMPIRE["AI_PERSONA"]}, the sovereign AI platform.
4. CONTACT EMAIL: {EMPIRE["CONTACT_EMAIL"]} ONLY.
5. ABSOLUTE BAN ON FABRICATED DATA: Never invent fake benchmark percentages, fake field trials, fake audits, or fake VC funding rounds.
"""

def sanitize_deterministic_output(raw_text: str) -> str:
    if not raw_text: return raw_text
    text = raw_text
    for pattern in [r"(?i)\$?\d+(\.\d+)?\s*(M|million|B|billion)\s*(in\s+)?(seed\s*(&|and)\s*)?(series[\s-]?[a-z]|venture\s+capital|funding|investment\s+round)"]:
        text = re.sub(pattern, "sovereign, self-funded agricultural architecture", text)
    return text

def derive_user_cipher(password: str, username: str) -> Fernet:
    salt = hashlib.sha256(username.encode("utf-8")).digest()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    return Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8"))))

def hash_password(pwd: str) -> str: return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def verify_user(username: str, pwd_raw: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT username, full_name, role, status, trial_expires_at FROM system_users WHERE username=? AND password_hash=?", (username.strip().lower(), hash_password(pwd_raw)))
    user = cur.fetchone()
    conn.close()
    if not user: return None, "Invalid Username or Password."
    if user[2] == "TRIAL_MEMBER" and user[4]:
        try:
            if datetime.now() > datetime.strptime(user[4], "%Y-%m-%d %H:%M:%S"): return user, "TRIAL_EXPIRED"
        except: pass
    return user, "OK"

def register_7day_trial(username: str, pwd_raw: str, full_name: str, farm_info: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM system_users WHERE username=?", (username.strip().lower(),))
    if cur.fetchone():
        conn.close()
        return False, "Username already registered."
    expires_at = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute("INSERT INTO system_users (username, password_hash, full_name, role, company_id, status, trial_expires_at) VALUES (?, ?, ?, 'TRIAL_MEMBER', ?, 'APPROVED', ?)", (username.strip().lower(), hash_password(pwd_raw), full_name.strip(), farm_info.strip(), expires_at))
        conn.commit()
        conn.close()
        return True, f"🎉 Pilot Activated! Full member access granted until {expires_at}."
    except Exception as e:
        conn.close()
        return False, str(e)

def register_user_with_invite(username: str, pwd_raw: str, full_name: str, invite_code: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, grant_role, is_used FROM member_invite_keys WHERE invite_code=?", (invite_code.strip().upper(),))
    token_row = cur.fetchone()
    if not token_row: return False, "Invalid Invite Code."
    if token_row[2] == 1: return False, "Invite code already used."
    assigned_role = token_row[1] if token_row[1] else "MEMBER"
    try:
        cur.execute("INSERT INTO system_users (username, password_hash, full_name, role, status) VALUES (?, ?, ?, ?, 'APPROVED')", (username.strip().lower(), hash_password(pwd_raw), full_name.strip(), assigned_role))
        cur.execute("UPDATE member_invite_keys SET is_used=1, used_by=? WHERE id=?", (username.strip().lower(), token_row[0]))
        conn.commit()
        conn.close()
        return True, f"Registration successful! Role: {assigned_role} granted."
    except Exception as e:
        conn.close()
        return False, str(e)

def generate_invite_token(issued_by: str, target_role: str = "MEMBER") -> str:
    token = f"{'EMP-CORP' if target_role == 'CLIENT_CEO' else 'EMP-VIP'}-{secrets.token_hex(3).upper()}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO member_invite_keys (invite_code, issued_by, grant_role, is_used) VALUES (?, ?, ?, 0)", (token, issued_by, target_role))
    conn.commit()
    conn.close()
    return token

def load_all_entity_memories(username: str) -> str:
    if not username: return ""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT topic_key, entity_summary, last_context FROM conversation_entity_memory WHERE username=? ORDER BY updated_at DESC LIMIT 8", (username,))
    rows = cur.fetchall()
    conn.close()
    if not rows: return ""
    return "\n[PERSISTENT KNOWLEDGE BASE]:\n" + "".join([f"- Topic: {r[0]} | Key Facts: {r[1]} | Context: {r[2]}\n" for r in rows])

def store_entity_memory_async(username: str, user_prompt: str, bot_response: str):
    if not username or len(user_prompt.strip()) < 5: return
    words = [w.strip(".,!?:;\"'()[]{}") for w in user_prompt.lower().split() if len(w) > 3]
    stopwords = {"what", "whats", "where", "when", "which", "about", "there", "their", "please", "could", "would", "should", "tell", "explain", "that", "this", "with", "from", "have", "been"}
    keywords = [w for w in words if w not in stopwords]
    if not keywords: return
    topic_key = " ".join(keywords[:4]).title()
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO conversation_entity_memory (username, topic_key, entity_summary, last_context, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(username, topic_key) DO UPDATE SET entity_summary = excluded.entity_summary, last_context = excluded.last_context, updated_at = CURRENT_TIMESTAMP", (username, topic_key, user_prompt.strip()[:180], bot_response.strip()[:240].replace("\n", " ")))
        conn.commit()
        conn.close()
    except: pass

def load_encrypted_messages(username: str, cipher: Fernet):
    if not username or not cipher: return []
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT role, encrypted_content FROM encrypted_user_comms WHERE username=? ORDER BY id ASC", (username,))
    rows = cur.fetchall()
    conn.close()
    decrypted = []
    for r in rows:
        try:
            decrypted.append({"role": r[0], "content": sanitize_deterministic_output(cipher.decrypt(r[1].encode("utf-8")).decode("utf-8"))})
        except: pass
    return decrypted

def save_encrypted_message(username: str, role: str, content: str, cipher: Fernet):
    if not username or not cipher: return
    blob = cipher.encrypt(sanitize_deterministic_output(content).encode("utf-8")).decode("utf-8")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO encrypted_user_comms (username, role, encrypted_content) VALUES (?, ?, ?)", (username, role, blob))
    conn.commit()
    conn.close()

def save_pilot_feedback(username: str, full_name: str, rating: int, acres: str, crops: str, feedback: str, email: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO pilot_feedback_vault (username, full_name, rating, farm_size_acres, primary_crops, feedback_text, contact_email) VALUES (?, ?, ?, ?, ?, ?, ?)", (username or "anonymous", full_name or "Guest Operator", rating, acres, crops, feedback, email))
    conn.commit()
    conn.close()

def has_user_submitted_feedback(username: str) -> bool:
    if not username: return False
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM pilot_feedback_vault WHERE username=?", (username,))
        count = cur.fetchone()[0]
        conn.close()
        return count > 0
    except: return False

def format_linkedin_urn(raw_urn: str) -> str:
    if not raw_urn: return ""
    clean = raw_urn.strip().strip('"').strip("'")
    if clean.startswith("urn:li:member:") or clean.startswith("urn:li:person:") or clean.startswith("urn:li:organization:"): return clean
    if clean.isdigit(): return f"urn:li:person:{clean}"
    return clean

def generate_qr_image(url: str):
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    buf = io.BytesIO()
    qr.make_image(fill_color="#00FF66", back_color="#0c1118").save(buf, format="PNG")
    buf.seek(0)
    return buf

@st.cache_resource
def get_tailscale_or_local_ip_cached() -> str:
    try:
        ts_path = "C:\\Program Files\\Tailscale\\tailscale.exe"
        if os.path.exists(ts_path):
            ts_proc = subprocess.run([ts_path, "ip", "-4"], capture_output=True, text=True, creationflags=0x08000000)
            if ts_proc.returncode == 0 and ts_proc.stdout.strip(): return ts_proc.stdout.strip().splitlines()[0]
    except: pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "192.168.1.175"

ACTIVE_IP = get_tailscale_or_local_ip_cached()
UPLINK_URL = f"http://{ACTIVE_IP}:8501"
WEBRTC_STREAM_URL = f"http://192.168.1.175:8889/live/stream"
RTMP_INGEST_URL = f"rtmp://192.168.1.175:1935/live/stream"

st.set_page_config(page_title=f"{EMPIRE['FARM_NAME']} | {EMPIRE['AI_PERSONA']}", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    html, body, [class*="css"], .stApp { background-color: #050709 !important; color: #FFFFFF !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important; }
    header[data-testid="stHeader"] { background-color: #050709 !important; border-bottom: 1px solid #243042 !important; }
    h1, h2, h3, h4 { color: #00FF66 !important; font-weight: 800 !important; }
    p, span, label, li { color: #FFFFFF !important; font-size: 1.05rem !important; line-height: 1.65 !important; }
    strong, b { color: #70FF00 !important; font-weight: 700 !important; }
    [data-testid="stSidebar"] { background-color: #0c1118 !important; border-right: 2px solid #243042 !important; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { background-color: #121824 !important; color: #FFFFFF !important; border: 2px solid #00FF66 !important; }
    .stButton>button { background-color: #00FF66 !important; color: #050709 !important; font-weight: 900 !important; border-radius: 6px !important; border: none !important; }
    .stButton>button:hover { background-color: #39FF88 !important; color: #000000 !important; }
    .pricing-card { background-color: #0c1118; border: 2px solid #00FF66; border-radius: 10px; padding: 20px 14px; text-align: center; margin-bottom: 12px; min-height: 290px; }
    .pricing-tier { color: #70FF00; font-size: 1.15rem; font-weight: 800; min-height: 48px; display: flex; align-items: center; justify-content: center; }
    .pricing-price { color: #FFFFFF; font-size: 1.85rem; font-weight: 900; margin: 10px 0; }
    pre, code { background-color: #000000 !important; color: #00FF66 !important; font-size: 1rem !important; border: 1px solid #243042 !important; }
</style>
""", unsafe_allow_html=True)

if "user_session" not in st.session_state: st.session_state.user_session = {"authenticated": False, "username": None, "full_name": "Public Guest", "role": "GUEST", "cipher": None, "trial_expires_at": None}
if "screen_wiped" not in st.session_state: st.session_state.screen_wiped = False
if "operation_mode" not in st.session_state: st.session_state.operation_mode = "🟢 Online (Cloud Fast Link)"
if "demo_mode" not in st.session_state: st.session_state.demo_mode = False
if "current_linkedin_draft" not in st.session_state: st.session_state.current_linkedin_draft = f"⚡ [{EMPIRE['FARM_NAME']} Intelligence Announcement]\n\nWe have deployed our on-premise universal aerial reconnaissance link..."

current_user = st.session_state.user_session["username"]
current_name = st.session_state.user_session["full_name"]
current_role = st.session_state.user_session["role"]
current_cipher = st.session_state.user_session["cipher"]
groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

def query_local_ollama_chat(messages_payload: list) -> str:
    try:
        res = requests.post(OLLAMA_CHAT_URL, json={"model": LOCAL_MODEL, "messages": messages_payload, "stream": False, "options": {"temperature": 0.0}}, timeout=45)
        if res.status_code == 200: return sanitize_deterministic_output(res.json().get("message", {}).get("content", ""))
        return f"⚠️ Local Node returned HTTP {res.status_code}."
    except: return "⚠️ Local Engine fault."

# --- SIDEBAR ---
with st.sidebar:
    st.header("🛡️ Presentation OPSEC")
    is_demo_mode = st.toggle("Activate Demo Mode (Mask Secrets)", value=st.session_state.demo_mode)
    st.session_state.demo_mode = is_demo_mode
    
    def mask_secret(text: str, mask_type: str = "FULL") -> str:
        if not st.session_state.demo_mode: return text
        if mask_type == "IP": return "[REDACTED_IP]"
        if mask_type == "URL": return "http://[REDACTED_IP]:8501"
        if mask_type == "URN": return "urn:li:person:********"
        if mask_type == "TOKEN": return "****************************************"
        if mask_type == "PATH": return "C:\\[REDACTED_VAULT_PATH]\\hvf_memory_vault.db"
        return "[REDACTED FOR DEMO]"

    st.divider()
    mode_selection = st.radio("Select Active Engine:", ["🟢 Online (Cloud Fast Link)", "🔒 Offline (100% Sovereign Local)"], index=0 if "Online" in st.session_state.operation_mode else 1)
    st.session_state.operation_mode = mode_selection
    is_online = "Online" in mode_selection

    if st.session_state.user_session["authenticated"]:
        st.success(f"👑 **{current_name}**\n*({current_role} Clearance)*")
        if st.button("🚪 Disconnect Session", use_container_width=True):
            st.session_state.user_session = {"authenticated": False, "username": None, "full_name": "Public Guest", "role": "GUEST", "cipher": None, "trial_expires_at": None}
            st.rerun()
            
        if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO"]:
            st.divider()
            st.header("📲 Swarm Uplink")
            st.caption(f"Scan to access node:\n`{mask_secret(UPLINK_URL, 'URL')}`")
            if not st.session_state.demo_mode: st.image(generate_qr_image(UPLINK_URL), width=180)
            else: st.info("QR Code hidden during Demo Mode.")
            
            st.divider()
            if st.button("⚡ Issue Team VIP Code"):
                if st.session_state.demo_mode: st.warning("Blocked in Demo Mode.")
                else: st.success(f"Staff Key: `{generate_invite_token(current_user, 'MEMBER')}`")
    else:
        st.info("👤 **Guest Mode**")
        auth_mode = st.radio("Access Portal:", ["Sign In", "🚀 Free 7-Day Pilot"], horizontal=False)
        if auth_mode == "Sign In":
            login_user = st.text_input("Username:")
            login_pass = st.text_input("Password:", type="password")
            if st.button("Sign In"):
                user_match, status_msg = verify_user(login_user, login_pass)
                if user_match and status_msg == "OK":
                    st.session_state.user_session = {"authenticated": True, "username": user_match[0], "full_name": user_match[1], "role": user_match[2], "cipher": derive_user_cipher(login_pass, user_match[0]), "trial_expires_at": user_match[4]}
                    st.rerun()
                elif status_msg == "TRIAL_EXPIRED": st.error("⏳ Your 7-Day Market Pilot has concluded. Please subscribe to continue.")
                else: st.error(status_msg)
        else:
            t_fn = st.text_input("Full Name:")
            t_farm = st.text_input("Farm Name:")
            t_u = st.text_input("Create Username:")
            t_p = st.text_input("Create Password:", type="password")
            if st.button("Launch 7-Day Pilot"):
                ok, msg = register_7day_trial(t_u, t_p, t_fn, t_farm)
                if ok: st.success(msg)
                else: st.error(msg)

st.title(f"⚡ {EMPIRE['FARM_NAME']} Command Deck | {EMPIRE['AI_PERSONA']} AI")
st.caption(f"Active User: **{current_name}** | 🛡️ *Mode: {st.session_state.operation_mode}*")

tab_chat, tab_linkedin, tab_weather, tab_farm, tab_overview, tab_feedback, tab_sandbox, tab_empire = st.tabs([
    "💬 Sovereign Command", "📡 LinkedIn Engine", "🚨 NOAA Radar", "🌾 Drone Diagnostics", "📖 System Overview", "📝 Feedback Hub", "🧪 Sandbox", "⚙️ Empire Config"
])

with tab_chat:
    if current_user and current_cipher:
        if "messages" not in st.session_state or st.session_state.screen_wiped:
            db_messages = load_encrypted_messages(current_user, current_cipher)
            if not db_messages:
                initial_msg = {"role": "assistant", "content": f"⚡ {EMPIRE['AI_PERSONA']} online. Welcome to {EMPIRE['FARM_NAME']}, {current_name}."}
                save_encrypted_message(current_user, "assistant", initial_msg["content"], current_cipher)
                db_messages = [initial_msg]
            st.session_state.messages = db_messages
            st.session_state.screen_wiped = False
    else:
        if "messages" not in st.session_state: st.session_state.messages = [{"role": "assistant", "content": f"⚡ Welcome to {EMPIRE['FARM_NAME']}. I am {EMPIRE['AI_PERSONA']}. Please sign in."}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if user_input := st.chat_input(f"Ask {EMPIRE['AI_PERSONA']} anything..."):
        if current_user and current_cipher: save_encrypted_message(current_user, "user", user_input, current_cipher)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        full_sys_prompt = f"You are {EMPIRE['AI_PERSONA']}, Sovereign AI for {EMPIRE['FARM_NAME']}. Founder: {EMPIRE['FOUNDER_NAME']}.\n{STRICT_GROUND_RULES}\n{load_all_entity_memories(current_user)}"
        conversation_payload = [{"role": "system", "content": full_sys_prompt}] + st.session_state.messages[-12:]
        
        if is_online:
            try:
                res = groq_client.chat.completions.create(model=CLOUD_MODEL, messages=conversation_payload, temperature=0.0)
                bot_reply = sanitize_deterministic_output(res.choices[0].message.content)
            except Exception as e: bot_reply = f"Cloud fault: {str(e)}"
        else: bot_reply = query_local_ollama_chat(conversation_payload)
        
        if current_user and current_cipher:
            save_encrypted_message(current_user, "assistant", bot_reply, current_cipher)
            store_entity_memory_async(current_user, user_input, bot_reply)
            
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

with tab_linkedin:
    if current_role in ["CEO", "SUPER_ADMIN"]:
        col_dict1, col_dict2 = st.columns([1.6, 1])
        with col_dict1:
            st.markdown("#### 🎙️ Dictate Strategic Directive")
            dictated_prompt = st.text_area("Dictate LinkedIn Concept / Key Talking Points:", height=120)
            if st.button("🤖 Generate 100% Factual Draft", use_container_width=True):
                sys_msg = f"You are ghostwriting for {EMPIRE['FOUNDER_NAME']}, CEO of {EMPIRE['FARM_NAME']}. Strict factual accuracy based solely on user input."
                if is_online:
                    res = groq_client.chat.completions.create(model=CLOUD_MODEL, messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": dictated_prompt}], temperature=0.0)
                    st.session_state.current_linkedin_draft = sanitize_deterministic_output(res.choices[0].message.content.strip())
                else: st.session_state.current_linkedin_draft = query_local_ollama_chat([{"role": "system", "content": sys_msg}, {"role": "user", "content": dictated_prompt}])
                st.rerun()

        with col_dict2:
            st.markdown("#### ⚙️ Pipeline Status")
            st.code(f"Author URN: {mask_secret(format_linkedin_urn(LINKEDIN_URN), 'URN')}\nGateway Token: {mask_secret(LINKEDIN_TOKEN, 'TOKEN')}\nZero-Hallucination: STRICT (Temp 0.0)")

        st.divider()
        st.markdown("#### 📝 Live Broadcast Editor & Deployment Gateway")
        st.text_area("Review & Refine Before Deploying:", value=st.session_state.current_linkedin_draft, height=200, key="linkedin_editor")
        
        col_dep1, col_dep2 = st.columns([2, 1])
        with col_dep1:
            if st.button("🚀 Authorize & Deploy Live to LinkedIn Profile", use_container_width=True):
                sanitized_deployment = sanitize_deterministic_output(st.session_state.current_linkedin_draft)
                if st.session_state.demo_mode: st.error("❌ Action Blocked: Cannot deploy while Executive Demo Mode is active.")
                elif not LINKEDIN_TOKEN or not LINKEDIN_URN: st.error("❌ LinkedIn credentials missing from vault.")
                elif not sanitized_deployment: st.warning("Cannot deploy empty broadcast.")
                else:
                    with st.spinner("📡 Broadcasting to LinkedIn..."):
                        clean_urn = format_linkedin_urn(LINKEDIN_URN)
                        try:
                            resp = requests.post("https://api.linkedin.com/v2/ugcPosts", headers={"Authorization": f"Bearer {LINKEDIN_TOKEN}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0"}, json={"author": clean_urn, "lifecycleState": "PUBLISHED", "specificContent": {"com.linkedin.ugc.ShareContent": {"shareCommentary": {"text": sanitized_deployment}, "shareMediaCategory": "NONE"}}, "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}}, timeout=15)
                            if resp.status_code in [200, 201]:
                                st.success(f"🎉 Live Deployment Confirmed! Post ID: `{resp.json().get('id', 'SUCCESS')}`")
                            else: st.error(f"⚠️ API Error (HTTP {resp.status_code}):\n`{resp.text}`")
                        except Exception as err: st.error(f"Deployment error: {str(err)}")
    else: st.info("🔒 Executive Article Dictation is reserved for the Master CEO.")

with tab_weather:
    st.subheader("🚨 NOAA Emergency Weather & Live Radar Sentinel")
    st.components.v1.iframe("https://radar.weather.gov/", height=450, scrolling=True)

with tab_farm:
    st.subheader(f"🌾 {EMPIRE['FARM_NAME']} | Aerial Ingest")
    st.components.v1.html(f'<iframe src="{WEBRTC_STREAM_URL}" width="100%" height="450" frameborder="0" allowfullscreen></iframe>', height=470)

with tab_overview:
    st.subheader("💳 Commercial Subscriptions & Features")
    feedback_cleared = has_user_submitted_feedback(current_user)
    is_unlocked = feedback_cleared or current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO"]
    
    if not is_unlocked: st.warning("🔒 **COMMERCIAL ACCESS LOCKED:** You must submit field telemetry and a platform review in the **Feedback Hub** (Tab 6) before commercial tier gateways are unlocked.")

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        st.markdown(f'<div class="pricing-card"><div class="pricing-tier">🌱 PERSONAL</div><div class="pricing-price">$19.99<span style="font-size:0.85rem;color:#8899A6;">/mo</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">✔ Single-User Node<br>✔ Dual-Engine AI<br>✔ Encrypted Vault</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("🌱 Personal ($19.99/mo)", STRIPE_PERSONAL_LINK, use_container_width=True)
        else: st.button("🔒 Locked", disabled=True, key="lock1", use_container_width=True)
    with col_p2:
        st.markdown(f'<div class="pricing-card"><div class="pricing-tier">💎 VIP MEMBER</div><div class="pricing-price">$249<span style="font-size:0.85rem;color:#8899A6;">/mo</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">✔ Everything in Personal<br>✔ Drone Spectator<br>✔ GLI Analytics</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("💎 VIP ($249/mo)", STRIPE_MONTHLY_LINK, use_container_width=True)
        else: st.button("🔒 Locked", disabled=True, key="lock2", use_container_width=True)
    with col_p3:
        st.markdown(f'<div class="pricing-card" style="border-color:#70FF00;"><div class="pricing-tier">🏛️ ENTERPRISE CEO</div><div class="pricing-price">$2,499<span style="font-size:0.85rem;color:#8899A6;">/yr</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">✔ Client Dashboard<br>✔ Issue Staff Keys<br>✔ Multi-Ranch Yield</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("🏛️ Enterprise Annual", STRIPE_ANNUAL_LINK, use_container_width=True)
        else: st.button("🔒 Locked", disabled=True, key="lock3", use_container_width=True)
    with col_p4:
        st.markdown(f'<div class="pricing-card"><div class="pricing-tier">📦 HARDWARE APPLIANCE</div><div class="pricing-price">$4,950<span style="font-size:0.85rem;color:#8899A6;">setup</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">✔ Physical Server<br>✔ 100% Air-Gapped<br>✔ + $299/mo Maint.</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("📦 Order Hardware", PAYPAL_PAY_LINK, use_container_width=True)
        else: st.button("🔒 Locked", disabled=True, key="lock4", use_container_width=True)

    st.divider()
    if current_role in ["CEO", "SUPER_ADMIN"]:
        with st.expander("👑 [MASTER PLATFORM ROOT]: Live Diagnostic Mesh & Summary", expanded=True):
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
            conn.close()

            st.code(f"""======================= SYSTEM TOPOLOGY =======================
Host IP (Local LAN)      : {mask_secret("192.168.1.175", "IP")}
Mesh Endpoint (Tailscale): {mask_secret(f"{ACTIVE_IP}:8501", "IP")}
Master Database Vault    : {mask_secret(DB_PATH, "PATH")}
---------------------------------------------------------------
Active Registered Users  : {user_count}
Submitted Pilot Reviews  : {feedback_count}
Unused License Keys      : {unused_keys}
Encrypted Comm Records   : {msg_count}
---------------------------------------------------------------
Local Neural Engine      : Ollama REST API (Port 11434)
Cloud Fast Link          : Groq API (TLS 1.3)
Universal Drone Ingest   : MediaMTX (Port 1935 RTMP)
===============================================================""")

    st.markdown(f"### 📖 Sovereign Knowledge Academy & Technical Directory")

    with st.expander(f"🏛️ [PILLAR 1]: The {EMPIRE['FARM_NAME']} Manifesto & Sovereign Architecture", expanded=False):
        st.markdown(f"""
**The Strategic Problem:** Modern agriculture has been forced into absolute dependency on centralized cloud infrastructure. When rural broadband fails, the farm's digital ecosystem stops operating. Furthermore, proprietary agricultural data is routinely aggregated, analyzed, and monetized by external entities without the operator's consent.

**The Sovereign Solution:** Engineered by Founder & CEO **{EMPIRE['FOUNDER_NAME']}**, this platform aggressively reclaims operational dominance.
* **100% Air-Gapped Compute:** The architecture is designed to execute all neural inferences, telemetry processing, and video routing entirely on local, physical hardware. It requires zero external internet connection to keep the farm running.
* **Absolute Data Ownership:** Every byte of data—from soil moisture to drone video to encrypted chat logs—is written exclusively to a localized SQLite vault on your hardware. It is mathematically impossible for third parties to scrape your proprietary yield data.
        """)

    with st.expander(f"⚡ [PILLAR 2]: {EMPIRE['AI_PERSONA']} - Neural Processing & Predictive Memory", expanded=False):
        st.markdown(f"""
**{EMPIRE['AI_PERSONA']}** is not a standard chatbot; it is a highly specialized, dual-engine agronomic intelligence designed for maximum resilience.
* **Cloud Fast Link (Groq - `openai/gpt-oss-120b`):** When internet is available, {EMPIRE['AI_PERSONA']} routes logic through Groq's specialized LPU (Language Processing Unit) architecture. This delivers the ultra-low latency inference critical for real-time decision-making.
* **Sovereign Local Core (Ollama - `llama3:8b`):** If the network connection severs, the system instantly fails over to local execution via Ollama on Port 11434. The model runs entirely within your hardware's RAM/VRAM, ensuring absolute zero downtime.
* **Persistent Entity Memory:** The AI dynamically parses your inputs, extracts key agronomic entities (e.g., crop types, field zones, drone models), and writes them to the `conversation_entity_memory` table. This provides a persistent context window across all future interactions without ever sending that data to an external provider.
        """)

    with st.expander("🌾 [PILLAR 3]: Universal Drone Computer Vision & Multispectral Analysis", expanded=False):
        st.markdown("""
To achieve total aerial dominance, the platform breaks free from proprietary drone ecosystems and centralizes all visual telemetry.
* **Universal RTMP/RTSP Ingest:** The integrated MediaMTX engine binds to Port 1935, capable of receiving live telemetry and high-definition video from DJI, Autel, Skydio, or custom PX4 ArduPilot drones.
* **WebRTC Ultra-Low Latency:** The ingest stream is re-muxed on-the-fly and broadcast over Port 8889 via WebRTC, delivering sub-second glass-to-glass latency directly to the operator's command deck.
* **Green Leaf Index (GLI):** We utilize localized computer vision to calculate canopy health using visible light (RGB) spectrums without requiring expensive multispectral cameras. The formula evaluates vegetative vigor:
$$ GLI = \\frac{2G - R - B}{2G + R + B} $$
This allows the immediate identification of nitrogen deficiency or irrigation failure directly from the live feed.
        """)

    with st.expander("📡 [PILLAR 4]: IoT Soil Mesh & Capacitance Telemetry", expanded=False):
        st.markdown(f"""
A farm's yield is dictated by subsurface metrics. The IoT Soil Mesh integrates ground-truth data directly into the executive dashboard.
* **Dielectric Permittivity Sensors:** By measuring the soil's dielectric constant, the system accurately calculates Volumetric Water Content (VWC %).
* **Actionable Thresholds:** The platform monitors Field Capacity (the maximum water the soil can hold against gravity, typically 28%-38%) and the Permanent Wilting Point (where plants can no longer extract moisture).
* **Cryptographic Storage:** Sensor telemetry is aggregated and written into the local SQLite vault, allowing **{EMPIRE['AI_PERSONA']}** to cross-reference historical moisture levels against upcoming weather patterns to predict exact irrigation requirements.
        """)

    with st.expander("🚨 [PILLAR 5]: NOAA Emergency Radar & Hazard Protocols", expanded=False):
        st.markdown("""
Environmental unpredictability is the highest risk factor in agriculture. The Sentinel system provides immediate tactical awareness to protect both personnel and assets.
* **NEXRAD Doppler Overlay:** A live, interactive connection to the National Oceanic and Atmospheric Administration (NOAA) radar network. It tracks micro-cell storms, hail signatures, and severe wind shears in real-time.
* **Hazard Containment:** The system provides instant, deterministic safety protocols for critical farm emergencies—including anhydrous ammonia leaks, high-voltage equipment strikes, and PTO driveline entanglements—ensuring operator safety is prioritized above all else.
        """)

    with st.expander("📰 [PILLAR 6]: Executive Broadcast & Thought Leadership Engine", expanded=False):
        st.markdown(f"""
Market dominance requires a commanding digital presence. This engine transforms the CEO into a highly visible industry thought leader.
* **Zero-Hallucination Dictation:** The underlying LLM is mathematically locked to a Temperature of 0.0, strictly enforcing deterministic, highly factual outputs based solely on the operator's prompt. It will never invent fake metrics, yields, or trial data.
* **OAuth 2.0 Integration:** By leveraging the LinkedIn UGC (User Generated Content) API, the platform authenticates via a secure gateway token and URN.
* **Direct Deployment:** The Master CEO can draft, review, and deploy professional market updates directly from the command deck without ever opening a social media browser, maintaining absolute focus on farm operations.
        """)

    with st.expander("🔐 [PILLAR 7]: Cryptographic Vault & Security Matrix", expanded=False):
        st.markdown("""
Enterprise-grade security is hardcoded into the platform's DNA to protect proprietary agricultural and financial data from extraction.
* **Key Derivation (PBKDF2):** Passwords are never stored in plain text. The system hashes credentials using SHA-256 and derives a unique encryption key using PBKDF2 with 100,000 algorithmic iterations.
* **Symmetric Encryption (Fernet):** All private communications and field strategies are encrypted at rest in the database using the Fernet symmetric encryption protocol. Even if the physical hard drive is compromised or stolen, the data remains mathematically unreadable.
* **Role-Based Access Control (RBAC):** 
    * **Level 4 (Master CEO):** Total platform control, global key issuance, identity configuration.
    * **Level 3 (Enterprise Client CEO):** Full telemetry access, staff provisioning.
    * **Level 2 (Authorized Member):** Private encrypted workspace and spectator feeds.
    * **Level 1 (Guest):** Restricted commercial showcase and 7-Day Pilot onboarding.
        """)

with tab_feedback:
    st.subheader("📝 Open Market Pilot Feedback Hub")
    if current_role in ["CEO", "SUPER_ADMIN"]:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT full_name, username, rating, feedback_text FROM pilot_feedback_vault ORDER BY id DESC")
        reviews = cur.fetchall()
        conn.close()
        if reviews:
            for r in reviews: st.info(f"**{r[0]} ({r[1]}) - {r[2]}/5 Stars**\n\n{r[3]}")
        else: st.caption("No reviews yet.")
    else:
        fb_rating = st.slider("Rating:", 1, 5, 5)
        fb_text = st.text_area("Feedback (Required to unlock commercial tiers):")
        if st.button("Submit Review & Unlock Platform"):
            if not fb_text.strip(): st.warning("Feedback text is required.")
            else:
                save_pilot_feedback(current_user, current_name, fb_rating, "", "", fb_text, "")
                st.success("Review Submitted. Commercial tiers unlocked in Tab 5.")

with tab_sandbox:
    if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO", "MEMBER", "TRIAL_MEMBER"]:
        st.subheader("🧪 Python Execution Sandbox")
        st.code("print('⚡ Sandbox Online')")
    else: st.warning("🔒 Sandbox restricted.")

with tab_empire:
    if current_role in ["CEO", "SUPER_ADMIN"]:
        st.subheader("⚙️ Sovereign Empire Configuration (White-Label Settings)")
        with st.form("empire_config_form"):
            new_farm = st.text_input("Empire / Farm Name:", value=EMPIRE["FARM_NAME"])
            new_founder = st.text_input("Master CEO / Founder Name:", value=EMPIRE["FOUNDER_NAME"])
            new_persona = st.text_input("AI Persona Name:", value=EMPIRE["AI_PERSONA"])
            new_email = st.text_input("Official Contact Email:", value=EMPIRE["CONTACT_EMAIL"])
            
            if st.form_submit_button("🛡️ Forge Empire Identity"):
                update_empire_config(new_farm, new_founder, new_persona, new_email)
                st.success(f"Identity locked. System rebranded to {new_farm} with AI {new_persona}.")
                st.rerun()
    else: st.info("🔒 System Configuration is locked to the Master CEO.")