import logging
from hvf_content_generator import HVFContentGenerator
from hvf_email_node import HVFEmailNode
from hvf_linkedin_node import HVFLinkedInNode
import json
import os

# HVF Media Matrix - Central Orchestrator
# Engineered for multi-stream payload routing

class HVFOrchestrator:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("HVF_Orchestrator")
        self.generator = HVFContentGenerator()
        self.email_node = HVFEmailNode()
        self.linkedin_node = HVFLinkedInNode()
        self.dashboard_path = os.path.join(os.path.dirname(__file__), "ebony_dashboard", "data", "stream.json")

    def execute_matrix_protocol(self):
        self.logger.info("Initiating HVF Media Matrix Protocol...")
        
        # Extract the splintered dictionary from the Cognitive Core
        payloads = self.generator.generate_content()
        
        # 1. Route Tactical Intel to Dashboard
        os.makedirs(os.path.dirname(self.dashboard_path), exist_ok=True)
        with open(self.dashboard_path, "w", encoding="utf-8") as f:
            json.dump({"intel": payloads["dashboard"]}, f)
        self.logger.info("Unredacted dashboard payload secured and routed to Ebony Dashboard.")
        
        # 2. Route Executive & Long-Form Intel to Outbound Nodes
        self.logger.info("Engaging outbound API syndication nodes...")
        self.email_node.send_email(payloads["email"])
        self.linkedin_node.post_to_linkedin(payloads["linkedin"])
        
        self.logger.info("Matrix protocol execution sequence complete.")

if __name__ == "__main__":
    orchestrator = HVFOrchestrator()
    orchestrator.execute_matrix_protocol()
