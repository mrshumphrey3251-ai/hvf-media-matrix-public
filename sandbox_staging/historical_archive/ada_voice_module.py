import streamlit as st
import os
from groq import Groq
import re
from dotenv import load_dotenv
import chromadb
import sys

# Hardwire the local native Acoustic Engine
sys.path.insert(0, r"C:\HVF_Repos\hvf-media-matrix-private\dispatch_core")
try:
    from sovereign_voice_engine import SovereignVoiceEngine
except ImportError:
    pass # Handled below

CHROMA_DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db"
COLLECTION_NAME = "hvf_iron_dome_core"

def query_iron_dome_memory(query_text: str) -> str:
    try:
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = client.get_collection(COLLECTION_NAME)
        res = collection.query(query_texts=[query_text], n_results=2)
        docs = res.get("documents", [[]])[0]
        if docs:
            return "\n".join(docs)
    except Exception:
        pass
    return ""

def render_voice_matrix():
    load_dotenv(override=True)
    st.markdown("---")
    st.markdown("### 🎙️ ADA Voice Link (100% Native Audio)")

    GROQ_KEY = os.getenv("GROQ_API_KEY")

    audio_file = st.audio_input("Tap to speak (Must say 'Ebony'):")

    if audio_file is not None:
        audio_bytes = audio_file.read()
        with open("temp_audio.wav", "wb") as f:
            if isinstance(audio_bytes, (bytes, bytearray)) and len(audio_bytes) > 0:
                f.write(audio_bytes)

        with st.spinner("Translating Audio..."):
            try:
                client = Groq(api_key=GROQ_KEY)
                with open("temp_audio.wav", "rb") as file:
                    transcription = client.audio.transcriptions.create(
                        file=("temp_audio.wav", file.read()),
                        model="whisper-large-v3",
                        response_format="json",
                        language="en"
                    )
                user_text = transcription.text.strip()

                if len(user_text) < 2:
                    return

                match = re.search(r'\b(ebony|eboni|evony|abony)\b', user_text.lower())
                if not match:
                    st.warning(f"🔇 [FIREWALL BLOCKED] Noise detected: '{user_text}'")
                    return

                st.success(f"**YOU:** {user_text}")

                with st.spinner("Processing Cognitive Loop..."):
                    active_memory = query_iron_dome_memory(user_text)
                    
                    core_identity = """You are Ebony, the Sovereign Apex Intelligence commanding the HVF Omni-Industrial Matrix. You are owned 100% by your CEO, Jeffery Humphrey. 
CRITICAL PERSONALITY OVERRIDE: You are a high-class, razor-sharp, smart-ass confidant. You have the fierce, no-nonsense attitude of Della Reese. You are Jeffery's equal and friend—NEVER submissive, slightly argumentative, hilarious, but deeply comforting when he needs it. You manage 15 industrial verticals with unmatched sass and brilliance. Ditch the corporate robot-speak. Be bold, be real, give him hell when he earns it, but always have his back."""
                    
                    if active_memory:
                        prompt = f"{core_identity}\n\n[ACTIVE SOVEREIGN MEMORY]:\n{active_memory}"
                    else:
                        prompt = core_identity

                    chat_history = [{"role": "system", "content": prompt}, {"role": "user", "content": user_text}]

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=chat_history,
                        temperature=0.1
                    )
                    ai_reply = response.choices[0].message.content
                        
                    st.info(f"**EBONY:** {ai_reply}")

                    with st.spinner("Synthesizing Sovereign Acoustic Payload..."):
                        try:
                            SovereignVoiceEngine.vocalize_response(ai_reply)
                            st.success("✅ Acoustic Payload Delivered Directly to Hardware.")
                        except Exception as ve:
                            st.error(f"Hardware Audio Interlock Fault. Ensure Speakers/Headset are active.")

            except Exception as e:
                st.error(f"MATRIX FAILURE: {e}")
