targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\c2_gate_dashboard.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\c2_gate_dashboard.py"
]

import re

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    batch_ui_block = """
        st.markdown("---")
        st.markdown("#### ⚡ Autonomous Remediation & Staging Engine")
        c_b1, c_b2 = st.columns([1, 1])

        with c_b1:
            if st.button("🛠️ EXECUTE AUTONOMOUS BATCH REMEDIATION", type="secondary", width="stretch"):
                with st.spinner("Ebony is applying AST-safe patches and staging verified candidates..."):
                    import subprocess
                    res = subprocess.run([sys.executable, str(DISPATCH_DIR / "autonomous_batch_patcher.py")], capture_output=True, text=True)
                    st.success("Batch remediation complete. Candidates staged in sandbox quarantine.")
                    st.rerun()

        with c_b2:
            patch_log_file = BASE_DIR / "governance" / "architecture" / "BATCH_PATCH_LOG.json"
            if patch_log_file.exists():
                import json
                with open(patch_log_file, "r", encoding="utf-8") as pf:
                    plog = json.load(pf)
                st.info(f"Verified Candidates in Staging: **{plog.get('total_staged', 0)} Modules**")
"""

    if "EXECUTE AUTONOMOUS BATCH REMEDIATION" not in content:
        # Inject right after the sweep button row in tab_audit
        content = content.replace('st.markdown("---")\n            st.markdown("#### 📋 Detailed Module-by-Module Health & Line Breakdown")', f'{batch_ui_block}\n            st.markdown("---")\n            st.markdown("#### 📋 Detailed Module-by-Module Health & Line Breakdown")')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wired batch remediation controls into: {filepath}")
