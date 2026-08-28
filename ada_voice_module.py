import streamlit as st
import os
import requests
from groq import Groq
import base64
import re
from dotenv import load_dotenv

def render_voice_matrix():
    load_dotenv(override=True)
    st.markdown("---")
    st.markdown("### 🎙️ ADA Voice Link")
    
    GROQ_KEY = os.getenv("GROQ_API_KEY")
    EL_KEY = os.getenv("ELEVENLABS_API_KEY")
    EL_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
    
    audio_file = st.audio_input("Tap to speak (Must say 'Ebony'):")
    
    if audio_file is not None:
        audio_bytes = audio_file.read()
        with open("temp_audio.wav", "wb") as f:
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
                
                with st.spinner("Processing..."):
                    prompt = "You are Ebony, an elite AI agronomist for Humphrey Virtual Farms. The CEO is speaking to you. Respond concisely and authoritatively."
                    chat_history = [{"role": "system", "content": prompt}, {"role": "user", "content": user_text}]
                    
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=chat_history,
                        temperature=0.4
                    )
                    ai_reply = response.choices[0].message.content
                    st.info(f"**EBONY:** {ai_reply}")
                        
                    with st.spinner("Synthesizing..."):
                        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{EL_VOICE_ID}"
                        headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": EL_KEY}
                        data = {"text": ai_reply, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
                        
                        tts_response = requests.post(tts_url, json=data, headers=headers)
                        if tts_response.status_code == 200:
                            with open("response.mp3", "wb") as f:
                                f.write(tts_response.content)
                            with open("response.mp3", "rb") as f:
                                audio_b64 = base64.b64encode(f.read()).decode()
                            audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_b64}"></audio>'
                            st.markdown(audio_html, unsafe_allow_html=True)
                        else:
                            st.error("Audio Synthesis Failed.")
            except Exception as e:
                st.error(f"MATRIX FAILURE: {e}")
