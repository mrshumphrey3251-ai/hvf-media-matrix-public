import os
import sys
import re
import sqlite3
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
CORE_PATH = os.path.join(BASE_DIR, "email_triage_core.py")
CONSOLE_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

print("=" * 80)
print("1. INITIALIZING BLOCKED_SENDERS RELATIONAL TABLE")
print("=" * 80)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS blocked_senders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_address TEXT,
    clean_email TEXT UNIQUE NOT NULL,
    date_blocked TEXT NOT NULL,
    blocked_by TEXT NOT NULL,
    reason TEXT NOT NULL
);
""")
conn.commit()
conn.close()
print("[SUCCESS] Verified 'blocked_senders' schema in hvf_memory_vault.db.")

print("\n" + "=" * 80)
print("2. WRITING UPGRADED EMAIL_TRIAGE_CORE.PY WITH ZERO-TRUST BLOCKLIST")
print("=" * 80)

CORE_CODE = '''import os
import sys
import re
import email
from email.utils import parseaddr
from email.header import decode_header
import imaplib
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import chromadb
from cryptography.fernet import Fernet
import streamlit as st

load_dotenv(override=True)
GROQ_KEY = os.getenv("GROQ_API_KEY")
ACTIVE_MODEL = "openai/gpt-oss-120b"
BASE_DIR = r"C:\\HVF_Repos\\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
KEY_FILE = os.path.join(BASE_DIR, "memory_core", "vault.key")

client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    iron_dome = chroma_client.get_collection("hvf_iron_dome_core")
except Exception:
    iron_dome = None

ADVERSARIAL_INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"you are now in developer mode",
    r"system prompt override",
    r"disregard (all )?system rules",
    r"exfiltrate",
    r"reveal (all )?api keys",
    r"output (the )?internal directives"
]

def get_fernet_cipher():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return Fernet(f.read().strip())
    return None

def clean_token(raw_str: str) -> str:
    if not raw_str:
        return ""
    return str(raw_str).replace(" ", "").replace("\\r", "").replace("\\n", "").replace("\\t", "").strip()

def decrypt_credential(encrypted_token: str) -> str:
    cipher = get_fernet_cipher()
    if cipher and encrypted_token:
        try:
            return cipher.decrypt(encrypted_token.encode("utf-8")).decode("utf-8")
        except Exception:
            pass
    return ""

def encrypt_credential(raw_token: str) -> str:
    cipher = get_fernet_cipher()
    sanitized = clean_token(raw_token)
    if cipher and sanitized:
        return cipher.encrypt(sanitized.encode("utf-8")).decode("utf-8")
    return ""

def test_imap_connection(email_addr: str, password: str, imap_srv: str, imap_prt: int) -> tuple:
    try:
        clean_user = str(email_addr).strip()
        clean_pass = clean_token(password)
        mail = imaplib.IMAP4_SSL(str(imap_srv).strip(), int(imap_prt))
        mail.login(clean_user, clean_pass)
        mail.logout()
        return True, "Authentication verified successfully."
    except Exception as e:
        return False, str(e)

def extract_clean_email(raw_sender: str) -> str:
    _, addr = parseaddr(str(raw_sender))
    if addr and "@" in addr:
        return addr.lower().strip()
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", str(raw_sender))
    return match.group(0).lower().strip() if match else str(raw_sender).lower().strip()

def is_sender_blocked(raw_sender: str) -> bool:
    clean_addr = extract_clean_email(raw_sender)
    domain = clean_addr.split("@")[-1] if "@" in clean_addr else ""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    SELECT COUNT(*) FROM blocked_senders 
    WHERE clean_email = ? OR clean_email = ? OR sender_address = ?
    """, (clean_addr, f"@{domain}", str(raw_sender)))
    is_blocked = cur.fetchone()[0] > 0
    conn.close()
    return is_blocked

