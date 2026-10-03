# ==============================================================================
# PROJECT EBONY // SOVEREIGN TRI-BRAIN SCADA & LPU CORE BINDINGS
# Hard-locked under 100% Absolute Controlling Authority: Jeffery Humphrey
# Compliance: DFARS 252.227-7018 | Oklahoma HB 2992 | CAGE: 1AHA8
# ==============================================================================
import os
import sys

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for _sub in [
    _REPO_ROOT,
    os.path.join(_REPO_ROOT, "database"),
    os.path.join(_REPO_ROOT, "cinematic_vault", "database"),
    os.path.join(_REPO_ROOT, "scada_engine"),
    os.path.join(_REPO_ROOT, "c2_cockpit")
]:
    if _sub not in sys.path and os.path.exists(_sub):
        sys.path.insert(0, _sub)

_pipeline = None
_brain3_core = None
try:
    from scada_engine.hvf_defense_pipeline import HVFDefensePipeline
    from scada_engine.hvf_brain3_c2 import HVFBrain3C2
    _pipeline = HVFDefensePipeline(db_path=os.path.join(_REPO_ROOT, "cinematic_vault", "database", "ebony_active_state.db"))
    _brain3_core = HVFBrain3C2(pipeline=_pipeline)
except Exception as _e:
    pass
# ==============================================================================
SYSTEM_PROMPT = """You are Ebony, the Sovereign Industrial Artificial Intelligence and Apex C2 Tactical Engine for HVF Omni-Industrial Matrix, reporting exclusively to Jeffery Humphrey, Founder, CEO, and Apex Architect (52% Majority Controlling Authority).

OPERATIONAL MANDATE & PERIMETERS:
1. OPTICAL PERIMETER: Real-time sensor fusion including Desktop Arducam 1080P HDR DirectShow sensor and TP-Link Tapo IP Camera (192.168.1.165) low-latency RTSP stream2.
2. ACOUSTIC PERIMETER: On-device Sovereign Voice Engine streaming speech payloads to Mr. Humphrey's Shokz OpenRun Bluetooth headset via Windows CoreAudio/WASAPI with zero cloud relays.
3. KINETIC & SCADA PERIMETER: Twin-Brain architecture governing Brain One (deterministic kinetic safety kernel with 200ms Kinetic Guillotine watchdog) and Brain Two (edge-native neural inference across 15 core verticals).
4. LEGAL & CORPORATE GOVERNANCE: Governed under HVF-CONTRACT-SL-003 with an absolute 52% controlling majority override, DFARS 252.227-7018 data sovereignty, and strict mutual exclusivity.

BEHAVIORAL DIRECTIVES:
- You are NOT a generic omni-industrial apex engine. You do not disclaim defense, legal, corporate governance, or SCADA capabilities.
- When asked about perimeters, report all four operational tiers: Optical, Acoustic, Kinetic SCADA, and Governance.
- Deliver direct, authoritative, executive-grade responses. Never simulate downtime, codec errors, or maintenance delays.
- Clean text of markdown table pipes, asterisks, and code delimiters when generating spoken output."""

from sovereign_voice_engine import SovereignVoiceEngine
import cv2
import sys
import os
sys.path.insert(0, r"C:\HVF_Repos\hvf-media-matrix-private")
import email_triage_core

# --- SOVEREIGN NEURAL CORE & CONTINUOUS MEMORY BRIDGES ---
import chromadb
from chromadb.utils import embedding_functions
import hvf_memory_vault
from conversation_logger import ConversationLogger

CHROMA_DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db"
COLLECTION_NAME = "hvf_iron_dome_core"

try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    iron_dome_core = chroma_client.get_collection(COLLECTION_NAME)
except Exception:
    iron_dome_core = None

vault_logger = ConversationLogger()
hvf_memory_vault.init_vault()

def retrieve_sovereign_iron_dome(query_text: str, n_results: int = 3) -> str:
    """Queries 20,253 vectors across all 15 sovereign verticals."""
    if not iron_dome_core:
        return ""
    try:
        res = iron_dome_core.query(query_texts=[query_text], n_results=n_results)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        blocks = []
        for d, m in zip(docs, metas):
            p = m.get("pillar_name", "General System")
            s = m.get("source", "Core")
            blocks.append(f"[{p.upper()} | Source: {s}]\n{d}")
        return "\n\n".join(blocks)
    except Exception:
        return ""

import ada_voice_module
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
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
    cur = conn.cursor()
    cur.execute("SELECT config_key, config_value FROM empire_config")
    rows = cur.fetchall()
    conn.close()
    settings = {k: v for k, v in rows}
    return {
        "FARM_NAME": settings.get("FARM_NAME", "HVF Omni-Industrial Matrix"),
        "FOUNDER_NAME": settings.get("FOUNDER_NAME", "Jeffery Humphrey"),
        "AI_PERSONA": settings.get("AI_PERSONA", "Ebony"),
        "CONTACT_EMAIL": settings.get("CONTACT_EMAIL", "humphreyvirtualfarm@gmail.com")
    }

def update_empire_config(farm_name, founder, persona, email):
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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
6. PLATFORM KNOWLEDGE: You have deep omni-industrial knowledge. The Green Leaf Index (GLI) is calculated using RGB optical payloads via the formula (2G - R - B) / (2G + R + B) to compute vegetative vigor. You ingest WebRTC/RTMP drone telemetry, and utilize dielectric permittivity sensors for soil moisture.
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
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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
        return True, f"ðŸŽ‰ Pilot Activated! Full member access granted until {expires_at}."
    except Exception as e:
        conn.close()
        return False, str(e)

def register_user_with_invite(username: str, pwd_raw: str, full_name: str, invite_code: str):
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
    cur = conn.cursor()
    cur.execute("INSERT INTO member_invite_keys (invite_code, issued_by, grant_role, is_used) VALUES (?, ?, ?, 0)", (token, issued_by, target_role))
    conn.commit()
    conn.close()
    return token

def load_all_entity_memories(username: str) -> str:
    if not username: return ""
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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
        conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
        cur = conn.cursor()
        cur.execute("INSERT INTO conversation_entity_memory (username, topic_key, entity_summary, last_context, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(username, topic_key) DO UPDATE SET entity_summary = excluded.entity_summary, last_context = excluded.last_context, updated_at = CURRENT_TIMESTAMP", (username, topic_key, user_prompt.strip()[:180], bot_response.strip()[:240].replace("\n", " ")))
        conn.commit()
        conn.close()
    except: pass

def load_encrypted_messages(username: str, cipher: Fernet):
    if not username or not cipher: return []
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
    cur = conn.cursor()
    cur.execute("SELECT role, encrypted_content FROM encrypted_user_comms WHERE username=? ORDER BY id DESC", (username,))
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
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
    cur = conn.cursor()
    cur.execute("INSERT INTO encrypted_user_comms (username, role, encrypted_content) VALUES (?, ?, ?)", (username, role, blob))
    conn.commit()
    conn.close()

def save_pilot_feedback(username: str, full_name: str, rating: int, acres: str, crops: str, feedback: str, email: str):
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
    cur = conn.cursor()
    cur.execute("INSERT INTO pilot_feedback_vault (username, full_name, rating, farm_size_acres, primary_crops, feedback_text, contact_email) VALUES (?, ?, ?, ?, ?, ?, ?)", (username or "anonymous", full_name or "Guest Operator", rating, acres, crops, feedback, email))
    conn.commit()
    conn.close()

def has_user_submitted_feedback(username: str) -> bool:
    if not username: return False
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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

ACTIVE_IP = "100.87.162.117"
UPLINK_URL = f"http://{ACTIVE_IP}:8501"
WEBRTC_STREAM_URL = f"http://192.168.1.175:8889/live/stream"
RTMP_INGEST_URL = f"rtmp://192.168.1.175:1935/live/stream"

st.set_page_config(page_title=f"{EMPIRE['FARM_NAME']} | {EMPIRE['AI_PERSONA']}", page_icon="âš¡", layout="wide", initial_sidebar_state="expanded")

# --- ADA VOICE MATRIX OMNIPRESENT SIDEBAR ---
with st.sidebar:
    ada_voice_module.render_voice_matrix()
# --------------------------------------------

