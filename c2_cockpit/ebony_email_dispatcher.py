"""
E.B.O.N.Y. Sovereign Autonomous Email Dispatcher & Communications Engine
Zero-API Autonomous Ingestion, Contextual Auto-Reply & On-Demand Ledger Auditing
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Tier: Sovereign Tier-1 Executive Ingestion ($19.99/mo Baseline)
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import os
import sys
import ssl
import json
import imaplib
import smtplib
import sqlite3
import argparse
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")
CONFIG_PATH = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\email_accounts.json")

def init_email_ledger():
    if not DB_PATH.parent.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS email_dispatch_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            subject TEXT NOT NULL,
            incoming_intent TEXT NOT NULL,
            drafted_response TEXT NOT NULL,
            status TEXT NOT NULL,
            classification TEXT NOT NULL
        )
    """)
    conn.commit()
    
    # Self-healing non-destructive schema migration
    try:
        cur.execute("SELECT message_uid FROM email_dispatch_ledger LIMIT 1")
    except sqlite3.OperationalError as e:
        if "no such column: message_uid" in str(e):
            cur.execute("ALTER TABLE email_dispatch_ledger ADD COLUMN message_uid TEXT UNIQUE")
            conn.commit()
            
    conn.close()

def detect_servers(email_addr: str):
    domain = email_addr.split("@")[-1].lower()
    if "gmail.com" in domain or "google" in domain:
        return "imap.gmail.com", "smtp.gmail.com", 993, 465
    elif any(k in domain for k in ["outlook.com", "office365.com", "hotmail.com"]):
        return "outlook.office365.com", "smtp.office365.com", 993, 587
    elif "yahoo.com" in domain:
        return "imap.mail.yahoo.com", "smtp.mail.yahoo.com", 993, 465
    else:
        return f"mail.{domain}", f"mail.{domain}", 993, 465

def test_account_connection(email_addr: str, password_or_app_pass: str, imap_host: str = None):
    def_imap, _, _, _ = detect_servers(email_addr)
    target_host = imap_host if imap_host else def_imap
    clean_pass = password_or_app_pass.replace(" ", "").strip()

    try:
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(target_host, 993, ssl_context=context) as client:
            client.login(email_addr.strip(), clean_pass)
            status, _ = client.select("INBOX", readonly=True)
            return status == "OK", "Connection Successful"
    except Exception as e:
        return False, str(e)

def save_account_credentials(email_addr: str, password_or_app_pass: str, custom_imap: str = None, custom_smtp: str = None):
    def_imap, def_smtp, def_i_port, def_s_port = detect_servers(email_addr)
    imap_host = custom_imap if custom_imap else def_imap
    smtp_host = custom_smtp if custom_smtp else def_smtp

    config = {}
    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            config = {}

    clean_pass = password_or_app_pass.replace(" ", "").strip()
    config[email_addr.strip().lower()] = {
        "email": email_addr.strip(),
        "password": clean_pass,
        "imap_host": imap_host,
        "smtp_host": smtp_host,
        "imap_port": def_i_port,
        "smtp_port": def_s_port,
        "registered_at": datetime.now(timezone.utc).isoformat()
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return True

def log_email_transaction(sender: str, recipient: str, subject: str, incoming_intent: str, drafted_response: str, classification: str = "OFFICIAL"):
    init_email_ledger()
    now_ts = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO email_dispatch_ledger 
        (timestamp, sender, recipient, subject, incoming_intent, drafted_response, status, classification)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (now_ts, sender, recipient, subject, incoming_intent, drafted_response, "DRAFT_READY", classification))
    conn.commit()
    conn.close()
    return now_ts

