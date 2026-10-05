from pathlib import Path
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

for p in targets:
    if not p.exists():
        continue

    with open(p, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # 1. Add "🌾 Grain Silo Aeration" to radio list if missing
    if '"🌾 Grain Silo Aeration"' not in content:
        content = content.replace(
            '"⚡ Action Desk",',
            '"⚡ Action Desk",\n        "🌾 Grain Silo Aeration",'
        )
        print(f"[+] Added '🌾 Grain Silo Aeration' to navigation list in: {p.name}")

    # 2. Add router branch
    silo_router = """elif "Grain Silo" in str(active_module):
    import sys
    from pathlib import Path
    _cockpit_dir = Path(__file__).resolve().parent
    _target_ext = str(_cockpit_dir.parent / "level5_extensions")
    if _target_ext not in sys.path:
        sys.path.insert(0, _target_ext)
    import grain_silo_aeration_and_f
    grain_silo_aeration_and_f.render()"""

    if 'import grain_silo_aeration_and_f' not in content:
        content = content.replace(
            "import action_desk\n    action_desk.render()",
            "import action_desk\n    action_desk.render()\n" + silo_router
        )
        print(f"[+] Wired grain_silo_aeration_and_f router into: {p.name}")

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(p), doraise=True)
    print(f"[+] Verified clean compile on: {p.name}")
