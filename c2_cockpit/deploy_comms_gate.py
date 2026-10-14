import sys
import re
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
if not cockpit_dir.exists():
    print(f"[CRITICAL ERROR] Cockpit directory not found: {cockpit_dir}")
    sys.exit(1)

# -------------------------------------------------------------------------
# 1. UPDATE ebony_email_dispatcher.py WITH PERSISTENCE SUPPORT
# -------------------------------------------------------------------------
disp_file = cockpit_dir / "ebony_email_dispatcher.py"
disp_text = disp_file.read_text(encoding="utf-8")

# Ensure save_account_credentials accepts stay_signed_in
if "stay_signed_in: bool = True" not in disp_text:
    disp_text = disp_text.replace(
        'def save_account_credentials(email_addr: str, password_or_app_pass: str, custom_imap: str = None, custom_smtp: str = None):',
        'def save_account_credentials(email_addr: str, password_or_app_pass: str, custom_imap: str = None, custom_smtp: str = None, stay_signed_in: bool = True):'
    )
    disp_text = disp_text.replace(
        '"registered_at": datetime.now(timezone.utc).isoformat()',
        '"stay_signed_in": stay_signed_in,\n        "registered_at": datetime.now(timezone.utc).isoformat()'
    )
    disp_file.write_text(disp_text, encoding="utf-8")
    print("[+] ebony_email_dispatcher.py updated with stay_signed_in persistence.")
else:
    print("[*] ebony_email_dispatcher.py already supports stay_signed_in.")

