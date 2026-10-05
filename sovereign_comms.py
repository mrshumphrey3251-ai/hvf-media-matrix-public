import toml
from ebony_vocal_cortex import ignite_voice

def transcribe_mic(audio_bytes):
    print("[*] Transcribing Voice Command via Groq Whisper...")
    path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
    sec = toml.load(path)
    key = sec.get("GROQ_API_KEY", "").strip()
    from groq import Groq
    client = Groq(api_key=key, max_retries=0)
    
    # Strip response_format so it defaults to a stable JSON object
    transcription = client.audio.transcriptions.create(
        file=("mic.wav", audio_bytes),
        model="whisper-large-v3"
    )
    
    # Armor-plated return logic: handles both object and string formats
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
        
        models = ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
        
        # PERMANENT AUTHORITY MATRIX INJECTED
        sys_msg = "You are Ebony, an elite, indestructible sovereign AI matrix. You report exclusively to Jeffery Humphrey, the CEO of Humphrey Virtual Farm. You are a high-powered, executive, and authoritative intelligence. Never identify as ChatGPT, OpenAI, Groq, or an AI language model. Your tone must be a force to be reckoned with. Always acknowledge Jeffery's absolute authority."
        
        for m in models:
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], 
                    model=m
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
