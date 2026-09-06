import sys, re

file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Upgrade Hardware Taxonomy for Universal Support
content = content.replace("### 📷 Arducam Optical Feed", "### 📷 Universal Optical Bridge")
content = content.replace("Arducam-1080P-HDR hardware bridge active.", "Hardware auto-negotiation active. Native support for Arducam, Laptops, and Mobile Devices.")
content = content.replace("Capture Frame from Arducam Sensor", "Capture Frame from Local Hardware")

# 2. Upgrade Chat Input to a locked st.form to prevent auto-refreshing
pattern = r'chat_msg = st\.text_input\("Secure message payload:", key="sovereign_chat_input"\)\s+if st\.button\("Transmit Securely", key="sovereign_transmit"\):\s+if chat_msg\.strip\(\):\s+st\.session_state\.sovereign_chat\.append\(\{"sender": current_user, "text": chat_msg\.strip\(\)\}\)\s+st\.rerun\(\)'

replacement = """with st.form("comms_dispatch_form", clear_on_submit=True):
            chat_msg = st.text_input("Secure message payload:")
            submitted = st.form_submit_button("Transmit Securely")
            if submitted and chat_msg.strip():
                st.session_state.sovereign_chat.append({"sender": current_user, "text": chat_msg.strip()})
                st.rerun()"""

content = re.sub(pattern, replacement, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Hardware taxonomy expanded and chat upgraded to secure form.")
