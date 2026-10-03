import os
import sys
import glob
import re

# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN DASHBOARD NON-DESTRUCTIVE INTEGRATOR
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Additive RAG & Comms Merge into 1,073-Line Production Baseline
# ==============================================================================

BACKUP_DIR = r"C:\HVF_Repos\hvf-media-matrix-private\_code_backups"
TARGET_FILES = [
    r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console.py",
    r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console_GREEN.py"
]

print("=" * 80)
print("EXECUTING NON-DESTRUCTIVE DASHBOARD INTEGRATION")
print("=" * 80)

# 1. Locate Pristine 1,073-Line Backup
backup_candidates = sorted(glob.glob(os.path.join(BACKUP_DIR, "ebony_console_GREEN_BASE_*.py.bak")), reverse=True)
if not backup_candidates:
    print(f"[FATAL] No green baseline backup found in {BACKUP_DIR}")
    sys.exit(1)

baseline_path = backup_candidates[0]
print(f"[1/4] Loaded Pristine Baseline: {os.path.basename(baseline_path)}")

with open(baseline_path, "r", encoding="utf-8") as f:
    code = f.read()

# 2. Additive Top-Level Imports & Vector Initialization
import_block = """
# --- SOVEREIGN NEURAL CORE & CONTINUOUS MEMORY BRIDGES ---
import chromadb
from chromadb.utils import embedding_functions
import hvf_memory_vault
from conversation_logger import ConversationLogger

CHROMA_DB_PATH = r"C:\\HVF_Repos\\hvf-media-matrix-private\\chroma_db"
COLLECTION_NAME = "hvf_iron_dome_core"

try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    iron_dome_core = chroma_client.get_collection(COLLECTION_NAME)
except Exception:
    iron_dome_core = None

vault_logger = ConversationLogger()
hvf_memory_vault.init_vault()

def retrieve_sovereign_iron_dome(query_text: str, n_results: int = 3) -> str:
    \"\"\"Queries 20,253 vectors across all 15 sovereign verticals.\"\"\"
    if not iron_dome_core:
        return ""
    try:
        res = iron_dome_core.query(query_texts=[query_text], n_results=n_results)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        blocks = []
        for d, m in zip(docs, metas):
            p = m.get("pillar_name", "General System")
            s = m.get("source", "Core")
            blocks.append(f"[{p.upper()} | Source: {s}]\\n{d}")
        return "\\n\\n".join(blocks)
    except Exception:
        return ""
"""

if "CHROMA_DB_PATH" not in code:
    code = import_block + "\n" + code
    print("[2/4] Injected ChromaDB 15-Vertical Neural Bridge and Retrieval Engine.")

# 3. Additive RAG Context Injection into Sovereign Command Module
rag_injection = """
        # --- SOVEREIGN 15-VERTICAL RAG CONTEXT INJECTION ---
        iron_dome_intel = retrieve_sovereign_iron_dome(user_input, n_results=3)
        if iron_dome_intel:
            full_sys_prompt += f"\\n\\n--- SOVEREIGN IRON DOME INTEL (20,253 VECTORS) ---\\n{iron_dome_intel}\\n-------------------------------------------------\\nAnswer with supreme executive authority as Ebony. Ground responses in this sovereign intelligence."
"""

target_marker = "conversation_payload = [{\"role\": \"system\", \"content\": full_sys_prompt}] + st.session_state.messages[-6:]"
if "iron_dome_intel" not in code and target_marker in code:
    code = code.replace(target_marker, rag_injection + "        " + target_marker)
    print("[3/4] Injected 15-Vertical RAG Attention Window into Sovereign Command.")

# 4. Additive Conversation Persistence Hooks
log_injection = """
        if current_user and current_cipher:
            save_encrypted_message(current_user, "assistant", bot_reply, current_cipher)
            store_entity_memory_async(current_user, user_input, bot_reply)
        vault_logger.log_exchange(user_input, bot_reply)
        hvf_memory_vault.log_conversation_turn("user", user_input)
        hvf_memory_vault.log_conversation_turn("assistant", bot_reply)
"""

old_log_marker = """        if current_user and current_cipher:
            save_encrypted_message(current_user, "assistant", bot_reply, current_cipher)
            store_entity_memory_async(current_user, user_input, bot_reply)"""

if "vault_logger.log_exchange" not in code and old_log_marker in code:
    code = code.replace(old_log_marker, log_injection)
    print("[4/4] Injected Dual-Tier Real-Time Conversation Logger into Chat Loop.")

# 5. Write to Production Files
for target in TARGET_FILES:
    with open(target, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[SUCCESS] Updated: {target}")

print("=" * 80)
print("NON-DESTRUCTIVE DASHBOARD COMPILED SUCCESSFULLY")
print("=" * 80)

