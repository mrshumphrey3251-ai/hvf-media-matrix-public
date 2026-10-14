"""
E.B.O.N.Y. Tier 1 Commercial Subscriber Provisioning Utility
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

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
if str(cockpit_dir) not in sys.path:
    sys.path.insert(0, str(cockpit_dir))

from ebony_email_dispatcher import (
    detect_servers,
    test_account_connection,
    DB_PATH,
    CONFIG_PATH
)

def provision_tier1_subscriber(client_name: str, client_email: str, app_password: str = None):
    print("=" * 86)
    print("     E.B.O.N.Y. SOVEREIGN TIER-1 COMMERCIAL SUBSCRIBER ONBOARDING     ")
    print(f"     SUBSCRIBER: {client_name.upper()} | TIER: PERSONAL COMMS ($19.99/MO)")
    print("=" * 86)

    clean_email = client_email.strip().lower()
    def_imap, def_smtp, i_port, s_port = detect_servers(clean_email)
    
    config = {}
    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            config = {}

    auth_status = "PENDING_CREDENTIALS"
    clean_pass = app_password.replace(" ", "").strip() if app_password else "PENDING_CLIENT_APP_PASSWORD"

    if app_password:
        print(f"[*] Testing live TLS/SSL socket (Port 993) for {clean_email}...")
        ok, msg = test_account_connection(clean_email, clean_pass, def_imap)
        if ok:
            print("[+] Socket authentication: SUCCESSFUL. Mailbox verified.")
            auth_status = "ACTIVE_AUTHENTICATED"
        else:
            print(f"[!] Warning: Socket test returned: {msg}")
            auth_status = "SOCKET_FAILED_CHECK_PASSWORD"

    config[clean_email] = {
        "subscriber_name": client_name,
        "email": clean_email,
        "password": clean_pass,
        "tier": "TIER_1_PERSONAL",
        "monthly_rate": "$19.99",
        "vip_drone_reserved": True,
        "imap_host": def_imap,
        "smtp_host": def_smtp,
        "imap_port": i_port,
        "smtp_port": s_port,
        "stay_signed_in": True,
        "auth_status": auth_status,
        "provisioned_at": datetime.now(timezone.utc).isoformat()
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"[+] Subscriber '{clean_email}' successfully registered in email_accounts.json.")

    # Commit Commercial Onboarding Attestation into WORM Ledger
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        now_ts = datetime.now(timezone.utc).isoformat()
        attest_payload = (
            f"COMMERCIAL TIER-1 ONBOARDING ATTESTATION: Client {client_name} ({clean_email}) "
            f"provisioned under Tier 1 Personal Comms ($19.99/mo) with VIP Drone Tier reservation. "
            f"Air-gapped TLS/SSL ingestion authorized under Oklahoma Title 61 and CAGE 1AHA8."
        )
        cur.execute("""
            INSERT INTO audit_ledger (timestamp, session_id, role, content, model_core, latency_sec)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (now_ts, "COMMERCIAL_ONBOARDING", "EXECUTIVE_ATTESTATION", attest_payload, "EBONY_TIER1_V1", 0.0))
        conn.commit()
        conn.close()
        print("[+] Commercial subscription milestone committed to matrix_ledger.db.")
    except Exception as e:
        print(f"[!] Notice: Could not commit ledger attestation: {e}")

    # Generate 60-Second Client Onboarding Guide
    guide = f"""
--------------------------------------------------------------------------------------
           60-SECOND CLIENT ONBOARDING INSTRUCTIONS FOR {client_name.upper()}
--------------------------------------------------------------------------------------
1. Ensure 2-Step Verification is active on your Google/Corporate account.
2. Go to: https://myaccount.google.com/apppasswords
3. In 'App name', enter 'EBONY' and click Create.
4. Copy the generated 16-character passcode (e.g., abcd efgh ijkl mnop).
5. Transmit the code to Humphrey Virtual Farms LLC to activate autonomous sweeps.
--------------------------------------------------------------------------------------
"""
    print(guide)
    return config[clean_email]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E.B.O.N.Y. Subscriber Provisioning Utility")
    parser.add_argument("--name", type=str, default="Rob Teel", help="Subscriber full name")
    parser.add_argument("--email", type=str, default="rob.teel@ok.gov", help="Subscriber email address")
    parser.add_argument("--password", type=str, help="16-character App Password (if available)")
    args = parser.parse_args()

    provision_tier1_subscriber(args.name, args.email, args.password)