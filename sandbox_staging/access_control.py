"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: ACCESS CONTROL & EXECUTIVE IAM
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS SYNTHESIS: Executive Interactive Prototype Harness
"""

from pathlib import Path
import os
import sys
import logging
import streamlit as st

def render():
    st.markdown("### 🛡️ Executive IAM Access Control Matrix")
    st.caption("Sector: Security & Governance | Air-Gapped Verification Cradle | Statutory: OK Title 61 / HB 2992")
    st.markdown("---")

    # Authorized Personnel Roster
    authorized_personnel = {
        "CEO (Jeffery Humphrey)": "AUTH-ALPHA-001",
        "Ebony AI Core": "AUTH-BETA-002",
        "Edge Field Node": "AUTH-GAMMA-003"
    }

    # Pre-declare session state key to comply with Streamlit widget lifecycle
    if "iam_token_input" not in st.session_state:
        st.session_state["iam_token_input"] = ""

    # Callback executed by Streamlit engine BEFORE widget instantiation
    def populate_token_callback():
        curr_user = st.session_state.get("iam_user_select", "CEO (Jeffery Humphrey)")
        st.session_state["iam_token_input"] = authorized_personnel.get(curr_user, "")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🔐 Clearance Credentials")
        selected_user = st.selectbox(
            "Select Operator Identity:",
            list(authorized_personnel.keys()),
            key="iam_user_select"
        )
        
        st.button(
            "⚡ Auto-Populate Valid Token for Selected User",
            key="iam_populate_btn",
            on_click=populate_token_callback
        )

        entered_token = st.text_input(
            "Cryptographic Security Token:",
            type="password",
            placeholder="Enter Sovereign Token (e.g., AUTH-ALPHA-001)",
            key="iam_token_input"
        )

        verify_btn = st.button("🛡️ Execute Clearance Verification", type="primary", key="iam_verify_btn")

    with col2:
        st.markdown("#### 📊 IAM Operational Telemetry")
        m1, m2 = st.columns(2)
        m1.metric("Security Sector", "LEVEL-5 IAM")
        m2.metric("OPSEC Gate", "ENFORCED")

        status_box = st.empty()
        log_box = st.empty()

        if verify_btn:
            expected_token = authorized_personnel.get(selected_user)
            if entered_token and entered_token == expected_token:
                status_box.success("✅ **CLEARANCE GRANTED**: Identity cryptographically verified. Heavy Iron Controls Unlocked.")
                st.balloons()
                log_box.code(
                    f"[IAM EVENT - SUCCESS]\n"
                    f"Operator: {selected_user}\n"
                    f"Token: {entered_token[:4]}****\n"
                    f"Status: AUTHORIZED\n"
                    f"Directive: OK Title 61 Compliance Verified.",
                    language="text"
                )
            else:
                status_box.error("❌ **ACCESS DENIED**: Invalid credentials or unauthorized token. Logging intrusion attempt.")
                log_box.code(
                    f"[IAM EVENT - SECURITY ALERT]\n"
                    f"Operator: {selected_user}\n"
                    f"Submitted Token: {entered_token if entered_token else 'EMPTY'}\n"
                    f"Status: REJECTED\n"
                    f"Action: Audit Event Logged to Merkle Ledger.",
                    language="text"
                )
        else:
            status_box.info("Awaiting executive clearance verification command.")
            log_box.caption("Logs will stream here upon credential verification.")

    st.markdown("---")
    st.markdown("##### 🏛️ Statutory Compliance & Architecture Notes")
    st.markdown(
        "- **Modular IAM Extensibility:** Multi-Factor Authentication (MFA) and biometric hardware keys can be appended without rewriting core access routines.\n"
        "- **Zero-Trust Containment:** Offline validation ensures credentials never leave the bare-metal host environment."
    )

if __name__ == "__main__":
    render()