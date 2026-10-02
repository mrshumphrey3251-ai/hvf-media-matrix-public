"""
C2 COCKPIT: CEO AUTHORIZATION GATE & LEVEL 5 EXTENSION CONTROLLER
ROLE: Executive interface for inspecting sandboxed drafts, validating cryptographic
      signatures, promoting to Level 5, and executing dynamic modules.
"""

import streamlit as st
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DISPATCH_DIR = BASE_DIR / "dispatch_core"
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
EXT_DIR = BASE_DIR / "level5_extensions"

for p in [str(DISPATCH_DIR), str(BASE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import ceo_authorization_gate
import level5_loader

def render():
    st.markdown("## 🛡️ CEO Authorization Gate & Level 5 Shell")
    st.caption("Zero-Trust Staging Area | Non-Repudiable Cryptographic Promotion Pipeline")
    
    gate = ceo_authorization_gate.CEOAuthorizationGate()
    
    tab_gate, tab_ext, tab_ledger = st.tabs(["🚀 Pending Authorizations", "🧩 Active Level 5 Extensions", "📜 Merkle Audit Ledger"])
    
    with tab_gate:
        st.markdown("### 📋 Staged Sandbox Directives")
        sandbox_files = [f.name for f in SANDBOX_DIR.glob("*.py") if f.name != "sandbox_harness.py"]
        
        if not sandbox_files:
            st.info("🟢 No pending drafts in sandbox_staging. System core is fully synchronized.")
        else:
            selected_file = st.selectbox("Select Pending Sandbox Module:", sandbox_files)
            if selected_file:
                target_path = SANDBOX_DIR / selected_file
                sha_hash = gate.compute_sha256(target_path)
                
                with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                    code_text = f.read()
                
                st.markdown(f"**Target:** `{selected_file}` | **SHA-256:** `{sha_hash[:16]}...{sha_hash[-8:]}`")
                
                with st.expander("🔍 Inspect Generated Code & Blueprint", expanded=False):
                    st.code(code_text, language="python")
                
                st.divider()
                st.markdown("#### ✍️ Executive Cryptographic Sign-Off")
                st.caption("Promoting code transfers full operational and legal authority into the active production shell.")
                
                col_auth, col_btn = st.columns([3, 1])
                with col_auth:
                    auth_token = st.text_input("Enter CEO Authorization Token / Password:", type="password", key="ceo_gate_pwd")
                
                with col_btn:
                    st.write("")
                    st.write("")
                    if st.button("AUTHORIZE & PROMOTE", type="primary", width='stretch'):
                        # Retrieve authorized credential from secrets or env
                        expected_key = os.environ.get("HVF_CEO_PASSWORD")
                        if not expected_key and hasattr(st, "secrets"):
                            expected_key = st.secrets.get("HVF_CEO_PASSWORD")
                        
                        if not expected_key:
                            st.error("[-] Master CEO verification token is not configured in local secrets.")
                        else:
                            result = gate.sign_and_promote(selected_file, auth_token, expected_key)
                            if result.get("success"):
                                st.success(f"[+] {result.get('message')}")
                                st.rerun()
                            else:
                                st.error(f"[-] {result.get('error')}")

    with tab_ext:
        st.markdown("### ⚡ Live Level 5 Extensions")
        active_exts = level5_loader.discover_extensions()
        if not active_exts:
            st.info("No active Level 5 extensions mounted. The system is operating on pure Ring 0.")
        else:
            for name, data in active_exts.items():
                meta = data.get("metadata", {})
                with st.expander(f"📦 {meta.get('name', name)} (v{meta.get('version', '1.0.0')})", expanded=True):
                    st.write(f"**Description:** {meta.get('description', 'Autonomous extension module.')}")
                    if data.get("has_render"):
                        st.markdown("---")
                        data["module"].render()

    with tab_ledger:
        st.markdown("### 🔒 Merkle Authorization Audit Trail")
        ledger_file = gate.ledger_file
        if ledger_file.exists():
            import json
            try:
                with open(ledger_file, "r", encoding="utf-8") as f:
                    entries = json.load(f)
                st.dataframe(entries, width='stretch')
            except Exception as e:
                st.warning(f"Unable to parse audit ledger: {e}")
        else:
            st.info("No authorization events logged in Merkle ledger.")
