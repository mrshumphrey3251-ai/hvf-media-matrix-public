import sqlite3
import hashlib

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check existing columns
cur.execute("PRAGMA table_info(system_users)")
cols = [col[1] for col in cur.fetchall()]
print(f"Existing system_users columns: {cols}")

if "company_id" not in cols:
    cur.execute("ALTER TABLE system_users ADD COLUMN company_id TEXT DEFAULT 'HVF_MAIN'")
    print("✅ Added 'company_id' column to system_users.")

if "trial_expires_at" not in cols:
    cur.execute("ALTER TABLE system_users ADD COLUMN trial_expires_at TIMESTAMP")
    print("✅ Added 'trial_expires_at' column to system_users.")

# Provision/Reset the default pilot test account: dale_pilot / pilot2026
cur.execute("SELECT id FROM system_users WHERE username='dale_pilot'")
row = cur.fetchone()
if row:
    cur.execute("""
        UPDATE system_users 
        SET password_hash=?, full_name='Dale Robertson', role='TRIAL_MEMBER', company_id='Robertson Red River Ag', status='APPROVED', trial_expires_at=datetime('now', '+3 days')
        WHERE username='dale_pilot'
    """, (hash_password('pilot2026'),))
    print("✅ Reset active pilot account: dale_pilot / pilot2026")
else:
    cur.execute("""
        INSERT INTO system_users (username, password_hash, full_name, role, company_id, status, trial_expires_at)
        VALUES ('dale_pilot', ?, 'Dale Robertson', 'TRIAL_MEMBER', 'Robertson Red River Ag', 'APPROVED', datetime('now', '+3 days'))
    """, (hash_password('pilot2026'),))
    print("✅ Provisioned active pilot account: dale_pilot / pilot2026")

conn.commit()
conn.close()
print("🎉 [STEP 1 COMPLETE]: Database schema migrated successfully.")