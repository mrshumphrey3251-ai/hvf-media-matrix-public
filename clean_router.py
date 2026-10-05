from pathlib import Path
import re
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

clean_action_block = """elif "Action Desk" in str(active_module):
    import sys
    from pathlib import Path
    _cockpit_dir = Path(__file__).resolve().parent
    _target_ext = str(_cockpit_dir.parent / "level5_extensions")
    if _target_ext not in sys.path:
        sys.path.insert(0, _target_ext)
    import action_desk
    action_desk.render()"""

for p in targets:
    if not p.exists():
        continue

    with open(p, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Match from elif "Action Desk" down to action_desk.render()
    pattern = r'elif\s+["\']Action Desk["\']\s+in\s+str\(active_module\):[\s\S]*?action_desk\.render\(\)'
    
    if re.search(pattern, content):
        content = re.sub(pattern, clean_action_block, content)
        print(f"[+] Replaced router block cleanly in: {p.name}")
    else:
        print(f"[-] Could not find pattern in {p.name}")

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(p), doraise=True)
    print(f"[+] Compiled cleanly with ZERO errors: {p.name}")
