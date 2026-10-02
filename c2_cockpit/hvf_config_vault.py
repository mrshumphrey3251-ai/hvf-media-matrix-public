import os
import logging
from dotenv import load_dotenv

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
        self.PUBLIC_MODE = False

        # Load the classified local vault into system memory
        if not self.PUBLIC_MODE:
            load_dotenv()
            self.logger.info("Local `.env` vault successfully digested into memory.")

        self.settings = self._initialize_vault()

    def _initialize_vault(self):
        base_config = {
            "SYSTEM_VERSION": "8.f.1",
            "ENCRYPTION_LEVEL": "AES-256",
            "MAX_CONCURRENCY": 100
        }

        if self.PUBLIC_MODE:
            base_config["LINKEDIN_CLIENT_ID"] = "REDACTED_FOR_PUBLIC_REPO"
            base_config["LINKEDIN_CLIENT_SECRET"] = "REDACTED_FOR_PUBLIC_REPO"
            base_config["LINKEDIN_ACCESS_TOKEN"] = "REDACTED_FOR_PUBLIC_REPO"
            self.logger.info("Vault operating in PUBLIC mode. Sensitive data locked.")
        else:
            base_config["LINKEDIN_CLIENT_ID"] = os.getenv("LINKEDIN_CLIENT_ID", "NOT_SET")
            base_config["LINKEDIN_CLIENT_SECRET"] = os.getenv("LINKEDIN_CLIENT_SECRET", "NOT_SET")
            base_config["LINKEDIN_ACCESS_TOKEN"] = os.getenv("LINKEDIN_ACCESS_TOKEN", "NOT_SET")
            self.logger.info("Vault operating in PRIVATE mode. Credentials armed.")

        return base_config

    def get(self, key):
        return self.settings.get(key, None)

if __name__ == "__main__":
    vault = ConfigVault()
    print(f"\n--- VAULT DIAGNOSTIC ---")
    print(f"System Version: {vault.get('SYSTEM_VERSION')}")
    print(f"LinkedIn Client ID Loaded: {'YES' if vault.get('LINKEDIN_CLIENT_ID') != 'NOT_SET' else 'NO'}")
    print(f"LinkedIn Client Secret Loaded: {'YES' if vault.get('LINKEDIN_CLIENT_SECRET') != 'NOT_SET' else 'NO'}")