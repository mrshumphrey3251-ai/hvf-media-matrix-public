"""
E.B.O.N.Y. Executive Travel Autopilot & Return Debrief Glass UI
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

def render_communications_dispatch_ui(key_suffix="sovereign_deck_main"):
    st.divider()
    st.markdown("## ✈️ EXECUTIVE TRAVEL AUTOPILOT // INBOX GHOSTWRITER & DEBRIEF")
    st.caption("Autonomous Inbound Ingestion, Contextual SMTP Auto-Response & Executive Return Briefing // Level-5 Authority")

    col1, col2, col3, col4 = st.columns(4)
    db_p = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")
    total_count, sent_count, archived_count, flagged_count = 0, 0, 0, 0
    df = pd.DataFrame()

    if db_p.exists():
        try:
            conn = sqlite3.connect(str(db_p))
            q = "SELECT timestamp AS 'Timestamp (UTC)', sender AS 'Sender', subject AS 'Subject', classification AS 'Category', status AS 'Status', drafted_response AS 'Dispatched Response' FROM email_dispatch_ledger ORDER BY timestamp DESC"
            df = pd.read_sql_query(q, conn)
            conn.close()
            if not df.empty:
                total_count = len(df)
                sent_count = len(df[df['Status'] == 'SENT_AUTONOMOUSLY'])
                archived_count = len(df[df['Status'] == 'ARCHIVED_BULK'])
                flagged_count = len(df[df['Category'].str.contains('GRANT|STATE|EXECUTIVE|TITLE61|ODOT', case=False, na=False)])
        except Exception:
            pass

    col1.metric("Total Ingested", f"{total_count} Transmissions")
    col2.metric("Autonomously Resolved", f"{sent_count} Dispatched", delta=f"{sent_count} closed")
    col3.metric("Newsletters Filtered", f"{archived_count} Archived")
    col4.metric("Priority Action Items", f"{flagged_count} Flagged", delta="Action Required" if flagged_count > 0 else "Clear")

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

    with st.expander("📋 EXECUTIVE RETURN DEBRIEF // PLAIN-ENGLISH BRIEFING", expanded=True):
        st_msg = "🟢 ALL OPERATIONAL INQUIRIES RESOLVED AUTONOMOUSLY" if flagged_count == 0 else f"⚠️ {flagged_count} HIGH-PRIORITY ACTION ITEMS FLAGGED"
        st.markdown(f"""
        ### 🏛️ Operational Readout for Returning Executive
        - **Sovereign Node:** `HVFNexus` | **Active Mailbox:** `humphreyvirtualfarm@gmail.com`
        - **Mission Status:** {st_msg}
        
        **HOW E.B.O.N.Y. PROTECTED YOUR TIME WHILE AWAY:**
        1. **100% Inbound Scanning:** Ingested over encrypted TLS/SSL (Port 993) without third-party cloud data harvesting.
        2. **Noise Neutralization:** {archived_count} automated newsletters and alerts archived to the WORM ledger.
        3. **Autonomous Ghostwriting:** {sent_count} direct inquiries received contextual executive replies over SSL/TLS (Port 465).
        4. **Priority Filtration:** {flagged_count} items require personal review (Grants, ODOT Aerospace, Title 61).
        """)

    st.markdown("#### 🛡️ Tamper-Evident Communications Audit Ledger")
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No recorded communications in ledger. Queue is clear.")
