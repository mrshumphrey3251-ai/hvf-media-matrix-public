import os
import sys
import sqlite3
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

print("=" * 80)
print("1. EXECUTING NOISE SWEEP ON DATABASE VAULT")
print("=" * 80)

# Sweep commercial newsletters, explicitly protecting subcontractor / compliance mail
try:
    conn = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
    cur = conn.cursor()
    cur.execute("""
    UPDATE staged_email_dispatches 
    SET veto_status = 'ARCHIVED_NOISE' 
    WHERE veto_status = 'PENDING_CEO_APPROVAL'
      AND (
          sender_address LIKE '%newsletters-noreply%'
          OR sender_address LIKE '%zapier%'
          OR sender_address LIKE '%instagram%'
          OR sender_address LIKE '%nvidia%'
          OR sender_address LIKE '%hit-reply@linkedin.com%'
          OR sender_address LIKE '%editors-noreply@linkedin.com%'
      )
      AND subject NOT LIKE '%Signallink%'
      AND triage_category NOT IN ('SUBCONTRACTOR_SIGNALLINK', 'LEGAL_COMPLIANCE_EXECUTION', 'DEFENSE_PRIME_CONTRACTING');
    """)
    swept_count = cur.rowcount
    
    cur.execute("SELECT id, sender_address, subject, triage_category FROM staged_email_dispatches WHERE veto_status = 'PENDING_CEO_APPROVAL'")
    active_rows = cur.fetchall()
    conn.close()
    
    print(f"[SUCCESS] Archived {swept_count} commercial newsletter records into storage.")
    print(f"[SUCCESS] Active high-value transmissions remaining in queue: {len(active_rows)}")
    for r in active_rows:
        print(f"  * #{r[0]} [{r[3]}] From: {r[1]} | Subject: {r[2]}")
