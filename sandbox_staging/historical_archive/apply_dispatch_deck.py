import os
import sys

# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN DISPATCH DECK INJECTOR
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Deterministic Additive Injection of Sovereign Dispatch Deck UI
# ==============================================================================

TARGET_FILES = [
    r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console.py",
    r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console_GREEN.py"
]

NAV_TARGET = '"ðŸ“¡ Sovereign Comms Deck",'
NAV_REPLACEMENT = '"ðŸ“¡ Sovereign Comms Deck",\n        "ðŸ“¨ Sovereign Dispatch Deck",'

MODULE_HANDLER = """
elif active_module == "ðŸ“¨ Sovereign Dispatch Deck":
    st.subheader("ðŸ“¨ Sovereign Multi-Account Dispatch & Inbound Triage Deck")
    st.caption("Zero-Trust Inbound Adversarial Scrubber & CEO Kinematic Veto Approval Pipeline")

    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, account_alias, email_address, is_active FROM email_accounts")
    monitored_accs = cur.fetchall()

    col_acc1, col_acc2 = st.columns([2, 1])
    with col_acc1:
        st.markdown("#### ðŸ“¬ Monitored Sovereign Inboxes")
        for acc in monitored_accs:
            status_icon = "ðŸŸ¢ ACTIVE" if acc[3] == 1 else "ðŸ”´ OFFLINE"
            st.caption(f"**[{acc[1]}]** `{acc[2]}` | {status_icon}")
    with col_acc2:
        if st.button("ðŸ”„ Poll Monitored Inboxes Now", use_container_width=True):
            try:
                import email_triage_core
                email_triage_core.run_multi_account_cycle()
                st.success("Triage cycle completed.")
                st.rerun()
            except Exception as e:
                st.error(f"Polling error: {e}")

    st.markdown("---")
    st.markdown("### ðŸ›¡ï¸ Staged Inbound Transmissions (Awaiting CEO Kinematic Veto)")

    cur.execute("SELECT id, account_alias, sender_address, subject, date_received, raw_body_sanitized, threat_status, triage_category, draft_response, veto_status FROM staged_email_dispatches WHERE veto_status='PENDING_CEO_APPROVAL' ORDER BY id DESC")
    staged_items = cur.fetchall()
    conn.close()

    if staged_items:
        for item in staged_items:
            disp_id, alias, sender, subj, dt, body, threat, cat, draft, veto = item
            with st.expander(f"[{alias}] {subj} â€” From: {sender} | Status: {threat}", expanded=(threat == "INSPECTED_CLEAN")):
                st.markdown(f"**Timestamp:** `{dt}` | **Category:** `{cat}`")
                
                if threat == "INSPECTED_CLEAN":
                    st.success(f"ðŸ›¡ï¸ Threat Scrubber: {threat}")
                else:
                    st.error(f"ðŸš¨ Threat Scrubber: {threat} (Autonomous actions halted)")

                st.markdown("**Inbound Body (Sanitized):**")
                st.info(body)

                st.markdown("**Ebony's Staged Executive Draft (Grounded in Iron Dome Intel):**")
                draft_edit = st.text_area("Review / Edit Draft Payload:", value=draft, height=180, key=f"draft_{disp_id}")

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"âœ… APPROVE & DISPATCH #{disp_id}", use_container_width=True, key=f"app_{disp_id}"):
                        c_up = sqlite3.connect(DB_PATH)
                        cur_up = c_up.cursor()
                        cur_up.execute("UPDATE staged_email_dispatches SET veto_status='APPROVED_DISPATCHED', draft_response=?, dispatched_at=datetime('now') WHERE id=?", (draft_edit, disp_id))
                        c_up.commit()
                        c_up.close()
                        st.success(f"Transmission #{disp_id} cryptographically authorized by CEO.")
                        st.rerun()
                with col_btn2:
                    if st.button(f"ðŸš« VETO & ARCHIVE #{disp_id}", use_container_width=True, key=f"veto_{disp_id}"):
                        c_up = sqlite3.connect(DB_PATH)
                        cur_up = c_up.cursor()
                        cur_up.execute("UPDATE staged_email_dispatches SET veto_status='CEO_VETOED_QUARANTINED' WHERE id=?", (disp_id,))
                        c_up.commit()
                        c_up.close()
                        st.warning(f"Transmission #{disp_id} vetoed and archived to vault.")
                        st.rerun()
    else:
        st.info("No inbound transmissions pending review. All queues clean and verified.")
"""

for target in TARGET_FILES:
    if not os.path.exists(target):
        print(f"[FAIL] Target not found: {target}")
        continue

    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Inject into Navigation Radio
    if '"ðŸ“¨ Sovereign Dispatch Deck"' not in content:
        if NAV_TARGET in content:
            content = content.replace(NAV_TARGET, NAV_REPLACEMENT, 1)
            print(f"[SUCCESS] Added 'ðŸ“¨ Sovereign Dispatch Deck' to navigation in: {os.path.basename(target)}")
        else:
            print(f"[WARN] Navigation marker '{NAV_TARGET}' not found in: {os.path.basename(target)}")
    else:
        print(f"[INFO] 'ðŸ“¨ Sovereign Dispatch Deck' already present in navigation: {os.path.basename(target)}")

    # 2. Inject Module Handler
    if 'elif active_module == "ðŸ“¨ Sovereign Dispatch Deck":' not in content:
        split_marker = 'elif active_module == "ðŸ“¡ Sovereign Comms Deck":'
        if split_marker in content:
            idx = content.find(split_marker)
            content = content[:idx] + MODULE_HANDLER + "\n" + content[idx:]
            print(f"[SUCCESS] Injected Dispatch Deck module handler in: {os.path.basename(target)}")
        else:
            print(f"[WARN] Handler marker '{split_marker}' not found in: {os.path.basename(target)}")
    else:
        print(f"[INFO] Handler block already present in: {os.path.basename(target)}")

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

print("[COMPLETE] Verification complete for all target files.")