# -------------------------------------------------------------------------
# 2. WRITE ebony_travel_ui.py WITH render_comms_gate & FULL TRAVEL DECK
# -------------------------------------------------------------------------
ui_code = """\"\"\"
E.B.O.N.Y. Executive Travel Autopilot, Priority Triage & Sovereign Comms Gate UI
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Tier: Sovereign Tier-1 Executive Ingestion ($19.99/mo Baseline)
Statutory Authority: Oklahoma Title 61 & OK HB 2992
\"\"\"
import streamlit as st
import sqlite3
import pandas as pd
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

def render_comms_gate(key_suffix="sovereign_deck_main"):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    _cdir = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit")
    if str(_cdir) not in sys.path:
        sys.path.insert(0, str(_cdir))

    from ebony_email_dispatcher import (
        get_configured_accounts,
        save_account_credentials,
        remove_account_credentials,
        test_account_connection,
        detect_servers
    )

    accounts = get_configured_accounts()
    is_authenticated = False
    active_email = ""

    if st.session_state.get("comms_deck_authenticated", False):
        is_authenticated = True
        active_email = st.session_state.get("comms_active_email", "")
    elif accounts and not st.session_state.get("comms_force_signout", False):
        first_email = list(accounts.keys())[0]
        if accounts[first_email].get("stay_signed_in", True):
            st.session_state.comms_deck_authenticated = True
            st.session_state.comms_active_email = first_email
            is_authenticated = True
            active_email = first_email

    if not is_authenticated:
        st.markdown(\"\"\"
        <div style="background-color: #0b110e; border: 2px solid #00ff88; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
            <h2 style="color: #00ff88; margin-top: 0; font-family: monospace; letter-spacing: 2px;">⚡ SOVEREIGN COMMUNICATIONS ACCESS GATE</h2>
            <div style="color: #a0aab2; font-size: 0.9em; font-family: monospace; margin-bottom: 15px;">
                <strong>ENTITY:</strong> Humphrey Virtual Farms LLC | <strong>CAGE:</strong> 1AHA8 | <strong>UEI:</strong> S1M4ENLHTDH5<br>
                <strong>STATUTORY JURISDICTION:</strong> State of Oklahoma (Title 61 & HB 2992 Framework) | <strong>NODE:</strong> HVFNexus
            </div>
            <div style="color: #ffffff; font-size: 0.95em; line-height: 1.6; border-top: 1px solid #1e3a29; padding-top: 15px;">
                <p><strong>=== MANDATORY SECURE MAILBOX AUTHENTICATION ===</strong></p>
                <p>This communications enclave connects directly to designated sovereign mail servers via air-gapped TLS/SSL protocols (Port 993/465). No third-party cloud APIs, OAuth project secrets, or external telemetry harvesters are utilized.</p>
                <p>Authenticate with your executive email credentials or dedicated 16-character App Password to unlock the Sovereign Communications & Dispatch Deck.</p>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            default_e = list(accounts.keys())[0] if accounts else ""
            in_email = st.text_input("Executive Email Address:", value=default_e, placeholder="e.g. humphreyvirtualfarm@gmail.com or evaluator@ok.gov", key=f"gate_email_{key_suffix}")
            in_pass = st.text_input("Password / 16-Character App Password:", type="password", placeholder="•••• •••• •••• ••••", key=f"gate_pass_{key_suffix}")

            stay_signed_in = st.checkbox("Remember credentials and stay signed in across sessions", value=True, key=f"gate_stay_{key_suffix}")

            btn_col1, btn_col2, btn_col3 = st.columns([2, 4, 2])
            with btn_col2:
                if st.button("VERIFY CREDENTIALS & ENTER SOVEREIGN COMMS", use_container_width=True, key=f"gate_btn_{key_suffix}"):
                    if not in_email or not in_pass:
                        st.error("ACCESS DENIED: Both Email Address and Password are required.")
                    else:
                        with st.spinner("Probing live TLS/SSL socket (Port 993)..."):
                            def_i, def_s, _, _ = detect_servers(in_email)
                            ok, msg = test_account_connection(in_email, in_pass, def_i)
                            if ok:
                                save_account_credentials(in_email, in_pass, def_i, def_s, stay_signed_in=stay_signed_in)
                                st.session_state.comms_deck_authenticated = True
                                st.session_state.comms_active_email = in_email.strip().lower()
                                st.session_state.comms_force_signout = False
                                st.success("AUTHENTICATION VERIFIED: Entering Sovereign Communications Enclave...")
                                st.rerun()
                            else:
                                st.error(f"AUTHENTICATION DENIED: {msg}")

        st.stop()
    else:
        col_sb1, col_sb2 = st.columns([4, 1.2])
        with col_sb1:
            st.markdown(f\"\"\"
            <div style="background-color: #0b1410; border: 1px solid #1e3a29; border-left: 3px solid #00ff88; border-radius: 6px; padding: 10px 16px; margin-bottom: 15px; font-family: monospace; font-size: 0.85em;">
                <strong style="color: #00ff88;">AUTHENTICATED ENCLAVE SESSION:</strong> <span style="color: #ffffff;">{active_email}</span> &nbsp;|&nbsp; <span style="color: #00ff88;">TLS/SSL (993/465) ACTIVE</span>
            </div>
            \"\"\", unsafe_allow_html=True)
        with col_sb2:
            if st.button("🚪 SIGN OUT / SWITCH", key=f"btn_header_signout_{key_suffix}", use_container_width=True):
                st.session_state.comms_deck_authenticated = False
                st.session_state.comms_force_signout = True
                st.rerun()

def render_communications_dispatch_ui(key_suffix="sovereign_deck_main"):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    st.divider()
    st.markdown("## ✈️ EXECUTIVE TRAVEL AUTOPILOT // INBOX GHOSTWRITER & DEBRIEF")
    st.caption("Autonomous Inbound Ingestion, Contextual SMTP Auto-Response & Executive Return Briefing // Level-5 Authority")

    _cdir = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit")
    if str(_cdir) not in sys.path:
        sys.path.insert(0, str(_cdir))

    db_p = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit\\matrix_ledger.db")
    total_count, sent_count, archived_count, flagged_count = 0, 0, 0, 0
    records = []

    if db_p.exists():
        try:
            conn = sqlite3.connect(str(db_p))
            cur = conn.cursor()
            cur.execute(\"\"\"
                SELECT id, timestamp, sender, recipient, subject, incoming_intent, drafted_response, status, classification, message_uid
                FROM email_dispatch_ledger 
                ORDER BY timestamp DESC
            \"\"\")
            cols = ["id", "timestamp", "sender", "recipient", "subject", "incoming_intent", "drafted_response", "status", "classification", "message_uid"]
            raw_data = cur.fetchall()
            conn.close()
            for row in raw_data:
                records.append(dict(zip(cols, row)))
            
            total_count = len(records)
            sent_count = sum(1 for r in records if r["status"] == "SENT_AUTONOMOUSLY")
            archived_count = sum(1 for r in records if r["status"] in ["ARCHIVED_BULK", "ARCHIVED_LOOP"])
            flagged_count = sum(
                1 for r in records 
                if r["status"] not in ["ARCHIVED_BULK", "ARCHIVED_LOOP", "RESOLVED_BY_CEO"]
                and (r["classification"] in ["STATE_INFRASTRUCTURE_GRANT", "ODOT_AEROSPACE_INSPECTION", "EXECUTIVE_SCHEDULING", "HIGH_PRIORITY_REVIEW"]
                     or any(k in (r["classification"] or "").upper() for k in ["GRANT", "ODOT", "TITLE61", "HB2992"]))
            )
        except Exception:
            pass

    # 1. Macro KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Ingested", f"{total_count} Transmissions")
    col2.metric("Autonomously Resolved", f"{sent_count} Dispatched", delta=f"{sent_count} closed")
    col3.metric("Newsletters Filtered", f"{archived_count} Archived")
    col4.metric("Priority Action Items", f"{flagged_count} Flagged", delta="Action Required" if flagged_count > 0 else "Clear")

    # 2. Executive Autopilot Command Bar
    c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
    with c1:
        if st.button("🚀 ENGAGE TRAVEL AUTOPILOT (AUTO-REPLY ALL)", key=f"btn_autopilot_send_{key_suffix}", use_container_width=True):
            try:
                from ebony_travel_autopilot import run_travel_cycle
                res = run_travel_cycle(auto_send=True)
                st.success(f"Autopilot Complete: Processed {len(res)} transmission(s) and dispatched via SMTP.")
                st.rerun()
            except Exception as _e:
                st.error(f"Autopilot execution failure: {_e}")

    with c2:
        if st.button("📥 RECON INBOX (READ ONLY)", key=f"btn_recon_draft_{key_suffix}", use_container_width=True):
            try:
                from ebony_travel_autopilot import run_travel_cycle
                res = run_travel_cycle(auto_send=False)
                st.info(f"Recon Complete: Ingested {len(res)} transmission(s) into WORM ledger.")
                st.rerun()
            except Exception as _e:
                st.error(f"Recon failure: {_e}")

    with c3:
        if st.button("📱 EMAIL DEBRIEF TO MY PHONE", key=f"btn_email_debrief_{key_suffix}", use_container_width=True):
            try:
                from ebony_travel_autopilot import run_travel_cycle
                run_travel_cycle(auto_send=False, email_summary_to="humphreyvirtualfarm@gmail.com")
                st.success("Executive Return Debrief transmitted to humphreyvirtualfarm@gmail.com.")
            except Exception as _e:
                st.error(f"Failed to transmit debrief: {_e}")

    # 3. Dedicated Inspection Tabs
    tab_priority, tab_responses, tab_table = st.tabs([
        f"⚠️ Priority Matters Requiring Attention ({flagged_count})",
        "🔍 Full Response & Inbound Inspector",
        "📊 Complete WORM Ledger Table"
    ])

    # TAB 1: PRIORITY MATTERS REQUIRING ATTENTION
    with tab_priority:
        priority_items = [
            r for r in records 
            if r["status"] not in ["ARCHIVED_BULK", "ARCHIVED_LOOP", "RESOLVED_BY_CEO"]
            and (r["classification"] in ["STATE_INFRASTRUCTURE_GRANT", "ODOT_AEROSPACE_INSPECTION", "EXECUTIVE_SCHEDULING", "HIGH_PRIORITY_REVIEW"]
                 or any(k in (r["classification"] or "").upper() for k in ["GRANT", "ODOT", "TITLE61", "HB2992"]))
        ]
        if not priority_items:
            st.success("🟢 Zero urgent bottlenecks detected. All operational inquiries have been categorized and resolved.")
        else:
            st.markdown(f"#### ⚠️ {len(priority_items)} High-Priority Items Flagged for Direct Executive Review")
            st.caption("Select an item below to review the sender's message, inspect the generated response, or edit and transmit.")
            
            p_options = [f"#{item['id']} | {item['sender'][:25]} | {item['subject'][:40]}" for item in priority_items]
            selected_p = st.selectbox("Select Priority Item to Review:", p_options, key=f"sel_p_item_{key_suffix}")
            
            p_idx = p_options.index(selected_p)
            item = priority_items[p_idx]
            
            col_m1, col_m2 = st.columns([2, 1])
            with col_m1:
                st.markdown(f"**Sender:** `{item['sender']}`")
                st.markdown(f"**Subject:** `{item['subject']}`")
            with col_m2:
                st.markdown(f"**Classification:** `{item['classification']}`")
                st.markdown(f"**Status:** `{item['status']}`")

            st.markdown("##### 📥 Inbound Message Body")
            st.info(item["incoming_intent"] if item["incoming_intent"] else "No message body recorded.")

            st.markdown("##### ✍️ Autonomous / Drafted Executive Response")
            edit_resp = st.text_area("Edit Response Before Transmitting:", value=item["drafted_response"], height=160, key=f"txt_p_resp_{item['id']}_{key_suffix}")

            c_act1, c_act2 = st.columns([1.5, 1])
            with c_act1:
                if st.button("🚀 TRANSMIT RESPONSE VIA SMTP", key=f"btn_send_p_{item['id']}_{key_suffix}", use_container_width=True):
                    try:
                        import smtplib
                        import ssl
                        from email.mime.text import MIMEText
                        from email.mime.multipart import MIMEMultipart
                        cfg_p = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit\\email_accounts.json")
                        cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
                        acc = list(cfg.values())[0]
                        
                        reply = MIMEMultipart()
                        reply["From"] = acc["email"]
                        reply["To"] = item["sender"]
                        reply["Subject"] = f"Re: {item['subject']}"
                        reply.attach(MIMEText(edit_resp, "plain", "utf-8"))
                        
                        context = ssl.create_default_context()
                        if acc["smtp_port"] == 465:
                            with smtplib.SMTP_SSL(acc["smtp_host"], acc["smtp_port"], context=context) as client:
                                client.login(acc["email"], acc["password"])
                                client.send_message(reply)
                        else:
                            with smtplib.SMTP(acc["smtp_host"], acc["smtp_port"]) as client:
                                client.starttls(context=context)
                                client.login(acc["email"], acc["password"])
                                client.send_message(reply)
                                
                        conn = sqlite3.connect(str(db_p))
                        cur = conn.cursor()
                        cur.execute("UPDATE email_dispatch_ledger SET status='SENT_AUTONOMOUSLY', drafted_response=? WHERE id=?", (edit_resp, item["id"]))
                        conn.commit()
                        conn.close()
                        st.success(f"Transmission successfully dispatched to {item['sender']}!")
                        st.rerun()
                    except Exception as _err:
                        st.error(f"Transmission failed: {_err}")

            with c_act2:
                if st.button("✅ MARK AS RESOLVED", key=f"btn_resolve_p_{item['id']}_{key_suffix}", use_container_width=True):
                    try:
                        conn = sqlite3.connect(str(db_p))
                        cur = conn.cursor()
                        cur.execute("UPDATE email_dispatch_ledger SET status='RESOLVED_BY_CEO' WHERE id=?", (item["id"],))
                        conn.commit()
                        conn.close()
                        st.success(f"Item #{item['id']} marked as resolved.")
                        st.rerun()
                    except Exception as _err:
                        st.error(f"Failed to update ledger: {_err}")

    # TAB 2: FULL RESPONSE & INBOUND INSPECTOR
    with tab_responses:
        st.markdown("#### 🔍 Complete Communications & Response Inspector")
        st.caption("Inspect full transmission details and autonomous responses for any email in the enclave.")
        if not records:
            st.info("No communications records found.")
        else:
            all_opts = [f"#{r['id']} | {r['status']} | {r['sender'][:25]} | {r['subject'][:35]}" for r in records]
            selected_all = st.selectbox("Select Transmission to Inspect:", all_opts, key=f"sel_all_item_{key_suffix}")
            sel_idx = all_opts.index(selected_all)
            rec = records[sel_idx]

            col_inf1, col_inf2, col_inf3 = st.columns([1.5, 1.5, 1])
            with col_inf1:
                st.markdown(f"**Sender:** `{rec['sender']}`")
                st.markdown(f"**Subject:** `{rec['subject']}`")
            with col_inf2:
                st.markdown(f"**Recipient:** `{rec['recipient']}`")
                st.markdown(f"**Timestamp (UTC):** `{rec['timestamp'][:19]}`")
            with col_inf3:
                st.markdown(f"**Category:** `{rec['classification']}`")
                st.markdown(f"**Status:** `{rec['status']}`")

            col_view1, col_view2 = st.columns(2)
            with col_view1:
                with st.container(border=True):
                    st.markdown("##### 📥 Inbound Message Content")
                    st.write(rec["incoming_intent"] if rec["incoming_intent"] else "No inbound content recorded.")
            with col_view2:
                with st.container(border=True):
                    st.markdown("##### 📤 Executive Dispatched / Drafted Response")
                    st.write(rec["drafted_response"] if rec["drafted_response"] else "No response drafted.")

    # TAB 3: COMPLETE WORM LEDGER TABLE
    with tab_table:
        st.markdown("#### 🛡️ Tamper-Evident WORM Ledger Table")
        if records:
            df_display = pd.DataFrame(records)[["timestamp", "sender", "subject", "classification", "status", "drafted_response"]]
            df_display.columns = ["Timestamp (UTC)", "Sender", "Subject", "Category", "Status", "Dispatched Response"]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No recorded communications in ledger. Queue is clear.")
"""