except Exception as e:
    print(f"[FAIL] Database sweep error: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("2. DEPLOYING COMPLETE SOVEREIGN DISPATCH SECTION TO CONSOLES")
print("=" * 80)

NEW_DISPATCH_DECK_CODE = '''    st.header("📨 Sovereign Multi-Account Dispatch & Inbound Triage Deck")
    st.markdown("Zero-Trust Inbound Adversarial Scrubber & CEO Kinematic Veto Approval Pipeline")

    # --- SECTION 1: OUTBOUND COMPOSITION TERMINAL ---
    with st.expander("✍️ COMPOSE SOVEREIGN OUTBOUND TRANSMISSION (DIRECT DISPATCH)", expanded=False):
        st.markdown("<div style='color: #e2a03f; font-family: monospace; font-size: 0.95em; font-weight: bold; margin-bottom: 8px;'>DIRECT EXECUTIVE STRIKE TRANSMISSION // CAGE: 1AHA8</div>", unsafe_allow_html=True)
        
        comp_c1, comp_c2 = st.columns([2, 1])
        with comp_c1:
            out_to = st.text_input("Destination Recipient (RFC822 Email Address)", key="out_to_dest", placeholder="e.g. contracts@signallink.com")
            out_subject = st.text_input("Transmission Subject Line", key="out_subj_line", placeholder="e.g. Subcontractor LSA Execution Verification // DAF TENCAP Vol 2")
        with comp_c2:
            out_category = st.selectbox("Classification Category", [
                "DEFENSE_PRIME_CONTRACTING",
                "SUBCONTRACTOR_SIGNALLINK",
                "LEGAL_COMPLIANCE_EXECUTION",
                "FINANCIAL_TREASURY",
                "GENERAL_EXECUTIVE"
            ], key="out_cat_sel")
            st.markdown("<div style='font-size:0.85em; color:#94a3b8; margin-top:5px;'><b>Originating Endpoint:</b><br><span style='color:#e2a03f; font-family:monospace;'>humphreyvirtualfarm@gmail.com</span></div>", unsafe_allow_html=True)

        # AI Executive Draft Assistant
        with st.expander("⚡ Draft Assistance with Ebony AI (Grounded in Iron Dome Intel)", expanded=False):
            ai_directive = st.text_input("Strategic Directive for Ebony AI", placeholder="e.g. Request confirmation of executed LSA from Drew Phillips Jr. and set DAF TENCAP Volume 2 delivery date.")
            if st.button("⚡ Generate Authoritative Draft", key="btn_gen_ai_outbound"):
                if ai_directive:
                    with st.spinner("Retrieving Iron Dome intelligence and composing draft..."):
                        draft_ai = email_triage_core.generate_direct_draft_assistance(out_to, ai_directive)
                        st.session_state["out_body_buffer"] = draft_ai
                        st.rerun()
                else:
                    st.warning("Please specify an objective for Ebony AI.")

        default_out_body = st.session_state.get("out_body_buffer", "")
        out_body_val = st.text_area("Transmission Payload (Strict RFC5322 Plain Text)", value=default_out_body, height=200, key="out_body_val_key")

        col_snd1, col_snd2 = st.columns([1.5, 2])
        with col_snd1:
            if st.button("🚀 Authorize & Dispatch Transmission", key="btn_send_direct_out", type="primary"):
                if not out_to or not out_subject or not out_body_val:
                    st.error("Recipient, Subject, and Body are mandatory.")
                else:
                    with st.spinner("Connecting to smtp.gmail.com:465 & dispatching transmission..."):
                        s_ok, s_msg = email_triage_core.send_direct_outbound_email(
                            to_addr=out_to,
                            subject=out_subject,
                            body=out_body_val,
                            account_alias="HVF_PRIMARY_EXECUTIVE",
                            category=out_category
                        )
                    if s_ok:
                        st.success(f"🚀 {s_msg}")
                        st.session_state["out_body_buffer"] = ""
                        st.rerun()
                    else:
                        st.error(f"Delivery failed: {s_msg}")
        with col_snd2:
            if st.button("Clear Buffer", key="btn_clr_out_buff"):
                st.session_state["out_body_buffer"] = ""
                st.rerun()

    st.markdown("<hr style='border: 1px solid #242d3d; margin: 15px 0;'>", unsafe_allow_html=True)

    # --- SECTION 2: INBOX POLL CONTROLS & TELEMETRY ---
    poll_c1, poll_c2 = st.columns([2, 1])
    with poll_c1:
        if st.button("🔄 Poll Monitored Inboxes Now", key="btn_poll_inboxes_cockpit"):
            with st.spinner("Connecting to imap.gmail.com:993 & staging new messages..."):
                email_triage_core.run_multi_account_cycle()
            st.success("Polling cycle complete.")
            st.rerun()
    with poll_c2:
        if st.button("🧹 Purge Commercial Noise", key="btn_purge_noise_now"):
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
            st.info("Commercial newsletters archived.")
            st.rerun()

    # --- SECTION 3: FOCUSED SINGLE-TRANSMISSION C2 COCKPIT ---
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
                <div style='color: #94a3b8; font-size: 0.85em; margin-top: 6px;'>Queue is completely clear. Incoming transmissions will be staged at eye level.</div>
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
                key=f"eye_level_draft_{disp_id}"
            )

        col_act1, col_act2, col_act3 = st.columns([1.2, 1, 1.2])
        with col_act1:
            if st.button("✅ Approve & Dispatch", key=f"btn_act_app_{disp_id}", type="secondary"):
                with st.spinner("Connecting to smtp.gmail.com:465 & dispatching transmission..."):
                    d_ok, d_msg = email_triage_core.dispatch_outbound_transmission(disp_id, updated_draft)
                if d_ok:
                    st.success(f"🚀 {d_msg}")
                else:
                    st.error(f"Delivery failed: {d_msg}")
                st.rerun()

        with col_act2:
            if st.button("❌ Dismiss Record", key=f"btn_act_dis_{disp_id}"):
                c_act = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                cur_act = c_act.cursor()
                cur_act.execute("UPDATE staged_email_dispatches SET veto_status = 'DISMISSED_BY_CEO' WHERE id = ?", (disp_id,))
                c_act.close()
                st.info(f"Transmission #{disp_id} dismissed. Advancing queue.")
                st.rerun()

        with col_act3:
            if st.button("🚫 Block Sender", key=f"btn_act_blk_{disp_id}", type="primary"):
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

    # Anchor to start of Sovereign Dispatch Deck
    deck_start_anchor = 'st.header("📨 Sovereign Multi-Account Dispatch & Inbound Triage Deck")'
    if deck_start_anchor not in content:
        deck_start_anchor = 'st.header("📨 Sovereign Dispatch & Inbound Triage Deck")'

    # Anchor to end of Sovereign Dispatch Deck
    deck_end_anchor = 'elif active_module =='
    if deck_end_anchor not in content:
        deck_end_anchor = 'with col_side:'

    idx_start = content.find(deck_start_anchor)
    idx_end = content.find(deck_end_anchor, idx_start) if idx_start != -1 else -1

    if idx_start != -1 and idx_end != -1:
        new_content = content[:idx_start] + NEW_DISPATCH_DECK_CODE.strip() + "\n\n    " + content[idx_end:]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Injected Compose & Single-Item Stepper into {os.path.basename(fpath)}.")
    else:
        print(f"  * [FAIL] Could not match boundary anchors ({idx_start}, {idx_end}) in {os.path.basename(fpath)}.")

print("\n" + "=" * 80)
print("DECK ARCHITECTURE UPGRADE COMPLETE")
print("=" * 80)