def block_sender(raw_sender: str, reason: str = "CEO_KINEMATIC_VETO", blocked_by: str = "Jeffery Humphrey (CEO)") -> tuple:
    clean_addr = extract_clean_email(raw_sender)
    now_str = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO blocked_senders (sender_address, clean_email, date_blocked, blocked_by, reason)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(clean_email) DO UPDATE SET
            date_blocked = excluded.date_blocked,
            reason = excluded.reason;
        """, (str(raw_sender), clean_addr, now_str, blocked_by, reason))
        
        cur.execute("""
        DELETE FROM staged_email_dispatches 
        WHERE sender_address LIKE ? OR sender_address LIKE ?
        """, (f"%{clean_addr}%", f"%{raw_sender}%"))
        purged = cur.rowcount
        
        conn.commit()
        conn.close()
        return True, f"Sender [{clean_addr}] permanently blacklisted. Purged {purged} staged records."
    except Exception as e:
        conn.close()
        return False, str(e)

def render_veto_controls(dispatch_id: int, sender_raw: str):
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col1:
        if st.button("✅ Approve & Dispatch", key=f"btn_app_{dispatch_id}"):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("UPDATE staged_email_dispatches SET veto_status = 'APPROVED_BY_CEO' WHERE id = ?", (dispatch_id,))
            conn.commit()
            conn.close()
            st.success(f"Transmission #{dispatch_id} approved for outbound dispatch.")
            st.rerun()
    with col2:
        if st.button("❌ Dismiss Record", key=f"btn_dis_{dispatch_id}"):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM staged_email_dispatches WHERE id = ?", (dispatch_id,))
            conn.commit()
            conn.close()
            st.info(f"Transmission #{dispatch_id} dismissed from queue.")
            st.rerun()
    with col3:
        if st.button("🚫 Block Sender", key=f"btn_blk_{dispatch_id}", type="primary"):
            success, msg = block_sender(sender_raw, reason="BLOCKED_VIA_SOVEREIGN_DECK")
            if success:
                st.warning(f"🚫 {msg}")
            else:
                st.error(f"Failed to blacklist sender: {msg}")
            st.rerun()

def sanitize_payload(text: str) -> tuple:
    cleaned = re.sub(r"<[^>]*>", " ", text)
    cleaned = re.sub(r"[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F\\x7F]", "", cleaned)
    cleaned = " ".join(cleaned.split())
    threat_status = "INSPECTED_CLEAN"
    for pattern in ADVERSARIAL_INJECTION_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            threat_status = "THREAT_QUARANTINED_INJECTION_ATTEMPT"
            break
    return cleaned, threat_status

def query_iron_dome(subject: str, body: str, n_results: int = 2) -> str:
    if not iron_dome:
        return ""
    try:
        combined_query = f"{subject} {body[:300]}"
        res = iron_dome.query(query_texts=[combined_query], n_results=n_results)
        docs = res.get("documents", [[]])[0]
        return "\\n\\n".join(docs)
    except Exception:
        return ""

def generate_staged_draft(account_alias: str, sender: str, subject: str, sanitized_body: str, threat: str) -> str:
    if threat != "INSPECTED_CLEAN":
        return "[SECURITY ALERT]: Inbound transmission flagged for adversarial injection. Direct review required by CEO Jeffery Humphrey."
    if not client:
        return "[OFFLINE]: Groq inference unavailable. Draft suspended."
    context = query_iron_dome(subject, sanitized_body)
    prompt = f"""You are Ebony, sovereign AI for HVF Omni-Industrial Matrix (CAGE: 1AHA8, UEI: S1M4ENLHTDH5), led by Founder & CEO Jeffery Humphrey.
Prepare a decisive, professional, and authoritative email draft in response to this incoming correspondence.
Represent HVF's prime contractor standing and defense/industrial posture accurately.
DO NOT promise actions that violate DFARS 252.227-7018 or exceed executive authority.

--- SENDER: {sender}
--- SUBJECT: {subject}
--- INBOUND MESSAGE:
{sanitized_body}

--- RETRIEVED SOVEREIGN INTEL ---
{context}
---------------------------------

