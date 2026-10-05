import toml
from ebony_vocal_cortex import ignite_voice

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
        response_text = "[CLOUD FAILOVER -> BARE METAL] Sovereign Local Bare-Metal is active. Received: " + prompt
        
    print(f"\n[+] Output Generated.\n")
    
    speech_text = response_text.replace("[CLOUD FAILOVER -> BARE METAL]", "Notice: Cloud failover to bare metal.")
    ignite_voice(speech_text)
    
    # Critical patch: Hand the text back to the Streamlit UI
    return response_text

if __name__ == "__main__":
    run_dual_core_router("Provide a concise 1-sentence status report.")
