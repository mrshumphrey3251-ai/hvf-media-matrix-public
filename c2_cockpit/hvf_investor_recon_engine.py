import logging
import os
import json
from datetime import datetime

class InvestorReconEngine:
    """
    HVF Proprietary Investor Reconnaissance Engine.
    Engineered for dynamic database ingestion and strict executive filtering.
    """
    def __init__(self):
        self.logger = logging.getLogger("HVF_Recon")
        self.logger.info("Investor Reconnaissance Engine initialized. Standing by for targeting parameters.")
        self.api_client = None 
        self.target_queue = []
        
        self.filter_parameters = {
            "primary_keywords": ["SCADA", "Edge AI", "Industrial Control", "Series A", "Automation", "Series B"],
            "exclusion_keywords": ["Crypto", "Consumer SaaS", "Web3"],
            "minimum_fund_size_mm": 50
        }
        
        self.db_path = os.path.join(os.path.dirname(__file__), 'hvf_target_matrix.json')

    def run(self, payload_data=None):
        target_sector = payload_data.get("target_sector", "SCADA Edge AI Integration") if payload_data else "SCADA Edge AI Integration"
        return self.execute_recon_sequence(target_sector)

    def execute_recon_sequence(self, target_sector="SCADA Edge AI Integration"):
        self.logger.info("Executing Tactical Reconnaissance Sequence...")
        self.logger.info(f"[LOCK ACQUIRED] Scanning intelligence database for sector: {target_sector}")
        
        if not os.path.exists(self.db_path):
            self.logger.error(f"Intelligence database missing at {self.db_path}. Aborting scan.")
            return []
            
        try:
            # UPGRADED: 'utf-8-sig' safely consumes the hidden Windows BOM.
            with open(self.db_path, 'r', encoding='utf-8-sig') as f:
                raw_targets = json.load(f)
                
            self.logger.info(f"Ingested {len(raw_targets)} raw targets from matrix. Commencing filtration protocol.")
            
            for target in raw_targets:
                if target.get("fund_size_mm", 0) < self.filter_parameters["minimum_fund_size_mm"]:
                    self.logger.info(f"Target Dropped: {target['entity_name']} - Insufficient Capital.")
                    continue
                    
                target_keywords = target.get("keywords", [])
                if any(bad_word in target_keywords for bad_word in self.filter_parameters["exclusion_keywords"]):
                    self.logger.info(f"Target Dropped: {target['entity_name']} - Triggered exclusion filter.")
                    continue
                    
                target["acquisition_timestamp"] = datetime.utcnow().isoformat()
                target["status"] = "QUEUED_FOR_ENGAGEMENT"
                self.target_queue.append(target)
                self.logger.info(f"Target structurally verified and queued: {target['entity_name']}")

        except Exception as e:
            self.logger.error(f"Critical failure reading intelligence database: {str(e)}")

        self.logger.info(f"Reconnaissance complete. High-value targets locked in queue: {len(self.target_queue)}")
        return self.target_queue

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    engine = InvestorReconEngine()
    engine.run()
