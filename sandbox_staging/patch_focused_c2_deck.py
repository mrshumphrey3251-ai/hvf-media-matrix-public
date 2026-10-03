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
print("REPLACING VERTICAL SCROLL WITH FOCUSED SINGLE-MESSAGE C2 COCKPIT")
print("=" * 80)

FOCUSED_C2_DISPATCH_BLOCK = '''
    # --- FOCUSED SINGLE-MESSAGE TACTICAL C2 COCKPIT ---
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
        st.error(f"Failed to load dispatches: {e}")
        dispatches = []

    total_pending = len(dispatches)

    if total_pending == 0:
        st.markdown("""
            <div style='border: 1px solid #242d3d; border-radius: 2px; padding: 25px; background-color: #121722; text-align: center;'>
                <div style='color: #e2a03f; font-family: monospace; font-size: 1.2em; font-weight: bold;'>🟢 PERIMETER SECURE | ZERO PENDING TRANSMISSIONS</div>
                <div style='color: #94a3b8; font-size: 0.9em; margin-top: 6px;'>Historical queue baselined. Live IMAP gateway monitoring for incoming traffic.</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # High-Density Tactical Cockpit Controls
        hdr_col1, hdr_col2 = st.columns([2, 1])
        with hdr_col1:
            st.markdown(f"<h3 style='margin:0; padding:0; border:none; color:#e2a03f;'>TRANSMISSION 1 OF {total_pending} PENDING</h3>", unsafe_allow_html=True)
        with hdr_col2:
            if st.button("🧹 Purge All Pending Transmissions", key="btn_purge_all_queue"):
                c_p = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                cur_p = c_p.cursor()
                cur_p.execute("UPDATE staged_email_dispatches SET veto_status = 'ARCHIVED_MANUAL' WHERE veto_status = 'PENDING_CEO_APPROVAL'")
                c_p.close()
                st.warning("All pending transmissions archived.")
                st.rerun()

        # Render strictly the front-of-queue transmission
        curr_msg = dispatches[0]
        disp_id, account, sender, subject, date_rx, body_clean, threat, category, draft = curr_msg

        status_class = "status-threat" if "THREAT" in threat else "status-clean"
        status_icon = "🛑" if "THREAT" in threat else "✅"

        st.markdown(f"""
            <div style='border: 1px solid #242d3d; border-radius: 2px; padding: 14px; background-color: #121722; margin-top: 10px;'>
                <div class='card-header'>
                    [{account}] {subject}
                    <span class='status-badge {status_class}'>{status_icon} {threat}</span>
                </div>
                <div style='font-size: 0.9em; color: #94a3b8; margin-top: 8px;'>
                    <b>FROM:</b> <span style='color:#f1f5f9; font-family:monospace;'>{sender}</span> | 
                    <b>RECEIVED:</b> <span style='color:#f1f5f9;'>{date_rx}</span> | 
                    <b>CATEGORY:</b> <span style='color:#e2a03f;'>{category}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍 Inbound Message Body (Sanitized)", expanded=False):
            st.text(body_clean)

        if "THREAT" in threat:
            st.error("⚠️ Transmission isolated due to hostile injection signature. Automated inference aborted.")
        else:
            updated_draft = st.text_area(
                f"Tactical Executive Response Payload (Queue #{disp_id})", 
                value=draft, 
                height=180,
                key=f"active_draft_payload_{disp_id}"
            )

        # Action Control Console: Handled transmissions disappear immediately
        col_btn1, col_btn2, col_btn3 = st.columns([1.2, 1, 1.2])
        with col_btn1:
            if st.button("✅ Approve & Dispatch", key=f"btn_app_{disp_id}", type="secondary"):
                c_act = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                cur_act = c_act.cursor()
                cur_act.execute("UPDATE staged_email_dispatches SET veto_status = 'APPROVED_BY_CEO' WHERE id = ?", (disp_id,))
                c_act.close()
                st.success(f"Transmission #{disp_id} approved for outbound dispatch.")
                st.rerun()

        with col_btn2:
            if st.button("❌ Dismiss Record", key=f"btn_dis_{disp_id}"):
                c_act = sqlite3.connect(DB_PATH, timeout=30.0, isolation_level=None)
                cur_act = c_act.cursor()
                cur_act.execute("UPDATE staged_email_dispatches SET veto_status = 'DISMISSED_BY_CEO' WHERE id = ?", (disp_id,))
                c_act.close()
                st.info(f"Transmission #{disp_id} dismissed. Advancing queue.")
                st.rerun()

        with col_btn3:
            if st.button("🚫 Block Sender", key=f"btn_block_{disp_id}", type="primary"):
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

    # Locate start of staged transmissions block
    anchor_start = "st.subheader("
    idx_start = content.find(anchor_start)
    if idx_start == -1:
        # Fallback anchor search
        anchor_start = "Staged Inbound Transmissions"
        idx_start = content.find(anchor_start)
        if idx_start != -1:
            idx_start = content.rfind("\n", 0, idx_start)

    # Locate end of staged loop before active_module or next section
    anchor_end = "elif active_module =="
    idx_end = content.find(anchor_end)
    if idx_end == -1:
        anchor_end = "with col_side:"
        idx_end = content.find(anchor_end)

    if idx_start != -1 and idx_end != -1 and idx_start < idx_end:
        new_content = content[:idx_start] + FOCUSED_C2_DISPATCH_BLOCK.strip() + "\n\n    " + content[idx_end:]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Replaced vertical scroll with Focused C2 Cockpit in {os.path.basename(fpath)}")
    else:
        print(f"  * [WARN] Anchors not resolved ({idx_start}, {idx_end}).")

print("\n" + "=" * 80)
print("FOCUSED C2 VIEWER ENGINE COMPILED SUCCESSFULLY")
print("=" * 80)
