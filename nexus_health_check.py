"""
PRIVATE NEXUS HEALTH CHECK
--------------------------

Purpose:
    • Verify that the bare‑metal “Heavy Iron” edge hardware is online.
    • Confirm that all core modules (sync engine, vault manager, crypto core,
      transport protocol, payload scanner) can be imported and instantiated.
    • Run a quick self‑test of the HVFSwarmMatrix handshake and vault
      accessibility.
    • Log detailed diagnostics to the internal log directory.

NOTE:
    This script is for internal use only. It contains absolute filesystem
    paths and may expose cryptographic keys if printed; do **NOT** publish it
    outside the private repo.
"""

import os
import sys
import logging
from datetime import datetime

# ----------------------------------------------------------------------
# 1. BASIC ENVIRONMENT SETUP
# ----------------------------------------------------------------------
# Hard‑code the absolute path to the private HVF core so the script can locate
# the modules even when the working directory is different.
PRIVATE_CORE_PATH = r"C:\Users\mrshu\HVF_MEDIA_MATRIX\HVF_SYNC_CORE"
if PRIVATE_CORE_PATH not in sys.path:
    sys.path.append(PRIVATE_CORE_PATH)

# Configure a verbose logger that writes to the private logs folder.
LOG_DIR = r"C:\Users\mrshu\HVF_MEDIA_MATRIX\CINEMATIC_VAULT\logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"nexus_health_{datetime.utcnow():%Y%m%d_%H%M%S}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def _import_module(module_name: str):
    """Attempt to import a module and return (module, error)."""
    try:
        __import__(module_name)
        logging.info(f"✅ Imported {module_name}")
        return sys.modules[module_name], None
    except Exception as exc:
        logging.error(f"❌ Failed to import {module_name}: {exc}")
        return None, exc

# ----------------------------------------------------------------------
# 2. CORE MODULE IMPORT VALIDATION
# ----------------------------------------------------------------------
core_modules = [
    "hvf_sync_engine",      # HVFSwarmMatrix, HVFSyncNode
    "hvf_vault_manager",    # HVFVault
    "hvf_crypto_core",      # HVFCryptoCore
    "hvf_transport_protocol", # HVFTransportProtocol
    "hvf_payload_scanner",  # HVFPayloadScanner
]

imports = {}
for mod in core_modules:
    imports[mod], err = _import_module(mod)
    if err:
        raise SystemExit("Critical import failure – aborting health check.")

# ----------------------------------------------------------------------
# 3. COMPONENT INSTANTIATION & BASIC SELF‑TESTS
# ----------------------------------------------------------------------
try:
    # Matrix & node sanity
    matrix = imports["hvf_sync_engine"].HVFSwarmMatrix()
    node   = imports["hvf_sync_engine"].HVFSyncNode("NEXUS_HEALTH", "127.0.0.1")
    matrix.add_node(node)
    logging.info("✅ HVFSwarmMatrix instantiated and test node added.")

    # Crypto core sanity (demo key – internal only)
    crypto = imports["hvf_crypto_core"].HVFCryptoCore("HVF_SECURE_ALPHA_KEY_992")
    test_msg = b"HealthCheck"
    encrypted = crypto.encrypt(test_msg)
    decrypted = crypto.decrypt(encrypted)
    assert decrypted == test_msg
    logging.info("✅ HVFCryptoCore encrypt/decrypt cycle succeeded.")

    # Vault accessibility
    vault_path = r"C:\Users\mrshu\HVF_MEDIA_MATRIX\CINEMATIC_VAULT"
    vault = imports["hvf_vault_manager"].HVFVault(vault_path)
    if vault.is_accessible():
        logging.info(f"✅ Vault reachable at {vault_path}")
    else:
        logging.warning("⚠️ Vault reported inaccessible – check permissions.")

    # Transport protocol ping
    transport = imports["hvf_transport_protocol"].HVFTransportProtocol()
    ping_res = transport.ping(node.address)
    if ping_res:
        logging.info(f"✅ Transport protocol ping to {node.address} succeeded.")
    else:
        logging.warning(f"⚠️ Transport ping to {node.address} failed.")

    # Payload scanner sanity check (dry‑run)
    scanner = imports["hvf_payload_scanner"].HVFPayloadScanner()
    dummy_payload = b"dummy"
    scan_res = scanner.scan(dummy_payload)
    logging.info(f"✅ Payload scanner returned: {scan_res}")

except Exception as e:
    logging.exception(f"❌ Health‑check aborted due to unexpected error: {e}")
    raise SystemExit("Health‑check failed.") from e

# ----------------------------------------------------------------------
# 4. FINAL REPORT
# ----------------------------------------------------------------------
logging.info("=== NEXUS HEALTH CHECK COMPLETE – ALL SYSTEMS NOMINAL ===")
print("\n=== NEXUS HEALTH CHECK COMPLETE – SEE LOG FILE FOR DETAILS ===")
print(f"Log file: {log_file}")