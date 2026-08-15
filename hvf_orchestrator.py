import logging
import json
import os
from hvf_content_generator import HVFContentGenerator
from hvf_email_node import HVFEmailNode
from hvf_linkedin_node import HVFLinkedInNode

# HVF Media Matrix - Central Orchestrator (Public/Redacted)
# Architecture blueprint for automated data injection and syndication

class HVFOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger("HVF_Orchestrator")
        self.generator = HVFContentGenerator()
        self.email_node = HVFEmailNode()
        self.linkedin_node = HVFLinkedInNode()
        self.stream_path = os.path.join(os.path.dirname(__file__), "ebony_dashboard", "data", "stream.json")

    def execute_matrix_protocol(self):
        self.logger.info("Initiating HVF Media Matrix Protocol...")
        
        # 1. Generate Sanitized Intel
        payload = self.generator.generate_content()
        
        # 2. Inject into Dashboard PWA
        os.makedirs(os.path.dirname(self.stream_path), exist_ok=True)
        with open(self.stream_path, "w", encoding="utf-8") as f:
            json.dump({"status": "ACTIVE", "intel": "[REDACTED PUBLIC ARCHITECTURE DEMO]"}, f, indent=4)
        self.logger.info("Sanitized payload routed to Ebony Dashboard.")
        
        # 3. Syndicate to Outbound Nodes
        self.logger.info("Engaging outbound API syndication nodes...")
        self.email_node.dispatch(payload)
        self.linkedin_node.dispatch(payload)
            
        self.logger.info("Matrix protocol execution sequence complete.")
        return payload

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    orchestrator = HVFOrchestrator()
    orchestrator.execute_matrix_protocol()
