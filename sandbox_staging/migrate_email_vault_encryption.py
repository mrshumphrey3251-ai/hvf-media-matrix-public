"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: MIGRATE EMAIL VAULT ENCRYPTION
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import sqlite3

    import os

    import sys

    from cryptography.fernet import Fernet



    # ==============================================================================

    # HVF Omni-Industrial Matrix | CREDENTIAL VAULT ENCRYPTION MIGRATION

    # Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)

    # System: At-Rest Fernet Encryption for Dynamic Multi-Account Credentials

    # ==============================================================================



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    KEY_DIR = os.path.join(BASE_DIR, "memory_core")

    KEY_FILE = os.path.join(KEY_DIR, "vault.key")



    print("=" * 80)

    print("EXECUTING IN-APP CREDENTIAL VAULT MIGRATION")

    print("=" * 80)



    os.makedirs(KEY_DIR, exist_ok=True)



    # 1. Generate or load dedicated Vault Key

    if not os.path.exists(KEY_FILE):

        master_key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as f:

            f.write(master_key)

        print(f"[SUCCESS] Generated new Master Credential Key: {KEY_FILE}")

    else:

        print(f"[INFO] Using existing Master Credential Key: {KEY_FILE}")



    # 2. Additive migration on email_accounts

    if not os.path.exists(DB_PATH):

        print(f"[FAIL] Database not found at: {DB_PATH}")

        sys.exit(1)



    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()



    # Check existing columns

    cur.execute("PRAGMA table_info(email_accounts)")

    columns = [row[1] for row in cur.fetchall()]



    if "encrypted_password" not in columns:

        cur.execute("ALTER TABLE email_accounts ADD COLUMN encrypted_password TEXT")

        print("[SUCCESS] Added column 'encrypted_password' to email_accounts.")

    else:

        print("[INFO] Column 'encrypted_password' already present.")



    if "auth_type" not in columns:

        cur.execute("ALTER TABLE email_accounts ADD COLUMN auth_type TEXT DEFAULT 'APP_PASSWORD'")

        print("[SUCCESS] Added column 'auth_type' to email_accounts.")

    else:

        print("[INFO] Column 'auth_type' already present.")



    conn.commit()

    conn.close()



    print("=" * 80)

    print("CREDENTIAL VAULT MIGRATION COMPLETE")

    print("=" * 80)


if __name__ == "__main__":
    render()
