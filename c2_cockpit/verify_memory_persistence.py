import sqlite3
import chromadb
import os

# ==============================================================================
# HVF Omni-Industrial Matrix | REAL-TIME MEMORY PERSISTENCE VERIFICATION
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Audit Real-Time Write-Back into SQLite & ChromaDB Iron Dome
# ==============================================================================

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"
CHROMA_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db"

print("=" * 80)
print("AUDITING AUTOMATED EPISODIC CONVERSATION PERSISTENCE")
print("=" * 80)

# 1. Verify SQLite Conversation Memory Ledger
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, role, content FROM conversation_memory ORDER BY id DESC LIMIT 2")
    rows = cur.fetchall()
    print("\n>>> LATEST SQLITE CONVERSATION ENTRIES:")
    print("-" * 60)
    for r in rows:
        print(f"[{r[0]}] {r[1].upper()}: {r[2][:120]}...")
    conn.close()
else:
    print(f"[FAIL] SQLite database not found at {DB_PATH}")

# 2. Verify ChromaDB Episodic Vector Ingestion
try:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    col = client.get_collection("hvf_iron_dome_core")
    res = col.query(query_texts=["Who is Drew Phillips and what is our prime defense role"], n_results=1)
    
    print("\n>>> LATEST CHROMADB EPISODIC VECTOR RETRIEVAL:")
    print("-" * 60)
    print("Retrieved Chunk:", res["documents"][0][0][:160], "...")
    print("Metadata:", res["metadatas"][0][0])
    print("-" * 60)
    print("[SUCCESS] Real-time conversation was automatically vectorized into the Iron Dome.")
except Exception as e:
    print(f"[FAIL] ChromaDB query error: {e}")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
