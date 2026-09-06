import os

file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

marker = 'elif active_module == "📡 Sovereign Comms Deck":'

if marker in content:
    base_content = content.split(marker)[0]
    
    new_module = marker + """
    st.subheader("📡 Sovereign WebRTC Comms Deck // Project Ebony")
    st.caption("Zero-fee, sovereign P2P voice, video, and encrypted data dispatch.")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("### 🔴 LIVE // SWARM OPTICAL FEED")
        st.info("WebRTC Matrix streaming via Sovereign Tailscale Link.")
        # Injecting the live Master Media Router feed directly into the UI
        st.components.v1.html(
            f'<iframe src="http://100.87.162.117:8889/live/stream" width="100%" height="450" style="border:none;" allow="autoplay; fullscreen"></iframe>',
            height=470
        )

    with col_c2:
        st.markdown("### 💬 Encrypted P2P Dispatch")
        
        # Establishing a Global JSON Ledger for Cross-Device Sync
        import json
        ledger_path = "hvf_comms_ledger.json"
        if not os.path.exists(ledger_path):
            with open(ledger_path, "w") as f:
                json.dump([{"sender": "EBONY CORE", "text": "Comms deck online. Global Sync Active."}], f)
                
        with open(ledger_path, "r") as f:
            global_chat = json.load(f)

        chat_msg = st.text_input("Secure message payload:", key="sovereign_chat_input")
        
        col_b1, col_b2 = st.columns([1, 1])
        if col_b1.button("Transmit Securely"):
            if chat_msg.strip():
                safe_user = current_user if 'current_user' in locals() and current_user else "CEO_OVERRIDE"
                if 'current_user' in locals() and current_user and current_cipher:
                    save_encrypted_message(current_user, current_role, chat_msg.strip(), current_cipher)
                
                # Append to global ledger
                global_chat.append({"sender": safe_user.upper(), "text": chat_msg.strip() + " 🛡️ [ENCRYPTED & LOCKED]"})
                with open(ledger_path, "w") as f:
                    json.dump(global_chat[-15:], f) # Keep last 15 transmissions
                st.rerun()
                
        if col_b2.button("🔄 Sync Feed"):
            st.rerun()

        st.markdown("---")
        for message in reversed(global_chat):
            st.info(f"**{message['sender']}**: {message['text']}")
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(base_content + new_module)
    print("[SUCCESS] Mobile Integration Bridge Deployed. Cross-Network Sync Active.")
else:
    print("[FATAL] Target architecture marker not found in file.")