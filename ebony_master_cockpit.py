import streamlit as st
import time
from sovereign_comms import run_dual_core_router, transcribe_mic

st.set_page_config(page_title="Ebony Master Cockpit", page_icon="⚡", layout="wide")

# --- EXECUTIVE TELEMETRY & VOICE INPUT ---
with st.sidebar:
    st.title("⚙️ System Telemetry")
    st.markdown("---")
    st.metric(label="Primary Brain", value="Cloud Apex", delta="Online (Tier-1)")
    st.metric(label="Fallback Brain", value="Bare-Metal", delta="Standby")
    st.metric(label="Vocal Matrix", value="SAPI -> Media Player", delta="Active (Controllable)")
    st.markdown("---")
    st.markdown("### 🎙️ Verbal Command")
    audio_val = st.audio_input("Speak to the Matrix")

# --- MAIN COMMAND INTERFACE ---
st.title("⚡ Project Ebony: Master Cockpit")
st.markdown("### Executive Command Center")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("audio"):
            st.audio(msg["audio"])

# Process Voice Input
prompt = None
if audio_val:
    with st.spinner("Transcribing Voice Command..."):
        prompt = transcribe_mic(audio_val.read())

# Process Text Input (If voice wasn't used)
text_input = st.chat_input("Type your command to Ebony...")
if text_input:
    prompt = text_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing through Dual-Core Router..."):
            start_time = time.time()
            response, audio_file = run_dual_core_router(prompt)
            latency = round(time.time() - start_time, 2)
            
            st.markdown(response)
            if audio_file:
                # Native Streamlit audio player gives Pause/Rewind/Ffwd controls
                st.audio(audio_file, autoplay=True)
            
            st.caption(f"⏱️ Transmission Latency: {latency} seconds")
            
    st.session_state.messages.append({"role": "assistant", "content": response, "audio": audio_file})
