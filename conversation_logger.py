"""
================================================================================
HVF SOVEREIGN MEDIA MATRIX - REAL-TIME CONVERSATION LOGGER (PUBLIC BLUEPRINT)
System: Project Ebony - High-Concurrency Interaction Pipeline
Authority: Jeffery Humphrey, Founder & CEO
Compliance: DFARS 252.227-7018 Data Rights Protection (Sanitized Architecture)
================================================================================
"""

import os
import threading
from datetime import datetime
import hvf_memory_vault

class ConversationLogger:
    _lock = threading.Lock()

    def __init__(self, log_path: str = "conversation_log.txt"):
        self.log_path = os.path.abspath(log_path)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        hvf_memory_vault.init_vault()

    def _write_file(self, line: str):
        with self._lock, open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def log_user(self, message: str):
        timestamp = datetime.utcnow().isoformat()
        self._write_file(f"[{timestamp}] USER: {message}")
        threading.Thread(
            target=hvf_memory_vault.log_conversation_turn,
            args=("user", message),
            daemon=True
        ).start()

    def log_assistant(self, message: str):
        timestamp = datetime.utcnow().isoformat()
        self._write_file(f"[{timestamp}] ASSISTANT: {message}")
        threading.Thread(
            target=hvf_memory_vault.log_conversation_turn,
            args=("assistant", message),
            daemon=True
        ).start()

    def log_exchange(self, user_msg: str, assistant_msg: str):
        self.log_user(user_msg)
        self.log_assistant(assistant_msg)

if __name__ == "__main__":
    logger = ConversationLogger()
    print("Conversation Logger initialized.")