import os
import sys
import sqlite3
import getpass
from cryptography.fernet import Fernet

# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN VAULT CREDENTIAL ENCRYPTION
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# Endpoint: humphreyvirtualfarm@gmail.com (HVF_GMAIL_MAIN)
# ==============================================================================

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
KEY_FILE = os.path.join(BASE_DIR, "memory_core", "vault.key")

print("=" * 80)
print("ENCRYPTING AND LOCKING VERIFIED CREDENTIAL INTO SOVEREIGN VAULT")
print("=" * 80)

if not os.path.exists(KEY_FILE):
    print(f"[FAIL] Key file not found at: {KEY_FILE}")
    sys.exit(1)

if not os.path.exists(DB_PATH):
    print(f"[FAIL] Database not found at: {DB_PATH}")
    sys.exit(1)

with open(KEY_FILE, "rb") as f:
    cipher = Fernet(f.read().strip())

raw_token = getpass.getpass("Enter or Paste 16-Character App Password (input hidden): ")
clean_token = raw_token.replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "").strip()

if len(clean_token) != 16:
    print(f"[ERROR] Token length is {len(clean_token)}. Must be exactly 16 letters.")
    sys.exit(1)

encrypted_token = cipher.encrypt(clean_token.encode("utf-8")).decode("utf-8")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
INSERT INTO email_accounts 
(account_alias, email_address, imap_server, imap_port, smtp_server, smtp_port, encrypted_password, is_active, auth_type)
VALUES ('HVF_GMAIL_MAIN', 'humphreyvirtualfarm@gmail.com', 'imap.gmail.com', 993, 'smtp.gmail.com', 465, ?, 1, 'APP_PASSWORD')
ON CONFLICT(account_alias) DO UPDATE SET
    email_address = 'humphreyvirtualfarm@gmail.com',
    encrypted_password = excluded.encrypted_password,
    is_active = 1,
    imap_server = 'imap.gmail.com',
    imap_port = 993,
    smtp_server = 'smtp.gmail.com',
    smtp_port = 465;
""", (encrypted_token,))

conn.commit()

cur.execute("SELECT id, account_alias, email_address, is_active FROM email_accounts WHERE account_alias = 'HVF_GMAIL_MAIN'")
row = cur.fetchone()
conn.close()

print(f"[SUCCESS] Endpoint [{row[1]}] ({row[2]}) is active and encrypted at rest in hvf_memory_vault.db.")
print("=" * 80)
