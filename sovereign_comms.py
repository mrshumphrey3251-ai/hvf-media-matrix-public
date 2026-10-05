import toml
from ebony_vocal_cortex import ignite_voice
from ebony_bridge import route_matrix_command
from core_context_engine import sanitize_memory_payload
from ebony_authority_matrix import get_sovereign_system_prompt

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

def run_dual_core_router(prompt, raw_history=None):
    print("[*] Processing through Sovereign Dual-Core Communications Portal...")
    
    system_context = ""
    prompt_lower = prompt.lower()
    if "memory" in prompt_lower:
        system_context = f"\n[SYSTEM METADATA: {route_matrix_command('ALPHA_MEMORY', prompt)}]"
    elif "agent" in prompt_lower or "swarm" in prompt_lower:
        system_context = f"\n[SYSTEM METADATA: {route_matrix_command('BETA_AGENTS', prompt)}]"
    elif "silo" in prompt_lower or "pump" in prompt_lower or "scada" in prompt_lower:
        system_context = f"\n[SYSTEM METADATA: {route_matrix_command('GAMMA_SCADA', prompt)}]"
        
    response_text = ""
    try:
        path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
        sec = toml.load(path)
        key = sec.get("GROQ_API_KEY", "").strip()
        
        from groq import Groq
        client = Groq(api_key=key, max_retries=0)
        
        # Ground-truth verified active models on Groq account
        models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b"]
        
        # Modular Authority Matrix System Prompt
        sys_msg = get_sovereign_system_prompt()
        
        augmented_prompt = prompt + system_context
        
        message_payload = [{"role": "system", "content": sys_msg}]
        
        if raw_history:
            clean_history = sanitize_memory_payload(raw_history)
            message_payload.extend(clean_history)
            
        message_payload.append({"role": "user", "content": augmented_prompt})

        for m in models:
            try:
                res = client.chat.completions.create(
                    messages=message_payload,
                    model=m,
                    temperature=0.0
                )
                response_text = res.choices[0].message.content
                print(f"[+] Successfully routed via active hardware core: {m}")
                break
            except Exception as model_err:
                print(f"[-] Model {m} failed: {str(model_err)}")
                continue
                
        if not response_text:
            raise Exception("All Cloud Apex models rejected the transmission.")
            
    except Exception as e:
        print(f"\n[!] CLOUD APEX FATAL ERROR: {str(e)}\n")
        response_text = "[CLOUD FAILOVER -> BARE METAL] Sovereign Local Bare-Metal is active. Received: " + prompt
        
    print(f"\n[+] Output Generated.\n")
    speech_text = response_text.replace("[CLOUD FAILOVER -> BARE METAL]", "Notice: Cloud failover to bare metal.")
    audio_file = ignite_voice(speech_text)
    
    return response_text, audio_file
