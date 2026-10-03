import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
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
BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
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

def get_db_connection(timeout: float = 30.0) -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=timeout, isolation_level=None)
    conn.execute("PRAGMA busy_timeout = 30000;")
    return conn

def get_fernet_cipher():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return Fernet(f.read().strip())
    return None

def clean_token(raw_str: str) -> str:
    if not raw_str:
        return ""
    return str(raw_str).replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "").strip()

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

def extract_clean_email(raw_sender: str) -> str:
    _, addr = parseaddr(str(raw_sender))
    if addr and "@" in addr:
        return addr.lower().strip()
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", str(raw_sender))
    return match.group(0).lower().strip() if match else str(raw_sender).lower().strip()

def is_sender_blocked(raw_sender: str) -> bool:
    clean_addr = extract_clean_email(raw_sender)
    domain = clean_addr.split("@")[-1] if "@" in clean_addr else ""
    try:
        conn = get_db_connection(timeout=5.0)
        cur = conn.cursor()
        cur.execute("""
        SELECT COUNT(*) FROM blocked_senders 
        WHERE clean_email = ? OR clean_email = ? OR sender_address = ?
        """, (clean_addr, f"@{domain}", str(raw_sender)))
        is_blocked = cur.fetchone()[0] > 0
        conn.close()
        return is_blocked
    except Exception:
        return False

def block_sender(raw_sender: str, reason: str = "CEO_KINEMATIC_VETO", blocked_by: str = "Jeffery Humphrey (CEO)") -> tuple:
    clean_addr = extract_clean_email(raw_sender)
    now_str = datetime.now().isoformat()
    try:
        conn = get_db_connection(timeout=30.0)
        cur = conn.cursor()
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
        conn.close()
        return True, f"Sender [{clean_addr}] permanently blacklisted. Purged {purged} staged records."
    except Exception as e:
        return False, str(e)

def sanitize_payload(text: str) -> tuple:
    cleaned = re.sub(r"<[^>]*>", " ", text)
    cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", cleaned)
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
        return "\n\n".join(docs)
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
    """Polls newest unread messages, flags them \Seen immediately, and stages clean drafts."""
    password = ""
    if enc_pwd:
        password = decrypt_credential(enc_pwd)
    if not password and pwd_key and pwd_key != "DYNAMIC_VAULT_ENCRYPTED":
        password = os.getenv(pwd_key, "")

    clean_user = str(email_addr).strip()
    clean_pass = clean_token(password)

    if not clean_pass:
        print(f"  [WARN] No password found for '{account_alias}'.")
        return 0

    records_to_insert = []
    try:
        mail = imaplib.IMAP4_SSL(str(imap_srv).strip(), int(imap_prt))
        mail.login(clean_user, clean_pass)
        mail.select("INBOX")
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK" or not messages[0]:
            mail.logout()
            return 0

        uids = messages[0].split()
        print(f"  [{account_alias}] Discovered {len(uids)} unread transmissions.")

        # Check existing UIDs in SQLite to prevent duplicate drafting
        conn = get_db_connection(timeout=10.0)
        cur = conn.cursor()
        cur.execute("SELECT message_uid FROM staged_email_dispatches WHERE account_alias = ?", (account_alias,))
        existing_uids = set(r[0] for r in cur.fetchall())
        conn.close()

        # Ingest strictly the 5 newest unread messages to maintain rapid UI response
        target_uids = uids[-5:]

        for uid in target_uids:
            uid_str = uid.decode()

            # Flag as \Seen on IMAP immediately so it cannot be fetched again
            mail.store(uid, "+FLAGS", "\Seen")

            if uid_str in existing_uids:
                print(f"    [SKIP] Transmission #{uid_str} already staged in vault.")
                continue

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

                    records_to_insert.append((
                        account_alias, uid_str, sender, clean_user, subj,
                        date_str, sanitized_body, threat, category, draft
                    ))

        mail.logout()
    except Exception as e:
        print(f"  [ERROR] IMAP network cycle failed for '{account_alias}': {e}")
        return 0

    staged_count = len(records_to_insert)
    if staged_count > 0:
        try:
            conn = get_db_connection(timeout=30.0)
            cur = conn.cursor()
            cur.executemany("""
            INSERT INTO staged_email_dispatches 
            (account_alias, message_uid, sender_address, recipient_address, subject, date_received, raw_body_sanitized, threat_status, triage_category, draft_response, veto_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING_CEO_APPROVAL')
            """, records_to_insert)
            conn.close()
            print(f"  [SUCCESS] Staged {staged_count} new transmissions.")
        except Exception as e:
            print(f"  [ERROR] Database insert failed: {e}")
            return 0

    return staged_count

