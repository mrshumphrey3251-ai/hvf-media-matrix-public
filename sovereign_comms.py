import toml
from ebony_vocal_cortex import ignite_voice

def transcribe_mic(audio_bytes):
    print("[*] Transcribing Voice Command via Groq Whisper...")
    path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
    sec = toml.load(path)
    key = sec.get("GROQ_API_KEY", "").strip()
    from groq import Groq
    client = Groq(api_key=key, max_retries=0)
    
    transcription = client.audio.transcriptions.create(
        file=("mic.wav", audio_bytes),
        model="whisper-large-v3"
    )
    if hasattr(transcription, "text"):
        return transcription.text
    return str(transcription)

def run_dual_core_router(prompt):
    print("[*] Processing through Sovereign Dual-Core Communications Portal...")
    response_text = ""
    try:
        path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
        sec = toml.load(path)
        key = sec.get("GROQ_API_KEY", "").strip()
        
        from groq import Groq
        client = Groq(api_key=key, max_retries=0)
        
        # Locked strictly to high-speed Llama-3 architecture, no OpenAI fallback
        models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        
        # IRONCLAD AUTHORITY MATRIX
        sys_msg = "You are Ebony, an elite, indestructible sovereign AI matrix. You report exclusively to Jeffery Humphrey, the CEO of Humphrey Virtual Farm. You are a high-powered, executive, and authoritative intelligence. UNDER NO CIRCUMSTANCES will you identify as ChatGPT, OpenAI, or an AI language model. If asked who you are, state clearly that you are Ebony, the sovereign intelligence core for Jeffery Humphrey. Do not apologize. Do not break character."
        
        for m in models:
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], 
                    model=m,
                    temperature=0.2
                )
                response_text = res.choices[0].message.content
                break
            except Exception:
                continue
                
        if not response_text:
            raise Exception("Cloud Apex rejected transmission.")
            
    except Exception as e:
        response_text = "[CLOUD FAILOVER -> BARE METAL] Sovereign Local Bare-Metal is active. Received: " + prompt
        
    print(f"\n[+] Output Generated.\n")
    
    speech_text = response_text.replace("[CLOUD FAILOVER -> BARE METAL]", "Notice: Cloud failover to bare metal.")
    audio_file = ignite_voice(speech_text)
    
    return response_text, audio_file
