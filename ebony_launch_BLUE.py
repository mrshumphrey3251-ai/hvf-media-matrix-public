import os
from dotenv import load_dotenv
from groq import Groq

def execute_strike():
    print("==================================================")
    print("⚡ PERMANENT STRIKE PAYLOAD (MODULAR ARCHITECTURE) ⚡")
    print("==================================================")
    
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("[CRITICAL FAILURE]: GROQ_API_KEY not found in the vault.")
        return

    client = Groq(api_key=api_key)
    
    # Dynamic Executive Prompt
    prompt = """
    You are the CEO of a high-powered tech automation matrix. 
    Write a hard-hitting, 3-paragraph LinkedIn post about the brutal reality of building automation systems from scratch. 
    Focus on resilience, the necessity of cutting through corporate noise, and refusing to settle for "good enough" when the system fails. 
    Tone: Unfiltered, highly authoritative, executive. No hashtags. No emojis. Pure impact.
    """
    
    # Extensible design: Cycles through engines automatically to prevent future code rewrites
    target_models = ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama3-8b-8192"]
    active_engine = None
    
    for model_id in target_models:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_id
            )
            print(f"[SYSTEM]: Engine locked onto active model: {model_id}")
            print("\n--------------------------------------------------")
            print(response.choices[0].message.content)
            print("--------------------------------------------------")
            print("\n[SYSTEM]: Payload generated dynamically. Code rewrite is no longer required.")
            active_engine = model_id
            break
        except Exception:
            continue
            
    if not active_engine:
        print("\n[CRITICAL FAILURE]: Groq rejected all primary text engines. API Key limits may be exhausted.")

if __name__ == "__main__":
    execute_strike()
