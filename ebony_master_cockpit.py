import streamlit as st
from sovereign_comms import run_dual_core_router

st.set_page_config(page_title="Ebony Master Cockpit", page_icon="⚡", layout="wide")

st.title("⚡ Project Ebony: Master Cockpit")
st.markdown("### Sovereign Dual-Core Neural Matrix | Tier-1 Active | Zero-Cost Vocal Cortex")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Command the matrix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing through Dual-Core Router..."):
            response = run_dual_core_router(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
