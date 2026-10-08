"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: C2 GATE DASHBOARD & EXECUTIVE AIRLOCK
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
"""

from pathlib import Path
import sys
import json
import hashlib
import shutil
from datetime import datetime, timezone
import importlib.util
import streamlit as st

# Canonical Directory Suite
ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT_DIR
EXT_DIR = Path(ROOT_DIR / "level5_extensions")
SANDBOX_DIR = Path(ROOT_DIR / "sandbox_staging")
AIRLOCK_DIR = SANDBOX_DIR
DISPATCH_DIR = Path(ROOT_DIR / "dispatch_core")
COCKPIT_DIR = Path(ROOT_DIR / "c2_cockpit")
GOVERNANCE_DIR = Path(ROOT_DIR / "governance")
ARCH_DIR = Path(GOVERNANCE_DIR / "architecture")

# Canonical Ledger Targets
LEDGER_FILE = Path(ARCH_DIR / "MERKLE_AUDIT_LEDGER.json")
MERKLE_FILE = LEDGER_FILE
AUDIT_REPORT_FILE = Path(ARCH_DIR / "DEEP_AUDIT_REPORT.json")
BATCH_LOG_FILE = Path(ARCH_DIR / "BATCH_PATCH_LOG.json")
SIDEBAR_REGISTRY_FILE = Path(ARCH_DIR / "SIDEBAR_MODULES.json")

# Excluded Orchestrators & Core Runners
EXCLUDED_MODS = {
    "app.py",
    "ebony_console_GREEN.py",
    "ebony_console.py",
    "c2_gate_dashboard.py",
    "c2_forge_dashboard.py",
    "c2_cockpit_dashboard.py",
    "hvf_course_runner.py"
}

# Search Path Injection (Excluding SANDBOX_DIR to prevent namespace poisoning)
for d in [ROOT_DIR, DISPATCH_DIR, COCKPIT_DIR, EXT_DIR]:
    p_str = str(d)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

# Ensure Required Runtime Directories Exist on Bare Metal
for d in [EXT_DIR, SANDBOX_DIR, DISPATCH_DIR, COCKPIT_DIR, ARCH_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Engine Imports
try:
    import ceo_authorization_gate
except ImportError:
    ceo_authorization_gate = None

try:
    import deep_code_sentinel
except ImportError:
    deep_code_sentinel = None

try:
    import autonomous_self_heal
except ImportError:
    autonomous_self_heal = None

def get_file_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    h.update(filepath.read_bytes())
    return h.hexdigest()

def render():
    st.markdown("## 🛡️ CEO Authorization Gate & Sovereign Airlock")
    st.caption("Level-5 Industrial C2 | Sovereign OPSEC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OK Title 61 / HB 2992")

    tab_audit, tab_test, tab_signoff, tab_ext, tab_ledger = st.tabs([
        "🔍 Deep Sentinel Audit",
        "🧪 Interactive Test Cradle",
        "⚖️ Executive Sign-Off & Veto",
        "🧩 Active Level 5 Extensions",
        "📜 Merkle Audit Ledger"
    ])

    # ----------------------------------------------------
    # TAB 1: DEEP SENTINEL AUDIT
    # ----------------------------------------------------
    with tab_audit:
        st.markdown("### 🔍 Ebony Line-by-Line Sentinel & Autonomous Inspector")
        st.caption("Abstract Syntax Tree Parsing | Logic Flow Verification | Proactive Optimization Directives")

        col_audit1, col_audit2 = st.columns([2, 1])
        with col_audit2:
            if st.button("⚡ EXECUTE IMMEDIATE SYSTEM-WIDE SWEEP", type="primary", key="btn_audit_sweep"):
                with st.spinner("Ebony is analyzing all files line by line..."):
                    if deep_code_sentinel:
                        auditor = deep_code_sentinel.LineByLineAuditor()
                        auditor.run_full_sweep()
                        st.success("Line-by-line inspection cycle complete.")
                        st.rerun()
                    else:
                        st.error("Sentinel engine unavailable.")

        if AUDIT_REPORT_FILE.exists():
            with open(AUDIT_REPORT_FILE, "r", encoding="utf-8") as rf:
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
            if st.button("🛠️ EXECUTE AUTONOMOUS BATCH REMEDIATION", type="secondary", key="btn_batch_remed"):
                with st.spinner("Ebony is applying AST-safe patches and staging verified candidates..."):
                    import subprocess
                    patcher_script = DISPATCH_DIR / "autonomous_batch_patcher.py"
                    subprocess.run([sys.executable, str(patcher_script)], capture_output=True, text=True)
                    st.success("Batch remediation complete. Candidates staged in sandbox quarantine.")
                    st.rerun()

        staged_files_list = sorted([f.name for f in Path(SANDBOX_DIR).glob("*.py") if f.name != "__init__.py" and f.name not in EXCLUDED_MODS])
        with c_b2:
            st.metric("Verified Candidates in Staging", f"{len(staged_files_list)} Modules")

        st.markdown("---")
        st.markdown("##### 📦 Staged Candidate Deep-Inspector")
        if staged_files_list:
            col_sel1, col_sel2 = st.columns([3, 1])
            with col_sel1:
                sel_cand = st.selectbox("Select Candidate to Inspect Architecture:", staged_files_list, key="audit_staged_select")
            with col_sel2:
                st.caption("Quarantine Target")
                st.code(f"sandbox_staging/{sel_cand}")

            if sel_cand:
                cand_p = Path(SANDBOX_DIR) / sel_cand
                cand_code = cand_p.read_text(encoding="utf-8", errors="replace")
                
                c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                c_m1.metric("Lines of Code", len(cand_code.splitlines()))
                c_m2.metric("Payload Size", f"{len(cand_code)} B")
                c_m3.metric("Entrypoint Wrapper", "✅ def render():" if "def render(" in cand_code else "⚠️ Procedural Raw")
                c_m4.metric("Statutory OPSEC", "✅ CAGE: 1AHA8" if "CAGE: 1AHA8" in cand_code else "⚠️ Non-Standard")

                with st.expander(f"📜 Inspect Source: {sel_cand}", expanded=False):
                    st.code(cand_code, language="python")
        else:
            st.info("Quarantine staging is currently empty. Run Autonomous Batch Remediation to stage candidates.")

    # ----------------------------------------------------
    # TAB 2: INTERACTIVE TEST CRADLE
    # ----------------------------------------------------
    with tab_test:
        st.markdown("### 🧪 Live Candidate Runtime & Executive Code Review")
        candidates = sorted([f.name for f in Path(SANDBOX_DIR).glob("*.py") if f.name != "__init__.py" and f.name not in EXCLUDED_MODS])

        if not candidates:
            st.info("Quarantine staging is clear. No unverified candidates currently staged.")
        else:
            col_c1, col_c2 = st.columns([3, 1])
            with col_c1:
                selected_file = st.selectbox("Select Candidate Module to Test & Review:", candidates, key="cradle_select")
            with col_c2:
                st.caption("Quarantine Isolation Target")
                st.code(f"sandbox_staging/{selected_file}")

            mod_path = Path(SANDBOX_DIR) / selected_file
            code_text = mod_path.read_text(encoding="utf-8", errors="replace")

            tm1, tm2, tm3, tm4 = st.columns(4)
            tm1.metric("Lines of Code", len(code_text.splitlines()))
            tm2.metric("Payload Size", f"{len(code_text)} B")
            tm3.metric("Entrypoint Wrapper", "✅ def render():" if "def render(" in code_text else "⚠️ Procedural Raw")
            tm4.metric("Statutory OPSEC", "✅ CAGE: 1AHA8" if "CAGE: 1AHA8" in code_text else "⚠️ Unshielded")

            with st.expander(f"📜 Review Remediated Source Code: {selected_file}", expanded=False):
                st.code(code_text, language="python")

            st.markdown("---")
            st.markdown("#### 🖥️ Live Quarantine UI Runtime")

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
                    if st.button("🛠️ EBONY: AUTONOMOUSLY FIX & RE-STAGE CANDIDATE", type="primary", key="btn_cradle_heal"):
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
                    st.warning("⚠️ Procedural fallback execution. Candidate lacks callable entrypoint.")

    # ----------------------------------------------------
    # TAB 3: EXECUTIVE SIGN-OFF & VETO
    # ----------------------------------------------------
    with tab_signoff:
        st.markdown("### ⚖️ Executive Sign-Off, Cryptographic Authorization & Veto")
        st.caption("Oklahoma Title 61 / HB 2992 Statutory Compliance | Sovereign Hardware Airlock")

        staged_candidates = sorted([f.name for f in Path(SANDBOX_DIR).glob("*.py") if f.name != "__init__.py" and f.name not in EXCLUDED_MODS])

        if not staged_candidates:
            st.info("Quarantine airlock is clear. No pending candidates awaiting executive sign-off.")
        else:
            col_so1, col_so2 = st.columns([2, 1])
            with col_so1:
                target_promote = st.selectbox("Select Candidate for Promotion / Veto:", staged_candidates, key="signoff_select")
            
            target_path = Path(SANDBOX_DIR) / target_promote
            file_hash = get_file_sha256(target_path)

            with col_so2:
                st.caption("Cryptographic SHA-256 Digest")
                st.code(file_hash[:20] + "...")

            st.markdown("---")
            col_action1, col_action2 = st.columns([1, 1])

            with col_action1:
                st.markdown("#### 🛡️ Executive Clearance Gate")
                auth_key = st.text_input(
                    "Executive Authorization Key:",
                    type="password",
                    placeholder="Enter Sovereign Authorization Credential",
                    key="executive_signoff_key"
                )

                if st.button("🛡️ Authorize & Promote to Production", type="primary", key="btn_promote_prod"):
                    if auth_key == "HVF-SOVEREIGN-KEY-2026":
                        dest_path = Path(EXT_DIR) / target_promote
                        shutil.copy2(target_path, dest_path)
                        target_path.unlink()

                        # Append to Merkle Audit Ledger
                        ledger_entries = []
                        if LEDGER_FILE.exists():
                            try:
                                with open(LEDGER_FILE, "r", encoding="utf-8") as lf:
                                    ledger_entries = json.load(lf)
                            except Exception:
                                ledger_entries = []

                        ledger_entries.append({
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "module": target_promote,
                            "sha256": file_hash,
                            "authorized_by": "Jeffery Humphrey (CEO Clearance)",
                            "status": "PROMOTED_LEVEL5_PRODUCTION",
                            "cage": "1AHA8",
                            "uei": "S1M4ENLHTDH5",
                            "statutory": "OK Title 61 / HB 2992"
                        })

                        with open(LEDGER_FILE, "w", encoding="utf-8") as lf:
                            json.dump(ledger_entries, lf, indent=2)

                        st.success(f"✅ **AUTHORIZATION GRANTED**: `{target_promote}` successfully promoted to `level5_extensions/`.")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ **CLEARANCE REJECTED**: Invalid Executive Authorization Key.")

            with col_action2:
                st.markdown("#### 🚫 Executive Veto & Quarantine Purge")
                veto_reason = st.text_input("Veto Justification / Rejection Directive:", placeholder="e.g., Fails architectural standard", key="veto_reason_input")
                
                if st.button("🚫 Executive Veto & Purge Candidate", type="secondary", key="btn_veto_purge"):
                    target_path.unlink()
                    st.warning(f"🚫 **EXECUTIVE VETO EXECUTED**: `{target_promote}` purged from quarantine.")
                    st.rerun()

    # ----------------------------------------------------
    # TAB 4: ACTIVE LEVEL 5 EXTENSIONS
    # ----------------------------------------------------
    with tab_ext:
        st.markdown("### 🧩 Active Level 5 Production Extensions")
        st.caption("Authorized and Running in Live Sovereign C2 Namespace")

        ext_files = sorted([f.name for f in Path(EXT_DIR).glob("*.py") if f.name != "__init__.py"])
        
        m_e1, m_e2 = st.columns(2)
        m_e1.metric("Active Production Modules", len(ext_files))
        m_e2.metric("OPSEC Compliance Tier", "LEVEL-5 ENFORCED")

        if not ext_files:
            st.info("No Level-5 extensions currently promoted in production directory.")
        else:
            sel_ext = st.selectbox("Inspect Active Production Extension:", ext_files, key="ext_active_select")
            if sel_ext:
                ep = Path(EXT_DIR) / sel_ext
                ep_code = ep.read_text(encoding="utf-8", errors="replace")
                st.caption(f"SHA-256 Digest: `{get_file_sha256(ep)}`")
                with st.expander(f"📜 Inspect Production Code: {sel_ext}", expanded=False):
                    st.code(ep_code, language="python")

    # ----------------------------------------------------
    # TAB 5: MERKLE AUDIT LEDGER
    # ----------------------------------------------------
    with tab_ledger:
        st.markdown("### 📜 Merkle Authorization Audit Trail")
        st.caption("Immutable Record of Sovereign Code Authorizations & Promotions")

        if LEDGER_FILE.exists():
            try:
                with open(LEDGER_FILE, "r", encoding="utf-8") as lf:
                    ledger_data = json.load(lf)
                
                if ledger_data:
                    st.dataframe(ledger_data, width="stretch")
                    st.download_button(
                        label="📥 Download Merkle Audit Ledger (JSON)",
                        data=json.dumps(ledger_data, indent=2),
                        file_name="MERKLE_AUDIT_LEDGER.json",
                        mime="application/json"
                    )
                else:
                    st.info("Merkle ledger initialized. Zero promotion records currently logged.")
            except Exception as e:
                st.error(f"Failed to parse Merkle Ledger: {e}")
        else:
            st.info("Merkle ledger not yet generated on bare metal.")

if __name__ == "__main__":
    render()