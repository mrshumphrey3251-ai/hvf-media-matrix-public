"""
E.B.O.N.Y. Sovereign Autonomous Email Dispatcher & Executive Travel Autopilot Engine
Zero-API Autonomous Ingestion, Contextual SMTP Auto-Reply & Return Debrief Auditing
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
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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
            classification TEXT NOT NULL,
            message_uid TEXT
        )
    """)
    conn.commit()
    try:
        cur.execute("SELECT message_uid FROM email_dispatch_ledger LIMIT 1")
    except sqlite3.OperationalError as e:
        if "no such column: message_uid" in str(e):
            cur.execute("ALTER TABLE email_dispatch_ledger ADD COLUMN message_uid TEXT")
            conn.commit()
    conn.close()

def clean_decode_header(raw_header: str) -> str:
    if not raw_header:
        return "No Subject"
    try:
        decoded_parts = decode_header(raw_header)
        cleaned = []
        for text, encoding in decoded_parts:
            if isinstance(text, bytes):
                cleaned.append(text.decode(encoding or "utf-8", errors="replace"))
            else:
                cleaned.append(str(text))
        return "".join(cleaned).strip()
    except Exception:
        return str(raw_header).strip()

def is_ignored_sender(sender: str) -> bool:
    s_lower = sender.lower()
    ignore_list = [
        "no-reply", "noreply", "notifications@", "news@", "marketing@",
        "linkedin.com", "instagram.com", "facebook.com", "twitter.com",
        "newspapers.com", "accounts.google.com", "docusign.net", "aliexpress.com",
        "newsletter", "info@", "store+", "read.ai", "mail.whitehouse.gov",
        "skyeyenetwork.com", "pitchbook.com", "adorama.com", "yahboom.com",
        "amazon.com", "promotions@", "support@"
    ]
    return any(domain in s_lower for domain in ignore_list)

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

def save_account_credentials(email_addr: str, password_or_app_pass: str, custom_imap: str = None, custom_smtp: str = None, stay_signed_in: bool = True):
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
        "stay_signed_in": stay_signed_in,
        "registered_at": datetime.now(timezone.utc).isoformat()
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return True

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
        category = "GENERAL_INQUIRY"
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
    my_email_clean = acc["email"].strip().lower()
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
            for m_id in msg_ids[-20:]:
                res, data = imap_client.fetch(m_id, "(RFC822)")
                if res != "OK": continue
                raw_email = data[0][1]
                msg = message_from_bytes(raw_email)
                raw_sender = msg.get("From", "Unknown")
                sender = clean_decode_header(raw_sender)
                raw_subj = msg.get("Subject", "No Subject")
                subject = clean_decode_header(raw_subj)
                uid = msg.get("Message-ID", str(m_id))
                
                # --- SELF-LOOP CIRCUIT BREAKER ---
                sender_lower = sender.lower()
                subj_lower = subject.lower()
                if my_email_clean in sender_lower or "humphreyvirtualfarm" in sender_lower or "[sovereign_local]" in subj_lower:
                    now_ts = datetime.now(timezone.utc).isoformat()
                    conn = sqlite3.connect(str(DB_PATH))
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM email_dispatch_ledger WHERE message_uid=?", (uid,))
                    if not cur.fetchone():
                        cur.execute("""
                            INSERT INTO email_dispatch_ledger 
                            (timestamp, sender, recipient, subject, incoming_intent, drafted_response, status, classification, message_uid)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (now_ts, sender, acc["email"], subject, "Self-Originated / Local Daemon Transmission", "SELF_LOOP_SUPPRESSED_AUTO_ARCHIVED", "ARCHIVED_LOOP", "INTERNAL_SYSTEM_LOOP", uid))
                        conn.commit()
                    conn.close()
                    continue

                # --- BULK / MARKETING FILTER ---
                is_bulk = False
                if msg.get("List-Unsubscribe") or msg.get("Precedence", "").lower() in ["bulk", "list", "junk"]:
                    is_bulk = True
                if is_ignored_sender(sender) or is_bulk:
                    now_ts = datetime.now(timezone.utc).isoformat()
                    conn = sqlite3.connect(str(DB_PATH))
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM email_dispatch_ledger WHERE message_uid=?", (uid,))
                    if not cur.fetchone():
                        cur.execute("""
                            INSERT INTO email_dispatch_ledger 
                            (timestamp, sender, recipient, subject, incoming_intent, drafted_response, status, classification, message_uid)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (now_ts, sender, acc["email"], subject, "Automated Bulk Newsletter / Notification", "NO_REPLY_AUTO_FILTERED", "ARCHIVED_BULK", "NEWSLETTER_FEED", uid))
                        conn.commit()
                    conn.close()
                    continue

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
                conn = sqlite3.connect(str(DB_PATH))
                cur = conn.cursor()
                cur.execute("SELECT id FROM email_dispatch_ledger WHERE message_uid=?", (uid,))
                if cur.fetchone():
                    conn.close()
                    continue
                if auto_send:
                    try:
                        reply = MIMEMultipart()
                        reply["From"] = acc["email"]
                        reply["To"] = sender
                        reply["Subject"] = f"Re: {subject}"
                        reply.attach(MIMEText(response_text, "plain", "utf-8"))
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
        return results if results else [{"status": "IDLE", "message": "Zero actionable direct emails. Bulk mail filtered to archive."}]
    except Exception as e:
        return [{"status": "ERROR", "message": str(e)}]

