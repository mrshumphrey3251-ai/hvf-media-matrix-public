import os
import sys
import time
import chromadb
from chromadb.utils import embedding_functions

# ==============================================================================
# HUMPHREY VIRTUAL FARMS LLC | 15-VERTICAL SOVEREIGN NEURAL CORE BUILDER
# System: Project Ebony - Public Architectural Blueprint (Sanitized Baseline)
# Authority: Jeffery Humphrey, Founder & CEO
# Compliance: DFARS 252.227-7018 Data Rights Protection (Sanitized Architecture)
# ==============================================================================

CONFIG = {
    "master_dir": os.getenv("HVF_STORAGE_ROOT", "./defense_vault_staged"),
    "db_dir": os.getenv("HVF_CHROMA_DIR", "./chroma_db_public"),
    "collection_name": "hvf_iron_dome_public_blueprint",
    "chunk_size": 1000,
    "chunk_overlap": 150,
    "batch_size": 250,
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

# 15 Sovereign Verticals Taxonomy Schema
PILLAR_MAP = {
    "01": ("pillar_01_agriculture", "Sovereign Precision Agriculture & Soil Mesh"),
    "02": ("pillar_02_logistics", "Autonomous Supply Chain & Edge Logistics"),
    "03": ("pillar_03_defense", "Tactical Defense Systems & Kinetic Interceptors"),
    "04": ("pillar_04_energy", "Distributed Sovereign Microgrids & Energy Storage"),
    "05": ("pillar_05_manufacturing", "Advanced Additive Manufacturing & Edge Tooling"),
    "06": ("pillar_06_communications", "Secure Mesh Comms & Low-Probability Intercept P2P"),
    "07": ("pillar_07_financial", "Cryptographic Financial Ledgers & Autonomous Treasury"),
    "08": ("pillar_08_healthcare", "Edge Triage & Autonomous Biological Monitoring"),
    "09": ("pillar_09_aerospace", "Aerospace Perimeter Defense & High-Altitude Relays"),
    "10": ("pillar_10_civil_engineering", "Resilient Civil Infrastructure & Sub-Surface Fortification"),
    "11": ("pillar_11_mining", "Autonomous Resource Extraction & Geological Recon"),
    "12": ("pillar_12_deep_ocean", "Sub-Surface Maritime Telemetry & Oceanic Sensor Nodes"),
    "13": ("pillar_13_cryptography", "Post-Quantum Cryptographic Primitives & Optical Diodes"),
    "14": ("pillar_14_hydrogen", "Sovereign Hydrogen Generation & Fuel Cell Architecture"),
    "15": ("pillar_15_autonomous_warfare", "Multi-Agent Swarm Orchestration & Air-Gapped Warfare")
}

def classify_vertical(filepath: str):
    path_norm = filepath.replace("\\", "/").lower()
    for prefix, (pillar_id, pillar_name) in PILLAR_MAP.items():
        if f"/{prefix}_" in path_norm or f"docs/{prefix}" in path_norm:
            return pillar_id, pillar_name
    return "core_blueprint", "Sanitized Architectural System"

def clean_text_chunks(text: str, chunk_size: int, overlap: int):
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
    print("HUMPHREY VIRTUAL FARMS LLC - PUBLIC 15-VERTICAL BLUEPRINT COMPILATION")
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
                pillar_id, pillar_name = classify_vertical(filepath)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    chunks = clean_text_chunks(content, CONFIG["chunk_size"], CONFIG["chunk_overlap"])
                    for idx, chunk in enumerate(chunks):
                        doc_ids.append(f"{rel_path}_chunk_{idx}")
                        documents.append(chunk)
                        metadatas.append({
                            "source": rel_path,
                            "pillar_id": pillar_id,
                            "pillar_name": pillar_name,
                            "prime": "HVF_LLC"
                        })
                except Exception as e:
                    print(f"[WARN] Skipped {rel_path}: {e}")

    total_chunks = len(documents)
    if total_chunks == 0:
        print("[INFO] Public staging clean. Ready for public documentation ingestion.")
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