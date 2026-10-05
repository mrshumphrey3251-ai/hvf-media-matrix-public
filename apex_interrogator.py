import toml
try:
    path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
    sec = toml.load(path)
    key = sec.get("GROQ_API_KEY", "").strip()
    from groq import Groq
    client = Groq(api_key=key, max_retries=0)
    
    models = ["llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    for m in models:
        print(f"[*] Testing production model: {m}...")
        try:
            client.chat.completions.create(messages=[{"role": "user", "content": "Test"}], model=m)
            print(f"[+] {m} is ONLINE.")
        except Exception as e:
            print(f"[-] {m} FAILED: {type(e).__name__} - {str(e)}")
except Exception as e:
    print(f"[-] SYSTEM ERROR: {e}")
