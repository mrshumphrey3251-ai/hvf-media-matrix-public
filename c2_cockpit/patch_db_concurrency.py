import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGETS = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

print("=" * 80)
print("PATCHING CONSOLE DATABASE HANDLERS FOR CONCURRENT ACCESS")
print("=" * 80)

for fpath in TARGETS:
    if not os.path.exists(fpath):
        continue
        
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Ensure sqlite3.connect uses 30-second timeout everywhere
    code = re.sub(r'sqlite3\.connect\(DB_PATH\)', 'sqlite3.connect(DB_PATH, timeout=30.0)', code)
    code = re.sub(r'sqlite3\.connect\(r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault\.db"\)', 'sqlite3.connect(r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db", timeout=30.0)', code)
    code = re.sub(r"sqlite3\.connect\(r'C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault\.db'\)", 'sqlite3.connect(r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db", timeout=30.0)', code)

    # 2. Inject PRAGMA busy_timeout before write operations on line 1241+
    veto_pattern = r'(c_up\s*=\s*sqlite3\.connect\(DB_PATH[^\)]*\)\s*\n\s*cur_up\s*=\s*c_up\.cursor\(\))'
    if re.search(veto_pattern, code):
        code = re.sub(
            veto_pattern,
            r'\1\n        cur_up.execute("PRAGMA busy_timeout = 30000;")',
            code
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)

    py_compile.compile(fpath, doraise=True)
    print(f"[SUCCESS] Patched concurrency handling in: {os.path.basename(fpath)}")

print("=" * 80)
