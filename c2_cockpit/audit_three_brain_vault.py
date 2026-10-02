import os
import sqlite3

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT id, timestamp, action, details, status 
    FROM corporate_governance_log 
    WHERE action = 'THREE_BRAIN_ARCHITECTURE_SEALED' 
    ORDER BY id DESC LIMIT 1
""")

row = cursor.fetchone()
conn.close()

print("=" * 80)
if row:
    rec_id, ts, action, details, status = row
    print(f"[VAULT VERIFIED] Record #{rec_id} | Timestamp: {ts}")
    print(f"  Action : {action}")
    print(f"  Status : {status}")
    print(f"  Details: {details}")
else:
    print("[NOTE] No THREE_BRAIN_ARCHITECTURE_SEALED record found in vault.")
print("=" * 80)
