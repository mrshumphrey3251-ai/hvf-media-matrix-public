"""
HVF Media Matrix - Core Application Entry Point (Private)
Master initialization sequence for the entire HVF Matrix architecture.
Binds Audit, Config, Database, Auth, Analytics, Media, and launches the live API.
"""
import logging
import uvicorn
from audit import HVFAuditCore
from config import HVFConfigManager
from database import HVFDatabaseConnector
from auth import HVFAuthGateway
from analytics import HVFAnalyticsOrchestrator
from media_processing import HVFMediaOrchestrator
from api import api_app

class HVFMatrixCore:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - HVF_CORE - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("HVF_Matrix_Main")
        self.system_active = False

    def ignite_matrix(self) -> bool:
        """
        Strict top-down boot sequence.
        Engineered to fail securely if any single subsystem is compromised.
        """
        # 1. Spin up the Black Box Flight Recorder absolute first
        self.audit = HVFAuditCore()
        self.audit.log_event("SYSTEM_BOOT", "Initiating HVF Media Matrix Boot Sequence...")
        self.logger.info("INITIATING HVF MEDIA MATRIX BOOT SEQUENCE...")
        
        try:
            # 2. Initialize Configuration Vault & Persistent Memory
            self.config = HVFConfigManager()
            self.database = HVFDatabaseConnector()
            if not self.database.establish_connection():
                raise RuntimeError("Database connection pool failed to initialize.")

            # 3. Initialize Perimeter Defense
            self.auth_gateway = HVFAuthGateway()
            
            # 4. Initialize Core Operation Subsystems
            self.analytics = HVFAnalyticsOrchestrator()
            self.media = HVFMediaOrchestrator()
            
            # Execute Subsystem Boot Sequences
            if not self.analytics.boot_sequence():
                raise RuntimeError("Analytics Subsystem failed to boot.")
                
            if not self.media.boot_pipeline():
                raise RuntimeError("Media Subsystem failed to boot.")
                
            self.system_active = True
            self.audit.log_event("SYSTEM_ONLINE", "HVF MEDIA MATRIX IS SECURE. IGNITING API SERVER.")
            self.logger.info("MATRIX BOOT COMPLETE. IGNITING LIVE API SERVER...")
            
            # 5. Ignite the Live Web Server (Blocking Call)
            uvicorn.run(api_app, host="0.0.0.0", port=8000)
            
            return True
            
        except Exception as e:
            self.audit.log_critical_breach("SYSTEM_BOOT", f"Matrix Halted: {e}")
            self.logger.critical(f"SYSTEM BOOT FAILURE. MATRIX HALTED: {e}")
            self.system_active = False
            return False

if __name__ == "__main__":
    core = HVFMatrixCore()
    core.ignite_matrix()
