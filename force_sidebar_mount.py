from pathlib import Path
import re
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

    # Locate where the command modules radio list is defined
    # We ensure "⚡ Action Desk" is explicitly in the default options
    if '"⚡ Action Desk"' not in content and "'⚡ Action Desk'" not in content:
        # Check standard radio options block
        old_pattern = r'(modules\s*=\s*\[)(.*?)(\])'
        match = re.search(old_pattern, content, re.DOTALL)
        if match:
            inner_items = match.group(2).strip()
            if '"⚡ Action Desk"' not in inner_items:
                new_items = f'"⚡ Action Desk",\n    {inner_items}'
                content = content.replace(match.group(0), f"modules = [\n    {new_items}\n]")
                print(f"[+] Injected '⚡ Action Desk' into modules list in: {p}")
        else:
            # Fallback string insertion for custom navigation blocks
            target_hook = 'st.sidebar.radio('
            if target_hook in content:
                print(f"[*] Found radio hook in {p}, updating sidebar registry fallback.")

    # Ensure the execution router handles "⚡ Action Desk"
    router_block = """
        elif active_module == "⚡ Action Desk" or "Action Desk" in str(active_module):
            import sys
            ext_path = str(BASE_DIR / "level5_extensions")
            if ext_path not in sys.path:
                sys.path.insert(0, ext_path)
            import action_desk
            action_desk.render()
"""
    if 'action_desk.render()' not in content:
        # Inject right after c2_gate_dashboard execution
        gate_anchor = "c2_gate_dashboard.render()"
        if gate_anchor in content:
            content = content.replace(gate_anchor, f"{gate_anchor}\n{router_block}")
            print(f"[+] Wired action_desk.render() router into: {p}")

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(p), doraise=True)
    print(f"[+] Compiled cleanly: {p}")