def run_multi_account_cycle():
    try:
        conn = get_db_connection(timeout=10.0)
        cur = conn.cursor()
        cur.execute("SELECT account_alias, email_address, imap_server, imap_port, env_password_key, encrypted_password FROM email_accounts WHERE is_active = 1")
        accounts = cur.fetchall()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Could not query email_accounts: {e}")
        return

    if not accounts:
        print("[INFO] No active accounts configured.")
        return

    print(f"\nInitiating live triage across {len(accounts)} configured inboxes...")
    for acc in accounts:
        alias, addr, srv, prt, pwd_key, enc_pwd = acc
        staged = poll_and_stage_account(alias, addr, srv, prt, pwd_key, enc_pwd)
        print(f"  -> [{alias}]: {staged} messages staged for CEO Kinematic Review.")

def dispatch_outbound_transmission(dispatch_id: int, final_body_override: str = None) -> tuple:
    """
    Executes live outbound SMTP transmission for a CEO-approved dispatch.
    Decrypts stored application token in-memory, connects to SSL port 465,
    transmits the final payload, and logs the execution audit in SQLite vault.
    """
    try:
        conn = get_db_connection(timeout=30.0)
        cur = conn.cursor()
        
        # 1. Fetch staged dispatch payload
        cur.execute("""
            SELECT account_alias, sender_address, recipient_address, subject, draft_response 
            FROM staged_email_dispatches 
            WHERE id = ?
        """, (dispatch_id,))
        row = cur.fetchone()
        
        if not row:
            conn.close()
            return False, f"Dispatch ID #{dispatch_id} not found in staging ledger."
            
        acc_alias, to_addr, from_addr, orig_subj, original_draft = row
        body_to_send = final_body_override if final_body_override is not None else original_draft
        
        # 2. Extract clean recipient address
        clean_recipient = extract_clean_email(to_addr)
        if not clean_recipient:
            conn.close()
            return False, f"Invalid recipient destination: {to_addr}"
            
        # 3. Retrieve and decrypt account credentials
        cur.execute("""
            SELECT email_address, smtp_server, smtp_port, encrypted_password 
            FROM email_accounts 
            WHERE account_alias = ? AND is_active = 1
        """, (acc_alias,))
        acc_info = cur.fetchone()
        
        if not acc_info or not acc_info[3]:
            # Fallback to HVF_PRIMARY_EXECUTIVE
            cur.execute("""
                SELECT email_address, smtp_server, smtp_port, encrypted_password 
                FROM email_accounts 
                WHERE account_alias = 'HVF_PRIMARY_EXECUTIVE' AND is_active = 1
            """)
            acc_info = cur.fetchone()
            
        if not acc_info or not acc_info[3]:
            conn.close()
            return False, f"No active credentials configured for account '{acc_alias}'."
            
        auth_email, smtp_srv, smtp_prt, enc_pwd = acc_info
        clear_pwd = decrypt_credential(enc_pwd)
        
        if not clear_pwd:
            conn.close()
            return False, "Failed to decrypt SMTP authentication token in-memory."
            
        # 4. Construct RFC5322 MIME transmission
        subj_prefix = "Re: " if not orig_subj.lower().startswith("re:") else ""
        outbound_subj = f"{subj_prefix}{orig_subj}"
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = outbound_subj
        msg["From"] = f"HVF Omni-Industrial Matrix <{auth_email}>"
        msg["To"] = clean_recipient
        msg["Reply-To"] = auth_email
        msg["X-Originating-System"] = "Ebony AI Defense C2 Core"
        msg["X-HVF-CAGE"] = "1AHA8"
        
        msg.attach(MIMEText(body_to_send, "plain", "utf-8"))
        
        # 5. Connect and Transmit via SSL SMTP (Port 465)
        server = smtplib.SMTP_SSL(str(smtp_srv).strip(), int(smtp_prt), timeout=30.0)
        server.login(auth_email, clean_token(clear_pwd))
        server.sendmail(auth_email, [clean_recipient], msg.as_string())
        server.quit()
        
        # 6. Update Veto Ledger to Dispatched State
        now_ts = datetime.now().isoformat()
        cur.execute("""
            UPDATE staged_email_dispatches 
            SET veto_status = 'DISPATCHED_SUCCESS',
                draft_response = ?
            WHERE id = ?
        """, (body_to_send, dispatch_id))
        conn.close()
        
        return True, f"Outbound transmission #{dispatch_id} successfully delivered to {clean_recipient}."
        
    except Exception as e:
        return False, f"SMTP transmission failed: {str(e)}"

