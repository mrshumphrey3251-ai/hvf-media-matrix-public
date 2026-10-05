import toml
from groq import Groq

try:
    sec = toml.load(r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml")
    key = sec.get("GROQ_API_KEY", "").strip()
    client = Groq(api_key=key)
    res = client.chat.completions.create(
        messages=[{"role": "user", "content": "Test"}],
        model="llama3-8b-8192"
    )
    print("[+] CLOUD SUCCESS. Response:", res.choices[0].message.content)
except Exception as e:
    print("[-] CLOUD FAILURE EXPOSED. Read the exact error below:")
    print(str(e))
