import os
import sys

# ==============================================================================
# HVF Omni-Industrial Matrix | DYNAMIC CREDENTIAL UI INJECTOR
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Inject Dynamic Email Onboarding & Credential Manager into Console
# ==============================================================================

TARGET_FILES = [
    r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console.py",
    r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console_GREEN.py"
]

OLD_MODULE_START = 'elif active_module == "ðŸ“¨ Sovereign Dispatch Deck":'

NEW_MODULE_BODY = """elif active_module == "ðŸ“¨ Sovereign Dispatch Deck":
    st.subheader("ðŸ“¨ Sovereign Multi-Account Dispatch & Inbound Triage Deck")
    st.caption("Zero-Trust Inbound Adversarial Scrubber & CEO Kinematic Veto Approval Pipeline")

    import sqlite3
    import email_triage_core

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, account_alias, email_address, imap_server, imap_port, smtp_server, smtp_port, is_active, encrypted_password FROM email_accounts")
    monitored_accs = cur.fetchall()

    # --- IN-APP ACCOUNT & CREDENTIAL MANAGER ---
    with st.expander("âš™ï¸ IN-APP EMAIL ACCOUNT & CREDENTIAL MANAGER (Add / Edit Inboxes)", expanded=False):
        st.caption("Securely add or modify email endpoints. Passwords are encrypted at-rest using the sovereign Fernet vault key.")
        
        tab_acc1, tab_acc2 = st.tabs(["âž• Add New Inbox", "ðŸ“‹ Manage Configured Inboxes"])
        
        with tab_acc1:
            with st.form("add_account_form", clear_on_submit=True):
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    new_alias = st.text_input("Account Alias / Label:", placeholder="e.g., HVF_GMAIL_MAIN")
                    new_email = st.text_input("Email Address:", placeholder="e.g., humphreyvirtualfarm@gmail.com")
                    new_pwd = st.text_input("App Password / Token:", type="password", placeholder="Enter 16-character App Password")
                with col_f2:
                    new_imap_srv = st.text_input("IMAP Server:", value="imap.gmail.com")
                    new_imap_prt = st.number_input("IMAP Port:", value=993)
                    new_smtp_srv = st.text_input("SMTP Server:", value="smtp.gmail.com")
                    new_smtp_prt = st.number_input("SMTP Port:", value=465)

                btn_test_save = st.form_submit_button("ðŸ”’ TEST CONNECTION & SAVE INBOX", use_container_width=True)

                if btn_test_save:
                    if not new_alias or not new_email or not new_pwd:
                        st.error("Alias, Email Address, and App Password are required.")
                    else:
                        with st.spinner("Testing TLS/SSL connection to IMAP server..."):
                            success, msg = email_triage_core.test_imap_connection(new_email, new_pwd, new_imap_srv, int(new_imap_prt))
                        if success:
                            enc_pass = email_triage_core.encrypt_credential(new_pwd)
                            c_in = sqlite3.connect(DB_PATH)
                            cur_in = c_in.cursor()
                            cur_in.execute(\"\"\"
                            INSERT OR REPLACE INTO email_accounts 
                            (account_alias, email_address, imap_server, imap_port, smtp_server, smtp_port, env_password_key, encrypted_password, is_active)
                            VALUES (?, ?, ?, ?, ?, ?, 'DYNAMIC_VAULT_ENCRYPTED', ?, 1)
                            \"\"\", (new_alias.strip().upper(), new_email.strip(), new_imap_srv.strip(), int(new_imap_prt), new_smtp_srv.strip(), int(new_smtp_prt), enc_pass))
                            c_in.commit()
                            c_in.close()
                            st.success(f"Verified & Saved inbox [{new_alias.upper()}]. Encrypted at rest.")
                            st.rerun()
                        else:
                            st.error(f"Connection Failed: {msg}")

        with tab_acc2:
            if monitored_accs:
                for acc in monitored_accs:
                    a_id, a_alias, a_email, a_srv, a_prt, _, _, a_act, a_enc = acc
                    c_info, c_toggle, c_del = st.columns([3, 1, 1])
                    with c_info:
                        pass_indicator = "ðŸŸ¢ Key Encrypted" if a_enc else "ðŸŸ¡ No Password Stored"
                        st.markdown(f"**[{a_alias}]** `{a_email}` ({a_srv}:{a_prt}) â€” {pass_indicator}")
                    with c_toggle:
                        toggle_lbl = "Deactivate" if a_act == 1 else "Activate"
                        if st.button(toggle_lbl, key=f"tgl_{a_id}", use_container_width=True):
                            new_st = 0 if a_act == 1 else 1
                            c_up = sqlite3.connect(DB_PATH)
                            cur_up = c_up.cursor()
                            cur_up.execute("UPDATE email_accounts SET is_active = ? WHERE id = ?", (new_st, a_id))
                            c_up.commit()
                            c_up.close()
                            st.rerun()
                    with c_del:
                        if st.button("Delete", key=f"del_{a_id}", use_container_width=True):
                            c_del_db = sqlite3.connect(DB_PATH)
                            cur_del = c_del_db.cursor()
                            cur_del.execute("DELETE FROM email_accounts WHERE id = ?", (a_id,))
                            c_del_db.commit()
                            c_del_db.close()
                            st.rerun()
            else:
                st.info("No inboxes configured. Add your first inbox above.")

    # --- TOP CONTROLS & MONITOR STATUS ---
    col_acc1, col_acc2 = st.columns([2, 1])
    with col_acc1:
        st.markdown("#### ðŸ“¬ Active Monitored Inboxes")
        for acc in monitored_accs:
            if acc[7] == 1:
                st.caption(f"**[{acc[1]}]** `{acc[2]}` | ðŸŸ¢ ACTIVE")
    with col_acc2:
        if st.button("ðŸ”„ Poll Monitored Inboxes Now", use_container_width=True):
            try:
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

print("=" * 80)
print("INJECTING IN-APP CREDENTIAL MANAGER INTO CONSOLE HUD")
print("=" * 80)

for target in TARGET_FILES:
    if not os.path.exists(target):
        continue
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    next_marker = 'elif active_module == "ðŸ“¡ Sovereign Comms Deck":'
    if OLD_MODULE_START in content and next_marker in content:
        start_idx = content.find(OLD_MODULE_START)
        end_idx = content.find(next_marker)
        content = content[:start_idx] + NEW_MODULE_BODY + "\n" + content[end_idx:]
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[SUCCESS] Injected Dynamic Credential Manager into: {os.path.basename(target)}")
    else:
        print(f"[WARN] Marker boundaries not found in: {os.path.basename(target)}")

print("=" * 80)
print("INJECTION COMPLETE")
print("=" * 80)
