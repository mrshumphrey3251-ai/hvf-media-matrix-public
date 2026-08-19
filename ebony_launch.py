import os
import random
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

def execute_strike():
    print("==================================================")
    print("⚡ BLUE DEV: DYNAMIC ARSENAL + CALIBRATED ENGINES ⚡")
    print("==================================================")
    
    topics = [
        "the brutal reality of building automation systems from scratch and refusing to settle.",
        "why third-party API limits are a liability and the push for sovereign, locally-hosted AI.",
        "the difference between theoretical leadership and actually executing in the trenches.",
        "why eliminating middle-management bottlenecks is critical for operational velocity.",
        "the strategic pivot from generic automated content to high-impact digital warfare."
    ]
    
    selected_topic = random.choice(topics)
    print(f"[SYSTEM]: Ammunition loaded. Target topic: {selected_topic}")
    print("[SYSTEM]: Engaging Groq Neural Core...")
    
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("[CRITICAL FAILURE]: GROQ_API_KEY not found in the vault.")
        return

    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are the CEO of a high-powered tech automation matrix. 
    Write a hard-hitting, 3-paragraph LinkedIn post about {selected_topic}
    Focus on raw execution, cutting through corporate noise, and absolute authority. 
    Tone: Unfiltered, executive, sharp. No hashtags. No emojis. Pure impact.
    """
    
    # EXACT ENGINES PULLED FROM YOUR CONSOLE READOUT
    target_models = ["openai/gpt-oss-120b", "qwen/qwen3.6-27b", "openai/gpt-oss-20b"]
    active_engine = None
    
    for model_id in target_models:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_id
            )
            
            ai_content = response.choices[0].message.content
            
            signature = "\n\n---\n"
            signature += "Contact: humphreyvirtualfarm@gmail.com\n"
            signature += "GitHub Open-Source Matrix: https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public"
            
            post_content = ai_content + signature
            
            print(f"\n[SYSTEM]: Engine locked onto active model: {model_id}")
            print("[SYSTEM]: Executive signature stamped.")
            
            os.makedirs("content_vault", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join("content_vault", f"Blue_Strike_{timestamp}.txt")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(post_content)
                
            print("\n--------------------------------------------------")
            print(post_content)
            print("--------------------------------------------------")
            print(f"\n[SYSTEM]: Payload secured in vault: {filepath}")
            active_engine = model_id
            break
        except Exception as e:
            print(f"[SYSTEM]: Engine {model_id} misfire. Retrying next...")
            continue
            
    if not active_engine:
        print("\n[CRITICAL FAILURE]: Groq rejected the calibrated text engines. Check API token limits.")

if __name__ == "__main__":
    execute_strike()
