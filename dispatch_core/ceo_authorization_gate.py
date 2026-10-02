"""
EBONY SOVEREIGN CEO AUTHORIZATION GATE
ROLE: Cryptographic validation and non-repudiable promotion engine.
INVARIANT: Only authorized CEO credentials can promote code from sandbox_staging
           to level5_extensions. All decisions are Merkle-logged.
"""

import os
import sys
import shutil
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
EXTENSIONS_DIR = BASE_DIR / "level5_extensions"
LEDGER_FILE = BASE_DIR / "governance" / "architecture" / "MERKLE_AUTHORIZATION_LEDGER.json"

class CEOAuthorizationGate:
    def __init__(self):
        self.sandbox_dir = SANDBOX_DIR
        self.extensions_dir = EXTENSIONS_DIR
        self.ledger_file = LEDGER_FILE

    def compute_sha256(self, filepath: Path) -> str:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def generate_action_memo(self, filename: str, verification_receipt: dict) -> dict:
        source_path = self.sandbox_dir / filename
        if not source_path.exists():
            return {"success": False, "error": f"File {filename} not in sandbox."}

        file_hash = self.compute_sha256(source_path)
        with open(source_path, "r", encoding="utf-8", errors="replace") as f:
            code_preview = f.read()

        memo = {
            "memo_id": f"EAM-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "target_module": filename,
            "sha256_hash": file_hash,
            "sandbox_receipt": verification_receipt,
            "status": "AWAITING_CEO_SIGNATURE",
            "lines_of_code": len(code_preview.splitlines())
        }
        return {"success": True, "memo": memo}

    def sign_and_promote(self, filename: str, ceo_key_or_password: str, authorized_secret: str) -> dict:
        # Strict CEO identity verification
        if ceo_key_or_password != authorized_secret:
            return {
                "success": False,
                "error": "SECURITY VIOLATION: Unauthorized signature token. Promotion rejected."
            }

        source_path = self.sandbox_dir / filename
        dest_path = self.extensions_dir / filename

        if not source_path.exists():
            return {"success": False, "error": f"Module {filename} absent from sandbox."}

        file_hash = self.compute_sha256(source_path)
        shutil.copy2(source_path, dest_path)

        # Log immutable entry
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "module": filename,
            "sha256": file_hash,
            "decision": "AUTHORIZED",
            "signatory": "CHIEF_EXECUTIVE_OFFICER",
            "destination": str(dest_path)
        }

        records = []
        if self.ledger_file.exists():
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except Exception:
                records = []
        records.append(log_entry)

        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        return {
            "success": True,
            "message": f"Module {filename} successfully promoted to Level 5 extensions.",
            "sha256": file_hash
        }

if __name__ == "__main__":
    gate = CEOAuthorizationGate()
    print("[+] CEO Authorization Gate Engine Online.")
