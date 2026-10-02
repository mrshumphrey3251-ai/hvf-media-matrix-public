import sqlite3
import os

db_path = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Ensure system_users table exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS system_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'MEMBER',
        status TEXT NOT NULL DEFAULT 'APPROVED',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 2. Check and add missing status column if needed
cur.execute("PRAGMA table_info(system_users)")
columns = [row[1] for row in cur.fetchall()]

if "status" not in columns:
    cur.execute("ALTER TABLE system_users ADD COLUMN status TEXT NOT NULL DEFAULT 'APPROVED'")
    print("[HVF DB]: Added 'status' column to system_users.")
else:
    print("[HVF DB]: 'status' column already present.")

# 3. Ensure all existing accounts are set to APPROVED
cur.execute("UPDATE system_users SET status = 'APPROVED' WHERE status IS NULL OR status = ''")

# 4. Ensure member_invite_keys table exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS member_invite_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invite_code TEXT UNIQUE NOT NULL,
        issued_by TEXT NOT NULL,
        is_used INTEGER DEFAULT 0,
        used_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 5. Seed initial VIP key
cur.execute("""
    INSERT OR IGNORE INTO member_invite_keys (invite_code, issued_by, is_used)
    VALUES ('HVF-VIP-INITIAL', 'ceo', 0)
""")

conn.commit()
conn.close()
print("[HVF DB]: Database migration and tables fully verified.")