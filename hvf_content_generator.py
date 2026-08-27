import json
import os
from google import genai

# HVF Media Matrix - Content Generator Node
# Engineered for Next-Gen Google GenAI SDK and Future-Proof Model Routing

class HVFContentGenerator:
    def __init__(self):
        self.api_key = self._load_key()
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def _load_key(self):
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        return line.strip().split("=", 1)[1]
        return None

    def generate_content(self):
        payloads = {
            "dashboard": "System Online. Matrix operational.",
            "email": "Executive Briefing: Matrix Nominal.",
            "linkedin": "Innovation drives the Humphrey Virtual Farm Matrix."
        }
        if self.client:
            try:
                dash_prompt = "You are Ebony, Executive AI for Humphrey Virtual Farm. Write a 2-sentence tactical status update for the CEO's dashboard."
                dash_res = self.client.models.generate_content(model='gemini-flash-latest', contents=dash_prompt)
                payloads["dashboard"] = dash_res.text.strip()
                
                email_prompt = "Write a professional executive summary email updating stakeholders on the status of HVF automated systems."
                email_res = self.client.models.generate_content(model='gemini-flash-latest', contents=email_prompt)
                payloads["email"] = email_res.text.strip()
                
                li_prompt = "Write a high-value, long-form professional LinkedIn article about leadership and automation. No hashtags."
                li_res = self.client.models.generate_content(model='gemini-flash-latest', contents=li_prompt)
                payloads["linkedin"] = li_res.text.strip()
            except Exception as e:
                print(f"Content Gen Error: {e}")
        return payloads
