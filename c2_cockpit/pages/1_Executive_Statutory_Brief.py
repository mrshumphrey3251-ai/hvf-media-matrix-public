import streamlit as st
import sqlite3
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Executive Statutory Brief | HVF LLC", page_icon="📜", layout="wide")

st.markdown("""
<div style="background: linear-gradient(90deg, #0b110e 0%, #131d18 100%); border-left: 4px solid #00ff88; border-right: 1px solid #1f3326; border-top: 1px solid #1f3326; border-bottom: 1px solid #1f3326; border-radius: 6px; padding: 14px 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
    <div>
        <span style="color: #00ff88; font-weight: 800; font-size: 1.05em; letter-spacing: 1.5px; font-family: monospace;">HUMPHREY VIRTUAL FARMS LLC</span>
        <span style="color: #a0aab2; font-size: 0.85em; margin-left: 12px; font-family: monospace;">| EXECUTIVE STATUTORY COMPACT & LEGAL BRIEF</span>
    </div>
    <div>
        <span style="background-color: #002b16; border: 1px solid #00ff88; color: #00ff88; padding: 4px 10px; border-radius: 4px; font-size: 0.8em; font-family: monospace; font-weight: bold; margin-right: 8px;">CAGE: 1AHA8</span>
        <span style="background-color: #002b16; border: 1px solid #00ff88; color: #00ff88; padding: 4px 10px; border-radius: 4px; font-size: 0.8em; font-family: monospace; font-weight: bold; margin-right: 8px;">UEI: S1M4ENLHTDH5</span>
        <span style="background-color: #121c16; border: 1px solid #285437; color: #7fe6a7; padding: 4px 10px; border-radius: 4px; font-size: 0.8em; font-family: monospace;">HOST: HVFNexus</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("📜 Sovereign Executive Legal Brief & Statutory Compact")
st.caption("Binding Corporate & Federal Governance Directives // Controlled by Jeffery Humphrey, CEO & Sole Proprietary Authority")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 1. Corporate Governance & Proprietary Ownership")
    st.info("""
    **Entity:** Humphrey Virtual Farms LLC  
    **Sole Controlling Authority & SME:** Jeffery Humphrey, Founder & CEO  
    **Federal CAGE Code:** `1AHA8`  
    **SAM.gov UEI:** `S1M4ENLHTDH5`  
    **Infrastructure Core:** Bare-Metal Edge Isolation (`HVFNexus`)  
    """)

    st.markdown("### 2. Statutory Framework Compliance")
    st.markdown("""
    * **Oklahoma Statutes Title 61:** Fully structured for sovereign state infrastructure, public bidding, and physical works compliance.
    * **Oklahoma House Bill 2992 (OK HB 2992):** Strict sovereign data protection, zero foreign adversary supply-chain exposure, and mandatory hardware sovereignty.
    * **Zero-Cloud Sovereignty:** Zero reliance on recurring third-party cloud telemetry, external vendor kill-switches, or remote credential harvesting. All weights, ledgers, and logs remain locked on local bare-metal disk.
    """)

with col2:
    st.markdown("### 🏛️ WORM Ledger Audit Integrity")
    st.caption("Immutable attestation proof pulled live from `matrix_ledger.db`:")

    ledger_path = Path("matrix_ledger.db")
    if ledger_path.exists():
        try:
            conn = sqlite3.connect(str(ledger_path))
            cur = conn.cursor()
            cur.execute("SELECT id, timestamp, role, model_core, content FROM audit_ledger WHERE role = 'EXECUTIVE_ATTESTATION' ORDER BY id DESC LIMIT 1;")
            row = cur.fetchone()
            conn.close()

            if row:
                st.success("🔒 VALIDATED: Executive Attestation on File")
                st.code(f"RECORD ID: {row[0]}\nTIMESTAMP: {row[1]}\nROLE: {row[2]}\nCORE: {row[3]}\nPAYLOAD: {row[4]}", language="text")
            else:
                st.warning("No attestation record logged yet in active ledger.")
        except Exception as e:
            st.error(f"Ledger Query Exception: {e}")
    else:
        st.error("Matrix Ledger DB not found.")

st.markdown("---")
st.markdown("""
<div style="background-color: #0b110e; border: 1px solid #1f3326; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 0.85em; color: #a0aab2; text-align: center;">
    CONFIDENTIAL // PROPRIETARY SOVEREIGN ASSET // HUMPHREY VIRTUAL FARMS LLC // ALL RIGHTS RESERVED
</div>
""", unsafe_allow_html=True)
