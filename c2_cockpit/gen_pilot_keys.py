import sqlite3
import secrets
import os

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

keys = []
for i in range(3):
    token = f"HVF-PILOT-{secrets.token_hex(3).upper()}"
    cur.execute("INSERT INTO member_invite_keys (invite_code, issued_by, is_used) VALUES (?, 'CEO_MR_HUMPHREY', 0)", (token,))
    keys.append(token)

conn.commit()
conn.close()

print("\n=================== 🎟️ HVF COMMERCIAL PILOT KEYS ISSUED ===================")
for idx, k in enumerate(keys, 1):
    print(f"  Pilot License #{idx}: {k}")
print("==========================================================================\n")