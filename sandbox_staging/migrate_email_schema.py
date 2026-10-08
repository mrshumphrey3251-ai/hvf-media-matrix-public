"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: MIGRATE EMAIL SCHEMA
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import sqlite3

    import os

    import sys



    # ==============================================================================

    # HVF Omni-Industrial Matrix | MULTI-ACCOUNT EMAIL DISPATCH SCHEMA MIGRATION

    # Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)

    # Database: hvf_memory_vault.db (Additive Non-Destructive Update)

    # ==============================================================================



    DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"



    print("=" * 80)

    print("EXECUTING MULTI-ACCOUNT EMAIL SCHEMA MIGRATION")

    print("=" * 80)



    if not os.path.exists(DB_PATH):

        print(f"[FAIL] Database file not found: {DB_PATH}")

        sys.exit(1)



    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()



    # 1. Multi-Account Configuration Table

    cur.execute("""

    CREATE TABLE IF NOT EXISTS email_accounts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        account_alias TEXT UNIQUE NOT NULL,

        email_address TEXT NOT NULL,

        imap_server TEXT NOT NULL,

        imap_port INTEGER NOT NULL DEFAULT 993,

        smtp_server TEXT NOT NULL,

        smtp_port INTEGER NOT NULL DEFAULT 465,

        env_password_key TEXT NOT NULL,

        use_ssl INTEGER NOT NULL DEFAULT 1,

        is_active INTEGER NOT NULL DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );

    """)



    # 2. Inbound Triage & Staged Outbound Dispatch Table (CEO Kinematic Veto)

    cur.execute("""

    CREATE TABLE IF NOT EXISTS staged_email_dispatches (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        account_alias TEXT NOT NULL,

        message_uid TEXT NOT NULL,

        sender_address TEXT NOT NULL,

        sender_name TEXT,

        recipient_address TEXT NOT NULL,

        subject TEXT NOT NULL,

        date_received TEXT,

        raw_body_sanitized TEXT NOT NULL,

        threat_status TEXT NOT NULL DEFAULT 'INSPECTED_CLEAN',

        triage_category TEXT NOT NULL DEFAULT 'GENERAL',

        iron_dome_context TEXT,

        draft_response TEXT,

        veto_status TEXT NOT NULL DEFAULT 'PENDING_CEO_APPROVAL',

        dispatched_at TIMESTAMP,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(account_alias) REFERENCES email_accounts(account_alias)

    );

    """)



    conn.commit()



    # Verify Tables

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('email_accounts', 'staged_email_dispatches')")

    tables = [row[0] for row in cur.fetchall()]

    conn.close()



    print(f"[SUCCESS] Verified provisioned tables: {tables}")

    print("=" * 80)

    print("MIGRATION COMPLETE - NO EXISTING DATA TOUCHED")

    print("=" * 80)


if __name__ == "__main__":
    render()
