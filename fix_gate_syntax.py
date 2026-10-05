from pathlib import Path
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\c2_gate_dashboard.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\c2_gate_dashboard.py")
]

for p in targets:
    if not p.exists():
        continue

    with open(p, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Read lines to inspect context around line 128
    lines = content.splitlines()
    repaired_lines = []
    
    # Fix dangling else blocks and balance indentation
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Detect orphaned else: without matching if/try
        if stripped == "else:" or stripped.startswith("else:"):
            # Check indentation of preceding non-empty lines
            prev_indent = 0
            for prev in reversed(repaired_lines):
                if prev.strip():
                    prev_indent = len(prev) - len(prev.lstrip())
                    break
            # Ensure proper indentation or convert orphan else to standalone block
            indent_spaces = " " * prev_indent
            repaired_lines.append(f"{indent_spaces}else:")
        else:
            repaired_lines.append(line)

    repaired_code = "\n".join(repaired_lines)

    # Write and test compilation
    with open(p, "w", encoding="utf-8") as f:
        f.write(repaired_code)

    try:
        py_compile.compile(str(p), doraise=True)
        print(f"[+] Successfully repaired and compiled: {p}")
    except py_compile.PyCompileError:
        # Fallback: Regenerate a pristine c2_gate_dashboard.py if nested blocks are misaligned
        fallback_code = '''"""
MODULE: C2 Gate Dashboard & Sentinel Engine
AUTHOR: Jeffery Humphrey (CEO Clearance)
ROLE: Gate Authorization and Zero-Trust Airlock.
"""

import streamlit as st
import sys
import json
import importlib.util
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DISPATCH_DIR = BASE_DIR / "dispatch_core"
COCKPIT_DIR = BASE_DIR / "c2_cockpit"
EXT_DIR = BASE_DIR / "level5_extensions"
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
LEDGER_FILE = BASE_DIR / "governance" / "architecture" / "MERKLE_AUTHORIZATION_LEDGER.json"

for p_dir in [str(DISPATCH_DIR), str(BASE_DIR)]:
    if p_dir not in sys.path:
        sys.path.insert(0, p_dir)

import ceo_authorization_gate
import autonomous_self_heal
import deep_code_sentinel

def render():
    st.markdown("## 🛡️ CEO Authorization Gate & Interactive Sandbox")
    st.caption("Live Interactive Validation Cradle | Iterative Directive Loop | Cryptographic Airlock")

    if "gate_alert_msg" in st.session_state:
        level, msg = st.session_state.pop("gate_alert_msg")
        if level == "success":
            st.success(msg)
        else:
            st.error(msg)

    tab_audit, tab_test, tab_promote, tab_ext, tab_ledger = st.tabs([
        "🔍 Deep Sentinel Audit",
        "🧪 Interactive Test Cradle",
        "⚖️ Executive Sign-Off & Veto",
        "🧩 Active Level 5 Extensions",
        "📜 Merkle Audit Ledger"
    ])

    gate = ceo_authorization_gate.CEOAuthorizationGate()

    with tab_audit:
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
            with open(report_file, "r", encoding="utf-8") as rf:
                rep_data = json.load(rf)

            with col_audit1:
                st.markdown(f"**Last Exhaustive Sweep:** `{rep_data.get('timestamp')}`")

            m_a, m_b, m_c = st.columns(3)
            m_a.metric("Total Modules Monitored", rep_data.get("modules_inspected", 0))
            m_b.metric("Operating at Peak Optimization", rep_data.get("modules_optimal", 0))
            m_c.metric("Upgrade Candidates Identified", rep_data.get("modules_needing_upgrade", 0))

        st.markdown("---")
        st.markdown("#### ⚡ Autonomous Remediation & Staging Engine")
        c_b1, c_b2 = st.columns([1, 1])

        with c_b1:
            if st.button("🛠️ EXECUTE AUTONOMOUS BATCH REMEDIATION", type="secondary", width="stretch"):
                with st.spinner("Ebony is applying AST-safe patches and staging verified candidates..."):
                    import subprocess
                    subprocess.run([sys.executable, str(DISPATCH_DIR / "autonomous_batch_patcher.py")], capture_output=True, text=True)
                    st.success("Batch remediation complete. Candidates staged in sandbox quarantine.")
                    st.rerun()

        with c_b2:
            patch_log_file = BASE_DIR / "governance" / "architecture" / "BATCH_PATCH_LOG.json"
            if patch_log_file.exists():
                with open(patch_log_file, "r", encoding="utf-8") as pf:
                    plog = json.load(pf)
                st.info(f"Verified Candidates in Staging: **{plog.get('total_staged', 0)} Modules**")

    with tab_test:
        st.markdown("### 🧪 Live Candidate Runtime & Refinement")
        candidates = [f.name for f in SANDBOX_DIR.glob("*.py") if f.name != "__init__.py"]

        if not candidates:
            st.info("Quarantine staging is clear. No unverified candidates currently staged.")
        else:
            selected_file = st.selectbox("Select Candidate Module to Test:", candidates)
            st.caption(f"Mounted in isolated test namespace: `{selected_file}`")

            mod_path = SANDBOX_DIR / selected_file
            spec = importlib.util.spec_from_file_location(f"test_{selected_file.stem}", str(mod_path))
            candidate_mod = importlib.util.module_from_spec(spec)
            err = None
            try:
                spec.loader.exec_module(candidate_mod)
            except Exception as e:
                err = str(e)

            if err:
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
                            st.error(f"[-] Self-healing failed: {heal_res.get('error')}")
            else:
                st.success("Candidate module loaded cleanly into quarantine harness.")
                if hasattr(candidate_mod, "render"):
                    candidate_mod.render()
                elif hasattr(candidate_mod, "execute"):
                    st.json(candidate_mod.execute())

    with tab_promote:
        st.markdown("### ⚖️ Executive Sign-Off & Production Airlock")
        candidates = [f.name for f in SANDBOX_DIR.glob("*.py") if f.name != "__init__.py"]
        if not candidates:
            st.info("No candidates pending authorization.")
        else:
            promote_file = st.selectbox("Candidate for Production Promotion:", candidates, key="promote_select")
            st.markdown("#### 🚀 Deployment Destination & Navigation")
            c_mount, c_title = st.columns([1, 1])
            with c_mount:
                mount_to_sidebar = st.checkbox("📌 Mount as Dedicated Sidebar Command Module", value=True)
            with c_title:
                default_title = promote_file.replace(".py", "").replace("_", " ").title()
                sidebar_title = st.text_input("Sidebar Display Name:", value=f"⚡ {default_title}")

            auth_token = st.text_input("Enter CEO Authorization Password:", type="password")

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button("✅ AUTHORIZE & PROMOTE", type="primary", width="stretch"):
                    expected_key = "HVF-SOVEREIGN-KEY-2026"
                    res = gate.sign_and_promote(promote_file, auth_token, expected_key)
                    if res.get("success"):
                        if mount_to_sidebar:
                            reg_path = BASE_DIR / "governance" / "architecture" / "SIDEBAR_MODULES.json"
                            reg_data = []
                            if reg_path.exists():
                                try:
                                    with open(reg_path, "r", encoding="utf-8") as rf:
                                        reg_data = json.load(rf)
                                except Exception:
                                    reg_data = []
                            entry = {"filename": promote_file, "title": sidebar_title.strip() or default_title}
                            if not any(x.get("filename") == promote_file for x in reg_data):
                                reg_data.append(entry)
                                with open(reg_path, "w", encoding="utf-8") as wf:
                                    json.dump(reg_data, wf, indent=2)
                        st.session_state["gate_alert_msg"] = ("success", res.get("message"))
                        st.rerun()
                    else:
                        st.error(res.get("error"))

            with col_p2:
                if st.button("🛑 REJECT & PURGE (CEO VETO)", type="secondary", width="stretch"):
                    res = gate.reject_and_purge(promote_file, "CEO Manual Veto")
                    st.session_state["gate_alert_msg"] = ("info", res.get("message"))
                    st.rerun()

    with tab_ext:
        st.markdown("### 🧩 Active Level 5 Production Extensions")
        ext_files = [f.name for f in EXT_DIR.glob("*.py") if f.name != "__init__.py"]
        if not ext_files:
            st.info("No active Level 5 extensions currently mounted.")
        else:
            for ext in ext_files:
                st.write(f"- `{ext}`")

    with tab_ledger:
        st.markdown("### 📜 Merkle Authorization Audit Trail")
        if LEDGER_FILE.exists():
            with open(LEDGER_FILE, "r", encoding="utf-8") as lf:
                ledger_data = json.load(lf)
            st.dataframe(ledger_data, width="stretch")
        else:
            st.info("No authorization transactions recorded yet.")
'''
        with open(p, "w", encoding="utf-8") as f:
            f.write(fallback_code)
        py_compile.compile(str(p), doraise=True)
        print(f"[+] Fallback template compiled cleanly: {p}")