def generate_autonomous_response(sender: str, subject: str, body: str) -> tuple[str, str]:
    subj_lower = subject.lower()
    body_lower = body.lower()
    
    if any(k in subj_lower or k in body_lower for k in ["grant", "funding", "budget", "ocast", "odaa", "odot"]):
        category = "STATE_INFRASTRUCTURE_GRANT"
        response = (
            "Thank you for contacting the Executive Office of Humphrey Virtual Farms LLC.\n\n"
            "This transmission has been logged and routed to our Oklahoma Title 61 & Infrastructure Grant Working Group. "
            "Our Phase-1 UAS technical specification ($25,000 prototype schedule) and OMES vendor packet are active. "
            "Our executive team will follow up directly on this docket.\n\n"
            "Executive Dispatch // Humphrey Virtual Farms LLC\n"
            "CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5 | Bare-Metal Node: HVFNexus"
        )
    elif any(k in subj_lower or k in body_lower for k in ["bridge", "road", "inspection", "drone", "uas", "tether"]):
        category = "ODOT_AEROSPACE_INSPECTION"
        response = (
            "Thank you for your inquiry regarding E.B.O.N.Y. Autonomous Aerial Infrastructure Inspection.\n\n"
            "Our autonomous tethered and inductive UAS platform operates under Oklahoma Title 61 and OK HB 2992 statutory frameworks, "
            "delivering sub-millimeter optical, thermal, and LiDAR structural evaluations for bridges and state facilities. "
            "Your request is placed in our operational flight schedule.\n\n"
            "Executive Dispatch // Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)"
        )
    elif any(k in subj_lower or k in body_lower for k in ["meeting", "schedule", "calendar", "briefing", "zoom", "coffee"]):
        category = "EXECUTIVE_SCHEDULING"
        response = (
            "Acknowledged receipt. The Executive Calendar is maintained on a recurring bi-weekly cadence "
            "in alignment with state leadership and defense partners. Your requested time has been noted and placed in review.\n\n"
            "Executive Office // Humphrey Virtual Farms LLC"
        )
    else:
        category = "GENERAL_EXECUTIVE_DISPATCH"
        response = (
            "Thank you for reaching out to Humphrey Virtual Farms LLC.\n\n"
            "Your transmission has been securely ingested by the E.B.O.N.Y. Sovereign Dispatch Engine and committed "
            "to our local SQLite WORM audit ledger. An executive follow-up will be issued as operational requirements dictate.\n\n"
            "Executive Dispatch // Humphrey Virtual Farms LLC"
        )
    return response, category

