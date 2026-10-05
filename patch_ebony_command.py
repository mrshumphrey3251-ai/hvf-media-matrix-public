targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_command_deck_controller.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_command_deck_controller.py"
]

import re

for filepath in targets:
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            content = f.read()

        # Inject command bridge import
        if "import ebony_command_bridge" not in content:
            content = "import ebony_command_bridge\n" + content

        # Wire live module capability status into Ebony Command
        check_block = "bridge = ebony_command_bridge.EbonyCommandBridge()"
        if check_block not in content:
            hud_code = """
    # Live Level 5 Extension Telemetry Hook for Ebony Command
    bridge = ebony_command_bridge.EbonyCommandBridge()
    active_tools = bridge.refresh_registry()
    
    with st.expander("⚡ Ebony Command: Connected Level 5 Modules", expanded=False):
        st.caption("Modules actively bound to Ebony's conversational and autonomous execution core:")
        cols = st.columns(max(1, min(4, len(active_tools))))
        for idx, (t_name, t_meta) in enumerate(active_tools.items()):
            col = cols[idx % len(cols)]
            has_exec = t_meta.get("has_execute", False)
            col.markdown(f"**{'🟢' if has_exec else '🔵'} {t_name}**")
            col.caption(t_meta.get("description", "Active"))
            if has_exec:
                if col.button(f"Poll {t_name}", key=f"cmd_poll_{t_name}"):
                    out = bridge.execute_module_command(t_name)
                    st.json(out)
"""
            # Insert HUD into render function
            if "def render" in content:
                content = re.sub(r'(def render\([^)]*\):)', r'\1\n' + hud_code, content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Wired Ebony Command module integration into: {filepath}")
    except Exception as e:
        print(f"[-] Could not patch {filepath}: {e}")