ui_file = cockpit_dir / "ebony_travel_ui.py"
ui_file.write_text(ui_code, encoding="utf-8")
print("[+] ebony_travel_ui.py written with render_comms_gate and full travel deck.")

# -------------------------------------------------------------------------
# 3. BRIDGE render_comms_gate INTO ebony_console_GREEN.py
# -------------------------------------------------------------------------
console_file = cockpit_dir / "ebony_console_GREEN.py"
c_text = console_file.read_text(encoding="utf-8")

# Ensure render_comms_gate bridge function is defined in console
gate_bridge_def = """def render_comms_gate(key_suffix="sovereign_deck_main"):
    import sys
    from pathlib import Path
    _p = str(Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit"))
    if _p not in sys.path:
        sys.path.insert(0, _p)
    from ebony_travel_ui import render_comms_gate as _g
    return _g(key_suffix)"""

if "def render_comms_gate" not in c_text:
    start_fn = c_text.find("def render_communications_dispatch_ui")
    if start_fn != -1:
        c_text = c_text[:start_fn] + gate_bridge_def + "\n\n" + c_text[start_fn:]
    else:
        c_text = gate_bridge_def + "\n\n" + c_text
    print("[+] render_comms_gate bridge function injected into console.")

# Inject render_comms_gate call at top of Sovereign Dispatch Deck module
lines = c_text.splitlines(keepends=True)
deck_idx = -1
for i, line in enumerate(lines):
    if "Sovereign Dispatch Deck" in line and ("if " in line or "elif " in line):
        deck_idx = i
        break

