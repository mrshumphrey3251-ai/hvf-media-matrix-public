import logging
import os
from datetime import datetime

# 1. Establish Secure Logging Vault (Public Blueprint)
# Note: The 'logs' directory is git-ignored to protect HVF operational data.
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"patrol_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("HVF_Patrol")
logger.info("Autonomous Patrol Matrix (Public Blueprint) initializing...")
logger.info("Logging infrastructure established. Core execution logic and payload delivery [REDACTED].")
