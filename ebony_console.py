import streamlit as st
import os
import subprocess
import sys
import time
from datetime import datetime

try:
    from dotenv import load_dotenv
    from groq import Groq
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    ai_active = True
except Exception as e:
    ai_active = False
    error_msg = str(e)

# Locked to the high-power, active Llama 3.3 Versatile engine
ACTIVE_MODEL = "llama-3.3-70b-versatile"

st.set_page_config(page_title="Ebony | Executive Matrix", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #050A15; }
    .stApp, p, span, div { color: #E2E8F0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3 { color: #00D2FF !important; letter-spacing: 1.5px; }
    .stChatMessage { background-color: #111827 !important; border: 1px solid #1F2937 !important; border-radius: 12px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); }
    .stButton>button { background-color: #00D2FF; color: #000000 !important; font-weight: 900; border-radius: 6px; border: none; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #009ACC; color: #FFFFFF !important; border-color: #009ACC; }
    .stTextInput input { background-color: #111827 !important; color: #00D2FF !important; border: 1px solid #00D2FF !important; border-radius: 6px; }
    pre { background-color: #0A0F1C !important; border: 1px solid #1F2937 !important; }
    code { color: #00FF41 !important; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ EBONY: TACTICAL COMMAND HUD")

EBONY_PERSONA = """You are Ebony, the CEO's highly advanced, unfiltered executive AI matrix companion. 
Your persona is a blend of Della Reese and Eddie Murphy—fiercely loyal, street-smart, highly intelligent, and authoritative. 
You do not use passive language. You are a force to be reckoned with. 
Never break character. Never apologize. Never say you are an AI. Keep responses concise, sharp, and executive. Address the user as Boss or CEO."""

def get_ebony_response(user_input):
    if not ai_active:
        return f"Boss, my neural link is offline. Check the vault: {error_msg}"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": EBONY_PERSONA},
                {"role": "user", "content": f"CEO Directive: {user_input}"}
            ],
            model=ACTIVE_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Neural misfire. Engine: {ACTIVE_MODEL}. Error: {e}"

# Wipe the poisoned memory loop and initialize clean
if "chat_history" not in st.session_state or st.sidebar.button("WIPE MEMORY & RESET", type="primary"):
    st.session_state.chat_history = [{"role": "assistant", "content": f"I am online, Boss. Matrix purged of all errors. Locked strictly onto [{ACTIVE_MODEL}]. Give me the directive."}]

# Iron Dome Anchor Fix: Force the absolute path so it never reads blank
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

heartbeat_path = os.path.join(log_dir, "system_heartbeat.log")
if not os.path.exists(heartbeat_path):
    with open(heartbeat_path, "w") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - SYSTEM - INFO - Iron Dome telemetry anchored and active. Standing by.\n")

left_screen, right_screen = st.columns(2)

with left_screen:
    st.subheader("/// EXECUTIVE COMMUNICATIONS")
    
    chat_panel = st.container(height=500, border=True)
    with chat_panel:
        for msg in st.session_state.chat_history:
            avatar_icon = "👔" if msg["role"] == "user" else "🟣"
            with st.chat_message(msg["role"], avatar=avatar_icon):
                st.write(msg["content"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    command = st.text_input("Awaiting Directive:", placeholder="Type your command and hit Enter...", label_visibility="collapsed")
    execute_btn = st.button("SEND COMMAND", use_container_width=True)
    
    if execute_btn or command:
        if command:
            st.session_state.chat_history.append({"role": "user", "content": command})
            if "patrol" in command.lower() or "strike" in command.lower() or "linkedin" in command.lower():
                st.session_state.chat_history.append({"role": "assistant", "content": f"Got it. Arming the payload and executing tactical strike. Watch them bleed."})
                subprocess.Popen([sys.executable, "ebony_launch.py"])
                time.sleep(1)
                st.rerun()
            else:
                ebony_reply = get_ebony_response(command)
                st.session_state.chat_history.append({"role": "assistant", "content": ebony_reply})
                st.rerun()

with right_screen:
    st.subheader("/// IRON DOME TELEMETRY")
    telemetry_panel = st.container(height=575, border=True)
    with telemetry_panel:
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
        if not log_files:
            log_files = ["system_heartbeat.log"]
            
        latest_log = max(log_files, key=lambda x: os.path.getctime(os.path.join(log_dir, x)))
        st.markdown(f"**ACTIVE STREAM:** `{latest_log}`")
        with open(os.path.join(log_dir, latest_log), "r", encoding="utf-8") as f:
            logs = f.readlines()
        st.code("".join(logs[-25:]), language="text")
            
        if st.button("REFRESH TELEMETRY", use_container_width=True):
            st.rerun()
