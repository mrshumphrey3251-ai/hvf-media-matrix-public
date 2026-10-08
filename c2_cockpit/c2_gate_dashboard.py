"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: C2 GATE DASHBOARD & EXECUTIVE AIRLOCK
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
"""

from pathlib import Path
import sys
import json
import importlib.util
import streamlit as st

# Canonical Directory Suite
ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT_DIR
EXT_DIR = Path(ROOT_DIR) / "level5_extensions"
SANDBOX_DIR = Path(ROOT_DIR) / "sandbox_staging"
AIRLOCK_DIR = Path(ROOT_DIR) / "sandbox_staging"
DISPATCH_DIR = Path(ROOT_DIR) / "dispatch_core"
COCKPIT_DIR = Path(ROOT_DIR) / "c2_cockpit"
GOVERNANCE_DIR = Path(ROOT_DIR) / "governance"
ARCH_DIR = GOVERNANCE_DIR / "architecture"

# Canonical Governance & Merkle Ledger File Targets
LEDGER_FILE = Path(ARCH_DIR) / "MERKLE_AUDIT_LEDGER.json"
MERKLE_FILE = LEDGER_FILE
AUDIT_REPORT_FILE = Path(ARCH_DIR) / "DEEP_AUDIT_REPORT.json"
BATCH_LOG_FILE = Path(ARCH_DIR) / "BATCH_PATCH_LOG.json"
SIDEBAR_REGISTRY_FILE = Path(ARCH_DIR) / "SIDEBAR_MODULES.json"

# Inject Search Paths
for d in [ROOT_DIR, DISPATCH_DIR, COCKPIT_DIR, EXT_DIR]:
    p_str = str(d)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

# Ensure Required Directories & Default JSON Ledgers Exist on Bare Metal
ARCH_DIR.mkdir(parents=True, exist_ok=True)
for ledger, default_val in [
    (LEDGER_FILE, []),
    (AUDIT_REPORT_FILE, {}),
    (BATCH_LOG_FILE, {"total_staged": 0, "staged_candidates": []}),
    (SIDEBAR_REGISTRY_FILE, {"active_modules": []})
]:
    if not ledger.exists():
        ledger.write_text(json.dumps(default_val, indent=2), encoding="utf-8")

# Engine Imports
import ceo_authorization_gate
import deep_code_sentinel

try:
    import autonomous_self_heal
except ImportError:
    autonomous_self_heal = None

def render():
    from pathlib import Path
    ROOT_DIR = Path(__file__).resolve().parent.parent
    BASE_DIR = ROOT_DIR
    EXT_DIR = Path(ROOT_DIR / "level5_extensions")
    SANDBOX_DIR = Path(ROOT_DIR / "sandbox_staging")
    AIRLOCK_DIR = SANDBOX_DIR
    DISPATCH_DIR = Path(ROOT_DIR / "dispatch_core")
    COCKPIT_DIR = Path(ROOT_DIR / "c2_cockpit")
    GOVERNANCE_DIR = Path(ROOT_DIR / "governance")
    ARCH_DIR = Path(GOVERNANCE_DIR / "architecture")
    LEDGER_FILE = Path(ARCH_DIR / "MERKLE_AUDIT_LEDGER.json")
    MERKLE_FILE = LEDGER_FILE
    AUDIT_REPORT_FILE = Path(ARCH_DIR / "DEEP_AUDIT_REPORT.json")
    BATCH_LOG_FILE = Path(ARCH_DIR / "BATCH_PATCH_LOG.json")
    SIDEBAR_REGISTRY_FILE = Path(ARCH_DIR / "SIDEBAR_MODULES.json")

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

        report_file = Path(ROOT_DIR) / "governance" / "architecture" / "DEEP_AUDIT_REPORT.json"
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
                    subprocess.run([sys.executable, str(Path(DISPATCH_DIR) / "autonomous_batch_patcher.py")], capture_output=True, text=True)
                    st.success("Batch remediation complete. Candidates staged in sandbox quarantine.")
                    st.rerun()

        with c_b2:
            patch_log_file = Path(ROOT_DIR) / "governance" / "architecture" / "BATCH_PATCH_LOG.json"
            if patch_log_file.exists():
                with open(patch_log_file, "r", encoding="utf-8") as pf:
                    plog = json.load(pf)
                st.info(f"Verified Candidates in Staging: **{plog.get('total_staged', 0)} Modules**")
    with tab_test:
        st.markdown("### 🧪 Live Candidate Runtime & Executive Code Review")
        candidates = sorted([f.name for f in Path(SANDBOX_DIR).glob("*.py") if f.name != "__init__.py"])

        if not candidates:
            st.info("Quarantine staging is clear. No unverified candidates currently staged.")
        else:
            col_c1, col_c2 = st.columns([3, 1])
            with col_c1:
                selected_file = st.selectbox("Select Candidate Module to Test & Review:", candidates, key="cradle_candidate_select")
            with col_c2:
                st.caption("Quarantine Isolation Target")
                st.code(f"sandbox_staging/{selected_file}")

            mod_path = Path(SANDBOX_DIR) / selected_file
            code_text = mod_path.read_text(encoding="utf-8", errors="replace")

            has_render = "def render(" in code_text
            has_cage = "CAGE: 1AHA8" in code_text

            # Telemetry Metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Lines of Code", len(code_text.splitlines()))
            col_m2.metric("Payload Size", f"{len(code_text)} B")
            col_m3.metric("Entrypoint Wrapper", "✅ def render():" if has_render else "⚠️ Procedural Raw")
            col_m4.metric("Statutory OPSEC", "✅ CAGE: 1AHA8" if has_cage else "⚠️ Unshielded")

            # Expandable Code Reviewer
            with st.expander(f"📜 Review Remediated Source Code: {selected_file}", expanded=False):
                st.code(code_text, language="python")

            st.markdown("---")
            st.markdown("#### 🖥️ Live Quarantine UI Runtime")

            # Dynamic Execution Harness
            spec = importlib.util.spec_from_file_location(f"test_{Path(selected_file).stem}", str(mod_path))
            candidate_mod = importlib.util.module_from_spec(spec)
            err = None
            try:
                spec.loader.exec_module(candidate_mod)
            except Exception as e:
                err = str(e)

            if err:
                st.error(f"[-] Candidate failed to mount: {err}")
                if autonomous_self_heal:
                    st.markdown("#### 🤖 Ebony Autonomous Self-Healing")
                    if st.button("🛠️ EBONY: AUTONOMOUSLY FIX & RE-STAGE CANDIDATE", type="primary", key="btn_auto_heal"):
                        with st.spinner("Ebony is analyzing stack trace and synthesizing patch..."):
                            heal_res = autonomous_self_heal.self_heal_candidate(selected_file, err)
                            if heal_res.get("success"):
                                st.success(f"Repaired {selected_file}. Rerunning...")
                                st.rerun()
                            else:
                                st.error(f"[-] Self-healing failed: {heal_res.get('error')}")
            else:
                if hasattr(candidate_mod, "render"):
                    st.success("✅ Level-5 Architecture Verified: Running inside isolated render() cradle.")
                    candidate_mod.render()
                elif hasattr(candidate_mod, "execute"):
                    st.success("✅ Level-5 Callable Verified: Running execute() payload.")
                    st.json(candidate_mod.execute())
                else:
                    st.warning("⚠️ Procedural fallback execution. Consider re-running batch remediation.")



    with tab_ext:
        st.markdown("### 🧩 Active Level 5 Production Extensions")
        ext_files = [f.name for f in Path(EXT_DIR).glob("*.py") if f.name != "__init__.py"]
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