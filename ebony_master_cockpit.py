import streamlit as st
import time
from sovereign_comms import run_dual_core_router, transcribe_mic

st.set_page_config(page_title="HVF Omni-Industrial Matrix", page_icon="⚡", layout="wide")

# --- MASTER HEADER ---
st.title("⚡ HVF Omni-Industrial Matrix Command Deck | Ebony AI")
st.markdown("**Active User: Jeffery Humphrey | 🛡️ Mode: 🟢 Online (Cloud Fast Link)**")
st.markdown("---")

st.markdown("### ⚡ Sovereign Command Nexus")
interface_mode = st.radio(
    "Select Command Interface:", 
    ["⌨️ Secure Text Terminal", "🎙️ Acoustic Voice Link"], 
    horizontal=True
)
st.markdown("---")

# --- CHAT MATRIX & DYNAMIC WIDGET STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey Jeffery, I'm online and wired in. You want to type or talk today?", "audio": None}
    ]
    
if "mic_key" not in st.session_state:
    st.session_state.mic_key = 0

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("audio"):
            is_last = (i == len(st.session_state.messages) - 1)
            try:
                st.audio(msg["audio"], autoplay=is_last)
            except TypeError:
                st.audio(msg["audio"])

# --- DUAL-VECTOR INPUT ROUTING ---
prompt = None

if "Text" in interface_mode:
    prompt = st.chat_input("Secure Text Terminal active... Type command here.")
else:
    st.info("🎙️ Acoustic Voice Link Active. Click the microphone below to transmit your verbal orders.")
    audio_val = st.audio_input("Speak to the Matrix", key=f"mic_{st.session_state.mic_key}")
    
    if audio_val:
        with st.spinner("Transcribing Voice Command..."):
            prompt = transcribe_mic(audio_val.read())
        st.session_state.mic_key += 1

# --- HARD RESET PROCESSING PIPELINE ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt, "audio": None})
    with st.spinner("Processing through Dual-Core Router..."):
        response, audio_file = run_dual_core_router(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response, "audio": audio_file})
    st.rerun()
