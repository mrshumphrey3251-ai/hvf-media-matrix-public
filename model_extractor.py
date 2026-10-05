import toml
try:
    path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
    sec = toml.load(path)
    key = sec.get("GROQ_API_KEY", "").strip()
    from groq import Groq
    client = Groq(api_key=key, max_retries=0)
    
    print("[*] Interrogating Groq servers for authorized model registry...")
    models = client.models.list()
    active_models = [m.id for m in models.data]
    print(f"[+] Authorized Models: {', '.join(active_models)}")
    
    if active_models:
        target = active_models[0]
        print(f"[*] Firing live payload at authorized target: {target}...")
        res = client.chat.completions.create(messages=[{"role": "user", "content": "Status check"}], model=target)
        print(f"[+] CLOUD STRIKE SUCCESSFUL using {target}. The Apex is online.")
    else:
        print("[-] FATAL: Groq reports zero authorized models for this key.")
except Exception as e:
    print(f"[-] SYSTEM ERROR: {type(e).__name__} - {str(e)}")
