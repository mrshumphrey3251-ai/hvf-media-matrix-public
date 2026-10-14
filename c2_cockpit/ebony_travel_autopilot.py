"""
E.B.O.N.Y. Autonomous Executive Travel Autopilot & Return Debrief Engine
Authoritative Ghostwriter & Unattended Communications Manager
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Tier: Sovereign Tier-1 Executive Ingestion ($19.99/mo Baseline)
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import os
import sys
import json
import sqlite3
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Enforce UTF-8 encoding across Windows console streams
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
if str(cockpit_dir) not in sys.path:
    sys.path.insert(0, str(cockpit_dir))

from ebony_email_dispatcher import (
    poll_and_auto_dispatch,
    generate_travel_debrief_report,
    DB_PATH,
    CONFIG_PATH
)

def run_travel_cycle(auto_send=True, email_summary_to=None):
    # Enforce stream encoding inside execution thread
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    print("=" * 88)
    print("     E.B.O.N.Y. EXECUTIVE TRAVEL AUTOPILOT // AUTONOMOUS SWEEP ENGAGED      ")
    print(f"     TIMESTAMP: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | NODE: HVFNexus")
    print("=" * 88)
    print("[*] Connecting to live mailbox over TLS/SSL (Port 993/465)...")
    results = poll_and_auto_dispatch(auto_send=auto_send)
    processed_count = len(results)
    print(f"[+] Autonomous cycle complete. Processed {processed_count} transmission(s).")
    for r in results:
        status = r.get("status", "UNKNOWN")
        sender = r.get("sender", "N/A")
        subj = r.get("subject", r.get("message", "N/A"))
        print(f"  • [{status}] {sender[:30]} | {subj[:40]}")
    print("\n[*] Compiling Executive Return Debrief from WORM Ledger...")
    debrief_text = generate_travel_debrief_report()
    try:
        print(debrief_text)
    except Exception:
        print(debrief_text.encode("ascii", "replace").decode("ascii"))
    if email_summary_to and CONFIG_PATH.exists():
        try:
            import smtplib
            import ssl
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if cfg:
                acc = list(cfg.values())[0]
                msg = MIMEMultipart()
                msg["From"] = acc["email"]
                msg["To"] = email_summary_to
                msg["Subject"] = f"E.B.O.N.Y. TRAVEL DEBRIEF: {processed_count} Transmissions Handled While Away"
                msg.attach(MIMEText(debrief_text, "plain", "utf-8"))
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(acc["smtp_host"], acc["smtp_port"], context=context) as client:
                    client.login(acc["email"], acc["password"])
                    client.send_message(msg)
                print(f"\n[+] Debrief report successfully transmitted to executive mobile: {email_summary_to}")
        except Exception as e:
            print(f"[!] Notice: Could not transmit debrief email: {e}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E.B.O.N.Y. Travel Autopilot Engine")
    parser.add_argument("--send", action="store_true", default=True, help="Auto-send replies via SMTP")
    parser.add_argument("--draft-only", action="store_true", help="Stage drafts without sending")
    parser.add_argument("--email-summary", type=str, help="Email address to receive the final debrief")
    args = parser.parse_args()
    should_send = not args.draft_only
    run_travel_cycle(auto_send=should_send, email_summary_to=args.email_summary)
