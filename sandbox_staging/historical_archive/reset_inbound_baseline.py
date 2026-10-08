import os
import sys
import sqlite3
import imaplib
import email_triage_core

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

print("=" * 80)
print("PURGING HISTORICAL BACKLOG & SETTING INBOUND IMAP BASELINE")
print("=" * 80)

# 1. Archive existing staged transmissions so active console starts at 0
try:
    conn = email_triage_core.get_db_connection(timeout=30.0)
    cur = conn.cursor()
    cur.execute("""
    UPDATE staged_email_dispatches 
    SET veto_status = 'ARCHIVED_BASELINE' 
    WHERE veto_status = 'PENDING_CEO_APPROVAL'
    """)
    archived_count = cur.rowcount
    conn.close()
    print(f"[SUCCESS] Archived {archived_count} backlogged messages from active review deck.")
except Exception as e:
    print(f"[ERROR] Could not archive database records: {e}")
    sys.exit(1)

# 2. Mark existing IMAP unread messages as SEEN so historical mail is not re-ingested
try:
    conn = email_triage_core.get_db_connection(timeout=10.0)
    cur = conn.cursor()
    cur.execute("""
    SELECT account_alias, email_address, imap_server, imap_port, encrypted_password 
    FROM email_accounts 
    WHERE is_active = 1 AND account_alias = 'HVF_PRIMARY_EXECUTIVE'
    """)
    acc = cur.fetchone()
    conn.close()

    if acc and acc[4]:
        alias, email_addr, srv, port, enc_pwd = acc
        clear_pwd = email_triage_core.decrypt_credential(enc_pwd)
        if clear_pwd:
            print(f"Connecting to IMAP {srv}:{port} to establish inbox baseline...")
            mail = imaplib.IMAP4_SSL(srv, int(port))
            mail.login(email_addr, clear_pwd)
            mail.select("INBOX")
            status, data = mail.search(None, "UNSEEN")
            if status == "OK" and data[0]:
                uids = data[0].split()
                print(f"  * Baseline synchronization: Flagging {len(uids)} existing unread messages as SEEN...")
                for u in uids:
                    mail.store(u, "+FLAGS", "\\Seen")
            mail.logout()
            print("[SUCCESS] IMAP inbox baselined. Only newly arriving inbound emails will be staged.")
except Exception as ex:
    print(f"[WARN] IMAP baseline flag could not be set: {ex}")

print("=" * 80)
print("INBOUND QUEUE IS PURGED AND SYNCHRONIZED FOR FRESH START")
print("=" * 80)