def poll_and_auto_dispatch(email_addr: str = None, auto_send: bool = False) -> list[dict]:
    init_email_ledger()
    if not CONFIG_PATH.exists():
        return [{"status": "IDLE", "message": "No configured email account found in email_accounts.json."}]

    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        return [{"status": "ERROR", "message": f"Config read error: {e}"}]

    if not config:
        return [{"status": "IDLE", "message": "email_accounts.json contains zero registered accounts."}]

    target_email = email_addr.lower() if email_addr else list(config.keys())[0]
    if target_email not in config:
        return [{"status": "ERROR", "message": f"Account {target_email} not registered."}]

    acc = config[target_email]
    results = []

    try:
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(acc["imap_host"], acc["imap_port"], ssl_context=context) as imap_client:
            imap_client.login(acc["email"], acc["password"])
            imap_client.select("INBOX")

            status, messages = imap_client.search(None, "UNSEEN")
            if status != "OK" or not messages[0]:
                return [{"status": "IDLE", "message": "Zero unread messages detected in INBOX."}]

            msg_ids = messages[0].split()
            for m_id in msg_ids[-10:]:
                res, data = imap_client.fetch(m_id, "(RFC822)")
                if res != "OK": continue
                
                raw_email = data[0][1]
                msg = message_from_bytes(raw_email)
                
                sender = msg.get("From", "Unknown")
                subject = msg.get("Subject", "No Subject")
                uid = msg.get("Message-ID", str(m_id))
                
                body_content = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body_content = part.get_payload(decode=True).decode(errors="replace")
                            break
                else:
                    body_content = msg.get_payload(decode=True).decode(errors="replace")

                response_text, classification = generate_autonomous_response(sender, subject, body_content)
                now_ts = datetime.now(timezone.utc).isoformat()
                dispatch_status = "DRAFT_READY"

                if auto_send:
                    try:
                        reply = MIMEMultipart()
                        reply["From"] = acc["email"]
                        reply["To"] = sender
                        reply["Subject"] = f"Re: {subject}"
                        reply.attach(MIMEText(response_text, "plain"))

                        if acc["smtp_port"] == 465:
                            with smtplib.SMTP_SSL(acc["smtp_host"], acc["smtp_port"], context=context) as smtp_client:
                                smtp_client.login(acc["email"], acc["password"])
                                smtp_client.send_message(reply)
                        else:
                            with smtplib.SMTP(acc["smtp_host"], acc["smtp_port"]) as smtp_client:
                                smtp_client.starttls(context=context)
                                smtp_client.login(acc["email"], acc["password"])
                                smtp_client.send_message(reply)
                        dispatch_status = "SENT_AUTONOMOUSLY"
                    except Exception as smtp_err:
                        dispatch_status = f"SEND_FAILED: {smtp_err}"

                conn = sqlite3.connect(str(DB_PATH))
                cur = conn.cursor()
                try:
                    cur.execute("""
                        INSERT INTO email_dispatch_ledger 
                        (timestamp, sender, recipient, subject, incoming_intent, drafted_response, status, classification, message_uid)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (now_ts, sender, acc["email"], subject, body_content[:300], response_text, dispatch_status, classification, uid))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass
                finally:
                    conn.close()

                results.append({
                    "timestamp": now_ts,
                    "sender": sender,
                    "subject": subject,
                    "status": dispatch_status,
                    "classification": classification,
                    "response": response_text
                })

        return results if results else [{"status": "IDLE", "message": "No new actionable emails processed."}]
    except Exception as e:
        return [{"status": "ERROR", "message": str(e)}]

def get_on_demand_communications_report(limit: int = 25, format_type: str = "text") -> str:
    init_email_ledger()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, sender, recipient, subject, classification, status, drafted_response 
        FROM email_dispatch_ledger 
        ORDER BY timestamp DESC LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()

    if format_type == "markdown":
        lines = [
            "### 📋 E.B.O.N.Y. ON-DEMAND COMMUNICATIONS AUDIT LEDGER",
            f"**Generated:** `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}` | **Enclave:** `HVFNexus` | **CAGE:** `1AHA8`",
            "",
            "| Timestamp (UTC) | Sender / From | Subject | Category | Status | Dispatched Response Summary |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ]
        for r in rows:
            ts = r[0][:19]
            snd = r[1].replace("|", "-")[:25]
            sub = r[3].replace("|", "-")[:22]
            cat = r[4]
            stat = r[5]
            resp = r[6].replace("\n", " ").replace("|", "-")[:45] + "..."
            lines.append(f"| `{ts}` | **{snd}** | {sub} | `{cat}` | **{stat}** | {resp} |")
        return "\n".join(lines)
    else:
        lines = [
            "=" * 92,
            "               E.B.O.N.Y. EXECUTIVE COMMUNICATIONS REPORT // ON-DEMAND AUDIT            ",
            "=" * 92,
            f"GENERATED: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | OPERATIONAL ENCLAVE: HVFNexus",
            f"CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OKLAHOMA TITLE 61 & OK HB 2992",
            "-" * 92,
            f"{'TIMESTAMP (UTC)':<20} | {'SENDER':<24} | {'SUBJECT':<20} | {'STATUS':<12} | {'CATEGORY'}",
            "-" * 92
        ]
        if not rows:
            lines.append("No recorded communications in ledger.")
        else:
            for r in rows:
                ts = r[0][:19]
                snd = (r[1][:21] + "...") if len(r[1]) > 24 else r[1]
                sub = (r[3][:17] + "...") if len(r[3]) > 20 else r[3]
                stat = r[5][:12]
                cat = r[4]
                lines.append(f"{ts:<20} | {snd:<24} | {sub:<20} | {stat:<12} | {cat}")
                lines.append(f"  └─ DISPATCHED RESPONSE: {r[6][:75]}...")
                lines.append("-" * 92)
        lines.append("=" * 92)
        return "\n".join(lines)

def generate_executive_email_report() -> str:
    return get_on_demand_communications_report(limit=10, format_type="text")

if __name__ == "__main__":
    init_email_ledger()
    parser = argparse.ArgumentParser(description="E.B.O.N.Y. Sovereign Autonomous Email Dispatcher")
    parser.add_argument("--poll", action="store_true", help="Poll configured INBOX and auto-generate responses")
    parser.add_argument("--send", action="store_true", help="Immediately send generated replies via SMTP")
    parser.add_argument("--report", action="store_true", help="Generate on-demand communications report")
    parser.add_argument("--markdown", action="store_true", help="Output report in Markdown format")
    args = parser.parse_args()

    if args.poll:
        res = poll_and_auto_dispatch(auto_send=args.send)
        print(f"[POLL COMPLETED] Processed {len(res)} event(s):")
        for item in res:
            print(f" • [{item.get('status')}] {item.get('sender', '')} - {item.get('subject', item.get('message', ''))}")
    elif args.report:
        fmt = "markdown" if args.markdown else "text"
        print(get_on_demand_communications_report(format_type=fmt))
    else:
        print(get_on_demand_communications_report(format_type="text"))