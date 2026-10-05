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

    # 1. Inject "⚡ Action Desk" right at the top of the radio list
    old_radio = '''    active_module = st.radio("Navigation", [
        "🎛️ Master C2 Cockpit",'''
    new_radio = '''    active_module = st.radio("Navigation", [
        "⚡ Action Desk",
        "🎛️ Master C2 Cockpit",'''

    if old_radio in content:
        content = content.replace(old_radio, new_radio)
        print(f"[+] Successfully injected '⚡ Action Desk' into radio list: {p.name}")
    else:
        # Also check with double quotes or alternate spacing
        content = content.replace(
            'active_module = st.radio("Navigation", [',
            'active_module = st.radio("Navigation", [\n        "⚡ Action Desk",'
        )
        print(f"[+] Fallback injected '⚡ Action Desk' into radio list: {p.name}")

    # 2. Wire the router execution block
    router_check = 'if active_module == "⚡ Action Desk":'
    if router_check not in content and 'active_module == "⚡ Action Desk"' not in content:
        # Locate gate dashboard execution line
        gate_anchor = "c2_gate_dashboard.render()"
        action_desk_exec = """        if active_module == "⚡ Action Desk" or "Action Desk" in str(active_module):
            import sys
            ext_dir = str(BASE_DIR / "level5_extensions")
            if ext_dir not in sys.path:
                sys.path.insert(0, ext_dir)
            import action_desk
            action_desk.render()
        elif active_module == "🛡️ CEO Authorization Gate":
            c2_gate_dashboard.render()"""

        if 'elif active_module == "🛡️ CEO Authorization Gate":\n            c2_gate_dashboard.render()' in content:
            content = content.replace(
                'elif active_module == "🛡️ CEO Authorization Gate":\n            c2_gate_dashboard.render()',
                action_desk_exec
            )
            print(f"[+] Replaced gate elif with Action Desk + Gate router in: {p.name}")
        elif 'if active_module == "🛡️ CEO Authorization Gate":\n            c2_gate_dashboard.render()' in content:
            content = content.replace(
                'if active_module == "🛡️ CEO Authorization Gate":\n            c2_gate_dashboard.render()',
                action_desk_exec
            )
            print(f"[+] Replaced gate if with Action Desk + Gate router in: {p.name}")

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(p), doraise=True)
    print(f"[+] Compiled cleanly with ZERO errors: {p.name}")