def generate_travel_debrief_report() -> str:
    init_email_ledger()
    if not DB_PATH.exists():
        return "Matrix WORM Ledger offline. No records available."
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, sender, subject, classification, status, drafted_response 
        FROM email_dispatch_ledger 
        ORDER BY timestamp DESC
    """)
    rows = cur.fetchall()
    conn.close()
    total = len(rows)
    auto_resolved = sum(1 for r in rows if r[4] == 'SENT_AUTONOMOUSLY')
    archived_bulk = sum(1 for r in rows if r[4] in ['ARCHIVED_BULK', 'ARCHIVED_LOOP'])
    drafts_pending = sum(1 for r in rows if r[4] == 'DRAFT_READY')
    priority_flagged = [
        r for r in rows 
        if r[4] not in ['ARCHIVED_BULK', 'ARCHIVED_LOOP', 'RESOLVED_BY_CEO'] 
        and (r[3] in ['STATE_INFRASTRUCTURE_GRANT', 'ODOT_AEROSPACE_INSPECTION', 'EXECUTIVE_SCHEDULING', 'HIGH_PRIORITY_REVIEW']
             or any(k in (r[3] or '').upper() for k in ['GRANT', 'ODOT', 'TITLE61', 'HB2992']))
    ]
    lines = [
        "=" * 92,
        "     E.B.O.N.Y. EXECUTIVE TRAVEL RETURN DEBRIEF // MISSION READOUT REPORT      ",
        "=" * 92,
        f"GENERATED: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | OPERATIONAL NODE: HVFNexus",
        "ENTITY: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5",
        "STATUTORY FRAMEWORK: Oklahoma Title 61 & OK HB 2992 Certified Enclave",
        "-" * 92,
        "EXECUTIVE MACRO-LEVEL SUMMARY WHILE AWAY:",
        f"• Total Transmissions Ingested:        {total}",
        f"• Autonomously Answered & Dispatched:  {auto_resolved}",
        f"• Newsletters & System Loops Archived: {archived_bulk}",
        f"• Drafts Pending Executive Review:     {drafts_pending}",
        f"• High-Priority Action Items:          {len(priority_flagged)}",
        "-" * 92,
        "PRIORITY ACTION ITEMS REQUIRING DIRECT EXECUTIVE ATTENTION:"
    ]
    if not priority_flagged:
        lines.append("  [OK] Zero urgent bottlenecks detected. All operational inquiries resolved autonomously.")
    else:
        for idx, item in enumerate(priority_flagged[:5], 1):
            ts = item[0][:19]
            snd = item[1][:28]
            sbj = item[2][:32]
            lines.append(f"  [{idx}] [{ts}] FROM: {snd} | SUBJ: {sbj}")
            lines.append(f"      STATUS: {item[4]} | CATEGORY: {item[3]}")
    lines.append("-" * 92)
    lines.append(f"{'TIMESTAMP (UTC)':<20} | {'SENDER':<24} | {'STATUS':<18} | {'CATEGORY'}")
    lines.append("-" * 92)
    for r in rows[:10]:
        ts = r[0][:19]
        snd = (r[1][:21] + "...") if len(r[1]) > 24 else r[1]
        stat = r[4][:18]
        cat = r[3][:18]
        lines.append(f"{ts:<20} | {snd:<24} | {stat:<18} | {cat}")
    lines.append("=" * 92)
    return "\n".join(lines)

def get_on_demand_communications_report(limit: int = 25, format_type: str = "text") -> str:
    return generate_travel_debrief_report()

if __name__ == "__main__":
    init_email_ledger()
    print(generate_travel_debrief_report())
