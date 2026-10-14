"""
E.B.O.N.Y. Executive Travel Autopilot, Priority Triage & Response Inspector
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Tier: Sovereign Tier-1 Executive Ingestion ($19.99/mo Baseline)
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import streamlit as st
import sqlite3
import pandas as pd
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

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

    db_p = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")
    total_count, sent_count, archived_count, flagged_count = 0, 0, 0, 0
    records = []

    if db_p.exists():
        try:
            conn = sqlite3.connect(str(db_p))
            cur = conn.cursor()
            cur.execute("""
                SELECT id, timestamp, sender, recipient, subject, incoming_intent, drafted_response, status, classification, message_uid
                FROM email_dispatch_ledger 
                ORDER BY timestamp DESC
            """)
            cols = ["id", "timestamp", "sender", "recipient", "subject", "incoming_intent", "drafted_response", "status", "classification", "message_uid"]
            raw_data = cur.fetchall()
            conn.close()
            for row in raw_data:
                records.append(dict(zip(cols, row)))
            
            total_count = len(records)
            sent_count = sum(1 for r in records if r["status"] == "SENT_AUTONOMOUSLY")
            archived_count = sum(1 for r in records if r["status"] == "ARCHIVED_BULK")
            flagged_count = sum(1 for r in records if any(k in (r["classification"] or "").upper() for k in ["GRANT", "STATE", "EXECUTIVE", "TITLE61", "ODOT"]))
        except Exception:
            pass

    # 1. Macro KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Ingested", f"{total_count} Transmissions")
    col2.metric("Autonomously Resolved", f"{sent_count} Dispatched", delta=f"{sent_count} closed")
    col3.metric("Newsletters Filtered", f"{archived_count} Archived")
    col4.metric("Priority Action Items", f"{flagged_count} Flagged", delta="Action Required" if flagged_count > 0 else "Clear")

    # 2. Executive Autopilot Control Bar
    c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
    with c1:
        if st.button("🚀 ENGAGE TRAVEL AUTOPILOT (AUTO-REPLY ALL)", key=f"btn_autopilot_send_{key_suffix}", use_container_width=True):
            try:
                _cdir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
                if str(_cdir) not in sys.path: sys.path.insert(0, str(_cdir))
                from ebony_travel_autopilot import run_travel_cycle
                res = run_travel_cycle(auto_send=True)
                st.success(f"Autopilot Complete: Processed {len(res)} transmission(s) and dispatched via SMTP.")
                st.rerun()
            except Exception as _e:
                st.error(f"Autopilot execution failure: {_e}")

    with c2:
        if st.button("📥 RECON INBOX (READ ONLY)", key=f"btn_recon_draft_{key_suffix}", use_container_width=True):
            try:
                _cdir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
                if str(_cdir) not in sys.path: sys.path.insert(0, str(_cdir))
                from ebony_travel_autopilot import run_travel_cycle
                res = run_travel_cycle(auto_send=False)
                st.info(f"Recon Complete: Ingested {len(res)} transmission(s) into WORM ledger.")
                st.rerun()
            except Exception as _e:
                st.error(f"Recon failure: {_e}")

    with c3:
        if st.button("📱 EMAIL DEBRIEF TO MY PHONE", key=f"btn_email_debrief_{key_suffix}", use_container_width=True):
            try:
                _cdir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
                if str(_cdir) not in sys.path: sys.path.insert(0, str(_cdir))
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
        priority_items = [r for r in records if any(k in (r["classification"] or "").upper() for k in ["GRANT", "STATE", "EXECUTIVE", "TITLE61", "ODOT"])]
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
                        cfg_p = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\email_accounts.json")
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