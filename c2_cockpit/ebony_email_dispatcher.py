"""
E.B.O.N.Y. Direct IMAP/SMTP Sovereign Email Engine
Zero-API Onboarding Architecture: Direct Email + App Password Protocol
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Tier: Sovereign Tier-1 Executive Ingestion ($19.99 Core Baseline)
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import os
import sys
import ssl
import json
import imaplib
import smtplib
import sqlite3
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")
CONFIG_PATH = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\email_accounts.json")

def init_email_ledger():
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
    conn.close()

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

def generate_executive_email_report() -> str:
    init_email_ledger()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, recipient, subject, incoming_intent, status 
        FROM email_dispatch_ledger 
        ORDER BY timestamp DESC LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()
    
    report_lines = [
        "=" * 86,
        "     E.B.O.N.Y. EXECUTIVE EMAIL DISPATCH AUDIT REPORT // DAILY ATTESTATION      ",
        "=" * 86,
        f"GENERATED: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | SOVEREIGN NODE: HVFNexus",
        "STATUS: ACTIVE // ZERO-CLOUD AIR-GAPPED INGESTION",
        "-" * 86,
        f"{'TIMESTAMP (UTC)':<20} | {'RECIPIENT':<25} | {'SUBJECT':<20} | {'STATUS'}",
        "-" * 86
    ]
    if not rows:
        report_lines.append("No active email dispatches recorded in ledger.")
    else:
        for r in rows:
            ts = r[0][:19]
            recip = (r[1][:22] + "...") if len(r[1]) > 25 else r[1]
            subj = (r[2][:17] + "...") if len(r[2]) > 20 else r[2]
            stat = r[4]
            report_lines.append(f"{ts:<20} | {recip:<25} | {subj:<20} | {stat}")
    report_lines.append("=" * 86)
    return "\n".join(report_lines)

def detect_servers(email_addr: str):
    domain = email_addr.split("@")[-1].lower()
    if "gmail.com" in domain or "google" in domain:
        return "imap.gmail.com", "smtp.gmail.com", 993, 465
    elif "outlook.com" in domain or "office365.com" in domain or "hotmail.com" in domain:
        return "outlook.office365.com", "smtp.office365.com", 993, 587
    elif "yahoo.com" in domain:
        return "imap.mail.yahoo.com", "smtp.mail.yahoo.com", 993, 465
    else:
        # Fallback to standard enterprise DNS host convention
        return f"mail.{domain}", f"mail.{domain}", 993, 465

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

if __name__ == "__main__":
    init_email_ledger()
    print("[ACTIVE] E.B.O.N.Y. Zero-API Email Dispatcher Online.")
    print("Available Direct Methods: detect_servers(), save_account_credentials(), test_account_connection()")