def send_direct_outbound_email(to_addr: str, subject: str, body: str, account_alias: str = "HVF_PRIMARY_EXECUTIVE", category: str = "DIRECT_EXECUTIVE_OUTBOUND") -> tuple:
    """
    Directly composes and transmits a sovereign outbound email via SSL SMTP (Port 465).
    Enforces DFARS provenance headers, decrypts token in-memory, and writes an immutable
    audit entry into staged_email_dispatches with status 'DISPATCHED_SUCCESS'.
    """
    clean_recipient = extract_clean_email(to_addr)
    if not clean_recipient:
        return False, f"Invalid destination recipient address: {to_addr}"

    if not subject.strip():
        return False, "Outbound transmission must include a subject line."

    if not body.strip():
        return False, "Outbound transmission body cannot be empty."

    try:
        conn = get_db_connection(timeout=30.0)
        cur = conn.cursor()
        
        # 1. Retrieve authenticated endpoint credentials
        cur.execute("""
            SELECT email_address, smtp_server, smtp_port, encrypted_password 
            FROM email_accounts 
            WHERE account_alias = ? AND is_active = 1
        """, (account_alias,))
        acc_info = cur.fetchone()

        if not acc_info or not acc_info[3]:
            # Fallback to HVF_PRIMARY_EXECUTIVE
            cur.execute("""
                SELECT email_address, smtp_server, smtp_port, encrypted_password 
                FROM email_accounts 
                WHERE account_alias = 'HVF_PRIMARY_EXECUTIVE' AND is_active = 1
            """)
            acc_info = cur.fetchone()

        if not acc_info or not acc_info[3]:
            conn.close()
            return False, f"No active credentials configured for account '{account_alias}'."

        auth_email, smtp_srv, smtp_prt, enc_pwd = acc_info
        clear_pwd = decrypt_credential(enc_pwd)

        if not clear_pwd:
            conn.close()
            return False, "Failed to decrypt SMTP authentication credentials in-memory."

        # 2. Build RFC5322 MIME Transmission with Defense Headers
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject.strip()
        msg["From"] = f"HVF Omni-Industrial Matrix <{auth_email}>"
        msg["To"] = clean_recipient
        msg["Reply-To"] = auth_email
        msg["X-Originating-System"] = "Ebony AI Sovereign Command Deck"
        msg["X-HVF-CAGE"] = "1AHA8"
        msg["X-Compliance"] = "DFARS 252.227-7018"

        msg.attach(MIMEText(body.strip(), "plain", "utf-8"))

        # 3. Transmit via SSL SMTP (Port 465)
        server = smtplib.SMTP_SSL(str(smtp_srv).strip(), int(smtp_prt), timeout=30.0)
        server.login(auth_email, clean_token(clear_pwd))
        server.sendmail(auth_email, [clean_recipient], msg.as_string())
        server.quit()

        # 4. Record Dispatch in Audit Ledger
        now_ts = datetime.now().isoformat()
        cur.execute("""
            INSERT INTO staged_email_dispatches 
            (account_alias, message_uid, sender_address, recipient_address, subject, date_received, raw_body_sanitized, threat_status, triage_category, draft_response, veto_status)
            VALUES (?, 'OUTBOUND_DIRECT', ?, ?, ?, ?, ?, 'INSPECTED_CLEAN', ?, ?, 'DISPATCHED_SUCCESS')
        """, (account_alias, auth_email, clean_recipient, subject.strip(), now_ts, body.strip(), category, body.strip()))

        conn.close()
        return True, f"Outbound transmission successfully dispatched to {clean_recipient} via {smtp_srv}:{smtp_prt}."

    except Exception as e:
        return False, f"Direct outbound dispatch failed: {str(e)}"

def generate_direct_draft_assistance(to_recipient: str, objective_prompt: str) -> str:
    """Generates an executive-level outbound message grounded in the Iron Dome knowledge base."""
    if not client:
        return "Groq inference client offline. Please enter outbound message body manually."

    context = query_iron_dome(objective_prompt, objective_prompt)

    system_prompt = f"""You are Ebony, sovereign AI for HVF Omni-Industrial Matrix (CAGE: 1AHA8, UEI: S1M4ENLHTDH5), led by Founder & CEO Jeffery Humphrey.
Draft a commanding, professional, and authoritative outbound executive correspondence based on the objective provided.
Grounded in HVF's prime contracting standing, defense posture, and relevant operational intelligence.

--- DESTINATION RECIPIENT: {to_recipient}
--- STRATEGIC OBJECTIVE: {objective_prompt}

--- SOVEREIGN INTEL CONTEXT ---
{context}
-------------------------------

Provide ONLY the final email body text. Close with:
Office of the Chief Executive
HVF Omni-Industrial Matrix
Prime Contractor | CAGE: 1AHA8"""

    try:
        res = client.chat.completions.create(
            model=ACTIVE_MODEL,
            messages=[{"role": "user", "content": system_prompt}],
            temperature=0.2
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI DRAFTING ERROR]: {e}"

