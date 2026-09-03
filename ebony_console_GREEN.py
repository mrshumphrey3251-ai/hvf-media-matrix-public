import streamlit as st
import requests
import json

st.set_page_config(page_title="HVF Ebony Command Deck", layout="wide", initial_sidebar_state="expanded")

# Sidebar Vertical Navigation Menu
st.sidebar.title("🟢 Sovereign Node")
st.sidebar.caption("Humphrey Virtual Farm | 52% Control")
st.sidebar.markdown("---")

menu_options = [
    "1. System Status",
    "2. Treasury Matrix",
    "3. Autonomous Engine",
    "4. WebRTC Gateway",
    "5. DFARS & Data Rights",
    "6. Iron Dome Perimeter",
    "7. Audit Ledger",
    "8. Deal Pipeline",
    "9. Asset Synthesis"
]
selection = st.sidebar.radio("Command Modules", menu_options)

# Main Content Area
st.title("🟢 HVF Ebony Command Deck")
st.caption("Administrative Custody: Root | Executive Override: Active")

API_URL = "http://localhost:8000"
HEADERS = {"x-auth-token": "CEO_OVERRIDE"}

if selection == "1. System Status":
    st.header("Sovereign Telemetry & Health")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Governance State", "52% HVF Dominance", "Locked")
    with col2:
        st.metric("Backend Node", "Port 8000 (Active)", "Uptime 100%")
    with col3:
        st.metric("Zero-Trust Perimeter", "Iron Dome Active", "Enforced")
    
    if st.button("Query Full Telemetry"):
        try:
            res = requests.get(f"{API_URL}/telemetry", headers=HEADERS)
            st.json(res.json())
        except Exception as e:
            st.error(f"Backend Offline or Unreachable: {e}")

elif selection == "2. Treasury Matrix":
    st.header("The Humphrey Treasury Matrix")
    st.info("Administrative Custodianship: Sole control held by Jeffery Humphrey (HVF).")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Tax Escrow", "30%", "Federal/State Lock")
    col_t2.metric("OpEx Pool", "15%", "Dual-Sig Approved")
    col_t3.metric("Ecosystem CapEx", "15%", "R&D Restricted")
    col_t4.metric("Founder Distribution", "40%", "50/50 Net Split")

elif selection == "3. Autonomous Engine":
    st.header("Autonomous ML Predict-and-Act Control")
    st.write("Initiate internal matrix self-optimization protocols via sovereign API.")
    if st.button("Engage Autonomous ML Loop"):
        try:
            res = requests.post(f"{API_URL}/autonomous/engage", headers=HEADERS)
            st.success(res.json()["message"])
        except Exception as e:
            st.error(f"Execution Error: {e}")

elif selection == "4. WebRTC Gateway":
    st.header("Phase 2 WebRTC Secure Gateway")
    st.write("Target Node: SignalLink Protocol LLC (CAGE: 16WJ1)")
    st.warning("Awaiting Counterparty Schedule Confirmation for Live Architecture Demo.")

elif selection == "5. DFARS & Data Rights":
    st.header("Federal Data Rights & DFARS Compliance")
    st.markdown("""
    * **Background IP:** 100% HVF Sole Ownership (Project Ebony Base Architecture).
    * **Rights Assertion:** Restricted / Limited Rights asserted under DFARS clauses.
    * **Veto Power:** Absolute HVF Operational Veto over all federal bid tables.
    """)

elif selection == "6. Iron Dome Perimeter":
    st.header("Zero-Trust Iron Dome Security")
    st.success("Native PowerShell Execution Policy Enforced.")
    st.write("Legacy cmd.exe, shell injections, and unauthorized alternative nodes blocked at kernel boundary.")

elif selection == "7. Audit Ledger":
    st.header("Mutual Open-Book Audit Ledger")
    st.write("Section 4 Compliance: 48-Hour SLA for accounting and telemetry production.")
    st.code("""
    [2026-09-03 14:00:56] Definitive LOI executed via DocuSign (Envelope: FE1D11A1-80A0-8A93-82F7-B9F7FD872D92)
    [2026-09-03 14:02:19] Schedule A Clean Hands executed (Envelope: 59CCB77E-F36E-8DC0-83D6-E8E9F70E797C)
    [2026-09-03 14:05:00] Informal acknowledgment received from counterparty.
    [2026-09-03 15:00:00] Executive redirect to formal email deployed.
    """, language="text")

elif selection == "8. Deal Pipeline":
    st.header("Strategic Opportunities & Pipeline")
    st.markdown("""
    * **SignalLink Joint Venture:** Phase 1 Complete (Executed LOI). Transitioning to Phase 2 Live Demo.
    * **Digital Dojo Proposal:** On strategic hold to extract competitive positioning intelligence.
    * **Federal Prime Bids:** Sam.gov registration active (CAGE: 1AHA8, UEI: S1M4ENLHTDH5).
    """)

elif selection == "9. Asset Synthesis":
    st.header("Sovereign Image & Media Synthesis")
    prompt = st.text_input("Enter Generation Prompt:", "High-tech executive handshake: HVF on left, SignalLink on right, Project Ebony banner centered")
    if st.button("Generate Sovereign Asset"):
        try:
            res = requests.post(f"{API_URL}/synthesis/image", params={"prompt": prompt}, headers=HEADERS)
            st.info(res.json()["message"])
        except Exception as e:
            st.error(f"Matrix Offline: {e}")
