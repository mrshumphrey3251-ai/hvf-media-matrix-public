import os
import sys
import chromadb
from chromadb.utils import embedding_functions

# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN NEURAL CORE DIAGNOSTIC PROBE
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8)
# System: Project Ebony Iron Dome Memory Verification
# ==============================================================================

DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db"
COLLECTION_NAME = "hvf_iron_dome_core"

def run_diagnostics():
    print("=" * 80)
    print("PROJECT EBONY: NEURAL RETRIEVAL & COMMON KNOWLEDGE AUDIT")
    print(f"Target Database: {DB_PATH}")
    print(f"Active Collection: {COLLECTION_NAME}")
    print("=" * 80)

    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database directory not found at {DB_PATH}")
        sys.exit(1)

    client = chromadb.PersistentClient(path=DB_PATH)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()

    try:
        collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)
    except Exception as e:
        print(f"[ERROR] Unable to load collection '{COLLECTION_NAME}': {e}")
        sys.exit(1)

    total_vectors = collection.count()
    print(f"[SUCCESS] Core Connected. Total Registered Vectors: {total_vectors}\n")

    # TEST BATTERY
    test_cases = [
        {
            "tier": "TEST 1: PRIME SOVEREIGNTY & DATA RIGHTS",
            "query": "HVF Omni-Industrial Matrix Prime Contractor CAGE 1AHA8 DFARS 252.227-7018 sovereign technical data rights",
            "n_results": 2
        },
        {
            "tier": "TEST 2: EDGE HYPERVISOR & LATENCY BENCHMARKS",
            "query": "Bare-metal hypervisor AF_XDP sub-5ms hardware eviction zero-latency drone swarm architecture",
            "n_results": 2
        },
        {
            "tier": "TEST 3: NEGATIVE TRAP PROBE (AGRICULTURAL ISOLATION)",
            "query": "soil moisture dielectric drone sensor GLI vegetative index crop yield irrigation",
            "n_results": 2
        }
    ]

    for test in test_cases:
        print("-" * 80)
        print(f">>> {test['tier']}")
        print(f"Query: \"{test['query']}\"")
        print("-" * 80)

        results = collection.query(
            query_texts=[test["query"]],
            n_results=test["n_results"]
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0] if "distances" in results else [0.0] * len(docs)

        for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
            source = meta.get("source", "Unknown Source")
            chunk_idx = meta.get("chunk_index", "N/A")
            preview = doc.strip().replace("\n", " ")[:200]
            print(f"  [Match {i + 1}] Distance: {dist:.4f} | Source: {source} (Chunk {chunk_idx})")
            print(f"  Snippet: \"{preview}...\"\n")

    print("=" * 80)
    print("AUDIT COMPLETE - REVIEW MATCH SOURCES AND DISTANCE SCORES")
    print("=" * 80)

if __name__ == "__main__":
    run_diagnostics()

