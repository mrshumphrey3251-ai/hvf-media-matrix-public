import os
import sys
import requests
from datetime import datetime

try:
    from dotenv import load_dotenv
    from groq import Groq
    load_dotenv(override=True)
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"[EBONY LAUNCH]: Engine offline. Error: {e}")
    sys.exit(1)

def deploy_to_linkedin(topic):
    # 1. Generate the payload
    print(f"[EBONY LAUNCH]: Engine locked. Generating payload for: {topic}")
    prompt = f"Draft an executive LinkedIn post about: {topic}. Tone must be authoritative, concise, and high-powered. No fluff. Include this contact info at the bottom: \nContact: humphreyvirtualfarm@gmail.com\nGitHub Open-Source Matrix: https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public"
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the CEO's executive AI ghostwriter. Write with supreme authority."},
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-120b",
        )
        payload_text = chat_completion.choices[0].message.content
    except Exception as e:
        print(f"[EBONY LAUNCH]: Generation misfire. Error: {e}")
        return False

    # 2. Secure a local copy
    base_dir = os.path.dirname(os.path.abspath(__file__))
    vault_dir = os.path.join(base_dir, "content_vault")
    os.makedirs(vault_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(vault_dir, f"LinkedIn_Strike_{timestamp}.txt")
    
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(payload_text)
        
    print(f"[EBONY LAUNCH]: Payload drafted and secured locally: {backup_path}")

    # 3. Broadcast to LinkedIn
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.getenv("LINKEDIN_AUTHOR_URN")
    
    if author_urn:
        author_urn = author_urn.strip()
    
    if not access_token or not author_urn:
        print("[EBONY LAUNCH]: SECURE MODE. LinkedIn API keys missing in .env file. Payload saved to vault but NOT broadcasted.")
        return False

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202401",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": payload_text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    try:
        response = requests.post(url, headers=headers, json=post_data)
        if response.status_code == 201:
            print("[EBONY LAUNCH]: STRIKE SUCCESSFUL. Payload is live on the LinkedIn feed.")
            return True
        else:
            print(f"[EBONY LAUNCH]: STRIKE FAILED. Target Defended. Code: {response.status_code}. Error: {response.text}")
            return False
    except Exception as e:
        print(f"[EBONY LAUNCH]: CRITICAL SYSTEM ERROR during broadcast: {e}")
        return False

if __name__ == "__main__":
    target_topic = sys.argv[1] if len(sys.argv) > 1 else "The reality of leadership on the shop floor vs the boardroom."
    deploy_to_linkedin(target_topic)
