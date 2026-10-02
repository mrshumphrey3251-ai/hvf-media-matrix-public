import os
import sys
import sqlite3
import getpass
from cryptography.fernet import Fernet
import importlib
import email_triage_core

# ==============================================================================
# HVF Omni-Industrial Matrix | ENDPOINT CONSOLIDATION & LIVE INGESTION
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# Target: humphreyvirtualfarm@gmail.com -> HVF_PRIMARY_EXECUTIVE
# ==============================================================================

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
KEY_FILE = os.path.join(BASE_DIR, "memory_core", "vault.key")

print("=" * 80)
print("HVF SOVEREIGN VAULT: ENDPOINT CONSOLIDATION & TRIAGE EXECUTION")
print("=" * 80)

if not os.path.exists(KEY_FILE):
    print(f"[FAIL] Cryptographic key not found at: {KEY_FILE}")
    sys.exit(1)

if not os.path.exists(DB_PATH):
    print(f"[FAIL] Database not found at: {DB_PATH}")
    sys.exit(1)

# 1. Load Fernet Cipher
with open(KEY_FILE, "rb") as f:
    cipher = Fernet(f.read().strip())

# 2. Acquire & Sanitize App Password
raw_token = getpass.getpass("Enter or Paste 16-Character App Password (input hidden): ")
clean_token = raw_token.replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "").strip()

if len(clean_token) != 16:
    print(f"[FAIL] Token length is {len(clean_token)}. Must be exactly 16 characters.")
    sys.exit(1)

encrypted_token = cipher.encrypt(clean_token.encode("utf-8")).decode("utf-8")

# 3. Update Database Schema & State
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Deactivate unconfigured placeholder accounts
cur.execute("""
UPDATE email_accounts 
SET is_active = 0 
WHERE (encrypted_password IS NULL OR encrypted_password = '')
  AND account_alias NOT IN ('HVF_PRIMARY_EXECUTIVE')
""")

# Insert or update HVF_PRIMARY_EXECUTIVE with explicit env_password_key to satisfy NOT NULL constraint
cur.execute("""
INSERT INTO email_accounts 
(account_alias, email_address, imap_server, imap_port, smtp_server, smtp_port, env_password_key, encrypted_password, is_active, auth_type)
VALUES ('HVF_PRIMARY_EXECUTIVE', 'humphreyvirtualfarm@gmail.com', 'imap.gmail.com', 993, 'smtp.gmail.com', 465, 'DYNAMIC_VAULT_ENCRYPTED', ?, 1, 'APP_PASSWORD')
ON CONFLICT(account_alias) DO UPDATE SET
    email_address = 'humphreyvirtualfarm@gmail.com',
    env_password_key = 'DYNAMIC_VAULT_ENCRYPTED',
    encrypted_password = excluded.encrypted_password,
    is_active = 1,
    imap_server = 'imap.gmail.com',
    imap_port = 993,
    smtp_server = 'smtp.gmail.com',
    smtp_port = 465;
""", (encrypted_token,))

conn.commit()

# Telemetry of active accounts
cur.execute("SELECT account_alias, email_address, is_active FROM email_accounts WHERE is_active = 1")
active_rows = cur.fetchall()
conn.close()

print("\n[ACTIVE REGISTERED ENDPOINTS]")
for r in active_rows:
    print(f"  * {r[0]}: {r[1]} (Active: {bool(r[2])})")

print("=" * 80)
print("EXECUTING LIVE INTAKE & VECTOR RAG DRAFTING CYCLE")
print("=" * 80)

# 4. Trigger Ingestion Cycle
importlib.reload(email_triage_core)
email_triage_core.run_multi_account_cycle()

print("\n" + "=" * 80)
print("INGESTION CYCLE COMPLETE")
print("=" * 80)
