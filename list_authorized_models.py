import os
from google import genai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
OUTPUT_PATH = os.path.join(BASE_DIR, "authorized_models_list.txt")

api_key = None
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY="):
                api_key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                break

if not api_key:
    print("[!] No GEMINI_API_KEY found in .env.")
    exit(1)

try:
    client = genai.Client(api_key=api_key)
    print("=" * 60)
    print("QUERYING GOOGLE GEMINI API FOR AUTHORIZED MODELS...")
    print("=" * 60)
    
    models = list(client.models.list())
    
    output_lines = []
    output_lines.append(f"TOTAL MODELS DISCOVERED: {len(models)}\n")
    print(f"[*] Total Models Discovered: {len(models)}\n")
    
    for m in models:
        m_name = getattr(m, 'name', 'Unknown')
        m_display = getattr(m, 'display_name', '')
        m_methods = getattr(m, 'supported_generation_methods', []) or getattr(m, 'supported_actions', [])
        line_str = f"Model ID: {m_name} | Display: {m_display} | Methods: {m_methods}"
        print(line_str)
        output_lines.append(line_str)
        
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
        out.write("\n".join(output_lines))
        
    print("\n" + "=" * 60)
    print(f"[+] Full model list saved to: {OUTPUT_PATH}")
    print("=" * 60)

except Exception as e:
    print(f"[!] Direct API Query Error: {e}")
