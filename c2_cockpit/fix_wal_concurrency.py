import os
import sys
import sqlite3
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
TARGETS = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

print("=" * 80)
print("1. ENABLING WRITE-AHEAD LOGGING (WAL) ON SOVEREIGN VAULT")
print("=" * 80)

if os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=60.0)
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode = WAL;")
        mode = cur.fetchone()[0]
        cur.execute("PRAGMA synchronous = NORMAL;")
        cur.execute("PRAGMA busy_timeout = 30000;")
        cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Database journal mode set to: [{mode.upper()}]")
        print("[SUCCESS] SQLite busy timeout configured to 30,000ms.")
    except Exception as e:
        print(f"[FAIL] WAL activation error: {e}")
        sys.exit(1)
else:
    print(f"[FAIL] Database not found at: {DB_PATH}")
    sys.exit(1)

print("\n" + "=" * 80)
print("2. APPLYING LITERAL STRING REPLACEMENTS (ZERO REGEX ESCAPES)")
print("=" * 80)

for fpath in TARGETS:
    if not os.path.exists(fpath):
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()

    # Literal string replacements - eliminates re.sub regex backslash errors
    code = code.replace("sqlite3.connect(DB_PATH)", "sqlite3.connect(DB_PATH, timeout=30.0)")
    code = code.replace('sqlite3.connect(r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db")', 'sqlite3.connect(r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db", timeout=30.0)')
    code = code.replace("sqlite3.connect(r'C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db')", "sqlite3.connect(r'C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db', timeout=30.0)")

    # Inject busy timeout pragma on veto write cursor if present
    target_cursor = "cur_up = c_up.cursor()"
    if target_cursor in code and "cur_up.execute(\"PRAGMA busy_timeout = 30000;\")" not in code:
        code = code.replace(target_cursor, target_cursor + '\n        cur_up.execute("PRAGMA busy_timeout = 30000;")')

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)

    py_compile.compile(fpath, doraise=True)
    print(f"[SUCCESS] Patched concurrency handling in: {os.path.basename(fpath)}")

print("\n" + "=" * 80)
print("DATABASE CONCURRENCY & TIMEOUT PATCH COMPLETE")
print("=" * 80)
