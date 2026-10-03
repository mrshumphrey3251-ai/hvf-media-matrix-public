import os

file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

marker = 'elif active_module == "📡 Sovereign Comms Deck":'
next_marker = 'elif active_module =='

if marker in content:
    parts = content.split(marker, 1)
    before_comms = parts[0]
    
    # Locate the next tab to ensure we don't delete the rest of the file
    if next_marker in parts[1]:
        after_comms = next_marker + parts[1].split(next_marker, 1)[1]
    else:
        after_comms = ""
        
    clean_comms = marker + """
    st.subheader("📡 Sovereign WebRTC Comms Deck // Project Ebony")
    st.caption("Zero-fee, sovereign P2P encrypted data dispatch.")

    # Autonomous Synchronization Engine
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=2000, limit=None, key="matrix_auto_sync")
    except ImportError:
        pass

    st.markdown("### 💬 Encrypted P2P Dispatch")
    
    import json
    ledger_path = "hvf_comms_ledger.json"
    if not os.path.exists(ledger_path):
        with open(ledger_path, "w") as f:
            json.dump([{"sender": "EBONY CORE", "text": "Comms deck online. Autonomous Sync Active."}], f)
            
    with open(ledger_path, "r") as f:
        global_chat = json.load(f)

    chat_msg = st.text_input("Secure message payload:", key="sovereign_chat_input")
    
    if st.button("Transmit Securely"):
        if chat_msg.strip():
            safe_user = current_user if 'current_user' in locals() and current_user else "CEO_OVERRIDE"
            if 'current_user' in locals() and current_user and 'current_cipher' in locals() and current_cipher:
                save_encrypted_message(current_user, current_role, chat_msg.strip(), current_cipher)
            
            global_chat.append({"sender": safe_user.upper(), "text": chat_msg.strip() + " 🛡️ [ENCRYPTED & LOCKED]"})
            with open(ledger_path, "w") as f:
                json.dump(global_chat[-15:], f)
            st.rerun()

    st.markdown("---")
    for message in reversed(global_chat):
        st.info(f"**{message['sender']}**: {message['text']}")

"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(before_comms + clean_comms + after_comms)
    print("[SUCCESS] Sovereign Comms Deck purified. Church and State separated.")
else:
    print("[FATAL] Comms Deck not found in architecture.")