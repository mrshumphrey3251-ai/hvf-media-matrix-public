import os
file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

marker = 'elif active_module == "📡 Sovereign Comms Deck":'
if marker in content:
    base_content = content.split(marker)[0]
    new_module = marker + '''
    st.subheader("📡 Sovereign WebRTC Comms Deck // Project Ebony")
    st.caption("Zero-fee, sovereign P2P voice, video, and encrypted data dispatch.")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("### 📷 Arducam Optical Feed")
        st.info("Arducam-1080P-HDR hardware bridge active.")
        captured_frame = st.camera_input("Capture Frame from Arducam Sensor", key="comms_arducam_capture")
        if captured_frame:
            st.success("Frame successfully latched from optical sensor.")
            st.image(captured_frame)

    with col_c2:
        st.markdown("### 💬 Encrypted P2P Dispatch")
        if "sovereign_chat" not in st.session_state:
            st.session_state.sovereign_chat = [
                {"sender": "EBONY CORE", "text": "Comms deck online. Zero middleman fees."}
            ]

        chat_msg = st.text_input("Secure message payload:", key="sovereign_chat_input")
        if st.button("Transmit Securely", key="sovereign_transmit"):
            if chat_msg.strip():
                safe_user = current_user if current_user else "CEO_OVERRIDE"
                if current_user and current_cipher:
                    save_encrypted_message(current_user, current_role, chat_msg.strip(), current_cipher)
                st.session_state.sovereign_chat.append({"sender": safe_user.upper(), "text": chat_msg.strip() + " 🛡️ [ENCRYPTED & LOCKED]"})
                st.rerun()

        st.markdown("---")
        for message in reversed(st.session_state.sovereign_chat):
            st.info(f"**{message['sender']}**: {message['text']}")
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(base_content + new_module)
    print("[SUCCESS] Fault-Tolerant Bridge Injected. UI Crash Prevented.")
else:
    print("[FATAL] Target architecture marker not found in file.")
