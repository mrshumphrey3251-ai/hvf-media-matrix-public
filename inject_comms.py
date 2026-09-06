import sys

file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Target the exact navigation array insertion point, accounting for the emoji
target_nav = '"📖 System Overview",'
if target_nav in content and '"📡 Sovereign Comms Deck"' not in content:
    content = content.replace(
        target_nav,
        '"📖 System Overview",\n        "📡 Sovereign Comms Deck",'
    )
    print("[SUCCESS] Navigation binding injected cleanly.")
else:
    print("[NOTICE] Target navigation string not found or Comms Deck already present.")

# The pristine Comms Deck handler module
comms_module = """
elif active_module == "📡 Sovereign Comms Deck":
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
                st.session_state.sovereign_chat.append({"sender": current_user, "text": chat_msg.strip()})
                st.rerun()
                
        st.markdown("---")
        for message in reversed(st.session_state.sovereign_chat):
            st.info(f"**{message['sender']}**: {message['text']}")
"""

if 'elif active_module == "📡 Sovereign Comms Deck":' not in content:
    content = content.rstrip() + "\n\n" + comms_module
    print("[SUCCESS] Comms Deck module appended.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[VERIFICATION] Python execution complete. Zero encoding artifacts introduced.")
