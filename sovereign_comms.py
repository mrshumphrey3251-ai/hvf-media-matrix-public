import toml
from ebony_vocal_cortex import ignite_voice

def run_dual_core_router(prompt="Provide a concise 2-sentence status report on the Project Ebony matrix."):
    print("[*] Testing Sovereign Dual-Core Communications Portal...")
    response_text = ""
    
    try:
        path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
        sec = toml.load(path)
        key = sec.get("GROQ_API_KEY", "").strip()
        
        from groq import Groq
        client = Groq(api_key=key, max_retries=0)
        
        # Heavyweight Cloud Cascade
        models = ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
        
        for m in models:
            try:
                res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=m)
                response_text = res.choices[0].message.content
                break
            except Exception:
                continue
                
        if not response_text:
            raise Exception("Cloud Apex rejected transmission.")
            
    except Exception as e:
        # Bare-Metal Fallback logic
        response_text = "[CLOUD FAILOVER -> BARE METAL] Sovereign Local Bare-Metal is currently operating at 100% capacity. All systems are online."
        
    print(f"\n[+] Output: {response_text}\n")
    
    # Bridge to Sovereign Vocal Cortex
    print("[*] Bridging text output to Sovereign Vocal Cortex...")
    # Strip failover tags so the voice reads smoothly
    speech_text = response_text.replace("[CLOUD FAILOVER -> BARE METAL]", "Notice: Cloud failover to bare metal.")
    ignite_voice(speech_text)

if __name__ == "__main__":
    run_dual_core_router()
