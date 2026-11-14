import ast
import re
import socket
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def run_regression_audit() -> bool:
    all_ok = True
    py_files = [p for p in BASE_DIR.rglob("*.py") if ".git" not in p.parts and "venv" not in p.parts and ".venv" not in p.parts]
    ast_faults = 0
    for pf in py_files:
        raw = pf.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            ast_faults += 1
        try:
            ast.parse(raw.decode("utf-8"), filename=str(pf))
        except Exception:
            ast_faults += 1
    print(f"[1/3] AST & UTF-8 Check ({len(py_files)} .py files): {'PASS' if ast_faults == 0 else f'FAIL ({ast_faults})'}")
    if ast_faults:
        all_ok = False

    db_files = sorted(BASE_DIR.rglob("*.db"))
    db_faults = 0
    for dbf in db_files:
        c = sqlite3.connect(str(dbf))
        integ = c.execute("PRAGMA integrity_check;").fetchone()[0]
        c.close()
        if integ.lower() != "ok":
            db_faults += 1
    print(f"[2/3] SQLite Integrity Check ({len(db_files)} .db files): {'PASS' if db_faults == 0 else f'FAIL ({db_faults})'}")
    if db_faults:
        all_ok = False

    s = socket.socket()
    s.settimeout(0.5)
    c2_online = (s.connect_ex(("127.0.0.1", 8501)) == 0)
    s.close()
    print(f"[3/3] Local C2 Port 8501 Status: {'ONLINE' if c2_online else 'STANDBY'}")
    return all_ok

if __name__ == "__main__":
    ok = run_regression_audit()
    raise SystemExit(0 if ok else 1)