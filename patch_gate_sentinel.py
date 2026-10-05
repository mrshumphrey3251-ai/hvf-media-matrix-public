targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\c2_gate_dashboard.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\c2_gate_dashboard.py"
]

import re

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Import sentinel if not present
    if "import deep_code_sentinel" not in content:
        content = "import deep_code_sentinel\n" + content

    # Add the Sentinel tab to st.tabs
    old_tabs = 'tab_test, tab_promote, tab_ext, tab_ledger = st.tabs(['
    new_tabs = 'tab_audit, tab_test, tab_promote, tab_ext, tab_ledger = st.tabs([\n        "🔍 Deep Sentinel Audit",'

    if old_tabs in content:
        content = content.replace(old_tabs, new_tabs)

    # Render tab_audit content block right before tab_test
    audit_tab_ui = """    with tab_audit:
        st.markdown("### 🔍 Ebony Line-by-Line Sentinel & Autonomous Inspector")
        st.caption("Abstract Syntax Tree Parsing | Logic Flow Verification | Proactive Optimization Directives")

        col_audit1, col_audit2 = st.columns([2, 1])
        with col_audit2:
            if st.button("⚡ EXECUTE IMMEDIATE SYSTEM-WIDE SWEEP", type="primary", width="stretch"):
                with st.spinner("Ebony is analyzing all files line by line..."):
                    auditor = deep_code_sentinel.LineByLineAuditor()
                    auditor.run_full_sweep()
                    st.success("Line-by-line inspection cycle complete.")
                    st.rerun()

        report_file = BASE_DIR / "governance" / "architecture" / "DEEP_AUDIT_REPORT.json"
        if report_file.exists():
            import json
            with open(report_file, "r", encoding="utf-8") as rf:
                rep_data = json.load(rf)

            with col_audit1:
                st.markdown(f"**Last Exhaustive Sweep:** `{rep_data.get('timestamp')}`")
            
            m_a, m_b, m_c = st.columns(3)
            m_a.metric("Total Modules Monitored", rep_data.get("modules_inspected", 0))
            m_b.metric("Operating at Peak Optimization", rep_data.get("modules_optimal", 0))
            m_c.metric("Upgrade Candidates Identified", rep_data.get("modules_needing_upgrade", 0), delta="Actionable" if rep_data.get("modules_needing_upgrade", 0) > 0 else "Nominal")

            st.markdown("---")
            st.markdown("#### 📋 Detailed Module-by-Module Health & Line Breakdown")
            
            details = rep_data.get("details", {})
            for mod_name, mod_info in details.items():
                score = mod_info["metrics"]["complexity_score"]
                status_icon = "🟢" if score >= 90 else ("🟡" if score >= 70 else "🔴")
                
                with st.expander(f"{status_icon} {mod_name} — Health Score: {score}/100 | {mod_info['metrics']['total_lines']} Lines ({mod_info['metrics']['functions']} Functions)", expanded=score < 90):
                    st.write(f"**Physical Path:** `{mod_info['path']}`")
                    st.write(f"**Active Status:** `{mod_info['status']}`")
                    
                    if mod_info["findings"]:
                        st.markdown("**Line-by-Line Semantic Findings & Recommendations:**")
                        for f in mod_info["findings"]:
                            st.write(f"- Line `{f['line']}` [{f['severity']}] **{f['category']}**: {f['detail']}")
                    else:
                        st.success("✅ Clean AST scan. All lines strictly conform to operational specifications.")
        else:
            st.info("No deep audit report found. Click 'EXECUTE IMMEDIATE SYSTEM-WIDE SWEEP' to perform initial baseline inspection.")

"""

    if "with tab_audit:" not in content:
        content = content.replace("    with tab_test:", f"{audit_tab_ui}\n    with tab_test:")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Embedded Deep Sentinel Audit tab into: {filepath}")
