import os
import sys
from datetime import datetime

try:
    from dotenv import load_dotenv
    from groq import Groq
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"[GLOBAL COMMS]: Engine offline. Missing credentials. Error: {e}")
    sys.exit(1)

def generate_comms(topic, comm_type="Email"):
    try:
        prompt = f"Draft an executive {comm_type} regarding: {topic}. Tone must be authoritative, concise, and high-powered. No fluff. No passive language. Sign it as The CEO."
        
        print(f"[GLOBAL COMMS]: Drafting Executive {comm_type} on '{topic}'...")
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Ebony, the CEO's ruthless, highly intelligent executive ghostwriter. You write with supreme authority."},
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-120b",
        )
        
        payload = chat_completion.choices[0].message.content
        
        # Save to content vault
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        vault_dir = os.path.join(base_dir, "content_vault")
        if not os.path.exists(vault_dir):
            os.makedirs(vault_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Executive_{comm_type}_{timestamp}.txt"
        filepath = os.path.join(vault_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(payload)
            
        print(f"[GLOBAL COMMS]: {comm_type} secured in Content Vault as {filename}.")
        return filepath
    except Exception as e:
        print(f"[GLOBAL COMMS]: Misfire. Error: {e}")
        return None

if __name__ == "__main__":
    target_topic = sys.argv[1] if len(sys.argv) > 1 else "Mandatory Q3 Strategic Alignment"
    ctype = sys.argv[2] if len(sys.argv) > 2 else "Email"
    generate_comms(target_topic, ctype)
