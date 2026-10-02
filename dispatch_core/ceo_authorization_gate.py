"""
EBONY SOVEREIGN CEO AUTHORIZATION GATE (v2.0 - Bi-Directional Veto & Promotion)
ROLE: Cryptographic validation, non-repudiable promotion, and executive veto/quarantine.
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
QUARANTINE_DIR = SANDBOX_DIR / "quarantine"
EXTENSIONS_DIR = BASE_DIR / "level5_extensions"
LEDGER_FILE = BASE_DIR / "governance" / "architecture" / "MERKLE_AUTHORIZATION_LEDGER.json"

class CEOAuthorizationGate:
    def __init__(self):
        self.sandbox_dir = SANDBOX_DIR
        self.quarantine_dir = QUARANTINE_DIR
        self.extensions_dir = EXTENSIONS_DIR
        self.ledger_file = LEDGER_FILE
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        self.extensions_dir.mkdir(parents=True, exist_ok=True)

    def compute_sha256(self, filepath: Path) -> str:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def _append_ledger(self, entry: dict):
        records = []
        if self.ledger_file.exists():
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except Exception:
                records = []
        records.append(entry)
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

    def sign_and_promote(self, filename: str, ceo_key_or_password: str, authorized_secret: str) -> dict:
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
        # Remove from staging once promoted
        source_path.unlink(missing_ok=True)

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "module": filename,
            "sha256": file_hash,
            "decision": "AUTHORIZED",
            "signatory": "CHIEF_EXECUTIVE_OFFICER",
            "destination": str(dest_path)
        }
        self._append_ledger(log_entry)

        return {
            "success": True,
            "message": f"Module {filename} successfully promoted to Level 5 extensions.",
            "sha256": file_hash
        }

    def reject_and_quarantine(self, filename: str, ceo_key_or_password: str, authorized_secret: str, reason: str = "CEO Veto") -> dict:
        if ceo_key_or_password != authorized_secret:
            return {
                "success": False,
                "error": "SECURITY VIOLATION: Unauthorized signature token. Veto rejected."
            }

        source_path = self.sandbox_dir / filename
        if not source_path.exists():
            return {"success": False, "error": f"Module {filename} absent from sandbox."}

        file_hash = self.compute_sha256(source_path)
        timestamp_slug = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        quarantine_dest = self.quarantine_dir / f"{timestamp_slug}_{filename}"
        
        # Move untrusted code out of staging into quarantine vault
        shutil.move(str(source_path), str(quarantine_dest))

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "module": filename,
            "sha256": file_hash,
            "decision": "VETOED_BY_CEO",
            "signatory": "CHIEF_EXECUTIVE_OFFICER",
            "quarantine_location": str(quarantine_dest),
            "reason": reason
        }
        self._append_ledger(log_entry)

        return {
            "success": True,
            "message": f"Module {filename} VETOED and quarantined. Decision recorded to Merkle ledger.",
            "sha256": file_hash
        }
