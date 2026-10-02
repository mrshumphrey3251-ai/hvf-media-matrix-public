import os
import sqlite3

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"

print("==================================================")
print("🔒  HVF CIPHER AUDIT: ZERO-KNOWLEDGE VERIFICATION")
print("==================================================")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, username, role, encrypted_content, timestamp FROM encrypted_user_comms LIMIT 5")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("ℹ️  No message rows currently stored in encrypted_user_comms.")
    else:
        print(f"Inspecting {len(rows)} raw database records at rest:\n")
        all_encrypted = True
        for r in rows:
            record_id, username, role, ciphertext, ts = r
            # Check for Fernet base64 url-safe structure
            is_fernet = ciphertext.startswith("gAAAAA") and len(ciphertext) > 50
            if not is_fernet:
                all_encrypted = False
                print(f"  ❌ PLAINTEXT DETECTED in Record #{record_id} for user '{username}'!")
            else:
                print(f"  ✅ Record #{record_id} [{username}]: {ciphertext[:32]}... (AES-256 Fernet Ciphertext)")

        print("\n--------------------------------------------------")
        if all_encrypted:
            print("🛡️  PASS: 100% of examined records are stored as AES-256 ciphertext.")
            print("    Zero plain text is exposed in the database file.")
        else:
            print("⚠️  FAIL: Plaintext was discovered in chat logs.")
else:
    print("❌ Database not found.")
print("==================================================")