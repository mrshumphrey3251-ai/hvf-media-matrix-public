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
    import chromadb
    from conversation_logger import ConversationLogger
    
    load_dotenv(override=True)
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key) if groq_api_key else None
    ai_active = True if client else False
    error_msg = "" if client else "GROQ_API_KEY not configured."
except Exception as e:
    ai_active = False
    error_msg = str(e)

ACTIVE_MODEL = os.getenv("HVF_ACTIVE_MODEL", "openai/gpt-oss-120b")
CHROMA_DB_PATH = os.getenv("HVF_CHROMA_DIR", "./chroma_db_public")
COLLECTION_NAME = "hvf_iron_dome_public_blueprint"

try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    iron_dome_collection = chroma_client.get_collection(COLLECTION_NAME)
except Exception:
    iron_dome_collection = None

logger = ConversationLogger()

st.set_page_config(page_title="Ebony | Tactical Command HUD (Public Blueprint)", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050A15; }
    .stApp, p, span, div { color: #E2E8F0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3 { color: #00D2FF !important; letter-spacing: 1.5px; }
    .stChatMessage { background-color: #111827 !important; border: 1px solid #1F2937 !important; border-radius: 12px; padding: 15px; margin-bottom: 12px; }
    .stButton>button { background-color: #00D2FF; color: #000000 !important; font-weight: 900; border-radius: 6px; border: none; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ EBONY: TACTICAL COMMAND HUD [PUBLIC BLUEPRINT]")

EBONY_PERSONA = """You are Ebony, an executive defense AI for Humphrey Virtual Farms LLC. 
You write with authoritative precision. Address the user as Boss."""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
memory_dir = os.path.join(BASE_DIR, "memory_core")
os.makedirs(memory_dir, exist_ok=True)
MEMORY_FILE = os.path.join(memory_dir, "neural_memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except Exception: pass
    return [{"role": "assistant", "content": "Sovereign matrix blueprint active. Ready, Boss."}]

def save_memory(history):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    except Exception: pass

def retrieve_iron_dome_context(query: str, n_results: int = 2) -> str:
    if not iron_dome_collection: return ""
    try:
        results = iron_dome_collection.query(query_texts=[query], n_results=n_results)
        docs = results.get("documents", [[]])[0]
        return "\n\n".join(docs)
    except Exception: return ""

def get_ebony_response(user_input):
    if not ai_active: return f"Neural link offline: {error_msg}"
    try:
        context = retrieve_iron_dome_context(user_input)
        system_content = EBONY_PERSONA
        if context: system_content += f"\n\n--- ARCHITECTURAL CONTEXT ---\n{context}\n----------------------------"
        payload = [{"role": "system", "content": system_content}]
        for msg in st.session_state.chat_history[-6:]:
            payload.append({"role": msg["role"], "content": msg["content"]})
        payload.append({"role": "user", "content": user_input})
        chat = client.chat.completions.create(messages=payload, model=ACTIVE_MODEL, temperature=0.2)
        return chat.choices[0].message.content
    except Exception as e: return f"Misfire: {e}"

if "chat_history" not in st.session_state: 
    st.session_state.chat_history = load_memory()

st.subheader("/// EXECUTIVE COMMUNICATIONS")
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

with st.form("comms_form", clear_on_submit=True):
    cmd = st.text_input("Awaiting Directive:")
    submit = st.form_submit_button("SEND", use_container_width=True)

if submit and cmd:
    st.session_state.chat_history.append({"role": "user", "content": cmd})
    reply = get_ebony_response(cmd)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    logger.log_exchange(cmd, reply)
    save_memory(st.session_state.chat_history)
    st.rerun()