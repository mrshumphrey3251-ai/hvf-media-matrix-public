"""
HVF OMNI-INDUSTRIAL MASTER COMMAND COCKPIT
Project: Ebony Sovereign C2 Matrix
Compliance: CAGE 1AHA8 / UEI S1M4ENLHTDH5 // Submission 9-26-3703
Authority: Level-5 Sovereign Command (CEO Jeffery Humphrey)
"""

import streamlit as st
import os
import base64
from sovereign_comms import run_dual_core_router, transcribe_mic
from ebony_ledger import get_recent_entries
from ebony_scada_poll import poll_system_metrics, format_scada_telemetry_payload
from ebony_agent_swarm import dispatch_swarm_task

st.set_page_config(
    page_title="HVF Matrix C2 // Ebony Core",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark industrial command deck styling
st.markdown("""
<style>
    .reportview-container { background: #0b0f19; }
    .main { background: #0b0f19; color: #e2e8f0; }
    h1, h2, h3 { color: #38bdf8; font-family: 'Consolas', monospace; }
    .stButton>button { background-color: #1e293b; color: #38bdf8; border: 1px solid #38bdf8; }
    .stButton>button:hover { background-color: #38bdf8; color: #0b0f19; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ HVF Sovereign Command Nexus | Project Ebony")
st.caption("CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Submission: 9-26-3703 | Operational Brevity: Chronos")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col_main, col_hud = st.columns([3, 2])

with col_main:
    st.subheader("⌨️ Tactical Command Deck")
    user_directive = st.text_input("Enter Sovereign Directive:", key="directive_input")
    send_col, clear_col = st.columns([1, 5])
    
    with send_col:
        send_btn = st.button("Transmit", use_container_width=True)
    with clear_col:
        if st.button("Purge Session Display", use_container_width=False):
            st.session_state.chat_history = []
            st.rerun()

    if send_btn and user_directive.strip():
        with st.spinner("Dispatching through Dual-Core Router..."):
            response, audio_file = run_dual_core_router(
                user_directive.strip(), 
                raw_history=st.session_state.chat_history
            )
            st.session_state.chat_history.append({"role": "user", "content": user_directive.strip()})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            if audio_file and os.path.exists(audio_file):
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                    b64_audio = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio src="data:audio/wav;base64,{b64_audio}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)

    # Conversation Display
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"**CEO Humphrey:** `{msg['content']}`")
        else:
            st.markdown(f"**Ebony:**\n{msg['content']}")
            st.divider()

with col_hud:
    st.subheader("🛡️ Subsystem Telemetry HUD")
    tab_ledger, tab_scada, tab_swarm = st.tabs(["C2 Audit Ledger", "SCADA Telemetry", "Agent Swarm"])
    
    with tab_ledger:
        st.markdown("**Local SQLite WORM Ledger (`matrix_ledger.db`)**")
        entries = get_recent_entries(limit=8)
        if entries:
            for entry in entries:
                st.text(f"[{entry[1][:19]}] {entry[2].upper()} | Core: {entry[4]} | Latency: {entry[5]}s\nPayload: {entry[3][:120]}...")
                st.divider()
        else:
            st.info("No ledger entries logged.")
            
    with tab_scada:
        st.markdown("**Deterministic Host Diagnostics (`HVFNexus`)**")
        m = poll_system_metrics()
        if m.get("status") == "NOMINAL":
            st.metric("Primary Storage (C:\\)", f"{m['disk_free_gb']} GB Free", f"{m['disk_used_pct']}% Used")
            st.text(f"Host Node: {m['node']}")
            st.text(f"Environment: {m['os']}")
            st.text(f"Runtime Engine: Python {m['python_runtime']}")
            st.text(f"SCADA Link Status: {m['status']}")
        else:
            st.error(f"SCADA Poll Fault: {m.get('error')}")
            
    with tab_swarm:
        st.markdown("**Autonomous Triad Swarm Tasking (`BETA_AGENTS`)**")
        swarm_col1, swarm_col2 = st.columns(2)
        with swarm_col1:
            if st.button("Triad Sweep", use_container_width=True):
                st.code(dispatch_swarm_task("all"), language="text")
            if st.button("Recon Agent", use_container_width=True):
                st.code(dispatch_swarm_task("recon"), language="text")
        with swarm_col2:
            if st.button("Security Agent", use_container_width=True):
                st.code(dispatch_swarm_task("security"), language="text")
            if st.button("Analyst Agent", use_container_width=True):
                st.code(dispatch_swarm_task("analyst"), language="text")