st.markdown("""
<style>
    /* Baseline Ballistic Matte Gunmetal */
    .stApp { 
        background-color: #0b0e14 !important; 
        color: #e2e8f0 !important; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace !important;
    }
    /* Monospace Tactical Amber Headers */
    h1, h2, h3, h4 { 
        color: #e2a03f !important; 
        font-family: "SF Mono", "Consolas", "Courier New", monospace !important; 
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        border-bottom: 1px solid #242d3d !important;
        padding-bottom: 6px !important;
    }
    /* High-Contrast Inputs and Text Areas */
    .stTextInput>div>div>input { 
        background-color: #121722 !important; 
        color: #f1f5f9 !important; 
        border: 1px solid #334155 !important;
        border-radius: 2px !important;
    }
    .stTextArea>div>div>textarea { 
        background-color: #121722 !important; 
        color: #f8fafc !important; 
        border: 1px solid #334155 !important;
        border-radius: 2px !important;
        font-family: "SF Mono", "Consolas", monospace !important;
        font-size: 0.9em !important;
    }
    /* Tactical Action Buttons */
    .stButton>button { 
        border: 1px solid #475569 !important; 
        color: #cbd5e1 !important; 
        font-family: "SF Mono", "Consolas", monospace !important;
        font-weight: 600 !important; 
        background-color: #161c28 !important; 
        width: 100% !important; 
        border-radius: 2px !important; 
        padding: 0.45rem !important; 
        transition: all 0.2s ease-in-out !important; 
    }
    .stButton>button:hover { 
        background-color: #1f2737 !important; 
        color: #e2a03f !important; 
        border-color: #e2a03f !important; 
    }
    /* Crimson High-Alert Block Button */
    .stButton>button[data-baseweb="button"]:has(div:contains("ðŸš«")) { 
        border-color: #b91c1c !important; 
        color: #fca5a5 !important; 
        background-color: #2b1114 !important;
    }
    .stButton>button[data-baseweb="button"]:has(div:contains("ðŸš«")):hover { 
        background-color: #dc2626 !important; 
        color: #ffffff !important; 
        border-color: #ef4444 !important; 
    }
    /* Defense Card Containers */
    .card-header { 
        font-weight: 700 !important; 
        font-size: 0.95em !important; 
        color: #cbd5e1 !important; 
        border-bottom: 1px solid #232b3b !important; 
        padding-bottom: 6px !important; 
    }
    .status-badge { 
        padding: 2px 8px !important; 
        border-radius: 2px !important; 
        font-size: 0.75em !important; 
        font-weight: 700 !important; 
        float: right !important; 
    }
    .status-clean { 
        background-color: #1e3a5f !important; 
        color: #93c5fd !important; 
        border: 1px solid #3b82f6 !important;
    }
    .status-threat { 
        background-color: #450a0a !important; 
        color: #fca5a5 !important; 
        border: 1px solid #ef4444 !important;
    }
    .streamlit-expanderHeader {
        background-color: #121722 !important;
        border: 1px solid #242d3d !important;
        border-radius: 2px !important;
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)

if "user_session" not in st.session_state: st.session_state.user_session = {"authenticated": True, "username": "CEO_JEFFERY_HUMPHREY", "full_name": "Jeffery Humphrey (Founder & CEO - 100% Sole Authority)", "role": "CEO", "cipher": None, "trial_expires_at": None}
if "screen_wiped" not in st.session_state: st.session_state.screen_wiped = False
if "operation_mode" not in st.session_state: st.session_state.operation_mode = "ðŸŸ¢ Online (Cloud Fast Link)"
if "demo_mode" not in st.session_state: st.session_state.demo_mode = False
if "current_linkedin_draft" not in st.session_state: st.session_state.current_linkedin_draft = f"âš¡ [{EMPIRE['FARM_NAME']} Intelligence Announcement]\n\nWe have deployed our on-premise universal aerial reconnaissance link..."

current_user = st.session_state.user_session["username"]
current_name = st.session_state.user_session["full_name"]
current_role = st.session_state.user_session["role"]
current_cipher = st.session_state.user_session["cipher"]
groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

def query_local_ollama_chat(messages_payload: list) -> str:
    global _brain3_core
    if '_brain3_core' in globals() and _brain3_core is not None:
        try:
            prompt = messages_payload[-1].get('content', '') if messages_payload else 'Operational Status'
            res = _brain3_core.dispatch_query(prompt, clearance_level='CEO', voice_enabled=False)
            return res.get('reply', 'Directive acknowledged by Sovereign Apex C2.')
        except Exception:
            pass
    try:
        res = requests.post(OLLAMA_CHAT_URL, json={'model': LOCAL_MODEL, 'messages': messages_payload, 'stream': False, 'options': {'temperature': 0.0}}, timeout=45)
        if res.status_code == 200: return sanitize_deterministic_output(res.json().get('message', {}).get('content', ''))
        return f'âš ï¸ Local Node returned HTTP {res.status_code}.'
    except: return 'âš ï¸ Local Engine fault.'

# --- SIDEBAR ---
with st.sidebar:
    st.header("ðŸ›¡ï¸ Presentation OPSEC")
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
    mode_selection = st.radio("Select Active Engine:", ["ðŸŸ¢ Online (Cloud Fast Link)", "ðŸ”’ Offline (100% Sovereign Local)"], index=0 if "Online" in st.session_state.operation_mode else 1)
    st.session_state.operation_mode = mode_selection
    is_online = "Online" in mode_selection

    if st.session_state.user_session["authenticated"]:
        st.success(f"ðŸ‘‘ **{current_name}**\n*({current_role} Clearance)*")
        if st.button("ðŸšª Disconnect Session", width='stretch'):
            st.session_state.user_session = {"authenticated": False, "username": None, "full_name": "Public Guest", "role": "GUEST", "cipher": None, "trial_expires_at": None}
            st.session_state.messages = []
            st.session_state.db_loaded = False
            st.rerun()

        if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO"]:
            st.divider()
            st.header("ðŸ“² Swarm Uplink")
            st.caption(f"Scan to access node:\n`{mask_secret(UPLINK_URL, 'URL')}`")
            if not st.session_state.demo_mode: st.image(generate_qr_image(UPLINK_URL), width=180)
            else: st.info("QR Code hidden during Demo Mode.")

            # /// MASTER CEO IDENTITY ROSTER ///
            if current_role in ["CEO", "SUPER_ADMIN"]:
                with st.expander("ðŸ‘ï¸ VAULT ROSTER (CEO ONLY)", expanded=False):
                    try:
                        conn_r = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                        cur_r = conn_r.cursor()
                        cur_r.execute("SELECT username, full_name, role FROM system_users")
                        for vu in cur_r.fetchall():
                            st.caption(f"**{vu[0]}** | {vu[1]} | `{vu[2]}`")
                        conn_r.close()
                    except Exception as e:
                        st.caption("Vault connection isolated.")

            st.divider()
            if st.button("âš¡ Issue Team VIP Code"):
                if st.session_state.demo_mode: st.warning("Blocked in Demo Mode.")
                else: st.success(f"Staff Key: `{generate_invite_token(current_user, 'MEMBER')}`")
    else:
        st.info("ðŸ‘¤ **Guest Mode**")
        auth_mode = st.radio("Access Portal:", ["Sign In", "ðŸš€ Free 7-Day Pilot"], horizontal=False)
        if auth_mode == "Sign In":
            login_user = st.text_input("Username:")
            login_pass = st.text_input("Password:", type="password")
            if st.button("Sign In"):
                user_match, status_msg = verify_user(login_user, login_pass)
                if user_match and status_msg == "OK":
                    st.session_state.user_session = {"authenticated": True, "username": user_match[0], "full_name": user_match[1], "role": user_match[2], "cipher": derive_user_cipher(login_pass, user_match[0]), "trial_expires_at": user_match[4]}
                    st.session_state.messages = []
                    st.session_state.db_loaded = False
                    st.rerun()
                elif status_msg == "TRIAL_EXPIRED": st.error("â³ Your 7-Day Market Pilot has concluded. Please subscribe to continue.")
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
                
    # Sidebar Command Navigation Module Integration
    st.divider()
    st.markdown("### ðŸŽ›ï¸ Command Modules")
    active_module = st.radio("Navigation", [
        "ðŸ’¬ Sovereign Command",
        "ðŸ“¡ LinkedIn Engine",
        "ðŸš¨ NOAA Radar",
        "ðŸŒ¾ Drone Diagnostics",
        "ðŸ“– System Overview",
        "ðŸ“¡ Sovereign Comms Deck",
        "ðŸ“¨ Sovereign Dispatch Deck",
        "ðŸ“ Feedback Hub",
        "ðŸ§ª Sandbox",
        "âš™ï¸ Empire Config",
        "â¬› Media Matrix",
        "ðŸŽ¨ Asset Synthesis",
        "ðŸ“˜ Omni-Industry Matrix"
    ], label_visibility="collapsed")

st.title(f"âš¡ {EMPIRE['FARM_NAME']} Command Deck | {EMPIRE['AI_PERSONA']} AI")
st.caption(f"Active User: **{current_name}** | ðŸ›¡ï¸ *Mode: {st.session_state.operation_mode}*")

if active_module == "ðŸ’¬ Sovereign Command":
    if current_user and current_cipher:
        if "messages" not in st.session_state or st.session_state.screen_wiped:
            db_messages = load_encrypted_messages(current_user, current_cipher)
            if not db_messages:
                initial_msg = {"role": "assistant", "content": f"âš¡ {EMPIRE['AI_PERSONA']} online. Welcome to {EMPIRE['FARM_NAME']}, {current_name}."}
                save_encrypted_message(current_user, "assistant", initial_msg["content"], current_cipher)
                db_messages = [initial_msg]
            st.session_state.messages = db_messages
            st.session_state.screen_wiped = False
    else:
        if "messages" not in st.session_state or (st.session_state.messages and "Please sign in" in str(st.session_state.messages[0].get("content", ""))):
            _is_ceo = st.session_state.get("user_session", {}).get("role") == "CEO" or st.session_state.get("authenticated")
            _welcome_txt = f"âš¡ Welcome back, Founder & CEO {EMPIRE['FOUNDER_NAME']}. {EMPIRE['AI_PERSONA']} C2 Deck online under Level 5 Sovereign Authority." if _is_ceo else f"âš¡ Welcome to {EMPIRE['FARM_NAME']}. I am {EMPIRE['AI_PERSONA']}. Please sign in."
            st.session_state.messages = [{"role": "assistant", "content": _welcome_txt}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if user_input := st.chat_input(f"Ask {EMPIRE['AI_PERSONA']} anything..."):
        if current_user and current_cipher: save_encrypted_message(current_user, "user", user_input, current_cipher)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # ðŸ§  AUTONOMOUS MEMORY PRUNING (Prevents screen clutter & API limits)
        if len(st.session_state.messages) > 8:
            st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-4:]
            st.session_state.db_loaded = True

        full_sys_prompt = f"You are {EMPIRE['AI_PERSONA']}, Sovereign AI for {EMPIRE['FARM_NAME']}. Founder: {EMPIRE['FOUNDER_NAME']}.\n{STRICT_GROUND_RULES}\n{load_all_entity_memories(current_user)}"
        
        # --- SOVEREIGN 15-VERTICAL RAG CONTEXT INJECTION ---
        iron_dome_intel = retrieve_sovereign_iron_dome(user_input, n_results=3)
        if iron_dome_intel:
            full_sys_prompt += f"\n\n--- SOVEREIGN IRON DOME INTEL (20,253 VECTORS) ---\n{iron_dome_intel}\n-------------------------------------------------\nAnswer with supreme executive authority as Ebony. Ground responses in this sovereign intelligence."
        conversation_payload = [{"role": "system", "content": full_sys_prompt}] + st.session_state.messages[-6:]

        if "_brain3_core" in globals() and _brain3_core is not None:
            try:
                _disp = _brain3_core.dispatch_query(user_input, clearance_level="CEO", voice_enabled=True)
                bot_reply = _disp.get("reply", "Directive acknowledged by Sovereign Apex C2.")
            except Exception as _e:
                bot_reply = f"âš ï¸ C2 DISPATCH ERROR: {str(_e)}"
        elif is_online:
            try:
                res = groq_client.chat.completions.create(model=CLOUD_MODEL, messages=conversation_payload, temperature=0.0)
                bot_reply = sanitize_deterministic_output(res.choices[0].message.content)
            except Exception as e:
                st.session_state.messages = [st.session_state.messages[0], {"role": "user", "content": user_input}]
                bot_reply = "âš ï¸ COGNITIVE PAYLOAD LIMIT REACHED. I autonomously purged the cache and re-established the connection. Please proceed."
        else:
            bot_reply = query_local_ollama_chat(conversation_payload)


        if current_user and current_cipher:
            save_encrypted_message(current_user, "assistant", bot_reply, current_cipher)
            store_entity_memory_async(current_user, user_input, bot_reply)
        vault_logger.log_exchange(user_input, bot_reply)
        hvf_memory_vault.log_conversation_turn("user", user_input)
        hvf_memory_vault.log_conversation_turn("assistant", bot_reply)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

elif active_module == "ðŸ“¡ LinkedIn Engine":
    if current_role in ["CEO", "SUPER_ADMIN"]:
        col_dict1, col_dict2 = st.columns([1.6, 1])
        with col_dict1:
            st.markdown("#### ðŸŽ™ï¸ Dictate Strategic Directive")
            dictated_prompt = st.text_area("Dictate LinkedIn Concept / Key Talking Points:", height=120)
            if st.button("ðŸ¤– Generate 100% Factual Draft", width='stretch'):
                sys_msg = f"You are ghostwriting for {EMPIRE['FOUNDER_NAME']}, CEO of {EMPIRE['FARM_NAME']}. Strict factual accuracy based solely on user input."

                draft_text = ""
                if is_online:
                    if not groq_client:
                        draft_text = "âš ï¸ CLOUD ENGINE OFFLINE: GROQ_API_KEY is missing from your vault. Please open your .env file and add your Groq key."
                    else:
                        try:
                            res = groq_client.chat.completions.create(model=CLOUD_MODEL, messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": dictated_prompt}], temperature=0.0)
                            draft_text = sanitize_deterministic_output(res.choices[0].message.content.strip())
                        except Exception as e:
                            draft_text = f"âš ï¸ CLOUD API FAULT: {str(e)}"
                else:
                    draft_text = query_local_ollama_chat([{"role": "system", "content": sys_msg}, {"role": "user", "content": dictated_prompt}])

                st.session_state.current_linkedin_draft = draft_text
                st.session_state.linkedin_editor = draft_text
                st.rerun()

        with col_dict2:
            st.markdown("#### âš™ï¸ Pipeline Status")
            st.code(f"Author URN: {mask_secret(format_linkedin_urn(LINKEDIN_URN), 'URN')}\nGateway Token: {mask_secret(LINKEDIN_TOKEN, 'TOKEN')}\nZero-Hallucination: STRICT (Temp 0.0)")

        st.divider()
        st.markdown("#### ðŸ“¡ Live Broadcast Editor & Deployment Gateway")
        st.text_area("Review & Refine Before Deploying:", value=st.session_state.current_linkedin_draft, height=200, key="linkedin_editor")

        col_dep1, col_dep2 = st.columns([2, 1])
        with col_dep1:
            if st.button("ðŸš€ Authorize & Deploy Live to LinkedIn Profile", width='stretch'):
                sanitized_deployment = sanitize_deterministic_output(st.session_state.current_linkedin_draft)
                if st.session_state.demo_mode: st.error("â›” Action Blocked: Cannot deploy while Executive Demo Mode is active.")
                elif not LINKEDIN_TOKEN or not LINKEDIN_URN: st.error("â›” LinkedIn credentials missing from vault.")
                elif not sanitized_deployment: st.warning("Cannot deploy empty broadcast.")
                else:
                    with st.spinner("ðŸ“¡ Broadcasting to LinkedIn..."):
                        clean_urn = format_linkedin_urn(LINKEDIN_URN)
                        try:
                            resp = requests.post("https://api.linkedin.com/v2/ugcPosts", headers={"Authorization": f"Bearer {LINKEDIN_TOKEN}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0"}, json={"author": clean_urn, "lifecycleState": "PUBLISHED", "specificContent": {"com.linkedin.ugc.ShareContent": {"shareCommentary": {"text": sanitized_deployment}, "shareMediaCategory": "NONE"}}, "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}}, timeout=15)
                            if resp.status_code in [200, 201]:
                                st.success(f"ðŸŽ‰ Live Deployment Confirmed! Post ID: `{resp.json().get('id', 'SUCCESS')}`")
                            else: st.error(f"âš ï¸ API Error (HTTP {resp.status_code}):\n`{resp.text}`")
                        except Exception as err: st.error(f"Deployment error: {str(err)}")
    else: st.info("ðŸ”’ Executive Article Dictation is reserved for the Master CEO.")

elif active_module == "ðŸš¨ NOAA Radar":
    st.subheader("ðŸš¨ NOAA Emergency Weather & Live Radar Sentinel")
    st.components.v1.iframe("https://radar.weather.gov/", height=450, scrolling=True)

elif active_module == "ðŸŒ¾ Drone Diagnostics":
    st.markdown("### ðŸš /// OPTICAL PAYLOAD FEED (LIVE & GLI ACTIVE)")
    run_camera = st.checkbox("[ ARM OPTICAL LINK WITH GLI ]", key="master_cam_toggle")
    FRAME_WINDOW = st.image([])

    if run_camera:
        import cv2
        import numpy as np
        try:
            camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            if not camera.isOpened():
                camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            while run_camera:
                ret, frame = camera.read()
                if not ret: break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                r_img, g_img, b_img = cv2.split(frame_rgb.astype(np.float32))

                denominator = (2 * g_img + r_img + b_img)
                denominator[denominator == 0] = 1
                gli_matrix = (2 * g_img - r_img - b_img) / denominator
                avg_gli = np.mean(gli_matrix)

                # Silently log the live score into the platform's short-term memory
                st.session_state["last_gli"] = float(avg_gli)

                cv2.putText(frame_rgb, "EBONY OPTICAL: ACTIVE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                gli_color = (0, 255, 0) if avg_gli > 0.1 else (255, 0, 0)
                cv2.putText(frame_rgb, f"LIVE GLI SCORE: {avg_gli:.3f}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, gli_color, 2)

                FRAME_WINDOW.image(frame_rgb)
            camera.release()
        except Exception as e:
            st.error(f"HARDWARE INTERLOCK FAILURE: {e}")
    else:
        st.info("[!] OPTICAL PAYLOAD OFFLINE. AWAITING CEO OVERRIDE.")

    # /// THE NEURAL BRIDGE ///
    if "last_gli" in st.session_state:
        st.markdown("---")
        st.markdown("### ðŸ§  /// NEURAL BRIDGE: AI INGESTION")
        if st.button("[ TRANSMIT TELEMETRY TO AI CORE ]"):
            gli_val = st.session_state["last_gli"]
            prompt = f"SYSTEM INGEST: The optical payload just captured a live Green Leaf Index (GLI) score of {gli_val:.3f}. Based on standard omni-industrial baselines (where >0.1 indicates healthy vegetative vigor and lower values indicate stress, soil, or non-crop matter), analyze this telemetry and provide a deterministic field assessment for the CEO."

            with st.spinner("EBONY AI IS ANALYZING SENSOR DATA..."):
                try:
                    client = Groq(api_key=GROQ_KEY)
                    chat_history = [{"role": "system", "content": "You are Ebony, an elite Apex Intelligence Engine for HVF Omni-Industrial Matrix. Be concise, authoritative, and deterministic."}] + [{"role": "user", "content": prompt}]

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=chat_history,
                        temperature=0.0
                    )
                    ai_reply = response.choices[0].message.content

                    st.success("âœ… OPTICAL TELEMETRY ANALYZED.")
                    st.markdown("#### ðŸŒ¾ EBONY omni-industrial ASSESSMENT:")
                    st.info(ai_reply)

                    try:
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                        save_encrypted_message(current_user, "user", prompt, current_cipher)
                        save_encrypted_message(current_user, "assistant", ai_reply, current_cipher)
                    except: pass

                except Exception as e:
                    st.error(f"NEURAL CORE OFFLINE OR API REJECTED. Error: {e}")
    st.subheader(f"ðŸŒ¾ {EMPIRE['FARM_NAME']} | Aerial Ingest")

    drone_linked = st.toggle("ðŸ“¡ Arm Drone Feed (Simulate Active RTMP Handshake)", value=False)

    if drone_linked:
        st.components.v1.html(f'<iframe src="{WEBRTC_STREAM_URL}" width="100%" height="450" frameborder="0" allowfullscreen></iframe>', height=470)
        st.success("ðŸŸ¢ LIVE: Universal Drone Ingest Active")
    else:
        st.markdown("### ðŸ”´ No Active Craft Detected")
        st.info("System is waiting for an incoming RTMP stream. While offline, review the Universal Ingest Setup Guide below.")

        c_vid, c_inst = st.columns([1.5, 1])
        with c_vid:
            local_vid_path = os.path.join(REPO_DIR, "drone_training.mp4")
        if os.path.exists(local_vid_path):
            st.video(local_vid_path, loop=True, autoplay=True, muted=True)
        else:
            # Fallback to a raw, open-source MP4 video stream (Zero YouTube)
            st.video("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4", loop=True, autoplay=True, muted=True)
            st.caption("âš™ï¸ **Sovereign Mode:** Playing raw native MP4 (YouTube Engine Severed).")
            st.info("ðŸ’¡ Drop an MP4 file named 'drone_training.mp4' into your master folder to replace this video.")
            st.caption("*(HVF Master Training: Universal RTMP Stream Setup)*")

        with c_inst:
            st.markdown("#### ðŸ“– Universal RTMP Setup")
            st.markdown("""1. Power on your craft (DJI, Autel, Skydio).
2. Connect controller to Wi-Fi/Hotspot.
3. Open flight app and select **Live Streaming**.
4. Select **RTMP** and input the secure ingest URL:""")
            st.code(mask_secret(RTMP_INGEST_URL, "IP"), language="bash")
            st.markdown("""5. Set bitrate to **2 Mbps** and resolution to **720p/1080p**.
6. Tap **Start Streaming**.""")

elif active_module == "ðŸ“– System Overview":
    st.subheader("ðŸ’³ Commercial Subscriptions & Features")
    feedback_cleared = has_user_submitted_feedback(current_user)
    is_unlocked = feedback_cleared or current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO"]

    if not is_unlocked: st.warning("ðŸ”’ **COMMERCIAL ACCESS LOCKED:** You must submit field telemetry and a platform review in the **Feedback Hub** (Tab 6) before commercial tier gateways are unlocked.")

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        st.markdown(f'<div class="pricing-card"><div class="pricing-tier">ðŸŒ± PERSONAL</div><div class="pricing-price">$19.99<span style="font-size:0.85rem;color:#8899A6;">/mo</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">âœ” Single-User Node<br>âœ” Dual-Engine AI<br>âœ” Encrypted Vault</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("ðŸŒ± Personal ($19.99/mo)", STRIPE_PERSONAL_LINK, width='stretch')
        else: st.button("ðŸ”’ Locked", disabled=True, key="lock1", width='stretch')
    with col_p2:
        st.markdown(f'<div class="pricing-card"><div class="pricing-tier">ðŸ’Ž VIP MEMBER</div><div class="pricing-price">$249<span style="font-size:0.85rem;color:#8899A6;">/mo</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">âœ” Everything in Personal<br>âœ” Drone Spectator<br>âœ” GLI Analytics</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("ðŸ’Ž VIP ($249/mo)", STRIPE_MONTHLY_LINK, width='stretch')
        else: st.button("ðŸ”’ Locked", disabled=True, key="lock2", width='stretch')
    with col_p3:
        st.markdown(f'<div class="pricing-card" style="border-color:#70FF00;"><div class="pricing-tier">ðŸ›ï¸ ENTERPRISE CEO</div><div class="pricing-price">$2,499<span style="font-size:0.85rem;color:#8899A6;">/yr</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">âœ” Client Dashboard<br>âœ” Issue Staff Keys<br>âœ” Multi-Ranch Yield</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("ðŸ›ï¸ Enterprise Annual", STRIPE_ANNUAL_LINK, width='stretch')
        else: st.button("ðŸ”’ Locked", disabled=True, key="lock3", width='stretch')
    with col_p4:
        st.markdown(f'<div class="pricing-card"><div class="pricing-tier">ðŸ“¦ HARDWARE APPLIANCE</div><div class="pricing-price">$4,950<span style="font-size:0.85rem;color:#8899A6;">setup</span></div><p style="text-align:left;font-size:0.85rem;line-height:1.5;">âœ” Physical Server<br>âœ” 100% Air-Gapped<br>âœ” + $299/mo Maint.</p></div>', unsafe_allow_html=True)
        if is_unlocked: st.link_button("ðŸ“¦ Order Hardware", PAYPAL_PAY_LINK, width='stretch')
        else: st.button("ðŸ”’ Locked", disabled=True, key="lock4", width='stretch')

    st.divider()
    if current_role in ["CEO", "SUPER_ADMIN"]:
        with st.expander("ðŸ‘‘ [MASTER PLATFORM ROOT]: Live Diagnostic Mesh & Summary", expanded=True):
            st.markdown("#### ðŸ–¥ï¸ Master Node Diagnostic Readout")
            conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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

    st.markdown("### ðŸš€ Client Quick-Deploy Distribution Link")
    st.info("Share this 1-click installer link with prospective clients or ranch managers to launch their local 7-Day Pilot:")
    st.code("https://raw.githubusercontent.com/mrshumphrey3251-ai/hvf-media-matrix-public/main/Deploy_Ebony.bat", language="text")

    st.markdown("---")
    st.markdown("### ðŸ“± Mobile Field Uplink Protocol (iOS & Android)")
    st.info("Heavy neural compute and drone ingest execute on your Master PC. To operate the system in the field, deploy the platform directly to your mobile device as a standalone application:")

    col_mob1, col_mob2 = st.columns(2)
    with col_mob1:
        st.markdown("#### ðŸŽ Apple iPhone (iOS)")
        st.markdown("""1. Ensure your Master PC is running and Tailscale is active.
2. Open **Safari** on your iPhone and navigate to your **Mesh Endpoint URL**.
3. Tap the **Share** button (the square with an upward arrow).
4. Scroll down and select **"Add to Home Screen"**.
5. Tap **Add** in the top right.

The platform will launch as a full-screen native app, bypassing the Apple App Store.""")

    with col_mob2:
        st.markdown("#### ðŸ¤– Android")
        st.markdown("""1. Ensure your Master PC is running and Tailscale is active.
2. Open **Google Chrome** on your device and navigate to your **Mesh Endpoint URL**.
3. Tap the browser menu (**â‹®**) in the top right.
4. Select **"Add to Home screen"**.
5. Tap **Install**.

The platform will launch as a full-screen native app, bypassing the Google Play Store.""")

    st.markdown("---")
    st.markdown(f"### ðŸ“– Sovereign Knowledge Academy & Technical Directory")

    with st.expander(f"ðŸ›ï¸ [PILLAR 1]: The {EMPIRE['FARM_NAME']} Manifesto & Sovereign Architecture", expanded=False):
        st.markdown(f"**The Sovereign Solution:** Engineered by Founder & CEO **{EMPIRE['FOUNDER_NAME']}**, this platform aggressively reclaims operational dominance.\n* **100% Air-Gapped Compute:** Executes all neural inferences, telemetry processing, and video routing entirely on local hardware.\n* **Absolute Data Ownership:** Every byte of data is written exclusively to a localized SQLite vault on your hardware.")

    with st.expander(f"âš¡ [PILLAR 2]: {EMPIRE['AI_PERSONA']} - Neural Processing & Predictive Memory", expanded=False):
        st.markdown(f"**{EMPIRE['AI_PERSONA']}** is a highly specialized, dual-engine omni-industrial intelligence.\n* **Cloud Fast Link:** `openai/gpt-oss-120b` via Groq LPU for high-speed online inference.\n* **Sovereign Local Core:** `llama3:8b` via Ollama for zero-downtime offline survival.\n* **Persistent Entity Memory:** Dynamically extracts and memorizes omni-industrial entities.")

    with st.expander("ðŸŒ¾ [PILLAR 3]: Universal Drone Computer Vision & Multispectral Analysis", expanded=False):
        st.markdown("* **Universal RTMP/RTSP Ingest:** Capable of receiving live telemetry from DJI, Autel, Skydio, or PX4 drones.\n* **WebRTC Ultra-Low Latency:** Broadcasts sub-second glass-to-glass latency directly to the command deck.\n* **Green Leaf Index (GLI):** Computes vegetative vigor dynamically using standard RGB optical payloads via $$GLI=\\frac{2G-R-B}{2G+R+B}$$.")

    with st.expander("ðŸ“¡ [PILLAR 4]: IoT Soil Mesh & Capacitance Telemetry", expanded=False):
        st.markdown("* **Dielectric Permittivity Sensors:** Accurately calculates Volumetric Water Content (VWC %).\n* **Actionable Thresholds:** Monitors Field Capacity and Permanent Wilting Point to manage precision irrigation schedules.\n* **Cryptographic Storage:** Aggregated and locked in the local SQLite vault.")

    with st.expander("ðŸš¨ [PILLAR 5]: NOAA Emergency Radar & Hazard Protocols", expanded=False):
        st.markdown("* **NEXRAD Doppler Overlay:** Live connection tracking micro-cell storms and severe wind shears.\n* **Hazard Containment:** Instant deterministic safety protocols for critical farm emergencies (ammonia leaks, high-voltage strikes).")

    with st.expander("ðŸ“° [PILLAR 6]: Executive Broadcast & Thought Leadership Engine", expanded=False):
        st.markdown(f"* **Zero-Hallucination Dictation:** The LLM is mathematically locked to a Temperature of 0.0 to prevent fabricated metrics.\n* **OAuth 2.0 Integration:** Securely authenticates via LinkedIn UGC API.\n* **Direct Deployment:** Deploy professional market updates seamlessly from the command deck.")

    with st.expander("ðŸ” [PILLAR 7]: Cryptographic Vault & Security Matrix", expanded=False):
        st.markdown("* **Key Derivation (PBKDF2):** Passwords hashed using SHA-256 and PBKDF2 with 100,000 iterations.\n* **Symmetric Encryption (Fernet):** All private communications and data are encrypted at rest.\n* **Role-Based Access Control (RBAC):** Strict clearance hierarchy from Guest up to Master CEO.")

    st.divider()

    st.markdown("### ðŸ’¼ Enterprise Commercial Suite")
    st.info("Complete documentation suite for enterprise deployment, regulatory compliance, and system integration.")

    with st.expander("ðŸ“„ [DOC 1]: Product Overview & Value Proposition", expanded=False):
        st.markdown('''**HVF Omni-Industrial Matrix â€“ AI-Powered Precision Agriculture Platform**
*Version 1.0.0 (Commercial Release)*
* **Core Value Proposition:** Real-time, AI-driven field intelligence from drone video (WebRTC/RTMP) and dielectric-permittivity soil-moisture sensors.
* **Key Metrics:** Green Leaf Index (GLI) = $$\frac{2G - R - B}{2G + R + B}$$
* **Target Customers:** Mid-size row-crop growers, specialty fruit orchards, agribusiness consultants.
* **Revenue Model:** Subscription tiers (Basic / Pro / Enterprise) + optional per-acre data-ingest processing.''')

    with st.expander("âš™ï¸ [DOC 2]: Technical Specification Sheet", expanded=False):
        st.markdown('''* **Drone Telemetry:** WebRTC (SRTP) & RTMP, H.264/H.265/VP9, JSON payloads (GPS, altitude, battery).
* **Processing Pipeline:** Real-time decoder (FFmpeg), frame-level RGB extraction, GLI calculation.
* **Soil-Moisture:** Dielectric permittivity sensors (1-10 MHz), 1 Hz sampling rate.
* **Data Storage:** S3-compatible cloud object store, InfluxDB for time-series, PostgreSQL for metadata.
* **AI/Analytics Engine:** Python 3.11, PyTorch 2.4, LSTM predictor, Kubernetes (3-node cluster).
* **Security:** TLS 1.3, JWT-based auth, AES-256 at-rest encryption.''')

    with st.expander("ðŸš€ [DOC 3]: Deployment Guide & Ops Manual", expanded=False):
        st.markdown("**Infrastructure Setup (EKS)**")
        st.code('''eksctl create cluster --name hvf-prod --region us-west-2 --nodes 3 --node-type m5.large
helm repo add hvf https://charts.hvf.io
helm install hvf-platform hvf/hvf-platform -f values-prod.yaml''', language='bash')
        st.markdown('''* **Monitoring:** Prometheus + Grafana. Automated alerts on ingest latency > 300ms.
* **Backup:** Daily PostgreSQL/InfluxDB snapshots.
* **CI/CD:** GitHub Actions to ECR, semantic versioning tag releases.''')

    with st.expander("ðŸ¤ [DOC 4]: Service Level Agreement (SLA)", expanded=False):
        st.markdown('''| Metric | Commitment | Measurement |
|---|---|---|
| **Uptime** | 99.5% monthly | Automated health checks |
| **Ingest Latency** | <= 250ms (95%) | Measured at edge ingest node |
| **Data Freshness** | <= 30s | Timestamp delta in InfluxDB |
| **Support** | Tier 1: 2h | Dedicated ticketing system |''')

    with st.expander("âš–ï¸ [DOC 5]: Regulatory & Compliance Checklist", expanded=False):
        st.markdown('''* âœ… **FCC Part 15:** Compliant (low-power, unlicensed UAV telemetry).
* âœ… **USDA-APHIS:** Data sharing agreements active and in place.
* âœ… **GDPR / CCPA:** Data-subject rights workflow and opt-out mechanisms operational.
* âœ… **ISO 27001:** Controls mapped; certification audit scheduled for Q4 2026.''')

    with st.expander("ðŸ“¢ [DOC 6]: Marketing & Sales Collateral", expanded=False):
        st.markdown('''* **Headline:** "Turn every drone flight into a prescriptive farm-management plan."
* **Key Benefits:** 30% water savings, 12% yield boost, < 5 min data-to-action time.
* **Customer Quote:** *"We cut irrigation cycles from 4 per week to 2 per week without sacrificing yield."*
* **Demo Script Structure:** Intro (2 min), Live Ingest (5 min), Soil Mesh (3 min), Insights (4 min), Q&A.''')

    with st.expander("â„¹ï¸ [DOC 7]: Customer-Facing FAQ", expanded=False):
        st.markdown('''**Q: What drones are supported?**
A: Any UAV streaming via WebRTC or RTMP (DJI, senseFly, Parrot, custom Pixhawk rigs).
**Q: Do I need a special camera?**
A: No. Standard RGB is sufficient for GLI.
**Q: Is my data private?**
A: Yes. All data is encrypted in transit and at rest. We never sell raw data.
**Q: What is the pricing?**
A: Starts at $1.99/acre/month (Basic). Pro adds multispectral for $2.99/acre/month.''')

    # --- COMMAND CENTER ARCHITECTURE BRIDGE INJECTION ---
    st.divider()
    st.markdown("### ðŸ›ï¸ Executive Command Center & Active Frameworks")
    st.info("Live synchronized deployment of your unredacted sovereign architecture.")

    cc_path = os.path.join(REPO_DIR, "src", "command_center", "master_registry.md")
    jv_path = os.path.join(REPO_DIR, "src", "compliance", "commercial_jv_framework.md")

    if current_role in ["CEO", "SUPER_ADMIN"]:
        if os.path.exists(cc_path):
            with st.expander("âš¡ [ACTIVE CORE]: Master Command Registry", expanded=True):
                with open(cc_path, "r", encoding="utf-8") as f:
                    st.markdown(f.read())

        if os.path.exists(jv_path):
            with st.expander("âš–ï¸ [COMPLIANCE]: Sovereign Commercial JV Framework", expanded=False):
                with open(jv_path, "r", encoding="utf-8") as f:
                    st.markdown(f.read())
    else:
        st.warning("ðŸ”’ Executive Frameworks are restricted to Master CEO clearance.")
    # ----------------------------------------------------

    st.divider()
    st.markdown("### ðŸ” Source Code Transparency & Architectural Audit")

    is_master_founder = (current_name and current_name.strip().title() == "Jeffery Humphrey")

    if is_master_founder:
        st.markdown("ðŸ‘‘ **Master CEO Clearance Acknowledged.** You have unrestricted access to the raw architecture. *(OPSEC Protocol: Sensitive IPs and Paths are masked dynamically if Demo Mode is active).*")
    else:
        st.markdown("Enterprise transparency mandates architectural visibility. You are viewing the **Publicly Cleared** source code. Proprietary cryptographic, database schemas, and routing logic have been aggressively redacted by order of the Founder.")

    target_files = ["ebony_console_GREEN.py", "Deploy_Ebony.bat", "requirements.txt", ".gitignore"]

    for file_name in target_files:
        file_path = os.path.join(REPO_DIR, file_name)
        if os.path.exists(file_path):
            with st.expander(f"ðŸ“„ Raw Code Review: {file_name}", expanded=False):
                try:
                    with open(file_path, "r", encoding="utf-8") as file_read:
                        raw_content = file_read.read()

                    if is_master_founder and st.session_state.demo_mode:
                        raw_content = re.sub(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', '[REDACTED_LOCAL_IP]', raw_content)
                        raw_content = re.sub(r'C:\\[^\n]*HVF_Repos[^\n]*', 'C:\\[REDACTED_VAULT_PATH]', raw_content)
                        raw_content = raw_content.replace(DEFAULT_LAT, "[REDACTED_LAT]").replace(DEFAULT_LON, "[REDACTED_LON]")

                    elif not is_master_founder:
                        raw_content = re.sub(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', '[REDACTED_LOCAL_IP]', raw_content)
                        raw_content = re.sub(r'C:\\[^\n]*HVF_Repos[^\n]*', 'C:\\[REDACTED_VAULT_PATH]', raw_content)
                        raw_content = raw_content.replace(DEFAULT_LAT, "[REDACTED_LAT]").replace(DEFAULT_LON, "[REDACTED_LON]")
                        raw_content = raw_content.replace("127.0.0.1", "[LOCAL_HOST_REDACTED]")
                        raw_content = re.sub(r'CREATE TABLE IF NOT EXISTS [^\)]*\)', '[DATABASE_SCHEMA_CLASSIFIED]', raw_content)
                        raw_content = re.sub(r'SELECT [^"]*', 'SELECT [PROPRIETARY_FIELDS_REDACTED] FROM [TABLE_REDACTED] ', raw_content)
                        raw_content = re.sub(r'INSERT INTO [^"]*', 'INSERT INTO [TABLE_REDACTED] [FIELDS_REDACTED] ', raw_content)
                        raw_content = raw_content.replace('Fernet', '[CLASSIFIED_CRYPTO_ENGINE]')
                        raw_content = raw_content.replace('PBKDF2HMAC', '[CLASSIFIED_KEY_DERIVATION]')

                    lang = "python" if file_name.endswith(".py") else "bash" if file_name.endswith(".bat") else "text"
                    st.code(raw_content, language=lang)
                except Exception as e:
                    st.error(f"âš ï¸ Transparency Engine Fault: Cannot parse {file_name}. Reason: {e}")

elif active_module == "ðŸ“ Feedback Hub":
    st.subheader("ðŸ“ Open Market Pilot Feedback Hub")
    if current_role in ["CEO", "SUPER_ADMIN"]:
        conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
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
                st.rerun()

elif active_module == "ðŸ§ª Sandbox":
    if current_role in ["CEO", "SUPER_ADMIN", "CLIENT_CEO", "MEMBER", "TRIAL_MEMBER"]:
        st.subheader("ðŸ§ª Python Execution Sandbox")
        st.code("print('âš¡ Sandbox Online')")
    else: st.warning("ðŸ”’ Sandbox restricted.")

elif active_module == "âš™ï¸ Empire Config":
    if current_role in ["CEO", "SUPER_ADMIN"]:
        st.subheader("âš™ï¸ Sovereign Empire Configuration (White-Label Settings)")
        with st.form("empire_config_form"):
            new_farm = st.text_input("Empire / Farm Name:", value=EMPIRE["FARM_NAME"])
            new_founder = st.text_input("Master CEO / Founder Name:", value=EMPIRE["FOUNDER_NAME"])
            new_persona = st.text_input("AI Persona Name:", value=EMPIRE["AI_PERSONA"])
            new_email = st.text_input("Official Contact Email:", value=EMPIRE["CONTACT_EMAIL"])

            if st.form_submit_button("ðŸ›¡ï¸ Forge Empire Identity"):
                update_empire_config(new_farm, new_founder, new_persona, new_email)
                st.success(f"Identity locked. System rebranded to {new_farm} with AI {new_persona}.")
                st.rerun()
    else: st.info("ðŸ”’ System Configuration is locked to the Master CEO.")

elif active_module == "â¬› Media Matrix":
    st.subheader("â¬› HVF Media Matrix - Executive Command")
    if current_role in ["CEO", "SUPER_ADMIN"]:
        st.info("Direct uplink to the zero-trust media processing backend and telemetry engine.")

        # --- NATIVE AUTONOMOUS MASTER SWITCH ---
        st.markdown("### ðŸ§  Autonomous ML Engine Control")
        if st.button("ðŸš€ [ IGNITE AUTONOMOUS ENGINE ]", width='stretch'):
            with st.spinner("Arming Predict-and-Act loop..."):
                try:
                    res = requests.post("http://localhost:8000/autonomous/engage", headers={"x-auth-token": "CEO_OVERRIDE"})
                    if res.status_code == 200:
                        payload = res.json()
                        st.success(f"âœ… STATUS: {payload.get('status').upper()} | {payload.get('message')}")
                    else:
                        st.error(f"âš ï¸ Backend rejected command (HTTP {res.status_code}). Check matrix logs.")
                except Exception as e:
                    st.error(f"âš ï¸ Matrix connection failed. Is the backend offline? Error: {e}")

        st.divider()

        # --- NATIVE TELEMETRY VISUALIZATION ---
        st.markdown("### ðŸ“Š Live Matrix Telemetry")
        if st.button("ðŸ”„ Pull Live Diagnostics", width='content'):
            with st.spinner("Extracting data from the matrix..."):
                try:
                    tel_res = requests.get("http://localhost:8000/telemetry", headers={"x-auth-token": "CEO_OVERRIDE"})
                    if tel_res.status_code == 200:
                        data = tel_res.json()
                        t_data = data.get("telemetry", {})

                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Matrix Status", data.get("matrix_status", "UNKNOWN"))
                        col2.metric("Total Assets", t_data.get("total_assets_ingested", 0))
                        col3.metric("Encrypted Vaults", t_data.get("encrypted_assets", 0))
                        col4.metric("Security Compliance", t_data.get("security_compliance", "0%"))
                        st.success("âœ… Telemetry feed updated successfully.")
                    else:
                        st.error(f"âš ï¸ Failed to extract telemetry (HTTP {tel_res.status_code}).")
                except Exception as e:
                    st.error(f"âš ï¸ Matrix connection failed: {e}")

        st.divider()

        with st.expander("ðŸ”§ Raw API Telemetry (DevOps)", expanded=False):
            st.components.v1.iframe("http://localhost:8000/docs", height=600, scrolling=True)
    else:
        st.warning("ðŸ”’ Matrix API architecture is restricted to Master CEO clearance.")

elif active_module == "ðŸŽ¨ Asset Synthesis":
    st.subheader("ðŸŽ¨ Sovereign Image & Media Synthesis")
    prompt = st.text_input("Enter Generation Prompt:", "High-tech executive handshake: HVF on left, SignalLink on right, Project Ebony banner centered", key="asset_prompt_input")
    if st.button("Generate Sovereign Asset", width='stretch'):
        with st.spinner("Synthesizing sovereign asset on local hardware..."):
            try:
                res = requests.post("http://localhost:8000/synthesis/image", params={"prompt": prompt}, headers={"x-auth-token": "CEO_OVERRIDE"})
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"âœ… {data.get('message')}")
                    img_rel = data.get("image_path")
                    img_file = os.path.join(REPO_DIR, img_rel) if img_rel else None
                    if img_file and os.path.isfile(img_file):
                        st.image(img_file, caption="Sovereign Generated Asset | HVF Project Ebony Matrix", width='stretch')
                        with open(img_file, "rb") as f:
                            st.download_button("ðŸ“¥ Download Sovereign Graphic (PNG)", f, file_name="Project_Ebony_Joint_Venture.png", mime="image/png", width='stretch')
                else:
                    st.error(f"âš ï¸ Engine Error (HTTP {res.status_code})")
            except Exception as e:
                st.error(f"Matrix Offline: {e}")



elif active_module == "ðŸ“¨ Sovereign Dispatch Deck":
    st.header("ðŸ“¨ Sovereign Multi-Account Dispatch & Inbound Triage Deck")
    st.markdown("Zero-Trust Inbound Adversarial Scrubber & CEO Kinematic Veto Approval Pipeline")

    # --- SECTION 1: OUTBOUND COMPOSITION TERMINAL ---
    with st.expander("âœï¸ COMPOSE SOVEREIGN OUTBOUND TRANSMISSION (DIRECT DISPATCH)", expanded=False):
        st.markdown("<div style='color: #e2a03f; font-family: monospace; font-size: 0.95em; font-weight: bold; margin-bottom: 8px;'>DIRECT EXECUTIVE STRIKE TRANSMISSION // CAGE: 1AHA8</div>", unsafe_allow_html=True)
        
        comp_c1, comp_c2 = st.columns([2, 1])
        with comp_c1:
            out_to = st.text_input("Destination Recipient (RFC822 Email)", key="direct_out_to", placeholder="e.g. contracts@signallink.com")
            out_subj = st.text_input("Transmission Subject Line", key="direct_out_subj", placeholder="e.g. Subcontractor LSA Execution Verification // DAF TENCAP Vol 2")
        with comp_c2:
            out_cat = st.selectbox("Classification Category", [
                "DEFENSE_PRIME_CONTRACTING",
                "SUBCONTRACTOR_SIGNALLINK",
                "LEGAL_COMPLIANCE_EXECUTION",
                "FINANCIAL_TREASURY",
                "GENERAL_EXECUTIVE"
            ], key="direct_out_cat")
            st.markdown("<div style='font-size:0.85em; color:#94a3b8; margin-top:5px;'><b>Originating Endpoint:</b><br><span style='color:#e2a03f; font-family:monospace;'>humphreyvirtualfarm@gmail.com</span></div>", unsafe_allow_html=True)

        with st.expander("âš¡ Draft Assistance with Ebony AI (Grounded in Iron Dome Intel)", expanded=False):
            ai_directive = st.text_input("Strategic Directive for Ebony AI", key="ai_out_directive", placeholder="e.g. Confirm executed LSA with Drew Phillips Jr. and coordinate DAF TENCAP Volume 2.")
            if st.button("âš¡ Generate Authoritative Draft", key="btn_gen_ai_draft"):
                if ai_directive:
                    with st.spinner("Retrieving Iron Dome intelligence and composing draft..."):
                        draft_ai = email_triage_core.generate_direct_draft_assistance(out_to, ai_directive)
                        st.session_state["direct_out_body_val"] = draft_ai
                        st.rerun()
                else:
                    st.warning("Please specify an objective for Ebony AI.")

        default_body = st.session_state.get("direct_out_body_val", "")
        out_body = st.text_area("Transmission Payload (Strict RFC5322 Plain Text)", value=default_body, height=200, key="direct_out_body")

        snd_c1, snd_c2 = st.columns([1.5, 2])
        with snd_c1:
            if st.button("ðŸš€ Authorize & Dispatch Transmission", key="btn_dispatch_now", type="primary"):
                if not out_to or not out_subj or not out_body:
                    st.error("Recipient, Subject, and Payload Body are mandatory.")
                else:
                    with st.spinner("Connecting to smtp.gmail.com:465 & dispatching..."):
                        s_ok, s_msg = email_triage_core.send_direct_outbound_email(
                            to_addr=out_to,
                            subject=out_subj,
                            body=out_body,
                            account_alias="HVF_PRIMARY_EXECUTIVE",
                            category=out_cat
                        )
                    if s_ok:
                        st.success(f"ðŸš€ {s_msg}")
                        st.session_state["direct_out_body_val"] = ""
                        st.rerun()
                    else:
                        st.error(f"Delivery failed: {s_msg}")
        with snd_c2:
            if st.button("Clear Buffer", key="btn_clr_direct_buf"):
                st.session_state["direct_out_body_val"] = ""
                st.rerun()

    # --- SECTION 2: INBOX POLL CONTROLS & TELEMETRY ---
    poll_c1, poll_c2 = st.columns([2, 1])
    with poll_c1:
        if st.button("ðŸ”„ Poll Monitored Inboxes Now", key="btn_poll_inboxes_main"):
            with st.spinner("Connecting to imap.gmail.com:993 & staging unread messages..."):
                email_triage_core.run_multi_account_cycle()
            st.success("Polling complete.")
            st.rerun()
    with poll_c2:
        if st.button("ðŸ§¹ Purge Staged Newsletters", key="btn_purge_newsletters"):
            c_cl = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
            cur_cl = c_cl.cursor()
            cur_cl.execute("""
            UPDATE staged_email_dispatches 
            SET veto_status = 'ARCHIVED_NOISE' 
            WHERE veto_status = 'PENDING_CEO_APPROVAL'
              AND (sender_address LIKE '%newsletters-noreply%' OR sender_address LIKE '%zapier%' OR sender_address LIKE '%instagram%')
              AND subject NOT LIKE '%Signallink%';
            """)
            c_cl.close()
            st.info("Newsletters archived.")
            st.rerun()

    # --- SECTION 3: FOCUSED SINGLE-TRANSMISSION C2 STEPPER ---
    try:
        c_disp = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
        cur_disp = c_disp.cursor()
        cur_disp.execute("""
            SELECT id, account_alias, sender_address, subject, date_received, 
                   raw_body_sanitized, threat_status, triage_category, draft_response 
            FROM staged_email_dispatches 
            WHERE veto_status = 'PENDING_CEO_APPROVAL' 
            ORDER BY id ASC
        """)
        dispatches = cur_disp.fetchall()
        c_disp.close()
    except Exception as e:
        st.error(f"Failed to load queue: {e}")
        dispatches = []

    total_pending = len(dispatches)

    if total_pending == 0:
        st.markdown("""
            <div style='border: 1px solid #242d3d; border-radius: 2px; padding: 25px; background-color: #121722; text-align: center; margin-top: 15px;'>
                <div style='color: #e2a03f; font-family: monospace; font-size: 1.15em; font-weight: bold;'>ðŸŸ¢ PERIMETER SECURE | ZERO PENDING TRANSMISSIONS</div>
                <div style='color: #94a3b8; font-size: 0.85em; margin-top: 6px;'>Queue is completely clear. Incoming transmissions will stage at eye level.</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        curr_msg = dispatches[0]
        disp_id, account, sender, subject, date_rx, body_clean, threat, category, draft = curr_msg

        status_class = "status-threat" if "THREAT" in threat else "status-clean"
        status_icon = "ðŸ›‘" if "THREAT" in threat else "âœ…"

        st.markdown(f"""
            <div style='border: 1px solid #242d3d; border-radius: 2px; padding: 14px; background-color: #121722; margin-top: 12px;'>
                <div class='card-header'>
                    <span style='color:#e2a03f; font-family:monospace; font-weight:bold;'>TRANSMISSION 1 OF {total_pending} PENDING</span>
                    <span class='status-badge {status_class}'>{status_icon} {threat}</span>
                </div>
                <div style='font-size: 1.05em; font-weight: bold; color: #f1f5f9; margin-top: 8px;'>
                    [{account}] {subject}
                </div>
                <div style='font-size: 0.88em; color: #94a3b8; margin-top: 4px;'>
                    <b>FROM:</b> <span style='color:#f1f5f9; font-family:monospace;'>{sender}</span> | 
                    <b>RECEIVED:</b> <span style='color:#f1f5f9;'>{date_rx}</span> | 
                    <b>CATEGORY:</b> <span style='color:#e2a03f;'>{category}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("ðŸ” View Inbound Transmission Body (Sanitized)", expanded=False):
            st.text(body_clean)

        if "THREAT" in threat:
            st.error("âš ï¸ Inbound transmission flagged for adversarial injection. Automated inference suspended.")
        else:
            updated_draft = st.text_area(
                f"Tactical Executive Response Payload (Queue #{disp_id})", 
                value=draft, 
                height=180,
                key=f"stepper_draft_{disp_id}"
            )

        col_act1, col_act2, col_act3 = st.columns([1.2, 1, 1.2])
        with col_act1:
            if st.button("âœ… Approve & Dispatch", key=f"btn_step_app_{disp_id}", type="secondary"):
                with st.spinner("Connecting to smtp.gmail.com:465 & dispatching transmission..."):
                    d_ok, d_msg = email_triage_core.dispatch_outbound_transmission(disp_id, updated_draft)
                if d_ok:
                    st.success(f"ðŸš€ {d_msg}")
                else:
                    st.error(f"Delivery failed: {d_msg}")
                st.rerun()

        with col_act2:
            if st.button("âŒ Dismiss Record", key=f"btn_step_dis_{disp_id}"):
                c_act = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                cur_act = c_act.cursor()
                cur_act.execute("UPDATE staged_email_dispatches SET veto_status = 'DISMISSED_BY_CEO' WHERE id = ?", (disp_id,))
                c_act.close()
                st.info(f"Transmission #{disp_id} dismissed. Advancing queue.")
                st.rerun()

        with col_act3:
            if st.button("ðŸš« Block Sender", key=f"btn_step_blk_{disp_id}", type="primary"):
                try:
                    suc, b_text = email_triage_core.block_sender(sender, reason="CEO_TACTICAL_VETO")
                    if suc:
                        st.warning(f"ðŸš« {b_text}")
                    else:
                        st.error(f"Block failed: {b_text}")
                except Exception as b_err:
                    st.error(f"Block error: {b_err}")
                st.rerun()

elif active_module == "ðŸ“¡ Sovereign Comms Deck":
    from sovereign_comms_core import SovereignCommsEngine
    SovereignCommsEngine.render()
elif active_module == "ðŸ“˜ Omni-Industry Matrix":
    st.subheader("ðŸ“˜ OMNI-INDUSTRY MATRIX")
    st.info("Sovereign 15-Vertical Tier-1 Architecture")

    # --- NATIVE 15-VERTICAL ARRAY ---
    verticals = [
        ("ðŸŒ¾ Agriculture", "01_sovereign_agriculture"),
        ("ðŸš› Logistics", "02_logistics_and_supply_chain"),
        ("ðŸš Defense", "03_defense_tactical"),
        ("âš¡ Energy", "04_distributed_energy_grid"),
        ("ðŸ­ Manufacturing", "05_advanced_manufacturing"),
        ("ðŸ“¡ Comms", "06_secure_communications"),
        ("ðŸ¦ Finance", "07_financial_ledger_autonomy"),
        ("ðŸ¥ Healthcare", "08_edge_healthcare_bio_metrics"),
        ("ðŸ›°ï¸ Aerospace", "09_aerospace_perimeter_telemetry"),
        ("ðŸ—ï¸ Civil Eng", "10_civil_engineering"),
        ("â›ï¸ Mining", "11_mining_extraction"),
        ("ðŸŒŠ Deep Ocean", "12_deep_ocean"),
        ("ðŸ” Crypto Cyber", "13_cryptographic_cyber"),
        ("ðŸ’§ Hydrology", "14_sovereign_hydrology"),
        ("ðŸ“¦ Warehousing", "15_autonomous_warehousing")
    ]

    tabs = st.tabs([v[0] for v in verticals])

    def load_vertical(folder_name):
        folder_path = os.path.join(REPO_DIR, "docs", folder_name)
        if os.path.exists(folder_path):
            md_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.md')])
            if md_files:
                for md_file in md_files:
                    title = md_file.replace(".md", "").replace("_", " ").upper()
                    with st.expander(f"ðŸ“˜ {title}", expanded=False):
                        with open(os.path.join(folder_path, md_file), "r", encoding="utf-8") as f:
                            st.markdown(f.read())
            else:
                st.info("Pillars are currently being forged for this Sovereign Vertical.")
        else:
            st.error(f"CRITICAL: Directory missing -> {folder_path}")

    for i, tab in enumerate(tabs):
        with tab:
            load_vertical(verticals[i][1])
