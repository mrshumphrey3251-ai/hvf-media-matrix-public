"""
HVF OMNI-INDUSTRIAL UNIFIED C2 MASTER CONSOLE
Project: Ebony Sovereign Tri-Brain Matrix
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
    page_title="HVF Ebony C2 // Sovereign Master Console",
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
    .stButton>button { background-color: #1e293b; color: #38bdf8; border: 1px solid #38bdf8; font-weight: bold; }
    .stButton>button:hover { background-color: #38bdf8; color: #0b0f19; }
    .macro-btn>button { border-color: #f59e0b; color: #f59e0b; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ HVF Sovereign Command Nexus | Project Ebony C2 Console")
st.caption("CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Submission: 9-26-3703 | Classification: LEVEL-5 BARE-METAL C2")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_spoken_audio" not in st.session_state:
    st.session_state.last_spoken_audio = None

col_main, col_hud = st.columns([3, 2])

with col_main:
    st.subheader("📡 Tactical Ingress Deck (Voice & Direct Comms)")
    
    # 1. Voice Ingress Channel
    audio_val = st.audio_input("🎤 Record Sovereign Vocal Directive:")
    voice_prompt = ""
    if audio_val is not None:
        raw_bytes = audio_val.read()
        if len(raw_bytes) >= 1024:
            with st.spinner("Decoding Voice via Groq Whisper Ingestion Engine..."):
                voice_prompt = transcribe_mic(raw_bytes)
                if voice_prompt:
                    st.success(f"Transcribed Directive: \"{voice_prompt}\"")

    # 2. Text Ingress Channel
    default_text = voice_prompt if voice_prompt else ""
    user_directive = st.text_input("Enter or Edit Sovereign Directive:", value=default_text, key="directive_input")
    
    # 3. Tactical Command Macros
    st.markdown("**⚡ Tactical Command Quick-Action Macros:**")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    macro_trigger = None
    
    with m_col1:
        if st.button("🚨 System Readiness", use_container_width=True):
            macro_trigger = "Ebony, report your system readiness, CAGE governance, and operational status."
    with m_col2:
        if st.button("📊 SCADA Diagnostics", use_container_width=True):
            macro_trigger = "Ebony, pull real-time industrial SCADA metrics and storage integrity for node HVFNexus."
    with m_col3:
        if st.button("🛡️ Swarm Triad Audit", use_container_width=True):
            macro_trigger = "Ebony, dispatch the autonomous agent swarm triad and verify compliance."
    with m_col4:
        if st.button("🧹 Purge Session Display", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.last_spoken_audio = None
            st.rerun()

    # Active Execution Handler
    active_command = macro_trigger if macro_trigger else user_directive
    transmit_clicked = st.button("🚀 Transmit Directive", use_container_width=True)
    
    if (transmit_clicked or macro_trigger) and active_command.strip():
        with st.spinner("Processing through Sovereign Tri-Brain Router..."):
            response, audio_file = run_dual_core_router(
                active_command.strip(), 
                raw_history=st.session_state.chat_history
            )
            st.session_state.chat_history.append({"role": "user", "content": active_command.strip()})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            if audio_file and os.path.exists(audio_file):
                with open(audio_file, "rb") as f:
                    st.session_state.last_spoken_audio = base64.b64encode(f.read()).decode()

    # Playback Vocal Cortex Output
    if st.session_state.last_spoken_audio:
        st.markdown(
            f'<audio src="data:audio/wav;base64,{st.session_state.last_spoken_audio}" autoplay controls style="width: 100%; margin-top: 10px;"></audio>',
            unsafe_allow_html=True
        )

    st.markdown("### 💬 Live Command Stream")
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"**CEO Humphrey:** `{msg['content']}`")
        else:
            st.markdown(f"**Ebony (Chronos):**\n{msg['content']}")
            st.divider()

with col_hud:
    st.subheader("🛡️ Real-Time Telemetry HUD")
    tab_ledger, tab_scada, tab_swarm = st.tabs(["C2 Audit Ledger", "SCADA Telemetry", "Agent Swarm"])
    
    with tab_ledger:
        st.markdown("**Local SQLite WORM Ledger (`matrix_ledger.db`)**")
        entries = get_recent_entries(limit=8)
        if entries:
            for entry in entries:
                st.text(f"[{entry[1][:19]}] {entry[2].upper()} | Core: {entry[4]} | Latency: {entry[5]}s\nPayload: {entry[3][:110]}...")
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
            if st.button("Triad Sweep", key="hud_triad_btn", use_container_width=True):
                st.code(dispatch_swarm_task("all"), language="text")
            if st.button("Recon Agent", key="hud_recon_btn", use_container_width=True):
                st.code(dispatch_swarm_task("recon"), language="text")
        with swarm_col2:
            if st.button("Security Agent", key="hud_sec_btn", use_container_width=True):
                st.code(dispatch_swarm_task("security"), language="text")
            if st.button("Analyst Agent", key="hud_analyst_btn", use_container_width=True):
                st.code(dispatch_swarm_task("analyst"), language="text")
