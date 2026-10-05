from pathlib import Path
import re

target = Path(r"C:\HVF_Repos\hvf-media-matrix-private\level5_extensions\action_desk.py")

if target.exists():
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()
    
    print(f"[*] Scanning action_desk.py dispatch logic...")
    has_button = "st.button" in code
    has_session = "st.session_state" in code
    print(f"[+] Interactive controls present: {has_button}")
    print(f"[+] Session state integration: {has_session}")
