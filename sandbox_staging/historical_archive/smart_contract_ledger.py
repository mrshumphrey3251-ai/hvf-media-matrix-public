"""
=============================================================================
HVF MEDIA MATRIX : SMART-CONTRACT LEDGER (TARGET BRAVO)
CLASSIFICATION   : PRIVATE_UNREDACTED
VERSION          : 1.0.0
AUTHOR           : JEFFERY HUMPHREY (CEO / FOUNDER)
=============================================================================
DIRECTIVE:
Cryptographic gatekeeper enforcing the Sovereign Commercial JV Framework.
Forces digital signature and hashes agreement to the 52% control baseline
prior to system access. Logs to isolated legal database.
=============================================================================
"""

import os
import sqlite3
import hashlib
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEGAL_DB = os.path.join(BASE_DIR, "hvf_legal_ledger.db")

# The absolute baseline agreement
CORE_AGREEMENT_TEXT = "I acknowledge and agree that HVF Omni-Industrial Matrix (HVF) retains 52% operational control, Master IP Root Custody, and final executive authority over this Joint Venture and all deployed architectures."

def ensure_legal_ledger():
    """Initializes the secure SQL ledger for all cryptographic legal agreements."""
    conn = sqlite3.connect(LEGAL_DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jv_smart_contracts (
            signature_id TEXT PRIMARY KEY,
            client_username TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            agreement_text TEXT NOT NULL,
            cryptographic_hash TEXT NOT NULL,
            status TEXT DEFAULT 'EXECUTED'
        )
    """)
    conn.commit()
    conn.close()

def generate_signature_hash(username: str, timestamp: str, agreement: str) -> str:
    """Generates an immutable cryptographic hash of the execution."""
    raw_payload = f"{username}|{timestamp}|{agreement}|HVF_MASTER_ROOT"
    return hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

def execute_smart_contract(client_username: str):
    """
    Executes the digital signature, hashes the payload, and commits to the ledger.
    """
    ensure_legal_ledger()
    
    timestamp = datetime.utcnow().isoformat()
    sig_hash = generate_signature_hash(client_username, timestamp, CORE_AGREEMENT_TEXT)
    sig_id = f"SIG-{sig_hash[:12].upper()}"

    # Log to Sovereign Legal Database
    conn = sqlite3.connect(LEGAL_DB)
    cur = conn.cursor()
    
    # Check if already signed to prevent duplicates
    cur.execute("SELECT signature_id FROM jv_smart_contracts WHERE client_username=?", (client_username,))
    if cur.fetchone():
        return {"STATUS": "REJECTED", "REASON": "Client has already executed this contract."}

    cur.execute(
        "INSERT INTO jv_smart_contracts (signature_id, client_username, timestamp, agreement_text, cryptographic_hash) VALUES (?, ?, ?, ?, ?)",
        (sig_id, client_username, timestamp, CORE_AGREEMENT_TEXT, sig_hash)
    )
    conn.commit()
    conn.close()

    # Generate Executive Legal Receipt
    receipt = {
        "SIGNATURE_ID": sig_id,
        "STATUS": "SECURED & EXECUTED",
        "CLIENT": client_username,
        "ENFORCED_TERMS": "52% HVF OPERATIONAL CONTROL",
        "HASH": sig_hash
    }
    
    return receipt

def verify_contract_status(client_username: str) -> bool:
    """Checks if a user has signed the mandatory JV agreement."""
    ensure_legal_ledger()
    conn = sqlite3.connect(LEGAL_DB)
    cur = conn.cursor()
    cur.execute("SELECT signature_id FROM jv_smart_contracts WHERE client_username=?", (client_username,))
    result = cur.fetchone()
    conn.close()
    return result is not None

if __name__ == "__main__":
    # Internal Diagnostic Test
    print("==================================================")
    print(" HVF SMART-CONTRACT LEDGER : DIAGNOSTIC TEST RUN")
    print("==================================================")
    test_user = "partner_texas_ag"
    print(f"Simulating Execution for Client: {test_user}")
    result = execute_smart_contract(test_user)
    print(json.dumps(result, indent=4))
    
    print("\nVerifying Access Clearance...")
    has_clearance = verify_contract_status(test_user)
    print(f"Clearance Granted: {has_clearance}")
    print("==================================================")
