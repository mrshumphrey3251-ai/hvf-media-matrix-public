import os
import sys
import time
import chromadb
from chromadb.utils import embedding_functions

# ==============================================================================
# HUMPHREY VIRTUAL FARMS LLC | SOVEREIGN NEURAL CORE BUILDER
# System: Project Ebony - Bare-Metal Defense RAG Indexer (Sanitized Blueprint)
# Authority: Jeffery Humphrey, Founder & CEO
# Compliance: DFARS 252.227-7018 Data Rights Protection (Redacted Public Baseline)
# ==============================================================================

# Modular Configuration - Extensible for external staging
CONFIG = {
    "master_dir": os.getenv("HVF_STORAGE_ROOT", "./defense_vault_staged"),
    "db_dir": os.getenv("HVF_CHROMA_DIR", "./chroma_db_public"),
    "collection_name": "hvf_iron_dome_sanitized",
    "chunk_size": 1000,
    "chunk_overlap": 150,
    "batch_size": 250,  # Micro-batching threshold to prevent ONNX thread lock
    "valid_extensions": [".md", ".txt", ".json", ".py", ".yaml", ".yml", ".rst"],
    "ignore_directories": [
        ".git",
        ".github",
        "__pycache__",
        "venv",
        ".venv",
        "chroma_db",
        "_archive",
        "_quarantine"
    ]
}

def clean_text_chunks(text: str, chunk_size: int, overlap: int):
    """Slices text into deterministic, overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def build_neural_core():
    print("=" * 80)
    print("HUMPHREY VIRTUAL FARMS LLC - PUBLIC BLUEPRINT COMPILATION")
    print(f"Collection: {CONFIG['collection_name']}")
    print("=" * 80)

    os.makedirs(CONFIG["db_dir"], exist_ok=True)
    client = chromadb.PersistentClient(path=CONFIG["db_dir"])
    embed_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=CONFIG["collection_name"],
        embedding_function=embed_fn,
        metadata={"system": "Project Ebony", "classification": "Sanitized Public Architecture"}
    )

    doc_ids, documents, metadatas = [], [], []

    for root, dirs, files in os.walk(CONFIG["master_dir"]):
        dirs[:] = [d for d in dirs if d not in CONFIG["ignore_directories"]]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in CONFIG["valid_extensions"]:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, CONFIG["master_dir"])
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    chunks = clean_text_chunks(content, CONFIG["chunk_size"], CONFIG["chunk_overlap"])
                    for idx, chunk in enumerate(chunks):
                        doc_ids.append(f"{rel_path}_chunk_{idx}")
                        documents.append(chunk)
                        metadatas.append({"source": rel_path, "chunk_index": idx, "prime": "HVF_LLC"})
                except Exception as e:
                    print(f"[WARN] Skipped {rel_path}: {e}")

    total_chunks = len(documents)
    if total_chunks == 0:
        print("[INFO] No staged documents discovered. Staging directory clean.")
        return

    batch_size = CONFIG["batch_size"]
    total_batches = (total_chunks + batch_size - 1) // batch_size

    for b in range(total_batches):
        b_start = b * batch_size
        b_end = min(b_start + batch_size, total_chunks)
        collection.upsert(
            ids=doc_ids[b_start:b_end],
            documents=documents[b_start:b_end],
            metadatas=metadatas[b_start:b_end]
        )
        print(f"Committed batch [{b + 1}/{total_batches}]")

if __name__ == "__main__":
    build_neural_core()