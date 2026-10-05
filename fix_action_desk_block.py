from pathlib import Path
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

replacement_block = """elif "Action Desk" in str(active_module):
    import sys
    from pathlib import Path
    _repo_root = Path(__file__).resolve().parent.parent
    _ext_dir = str(_repo_root / "level5_extensions")
    if _ext_dir not in sys.path:
        sys.path.insert(0, _ext_dir)
    import action_desk
    action_desk.render()"""

for p in targets:
    if not p.exists():
        continue

    with open(p, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Match the entire broken elif block
    import re
    pattern = r'elif\s+["\']Action Desk["\']\s+in\s+str\(active_module\):.*?(?=elif|\Z)'
    
    # Simple direct replacement of lines around BASE_DIR
    old_target = 'ext_dir = str(BASE_DIR / "level5_extensions")'
    new_target = '_repo_root = Path(__file__).resolve().parent.parent\n    _ext_dir = str(_repo_root / "level5_extensions")'
    
    if old_target in content:
        content = content.replace("import sys\n    ext_dir = str(BASE_DIR / \"level5_extensions\")", 
                                  "import sys\n    from pathlib import Path\n    " + new_target)
        content = content.replace("ext_dir", "_ext_dir")
    else:
        # Fallback regex substitution for any formatting variant
        content = re.sub(
            r'elif\s+["\']Action Desk["\']\s+in\s+str\(active_module\):[\s\S]*?action_desk\.render\(\)',
            replacement_block,
            content
        )

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(p), doraise=True)
    print(f"[+] Fixed BASE_DIR and cleanly compiled: {p}")
