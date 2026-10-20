import sqlite3
DB_PATH = r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\hvf_memory_vault.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT invite_code, grant_role, is_used, used_by FROM member_invite_keys ORDER BY id DESC LIMIT 1")
row = cur.fetchone()
conn.close()
print(f"DATABASE VAULT VERIFIED: Key={row[0]} | Role={row[1]} | Used={row[2]} | Recipient={row[3]}")