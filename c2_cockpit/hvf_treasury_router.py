"""
=============================================================================
HVF MEDIA MATRIX : AUTOMATED TREASURY ROUTING ENGINE
CLASSIFICATION   : PRIVATE_UNREDACTED
VERSION          : 1.0.0
AUTHOR           : JEFFERY HUMPHREY (CEO / FOUNDER)
=============================================================================
DIRECTIVE:
Intercept gross revenue and automatically route allocations based on the 
Sovereign Commercial JV Framework (30/15/15/40 split). 
=============================================================================
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# --- SOVEREIGN TREASURY MATRIX ALLOCATIONS ---
# These are locked and non-negotiable per the Master Registry.
ALLOCATION_TAX_ESCROW = Decimal('0.30')
ALLOCATION_OPEX = Decimal('0.15')
ALLOCATION_CAPEX = Decimal('0.15')
ALLOCATION_FOUNDER = Decimal('0.40')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TREASURY_DB = os.path.join(BASE_DIR, "hvf_treasury_ledger.db")

def ensure_treasury_ledger():
    """Initializes the secure SQL ledger for all treasury routing events."""
    conn = sqlite3.connect(TREASURY_DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS treasury_routing_log (
            transaction_id TEXT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            gross_revenue_usd REAL NOT NULL,
            tax_escrow_usd REAL NOT NULL,
            opex_usd REAL NOT NULL,
            capex_usd REAL NOT NULL,
            founder_dist_usd REAL NOT NULL,
            source_description TEXT
        )
    """)
    conn.commit()
    conn.close()

def generate_tx_hash(timestamp_str: str, gross_amount: str) -> str:
    """Generates a secure cryptographic hash for the transaction."""
    raw = f"{timestamp_str}|{gross_amount}|HVF_TREASURY_ROOT"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def execute_treasury_routing(gross_revenue: float, source_description: str = "Standard Income"):
    """
    Executes the rigid 30/15/15/40 split on gross revenue and logs to the ledger.
    """
    ensure_treasury_ledger()
    
    # Convert to Decimal for absolute financial precision (no floating point errors)
    gross = Decimal(str(gross_revenue))
    
    tax_escrow = (gross * ALLOCATION_TAX_ESCROW).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    opex = (gross * ALLOCATION_OPEX).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    capex = (gross * ALLOCATION_CAPEX).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    founder = (gross * ALLOCATION_FOUNDER).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Validate mathematical integrity
    total_allocated = tax_escrow + opex + capex + founder
    if total_allocated != gross:
        # Failsafe adjustment to founder distribution to catch fractional penny rounding
        founder += (gross - total_allocated)

    timestamp = datetime.utcnow().isoformat()
    tx_id = f"TX-{generate_tx_hash(timestamp, str(gross))[:12].upper()}"

    # Log to Sovereign Database
    conn = sqlite3.connect(TREASURY_DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO treasury_routing_log (transaction_id, timestamp, gross_revenue_usd, tax_escrow_usd, opex_usd, capex_usd, founder_dist_usd, source_description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (tx_id, timestamp, float(gross), float(tax_escrow), float(opex), float(capex), float(founder), source_description)
    )
    conn.commit()
    conn.close()

    # Generate Executive Receipt
    receipt = {
        "TRANSACTION_ID": tx_id,
        "STATUS": "ROUTED & SECURED",
        "GROSS_REVENUE": f"${gross:,.2f}",
        "TAX_ESCROW_30": f"${tax_escrow:,.2f}",
        "OPEX_15": f"${opex:,.2f}",
        "CAPEX_15": f"${capex:,.2f}",
        "FOUNDER_DIST_40": f"${founder:,.2f}"
    }
    
    return receipt

if __name__ == "__main__":
    # Internal Diagnostic Test
    print("==================================================")
    print(" HVF TREASURY ROUTER : DIAGNOSTIC TEST RUN")
    print("==================================================")
    test_amount = 10000.00
    print(f"Simulating Gross Revenue: ${test_amount:,.2f}")
    result = execute_treasury_routing(test_amount, "Phase 9 Diagnostic Run")
    print(json.dumps(result, indent=4))
    print("==================================================")