import streamlit as st
import time
from sovereign_comms import run_dual_core_router, transcribe_mic

st.set_page_config(page_title="HVF Omni-Industrial Matrix", page_icon="⚡", layout="wide")

# --- MASTER HEADER ---
st.title("⚡ HVF Omni-Industrial Matrix Command Deck | Ebony AI")
st.markdown("**Active User: Jeffery Humphrey | 🛡️ Mode: 🟢 Online (Cloud Fast Link)**")
st.markdown("---")

st.markdown("### ⚡ Sovereign Command Nexus")

# --- COMMAND INTERFACE SELECTOR ---
interface_mode = st.radio(
    "Select Command Interface:", 
    ["⌨️ Secure Text Terminal", "🎙️ Acoustic Voice Link"], 
    horizontal=True
)

st.markdown("---")

# --- CHAT MATRIX ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey Jeffery, I'm online and wired in. You want to type or talk today?", "audio": None}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("audio"):
            st.audio(msg["audio"])

# --- DUAL-VECTOR INPUT ROUTING ---
prompt = None

if "Text" in interface_mode:
    text_input = st.chat_input("Secure Text Terminal active... Type command here.")
    if text_input:
        prompt = text_input
else:
    st.info("🎙️ Acoustic Voice Link Active. Click the microphone below to transmit your verbal orders.")
    audio_val = st.audio_input("Speak to the Matrix")
    if audio_val:
        with st.spinner("Transcribing Voice Command..."):
            prompt = transcribe_mic(audio_val.read())

# --- PROCESSING PIPELINE ---
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
                # Controllable UI Media Player (Pause/Stop/Rewind/Ffwd)
                st.audio(audio_file, autoplay=True)
            
            st.caption(f"⏱️ Transmission Latency: {latency} seconds")
            
    st.session_state.messages.append({"role": "assistant", "content": response, "audio": audio_file})
    
    # If using voice, force a rerun to clear the audio widget properly after submission
    if "Voice" in interface_mode:
        st.rerun()
