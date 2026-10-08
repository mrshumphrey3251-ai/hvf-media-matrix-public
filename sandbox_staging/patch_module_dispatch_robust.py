"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: PATCH MODULE DISPATCH ROBUST
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os
    import sys
    import re
    import py_compile

    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
    TARGET_FILES = [
        os.path.join(BASE_DIR, "ebony_console.py"),
        os.path.join(BASE_DIR, "ebony_console_GREEN.py")
    ]

    print("=" * 80)
    print("EXECUTING PATTERN-MATCHED INJECTION INTO SOVEREIGN DISPATCH MODULE")
    print("=" * 80)

    # Complete code for the module block (4-space indentation)
    MODULE_BODY = '''    st.header("📨 Sovereign Multi-Account Dispatch & Inbound Triage Deck")
        st.markdown("Zero-Trust Inbound Adversarial Scrubber & CEO Kinematic Veto Approval Pipeline")

        # --- SECTION 1: OUTBOUND COMPOSITION TERMINAL ---
        with st.expander("✍️ COMPOSE SOVEREIGN OUTBOUND TRANSMISSION (DIRECT DISPATCH)", expanded=False):
            st.markdown("<div style='color: #e2a03f; font-family: monospace; font-size: 0.95em; font-weight: bold; margin-bottom: 8px;'>DIRECT EXECUTIVE STRIKE TRANSMISSION // CAGE: 1AHA8</div>", unsafe_allow_html=True)

            comp_c1, comp_c2 = st.columns([2, 1])
            with comp_c1:
                out_to = st.text_input("Destination Recipient (RFC822 Email)", key="direct_out_to", placeholder="e.g. contracts@signallink.com")
                out_subj = st.text_input("Transmission Subject Line", key="direct_out_subj", placeholder="e.g. Subcontractor LSA Execution Verification // DAF TENCAP Vol 2")
            with comp_c2:
                out_cat = st.selectbox("Classification Category", [
                    "DEFENSE_PRIME_CONTRACTING",
                    "SUBCONTRACTOR_SIGNALLINK",
                    "LEGAL_COMPLIANCE_EXECUTION",
                    "FINANCIAL_TREASURY",
                    "GENERAL_EXECUTIVE"
                ], key="direct_out_cat")
                st.markdown("<div style='font-size:0.85em; color:#94a3b8; margin-top:5px;'><b>Originating Endpoint:</b><br><span style='color:#e2a03f; font-family:monospace;'>humphreyvirtualfarm@gmail.com</span></div>", unsafe_allow_html=True)

            with st.expander("⚡ Draft Assistance with Ebony AI (Grounded in Iron Dome Intel)", expanded=False):
                ai_directive = st.text_input("Strategic Directive for Ebony AI", key="ai_out_directive", placeholder="e.g. Confirm executed LSA with Drew Phillips Jr. and coordinate DAF TENCAP Volume 2.")
                if st.button("⚡ Generate Authoritative Draft", key="btn_gen_ai_draft"):
                    if ai_directive:
                        with st.spinner("Retrieving Iron Dome intelligence and composing draft..."):
                            draft_ai = email_triage_core.generate_direct_draft_assistance(out_to, ai_directive)
                            st.session_state["direct_out_body_val"] = draft_ai
                            st.rerun()
                    else:
                        st.warning("Please specify an objective for Ebony AI.")

            default_body = st.session_state.get("direct_out_body_val", "")
            out_body = st.text_area("Transmission Payload (Strict RFC5322 Plain Text)", value=default_body, height=200, key="direct_out_body")

            snd_c1, snd_c2 = st.columns([1.5, 2])
            with snd_c1:
                if st.button("🚀 Authorize & Dispatch Transmission", key="btn_dispatch_now", type="primary"):
                    if not out_to or not out_subj or not out_body:
                        st.error("Recipient, Subject, and Payload Body are mandatory.")
                    else:
                        with st.spinner("Connecting to smtp.gmail.com:465 & dispatching..."):
                            s_ok, s_msg = email_triage_core.send_direct_outbound_email(
                                to_addr=out_to,
                                subject=out_subj,
                                body=out_body,
                                account_alias="HVF_PRIMARY_EXECUTIVE",
                                category=out_cat
                            )
                        if s_ok:
                            st.success(f"🚀 {s_msg}")
                            st.session_state["direct_out_body_val"] = ""
                            st.rerun()
                        else:
                            st.error(f"Delivery failed: {s_msg}")
            with snd_c2:
                if st.button("Clear Buffer", key="btn_clr_direct_buf"):
                    st.session_state["direct_out_body_val"] = ""
                    st.rerun()

        # --- SECTION 2: INBOX POLL CONTROLS & TELEMETRY ---
        poll_c1, poll_c2 = st.columns([2, 1])
        with poll_c1:
            if st.button("🔄 Poll Monitored Inboxes Now", key="btn_poll_inboxes_main"):
                with st.spinner("Connecting to imap.gmail.com:993 & staging unread messages..."):
                    email_triage_core.run_multi_account_cycle()
                st.success("Polling complete.")
                st.rerun()
        with poll_c2:
            if st.button("🧹 Purge Staged Newsletters", key="btn_purge_newsletters"):
                c_cl = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                cur_cl = c_cl.cursor()
                cur_cl.execute("""
                UPDATE staged_email_dispatches 
                SET veto_status = 'ARCHIVED_NOISE' 
                WHERE veto_status = 'PENDING_CEO_APPROVAL'
                  AND (sender_address LIKE '%newsletters-noreply%' OR sender_address LIKE '%zapier%' OR sender_address LIKE '%instagram%')
                  AND subject NOT LIKE '%Signallink%';
                """)
                c_cl.close()
                st.info("Newsletters archived.")
                st.rerun()

        # --- SECTION 3: FOCUSED SINGLE-TRANSMISSION C2 STEPPER ---
        try:
            c_disp = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
            cur_disp = c_disp.cursor()
            cur_disp.execute("""
                SELECT id, account_alias, sender_address, subject, date_received, 
                       raw_body_sanitized, threat_status, triage_category, draft_response 
                FROM staged_email_dispatches 
                WHERE veto_status = 'PENDING_CEO_APPROVAL' 
                ORDER BY id ASC
            """)
            dispatches = cur_disp.fetchall()
            c_disp.close()
        except Exception as e:
            st.error(f"Failed to load queue: {e}")
            dispatches = []

        total_pending = len(dispatches)

        if total_pending == 0:
            st.markdown("""
                <div style='border: 1px solid #242d3d; border-radius: 2px; padding: 25px; background-color: #121722; text-align: center; margin-top: 15px;'>
                    <div style='color: #e2a03f; font-family: monospace; font-size: 1.15em; font-weight: bold;'>🟢 PERIMETER SECURE | ZERO PENDING TRANSMISSIONS</div>
                    <div style='color: #94a3b8; font-size: 0.85em; margin-top: 6px;'>Queue is completely clear. Incoming transmissions will stage at eye level.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            curr_msg = dispatches[0]
            disp_id, account, sender, subject, date_rx, body_clean, threat, category, draft = curr_msg

            status_class = "status-threat" if "THREAT" in threat else "status-clean"
            status_icon = "🛑" if "THREAT" in threat else "✅"

            st.markdown(f"""
                <div style='border: 1px solid #242d3d; border-radius: 2px; padding: 14px; background-color: #121722; margin-top: 12px;'>
                    <div class='card-header'>
                        <span style='color:#e2a03f; font-family:monospace; font-weight:bold;'>TRANSMISSION 1 OF {total_pending} PENDING</span>
                        <span class='status-badge {status_class}'>{status_icon} {threat}</span>
                    </div>
                    <div style='font-size: 1.05em; font-weight: bold; color: #f1f5f9; margin-top: 8px;'>
                        [{account}] {subject}
                    </div>
                    <div style='font-size: 0.88em; color: #94a3b8; margin-top: 4px;'>
                        <b>FROM:</b> <span style='color:#f1f5f9; font-family:monospace;'>{sender}</span> | 
                        <b>RECEIVED:</b> <span style='color:#f1f5f9;'>{date_rx}</span> | 
                        <b>CATEGORY:</b> <span style='color:#e2a03f;'>{category}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("🔍 View Inbound Transmission Body (Sanitized)", expanded=False):
                st.text(body_clean)

            if "THREAT" in threat:
                st.error("⚠️ Inbound transmission flagged for adversarial injection. Automated inference suspended.")
            else:
                updated_draft = st.text_area(
                    f"Tactical Executive Response Payload (Queue #{disp_id})", 
                    value=draft, 
                    height=180,
                    key=f"stepper_draft_{disp_id}"
                )

            col_act1, col_act2, col_act3 = st.columns([1.2, 1, 1.2])
            with col_act1:
                if st.button("✅ Approve & Dispatch", key=f"btn_step_app_{disp_id}", type="secondary"):
                    with st.spinner("Connecting to smtp.gmail.com:465 & dispatching transmission..."):
                        d_ok, d_msg = email_triage_core.dispatch_outbound_transmission(disp_id, updated_draft)
                    if d_ok:
                        st.success(f"🚀 {d_msg}")
                    else:
                        st.error(f"Delivery failed: {d_msg}")
                    st.rerun()

            with col_act2:
                if st.button("❌ Dismiss Record", key=f"btn_step_dis_{disp_id}"):
                    c_act = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                    cur_act = c_act.cursor()
                    cur_act.execute("UPDATE staged_email_dispatches SET veto_status = 'DISMISSED_BY_CEO' WHERE id = ?", (disp_id,))
                    c_act.close()
                    st.info(f"Transmission #{disp_id} dismissed. Advancing queue.")
                    st.rerun()

            with col_act3:
                if st.button("🚫 Block Sender", key=f"btn_step_blk_{disp_id}", type="primary"):
                    try:
                        suc, b_text = email_triage_core.block_sender(sender, reason="CEO_TACTICAL_VETO")
                        if suc:
                            st.warning(f"🚫 {b_text}")
                        else:
                            st.error(f"Block failed: {b_text}")
                    except Exception as b_err:
                        st.error(f"Block error: {b_err}")
                    st.rerun()
    '''

    for fpath in TARGET_FILES:
        if not os.path.exists(fpath):
            continue

        print(f"\nProcessing target: {os.path.basename(fpath)}")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Match the start of the dispatch module condition
        start_match = re.search(r'^[ \t]*(?:elif|if)\s+active_module\s*==\s*["\'][^"\']*?Dispatch[^"\']*?["\']\s*:\s*\n', content, re.MULTILINE)

        if not start_match:
            # Fallback search for any active_module line mentioning Comms or Deck
            start_match = re.search(r'^[ \t]*(?:elif|if)\s+active_module\s*==[^\n]*?Dispatch[^\n]*?:\s*\n', content, re.MULTILINE)

        if start_match:
            start_pos = start_match.end()
            # Find the next module condition or sidebar block
            end_match = re.search(r'^[ \t]*(?:elif|if)\s+active_module\s*==', content[start_pos:], re.MULTILINE)
            if end_match:
                end_pos = start_pos + end_match.start()
            else:
                # Fallback to sidebar anchor
                side_match = re.search(r'^[ \t]*with\s+col_side:', content[start_pos:], re.MULTILINE)
                end_pos = start_pos + side_match.start() if side_match else len(content)

            new_content = content[:start_pos] + MODULE_BODY + "\n" + content[end_pos:]
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)

            py_compile.compile(fpath, doraise=True)
            print(f"  * [SUCCESS] Replaced Dispatch Module body in {os.path.basename(fpath)} (chars {start_pos} to {end_pos}).")
        else:
            print(f"  * [WARN] Module start regex not matched in {os.path.basename(fpath)}.")

    print("\n" + "=" * 80)
    print("MODULE INJECTION SCRIPT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    render()
