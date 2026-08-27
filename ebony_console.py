import streamlit as st
import os
import subprocess
import sys
import time
import json
from datetime import datetime

try:
    from dotenv import load_dotenv
    from groq import Groq
    load_dotenv(override=True)
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    ai_active = True
except Exception as e:
    ai_active = False
    error_msg = str(e)

ACTIVE_MODEL = "openai/gpt-oss-120b"

st.set_page_config(page_title="Ebony | Executive Matrix (BLUE DEV)", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050A15; }
    .stApp, p, span, div { color: #E2E8F0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3 { color: #00D2FF !important; letter-spacing: 1.5px; }
    .stChatMessage { background-color: #111827 !important; border: 1px solid #1F2937 !important; border-radius: 12px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); }
    .stButton>button { background-color: #00D2FF; color: #000000 !important; font-weight: 900; border-radius: 6px; border: none; }
    .stButton>button:hover { background-color: #009ACC; color: #FFFFFF !important; }
    .stTextInput input { background-color: #111827 !important; color: #00D2FF !important; border: 1px solid #00D2FF !important; }
    pre { background-color: #0A0F1C !important; border: 1px solid #1F2937 !important; white-space: pre-wrap !important; word-wrap: break-word !important; }
    code { color: #00FF41 !important; white-space: pre-wrap !important; }
    div[data-baseweb="select"] > div { background-color: #000000 !important; border: 2px solid #00D2FF !important; }
    div[data-baseweb="select"] div[class*="singleValue"] { color: #00FF41 !important; font-weight: 900 !important; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ EBONY: TACTICAL COMMAND HUD [BLUE DEV]")

EBONY_PERSONA = """You are Ebony, the CEO's highly advanced executive AI. You write with supreme authority. Never break character. Address the user as Boss."""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, "logs")
vault_dir = os.path.join(BASE_DIR, "content_vault")
memory_dir = os.path.join(BASE_DIR, "memory_core")
recon_dir = os.path.join(BASE_DIR, "recon_intel")
auto_dir = os.path.join(BASE_DIR, "autonomous_ops")
comms_dir = os.path.join(BASE_DIR, "global_comms")

for directory in [log_dir, vault_dir, memory_dir, recon_dir, auto_dir, comms_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

if recon_dir not in sys.path: sys.path.append(recon_dir)

MEMORY_FILE = os.path.join(memory_dir, "neural_memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return [{"role": "assistant", "content": f"I am online, Boss. Predictive Neural Router engaged. Give me the directive."}]

def save_memory(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)

def analyze_intent(user_input):
    prompt = f"""You are the routing brain of an executive AI. Analyze the CEO's input and extract their true intent, ignoring fuzzy or informal language.
    Classify into ONE of three categories:
    1. "ARCHITECT" - CEO wants to create, edit, write, or modify a code file/script.
    2. "DRAFT" - CEO wants to draft a social media post, email, or external communication.
    3. "CHAT" - CEO is asking a general question, seeking advice, or having a conversation.

    Output ONLY a strict JSON object. No markdown. Format:
    {{"intent": "ARCHITECT"|"DRAFT"|"CHAT", "target_file": "filename.py" (if ARCHITECT, else ""), "directive": "extracted clean instructions"}}
    Input: {user_input}"""
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=ACTIVE_MODEL)
        raw = res.choices[0].message.content.strip()
        if raw.startswith("```json"): raw = raw[7:]
        if raw.endswith("```"): raw = raw[:-3]
        return json.loads(raw.strip())
    except Exception:
        return {"intent": "CHAT", "directive": user_input}

def get_ebony_response(user_input):
    if not ai_active: return f"Neural link offline. Error: {error_msg}"
    try:
        payload = [{"role": "system", "content": EBONY_PERSONA}]
        for msg in st.session_state.chat_history[-10:]:
            payload.append({"role": msg["role"], "content": msg["content"]})
        payload.append({"role": "user", "content": user_input})
        chat = client.chat.completions.create(messages=payload, model=ACTIVE_MODEL)
        return chat.choices[0].message.content
    except Exception as e: return f"Neural misfire. Error: {e}"

st.markdown("### /// SYSTEM CONTROLS")
if st.button("WIPE MEMORY & RESET", type="primary", use_container_width=True):
    default_msg = [{"role": "assistant", "content": "Memory wiped. Ready."}]
    st.session_state.chat_history = default_msg
    save_memory(default_msg)
    st.rerun()

st.markdown("---")
if "chat_history" not in st.session_state: st.session_state.chat_history = load_memory()

left_screen, right_screen = st.columns(2)

with left_screen:
    st.subheader("/// EXECUTIVE COMMUNICATIONS")
    chat_panel = st.container(height=500, border=True)
    with chat_panel:
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"], avatar="👔" if msg["role"] == "user" else "🟣").write(msg["content"])
    
    with st.form("tactical_comms_form", clear_on_submit=True):
        command = st.text_input("Awaiting Directive:", placeholder="Tell me what you need done in your own words...")
        submitted = st.form_submit_button("SEND COMMAND", use_container_width=True)
        
    if submitted and command:
        st.session_state.chat_history.append({"role": "user", "content": command})
        
        # INTERCEPT AND ROUTE INTENT
        analysis = analyze_intent(command)
        intent = analysis.get("intent", "CHAT")
        
        # --- PREDICTIVE ARCHITECT ---
        if intent == "ARCHITECT":
            target_file = analysis.get("target_file", "new_script.py")
            if not target_file: target_file = "new_script.py"
            directive = analysis.get("directive", command)
            filepath = os.path.join(BASE_DIR, target_file)
            
            current_code = ""
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f: current_code = f.read()
            
            prompt = f"You are an expert Python architect. Modify/Create the file {target_file}. Directive: {directive}\n"
            if current_code: prompt += f"CURRENT CODE:\n{current_code}\n"
            prompt += "\nOUTPUT ONLY RAW CODE. DO NOT WRAP IN ```python TAGS. DO NOT EXPLAIN. NO MARKDOWN."
            
            try:
                chat = client.chat.completions.create(
                    messages=[{"role": "system", "content": "You write raw, production-grade Python code. Only output code."}, {"role": "user", "content": prompt}],
                    model=ACTIVE_MODEL
                )
                raw_code = chat.choices[0].message.content.strip()
                if raw_code.startswith("```python"): raw_code = raw_code[9:]
                elif raw_code.startswith("```"): raw_code = raw_code[3:]
                if raw_code.endswith("```"): raw_code = raw_code[:-3]
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(raw_code.strip())
                    
                st.session_state.chat_history.append({"role": "assistant", "content": f"[PREDICTIVE ARCHITECT]: I understood your intent. I have autonomously forged `{target_file}` and written it to disk."})
            except Exception as e:
                st.session_state.chat_history.append({"role": "assistant", "content": f"[ARCHITECT MISFIRE]: {e}"})

        # --- PREDICTIVE COMMS ---
        elif intent == "DRAFT":
            st.session_state.chat_history.append({"role": "assistant", "content": f"[PREDICTIVE COMMS]: Intent recognized. Drafting payload now..."})
            subprocess.Popen([sys.executable, os.path.join(comms_dir, "comms_core.py"), analysis.get("directive", command), "LinkedIn"])
            time.sleep(2)
                
        # --- STANDARD CONVERSATION ---
        else:
            ebony_reply = get_ebony_response(command)
            st.session_state.chat_history.append({"role": "assistant", "content": ebony_reply})
            
        save_memory(st.session_state.chat_history)
        st.rerun()

with right_screen:
    st.subheader("/// UNIFIED ARCHITECTURE VIEWER")
    viewer_panel = st.container(height=320, border=True)
    with viewer_panel:
        category = st.selectbox("Select Sector:", ["Core Scripts (.py)", "Vault Payloads (.txt)", "Neural Memory (.json)"])
        target_dir = BASE_DIR if category == "Core Scripts (.py)" else vault_dir if "Vault" in category else memory_dir
        ext = '.py' if category == "Core Scripts (.py)" else '.txt' if "Vault" in category else '.json'
        
        if os.path.exists(target_dir):
            files = [f for f in os.listdir(target_dir) if f.endswith(ext)]
            if files:
                sel_file = st.selectbox("Select File:", sorted(files, reverse=True), label_visibility="collapsed")
                with open(os.path.join(target_dir, sel_file), "r", encoding="utf-8") as pf:
                    st.code(pf.read(), language='python' if ext=='.py' else 'text')
            else: st.write("Sector empty.")

    if st.button("REFRESH DASHBOARD", use_container_width=True): st.rerun()
