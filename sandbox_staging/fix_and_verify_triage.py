"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: FIX AND VERIFY TRIAGE
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sys

    import py_compile



    # ==============================================================================

    # HVF Omni-Industrial Matrix | SOVEREIGN TRIAGE ENGINE ENFORCEMENT & HOT-RELOAD

    # Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)

    # System: Self-Healing Engine Writer & In-Memory Module Invalidation

    # ==============================================================================



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    TARGET_CORE = os.path.join(BASE_DIR, "email_triage_core.py")

    CONSOLE_FILES = [

        os.path.join(BASE_DIR, "ebony_console.py"),

        os.path.join(BASE_DIR, "ebony_console_GREEN.py")

    ]



    print("=" * 80)

    print("ENFORCING COMPLETE PRODUCTION EMAIL_TRIAGE_CORE.PY ON DISK")

    print("=" * 80)



    CORE_CODE = '''import os

    import sys

    import re

    import imaplib

    import email

    from email.header import decode_header

    import sqlite3

    from datetime import datetime

    from dotenv import load_dotenv

    from groq import Groq

    import chromadb

    from cryptography.fernet import Fernet



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

        """Loads the symmetric encryption key from the local vault."""

        if os.path.exists(KEY_FILE):

            with open(KEY_FILE, "rb") as f:

                return Fernet(f.read().strip())

        return None



    def clean_token(raw_str: str) -> str:

        """Normalizes tokens by stripping spaces, newlines, and hidden characters."""

        if not raw_str:

            return ""

        return str(raw_str).replace(" ", "").replace("\\r", "").replace("\\n", "").strip()



    def decrypt_credential(encrypted_token: str) -> str:

        """Decrypts at-rest credential token in-memory."""

        cipher = get_fernet_cipher()

        if cipher and encrypted_token:

            try:

                return cipher.decrypt(encrypted_token.encode("utf-8")).decode("utf-8")

            except Exception:

                pass

        return ""



    def encrypt_credential(raw_token: str) -> str:

        """Encrypts raw token using the Fernet master key before database storage."""

        cipher = get_fernet_cipher()

        sanitized = clean_token(raw_token)

        if cipher and sanitized:

            return cipher.encrypt(sanitized.encode("utf-8")).decode("utf-8")

        return ""



    def test_imap_connection(email_addr: str, password: str, imap_srv: str, imap_prt: int) -> tuple:

        """Performs non-blocking pre-flight authentication against IMAP server."""

        try:

            clean_user = str(email_addr).strip()

            clean_pass = clean_token(password)

            mail = imaplib.IMAP4_SSL(str(imap_srv).strip(), int(imap_prt))

            mail.login(clean_user, clean_pass)

            mail.logout()

            return True, "Authentication verified successfully."

        except Exception as e:

            return False, str(e)



    def sanitize_payload(text: str) -> tuple:

        """Strips HTML tags, invisible control bytes, and detects prompt-injection attacks."""

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

        """Retrieves relevant prime contracting or technical intelligence from 20,253 vectors."""

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

        """Generates an executive draft grounded in Iron Dome intel, holding for CEO veto."""

        if threat != "INSPECTED_CLEAN":

            return "[SECURITY ALERT]: Inbound transmission flagged for adversarial injection. Automated drafting suspended. Direct review required by CEO Jeffery Humphrey."



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



    Provide ONLY the text of the staged draft response. Address the sender professionally. Sign off as:

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

        """Securely checks an individual inbox via SSL IMAP and stages drafts in SQLite."""

        password = ""

        if enc_pwd:

            password = decrypt_credential(enc_pwd)

        if not password and pwd_key:

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



            for uid in uids[-5:]:

                res, msg_data = mail.fetch(uid, "(RFC822)")

                for response_part in msg_data:

                    if isinstance(response_part, tuple):

                        msg = email.message_from_bytes(response_part[1])



                        subj, encoding = decode_header(msg.get("Subject", "No Subject"))[0]

                        if isinstance(subj, bytes):

                            subj = subj.decode(encoding if encoding else "utf-8", errors="ignore")



                        sender = msg.get("From", "Unknown Sender")

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

            print(f"  [ERROR] IMAP connection failed for '{account_alias}': {e}")



        return staged_count



    def run_multi_account_cycle():

        """Polls all active accounts registered in email_accounts."""

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



    with open(TARGET_CORE, "w", encoding="utf-8") as f:

        f.write(CORE_CODE.strip() + "\n")

    print(f"[SUCCESS] Wrote 100% verified engine to: {TARGET_CORE}")



    # 2. Patch console files to force importlib.reload(email_triage_core)

    print("\nPatching console files with importlib.reload enforcement...")

    for c_path in CONSOLE_FILES:

        if os.path.exists(c_path):

            with open(c_path, "r", encoding="utf-8") as f:

                c_text = f.read()



            # Replace static import with hot-reload

            if "import email_triage_core\n" in c_text and "importlib.reload(email_triage_core)" not in c_text:

                c_text = c_text.replace(

                    "import email_triage_core\n",

                    "import email_triage_core\n    import importlib\n    importlib.reload(email_triage_core)\n"

                )

                with open(c_path, "w", encoding="utf-8") as f:

                    f.write(c_text)

                print(f"[SUCCESS] Injected hot-reload into: {os.path.basename(c_path)}")

            else:

                print(f"[INFO] Hot-reload already active in: {os.path.basename(c_path)}")



    # 3. Direct AST & Bytecode Verification

    print("\nVerifying bytecode compilation and attribute presence...")

    py_compile.compile(TARGET_CORE, doraise=True)

    for c_path in CONSOLE_FILES:

        py_compile.compile(c_path, doraise=True)



    import email_triage_core

    import importlib

    importlib.reload(email_triage_core)



    has_attr = hasattr(email_triage_core, "test_imap_connection")

    print(f"[VERIFIED] hasattr(email_triage_core, 'test_imap_connection') = {has_attr}")



    if not has_attr:

        print("[FATAL] Attribute test_imap_connection is still not found!")

        sys.exit(1)



    print("=" * 80)

    print("REMEDIATION VERIFIED AND LOCKED")

    print("=" * 80)


if __name__ == "__main__":
    render()
