"""
E.B.O.N.Y. Sovereign Email Dispatch & Executive Reporting Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Tier: Sovereign Tier-1 Executive Ingestion ($19.99 Core Baseline)
Statutory Jurisdiction: State of Oklahoma Title 61 & OK HB 2992
"""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")

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
        "================================================================================",
        "     E.B.O.N.Y. EXECUTIVE EMAIL DISPATCH AUDIT REPORT // DAILY ATTESTATION      ",
        "================================================================================",
        f"GENERATED: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | SOVEREIGN NODE: HVFNexus",
        "STATUS: ACTIVE // ZERO-CLOUD AIR-GAPPED INGESTION",
        "--------------------------------------------------------------------------------",
        f"{'TIMESTAMP (UTC)':<20} | {'RECIPIENT':<25} | {'SUBJECT':<20} | {'STATUS'}",
        "--------------------------------------------------------------------------------"
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
    report_lines.append("================================================================================")
    return "\n".join(report_lines)

if __name__ == "__main__":
    init_email_ledger()
    log_email_transaction(
        sender="state.evaluator@ok.gov",
        recipient="humphreyvirtualfarm@gmail.com",
        subject="Follow-up: State Infrastructure & Drone Grant Allocation",
        incoming_intent="Inquiry regarding bridge inspection prototype and bi-weekly grant alignment.",
        drafted_response="Affirmed receipt. E.B.O.N.Y. autonomous drone specification and OMES vendor packet are staged for next week's grant working group.",
        classification="STATE_EXECUTIVE"
    )
    print(generate_executive_email_report())