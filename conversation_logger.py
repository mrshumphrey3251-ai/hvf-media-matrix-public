import os
import threading
from datetime import datetime

class ConversationLogger:
    """
    Thread‑safe logger that appends each user‑assistant exchange to a designated log file.
    The log format is:
        [TIMESTAMP] USER: <message>
        [TIMESTAMP] ASSISTANT: <message>
    """
    _lock = threading.Lock()

    def __init__(self, log_path: str = "conversation_log.txt"):
        self.log_path = os.path.abspath(log_path)
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _write_line(self, line: str):
        with self._lock, open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def log_user(self, message: str):
        timestamp = datetime.utcnow().isoformat()
        self._write_line(f"[{timestamp}] USER: {message}")

    def log_assistant(self, message: str):
        timestamp = datetime.utcnow().isoformat()
        self._write_line(f"[{timestamp}] ASSISTANT: {message}")

    def log_exchange(self, user_msg: str, assistant_msg: str):
        """Convenience method to log a full turn."""
        self.log_user(user_msg)
        self.log_assistant(assistant_msg)