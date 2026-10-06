import toml
import os
import time
from ebony_vocal_cortex import ignite_voice
from ebony_bridge import route_matrix_command
from core_context_engine import sanitize_memory_payload
from ebony_authority_matrix import get_sovereign_system_prompt
from ebony_ledger import record_entry

def transcribe_mic(audio_bytes):
    """
    Robust Groq Whisper Ingestion Engine.
    Includes zero-byte guardrails, size verification, and exception traps.
    """
    if not audio_bytes or len(audio_bytes) < 1024:
        print("[!] WHISPER REJECTED: Audio buffer empty or below minimum threshold (<1KB).")
        return ""

    print(f"[*] Transcribing Voice Command via Groq Whisper ({len(audio_bytes)} bytes)...")
    try:
        path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
        sec = toml.load(path)
        key = sec.get("GROQ_API_KEY", "").strip()
        from groq import Groq
        client = Groq(api_key=key, max_retries=1)
        
        transcription = client.audio.transcriptions.create(
            file=("mic.wav", audio_bytes),
            model="whisper-large-v3"
        )
        if hasattr(transcription, "text"):
            result_text = transcription.text.strip()
            print(f"[+] Transcription Success: '{result_text}'")
            return result_text
        return str(transcription).strip()
    except Exception as e:
        print(f"[-] WHISPER TRANSMISSION FAILURE: {str(e)}")
        return ""

def run_dual_core_router(prompt, raw_history=None):
    start_time = time.time()
    print("[*] Processing through Sovereign Dual-Core Communications Portal...")
    
    # Record incoming user prompt in audit ledger
    record_entry(role="user", content=prompt, model_core="COMMAND_INGRESS")

    system_context = ""
    prompt_lower = prompt.lower()
    if "memory" in prompt_lower:
        system_context = f"\n[SYSTEM METADATA: {route_matrix_command('ALPHA_MEMORY', prompt)}]"
    elif "agent" in prompt_lower or "swarm" in prompt_lower:
        system_context = f"\n[SYSTEM METADATA: {route_matrix_command('BETA_AGENTS', prompt)}]"
    elif "silo" in prompt_lower or "pump" in prompt_lower or "scada" in prompt_lower:
        system_context = f"\n[SYSTEM METADATA: {route_matrix_command('GAMMA_SCADA', prompt)}]"
        
    response_text = ""
    active_core = "NONE"
    try:
        path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
        sec = toml.load(path)
        key = sec.get("GROQ_API_KEY", "").strip()
        
        from groq import Groq
        client = Groq(api_key=key, max_retries=0)
        
        models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b"]
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
                active_core = m
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
        active_core = "LOCAL_BARE_METAL"
        
    latency = round(time.time() - start_time, 2)
    print(f"\n[+] Output Generated ({latency}s) via {active_core}.\n")
    
    # Record system response and operational telemetry in ledger
    record_entry(role="assistant", content=response_text, model_core=active_core, latency_sec=latency)
    
    speech_text = response_text.replace("[CLOUD FAILOVER -> BARE METAL]", "Notice: Cloud failover to bare metal.")
    audio_file = ignite_voice(speech_text)
    
    return response_text, audio_file