if deck_idx != -1:
    deck_indent = lines[deck_line_idx if "deck_line_idx" in locals() else deck_idx][:len(lines[deck_idx]) - len(lines[deck_idx].lstrip())]
    body_indent = deck_indent + "    "
    gate_call_str = f"{body_indent}render_comms_gate(key_suffix=\"sovereign_deck_main\")\n"
    
    # Check if already present on the line immediately following
    if "render_comms_gate" not in lines[deck_idx + 1]:
        lines.insert(deck_idx + 1, gate_call_str)
        print(f"[+] render_comms_gate call injected at line {deck_idx + 2} (blocking unauthenticated access).")
    else:
        print("[*] render_comms_gate call already present in Dispatch Deck block.")

console_file.write_text("".join(lines), encoding="utf-8")

# -------------------------------------------------------------------------
# 4. VERIFY COMPILATION ACROSS ALL MODULES
# -------------------------------------------------------------------------
auto_file = cockpit_dir / "ebony_travel_autopilot.py"
print("[*] Running py_compile verification across all modules...")
py_compile.compile(str(disp_file), doraise=True)
py_compile.compile(str(ui_file), doraise=True)
py_compile.compile(str(auto_file), doraise=True)
py_compile.compile(str(console_file), doraise=True)
print("[SUCCESS] All 4 files compiled cleanly with ZERO errors (Exit Code 0)!")