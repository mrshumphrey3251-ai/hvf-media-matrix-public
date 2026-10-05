targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\c2_gate_dashboard.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\c2_gate_dashboard.py"
]

import re

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Add Sidebar Registration Logic inside the promotion block
    old_promote_block = """                        result = gate.sign_and_promote(promote_file, auth_token, expected_key)
                        if result.get("success"):
                            st.session_state["gate_alert_msg"] = ("success", result.get("message"))
                            st.rerun()"""

    new_promote_block = """                        result = gate.sign_and_promote(promote_file, auth_token, expected_key)
                        if result.get("success"):
                            if mount_to_sidebar:
                                import json
                                registry_path = BASE_DIR / "governance" / "architecture" / "SIDEBAR_MODULES.json"
                                reg_data = []
                                if registry_path.exists():
                                    try:
                                        with open(registry_path, "r", encoding="utf-8") as rf:
                                            reg_data = json.load(rf)
                                    except Exception:
                                        reg_data = []
                                entry = {"filename": promote_file, "title": sidebar_title.strip() or promote_file.replace(".py", "").replace("_", " ").title()}
                                if not any(x.get("filename") == promote_file for x in reg_data):
                                    reg_data.append(entry)
                                    with open(registry_path, "w", encoding="utf-8") as wf:
                                        json.dump(reg_data, wf, indent=2)
                                msg = f"{result.get('message')} | 📌 Mounted to Master Sidebar as '{entry['title']}'."
                            else:
                                msg = result.get("message")
                            st.session_state["gate_alert_msg"] = ("success", msg)
                            st.rerun()"""

    ui_toggle_block = """            st.markdown("#### 🚀 Deployment Destination & Navigation")
            c_mount, c_title = st.columns([1, 1])
            with c_mount:
                mount_to_sidebar = st.checkbox("📌 Mount as Dedicated Sidebar Command Module", value=True)
            with c_title:
                default_title = promote_file.replace(".py", "").replace("_", " ").title()
                sidebar_title = st.text_input("Sidebar Display Name:", value=f"⚡ {default_title}")
"""

    if "mount_to_sidebar = st.checkbox" not in content:
        # Inject toggle right above Enter CEO Authorization Password
        content = content.replace('auth_token = st.text_input("Enter CEO Authorization Password:"', f'{ui_toggle_block}\n            auth_token = st.text_input("Enter CEO Authorization Password:"')
        content = content.replace(old_promote_block, new_promote_block)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Sidebar mount capability wired into: {filepath}")
