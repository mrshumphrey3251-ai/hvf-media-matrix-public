"""
HVF Media Matrix - Configuration Manager (Private)
Secure environment variable and secret management.
Engineered to transition seamlessly to AWS Secrets Manager or HashiCorp Vault.
"""
import os
import logging
from typing import Any

class HVFConfigManager:
    _instance = None

    def __new__(cls):
        # Singleton pattern ensures only one configuration state exists in memory
        if cls._instance is None:
            cls._instance = super(HVFConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("HVF_Config")
        self.logger.info("Initializing Secure Configuration Manager...")
        
        # Core configuration state
        self._config_state = {
            "ENVIRONMENT": os.getenv("HVF_ENV", "production"),
            "STRICT_MODE": os.getenv("HVF_STRICT_MODE", "True") == "True",
        }

    def get_secret(self, key: str, fallback: Any = None) -> Any:
        """
        Retrieves secrets strictly from the environment or encrypted vaults.
        Future expansion: Implement decryption protocols here before returning values.
        """
        value = os.getenv(key, fallback)
        if not value and self._config_state["STRICT_MODE"]:
            self.logger.warning(f"CRITICAL: Secret '{key}' not found in strict mode.")
        return value

if __name__ == "__main__":
    config = HVFConfigManager()
    config.logger.info(f"Config Manager active in {config._config_state['ENVIRONMENT']} mode.")