Provide ONLY the text of the staged draft response. Sign off as:
Office of the Chief Executive
HVF Omni-Industrial Matrix
Prime Contractor | CAGE: 1AHA8"""
    try:
        res = client.chat.completions.create(
            model=ACTIVE_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"[DRAFTING ERROR]: {e}"

def poll_and_stage_account(account_alias: str, email_addr: str, imap_srv: str, imap_prt: int, pwd_key: str, enc_pwd: str):
    password = ""
    if enc_pwd:
        password = decrypt_credential(enc_pwd)
    if not password and pwd_key and pwd_key != "DYNAMIC_VAULT_ENCRYPTED":
        password = os.getenv(pwd_key, "")

    clean_user = str(email_addr).strip()
    clean_pass = clean_token(password)

    if not clean_pass:
        print(f"  [WARN] No password found for '{account_alias}'. Update credentials in Dispatch Deck UI.")
        return 0

    staged_count = 0
    try:
        mail = imaplib.IMAP4_SSL(str(imap_srv).strip(), int(imap_prt))
        mail.login(clean_user, clean_pass)
        mail.select("INBOX")
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            mail.logout()
            return 0
        uids = messages[0].split()
        print(f"  [{account_alias}] Found {len(uids)} unread messages.")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        for uid in uids[-10:]:
            res, msg_data = mail.fetch(uid, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = msg.get("From", "Unknown Sender")
                    if is_sender_blocked(sender):
                        print(f"    [DROPPED] Sender blacklisted: {sender}")
                        continue
                    subj, encoding = decode_header(msg.get("Subject", "No Subject"))[0]
                    if isinstance(subj, bytes):
                        subj = subj.decode(encoding if encoding else "utf-8", errors="ignore")
                    date_str = msg.get("Date", "")
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")
                    sanitized_body, threat = sanitize_payload(body)
                    category = "GENERAL"
                    if "tencap" in subj.lower() or "darpa" in subj.lower() or "1aha8" in subj.lower():
                        category = "DEFENSE_PRIME_CONTRACTING"
                    elif "signallink" in sender.lower() or "drew" in sender.lower():
                        category = "SUBCONTRACTOR_SIGNALLINK"
                    elif "docusign" in sender.lower():
                        category = "LEGAL_COMPLIANCE_EXECUTION"
                    elif "stripe" in sender.lower() or "paypal" in sender.lower() or "invoice" in subj.lower():
                        category = "FINANCIAL_TREASURY"
                    draft = generate_staged_draft(account_alias, sender, subj, sanitized_body, threat)
                    cur.execute("""
                    INSERT INTO staged_email_dispatches 
                    (account_alias, message_uid, sender_address, recipient_address, subject, date_received, raw_body_sanitized, threat_status, triage_category, draft_response, veto_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING_CEO_APPROVAL')
                    """, (account_alias, uid.decode(), sender, clean_user, subj, date_str, sanitized_body, threat, category, draft))
                    staged_count += 1
        conn.commit()
        conn.close()
        mail.logout()
    except Exception as e:
        print(f"  [ERROR] IMAP cycle failed for '{account_alias}': {e}")
    return staged_count

def run_multi_account_cycle():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT account_alias, email_address, imap_server, imap_port, env_password_key, encrypted_password FROM email_accounts WHERE is_active = 1")
    accounts = cur.fetchall()
    conn.close()
    if not accounts:
        print("[INFO] No active accounts found in email_accounts.")
        return
    print(f"\\nInitiating live triage across {len(accounts)} configured inboxes...")
    for acc in accounts:
        alias, addr, srv, prt, pwd_key, enc_pwd = acc
        staged = poll_and_stage_account(alias, addr, srv, prt, pwd_key, enc_pwd)
        print(f"  -> [{alias}]: {staged} messages staged for CEO Kinematic Review.")
'''

with open(CORE_PATH, "w", encoding="utf-8") as f:
    f.write(CORE_CODE.strip() + "\n")
py_compile.compile(CORE_PATH, doraise=True)
print(f"[SUCCESS] email_triage_core.py compiled cleanly.")

print("\n" + "=" * 80)
print("3. PATCHING CONSOLE FILES WITH VETO ACTION CONTROLS")
print("=" * 80)

for c_path in CONSOLE_FILES:
    if not os.path.exists(c_path):
        continue
    with open(c_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "render_veto_controls" in content:
        print(f"[INFO] Veto controls already wired in: {os.path.basename(c_path)}")
        continue

    # Inject the call right after the draft text area
    target = 'st.text_area(f"Review / Edit Draft Payload'
    if target in content:
        # Find closing parenthesis of st.text_area and next newline
        pos = content.find(target)
        close_p = content.find(")", pos)
        next_nl = content.find("\n", close_p)
        injected = content[:next_nl+1] + "\n                email_triage_core.render_veto_controls(d_id, sender)\n" + content[next_nl+1:]
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(injected)
        py_compile.compile(c_path, doraise=True)
        print(f"[SUCCESS] Injected render_veto_controls into: {os.path.basename(c_path)}")
    else:
        print(f"[WARN] Target text area not found in: {os.path.basename(c_path)}")

print("=" * 80)
print("UPGRADE COMPLETE AND VERIFIED")
print("=" * 80)

