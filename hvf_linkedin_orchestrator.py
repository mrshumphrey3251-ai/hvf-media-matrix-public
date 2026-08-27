import logging
import os
from datetime import datetime
from google import genai
from hvf_linkedin_node import HVFLinkedInNode

# HVF Media Matrix - Dedicated LinkedIn Orchestrator
# Engineered for the 4-Hour Autonomous Cadence (Next-Gen SDK)

class HVFLinkedInOrchestrator:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("HVF_LinkedIn_Cadence")
        self.linkedin_node = HVFLinkedInNode()
        
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        api_key = None
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break
        
        self.client = None
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                self.logger.error(f"Client init error: {e}")
        else:
            self.logger.error("CRITICAL: GEMINI_API_KEY missing from vault.")

    def execute_cadence(self):
        self.logger.info("Initiating 4-Hour LinkedIn Cadence...")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        article = "Leadership requires continuous innovation. HVF Matrix 4-Hour Cadence Active."
        if self.client:
            try:
                prompt = "You are the Executive AI for Humphrey Virtual Farm. Write a high-value, long-form professional LinkedIn article about leadership, innovation, and digital architecture. Do not include hashtags. Return ONLY the article text."
                response = self.client.models.generate_content(model='gemini-flash-latest', contents=prompt)
                article = response.text.strip()
            except Exception as e:
                self.logger.error(f"AI Generation Failed: {e}")
            
        final_payload = f"{article}\n\n[AUTONOMOUS 4-HOUR CADENCE FIRED: {current_time}]"
        
        self.logger.info("Engaging LinkedIn Node...")
        self.linkedin_node.dispatch(final_payload)
        self.logger.info("LinkedIn 4-Hour Cadence sequence complete.")

if __name__ == "__main__":
    orchestrator = HVFLinkedInOrchestrator()
    orchestrator.execute_cadence()
