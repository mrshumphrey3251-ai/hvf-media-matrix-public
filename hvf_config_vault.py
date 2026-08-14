import os
import logging

# Forcing terminal output for executive oversight
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

class ConfigVault:
    """
    HVF Universal Configuration Vault.
    Maintains absolute security across Public and Private repositories.
    """
    def __init__(self):
        self.logger = logging.getLogger("HVF_Vault")
        # Set to False in the private repository
        self.PUBLIC_MODE = True 
        
        self.settings = self._initialize_vault()

    def _initialize_vault(self):
        base_config = {
            "SYSTEM_VERSION": "8.f.1",
            "ENCRYPTION_LEVEL": "AES-256",
            "MAX_CONCURRENCY": 100
        }

        if self.PUBLIC_MODE:
            base_config["API_KEY"] = "REDACTED_FOR_PUBLIC_REPO"
            base_config["DB_STRING"] = "REDACTED_FOR_PUBLIC_REPO"
            self.logger.info("Vault operating in PUBLIC mode. Sensitive data locked.")
        else:
            base_config["API_KEY"] = os.getenv("HVF_PRIVATE_API_KEY", "NOT_SET")
            base_config["DB_STRING"] = os.getenv("HVF_PRIVATE_DB_STRING", "NOT_SET")
            self.logger.info("Vault operating in PRIVATE mode. Systems armed.")

        return base_config

    def get(self, key):
        return self.settings.get(key, None)

if __name__ == "__main__":
    vault = ConfigVault()
    print(f"Vault Status: {vault.settings['SYSTEM_VERSION']}")