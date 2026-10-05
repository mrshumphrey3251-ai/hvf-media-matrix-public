import toml, os
try:
    env_key = os.environ.get("GROQ_API_KEY")
    if env_key:
        print(f"[-] WARNING: Ghost Environment Variable found overriding the vault: {env_key[:8]}...")
    
    path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
    sec = toml.load(path)
    vault_key = sec.get("GROQ_API_KEY", "").strip()
    print(f"[*] Vault Key loaded: {vault_key[:8]}...")
    
    from groq import Groq
    client = Groq(api_key=vault_key, max_retries=0)
    print("[*] Striking Cloud Apex with Llama-3.3...")
    res = client.chat.completions.create(messages=[{"role": "user", "content": "Test"}], model="llama-3.3-70b-versatile")
    print("[+] CLOUD STRIKE SUCCESSFUL. The Apex is online.")
except Exception as e:
    print(f"[-] ERROR EXPOSED: {type(e).__name__} - {str(e)}")
