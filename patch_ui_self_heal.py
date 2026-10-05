targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\c2_gate_dashboard.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\c2_gate_dashboard.py"
]

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Import self-heal module
    if "import autonomous_self_heal" not in content:
        content = "import autonomous_self_heal\n" + content

    # Replace raw error display with Autonomous Fix Card
    old_err_block = """            if err:
                st.error(f"[-] Candidate failed to mount: {err}")"""

    new_err_block = """            if err:
                st.error(f"[-] Candidate failed to mount: {err}")
                st.markdown("#### 🤖 Ebony Autonomous Self-Healing Alert")
                st.caption("Ebony can automatically analyze this exception, repair the syntax in quarantine, and re-present it for testing.")
                if st.button("🛠️ EBONY: AUTONOMOUSLY FIX & RE-STAGE CANDIDATE", type="primary", key="btn_auto_heal"):
                    with st.spinner("Ebony is analyzing stack trace and synthesizing patch..."):
                        heal_res = autonomous_self_heal.self_heal_candidate(selected_file, err)
                        if heal_res.get("success"):
                            st.session_state["gate_alert_msg"] = ("success", f"Ebony successfully repaired and re-staged {selected_file}. Zero errors detected.")
                            st.rerun()
                        else:
                            st.error(f"[-] Self-healing failed: {heal_res.get('error')}")"""

    if old_err_block in content:
        content = content.replace(old_err_block, new_err_block)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wired Autonomous Self-Healing UI into: {filepath}")
