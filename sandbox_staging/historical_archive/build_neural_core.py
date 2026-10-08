import os
import sys
import time
import chromadb
from chromadb.utils import embedding_functions

# ==============================================================================
# HVF Omni-Industrial Matrix | 15-VERTICAL SOVEREIGN NEURAL CORE BUILDER
# System: Project Ebony - Multi-Tenant Sovereign Vertical Architecture
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# Compliance: DFARS 252.227-7018 Data Rights Protection
# ==============================================================================

CONFIG = {
    "master_dir": r"C:\HVF_Repos",
    "db_dir": r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db",
    "collection_name": "hvf_iron_dome_core",
    "chunk_size": 1000,
    "chunk_overlap": 150,
    "batch_size": 250,
    "valid_extensions": [".md", ".txt", ".json", ".py", ".yaml", ".yml", ".rst"],
    "ignore_directories": [
        ".git",
        ".github",
        ".streamlit",
        "__pycache__",
        "venv",
        ".venv",
        "env",
        "node_modules",
        "chroma_db",
        "_chroma_db_legacy_backup",
        "_quarantine_legacy_agriculture",
        "branding_assets",
        "cinematic_vault",
        "logs"
    ]
}

# Explicit Mapping of all 15 Sovereign Verticals
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
    """
    Deterministically maps file paths to one of the 15 sovereign verticals,
    governance/legal, or the core bare-metal hypervisor.
    """
    path_norm = filepath.replace("\\", "/").lower()

    # Check for direct pillar directory indicators
    for prefix, (pillar_id, pillar_name) in PILLAR_MAP.items():
        if f"/{prefix}_" in path_norm or f"\\{prefix}_" in path_norm or f"docs/{prefix}" in path_norm:
            return pillar_id, pillar_name

    # Keyword fallbacks for un-prefixed files
    if any(k in path_norm for k in ["crop", "soil", "vegetat", "dielectric", "irrigation"]):
        return PILLAR_MAP["01"]
    elif any(k in path_norm for k in ["logistics", "supply_chain", "dispatch", "fleet"]):
        return PILLAR_MAP["02"]
    elif any(k in path_norm for k in ["defense", "kinetic", "perimeter", "tactical"]):
        return PILLAR_MAP["03"]
    elif any(k in path_norm for k in ["energy", "microgrid", "battery", "solar", "grid"]):
        return PILLAR_MAP["04"]
    elif any(k in path_norm for k in ["manufacturing", "fabrication", "additive", "cnc"]):
        return PILLAR_MAP["05"]
    elif any(k in path_norm for k in ["comms", "intercom", "mesh", "p2p", "rf_"]):
        return PILLAR_MAP["06"]
    elif any(k in path_norm for k in ["financial", "economic", "stripe", "ledger", "treasury", "payment"]):
        return PILLAR_MAP["07"]
    elif any(k in path_norm for k in ["healthcare", "health", "biometric", "triage"]):
        return PILLAR_MAP["08"]
    elif any(k in path_norm for k in ["aerospace", "aviation", "orbit", "drone_bridge"]):
        return PILLAR_MAP["09"]
    elif any(k in path_norm for k in ["civil_engineer", "concrete", "structural", "survey"]):
        return PILLAR_MAP["10"]
    elif any(k in path_norm for k in ["mining", "extraction", "geological", "mineral"]):
        return PILLAR_MAP["11"]
    elif any(k in path_norm for k in ["deep_ocean", "subsea", "maritime", "oceanic", "sonar"]):
        return PILLAR_MAP["12"]
    elif any(k in path_norm for k in ["cryptograph", "cipher", "diode", "signallink", "key_rotation", "zero_knowledge"]):
        return PILLAR_MAP["13"]
    elif any(k in path_norm for k in ["hydrogen", "fuel_cell", "electrolysis"]):
        return PILLAR_MAP["14"]
    elif any(k in path_norm for k in ["autonomous_war", "swarm", "guillotine", "tencap", "darpa"]):
        return PILLAR_MAP["15"]
    elif any(k in path_norm for k in ["legal", "compliance", "jv_framework", "dfars", "mnda", "lsa", "cage"]):
        return "governance_legal", "Legal, Contracts & Sovereign Compliance"
    else:
        return "core_hypervisor", "Bare-Metal Hypervisor & Operating System"

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
    print("HVF Omni-Industrial Matrix - INITIALIZING 15-VERTICAL NEURAL CORE")
    print(f"Master Repository Target: {CONFIG['master_dir']}")
    print(f"ChromaDB Storage Target: {CONFIG['db_dir']}")
    print("Architecture: 15 Sovereign Verticals + Governance + Core Hypervisor")
    print("Authority: CEO Jeffery Humphrey | CAGE: 1AHA8")
    print("=" * 80)

    os.makedirs(CONFIG["db_dir"], exist_ok=True)
    client = chromadb.PersistentClient(path=CONFIG["db_dir"])
    embed_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=CONFIG["collection_name"],
        embedding_function=embed_fn,
        metadata={"system": "Project Ebony", "prime_cage": "1AHA8", "architecture": "15_sovereign_verticals"}
    )

    doc_ids = []
    documents = []
    metadatas = []
    vertical_telemetry = {}

    print("\nScanning bare-metal repositories across all 15 verticals...")
    file_count = 0

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
                            "chunk_index": idx,
                            "prime_cage": "1AHA8",
                            "timestamp": str(time.time())
                        })

                    file_count += 1
                    vertical_telemetry[pillar_id] = vertical_telemetry.get(pillar_id, 0) + len(chunks)
                except Exception as e:
                    print(f"[WARN] Skipped {rel_path}: {e}")

    total_chunks = len(documents)
    print(f"\nIndexed {file_count} files across repositories.")
    print(f"Total Vector Chunks Generated: {total_chunks}")
    
    print("\n" + "=" * 80)
    print("SOVEREIGN VERTICAL ALLOCATION TELEMETRY")
    print("=" * 80)
    for p_id in sorted(vertical_telemetry.keys()):
        count = vertical_telemetry[p_id]
        print(f"  * {p_id.upper()}: {count} vectors")

    if total_chunks == 0:
        print("[ERROR] No files discovered. Verify master repository paths.")
        sys.exit(1)

    print(f"\nExecuting micro-batched ingestion (Batch Size: {CONFIG['batch_size']})...")
    start_time = time.time()
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
        pct = ((b + 1) / total_batches) * 100
        print(f"  -> Batch [{b + 1}/{total_batches}] committed ({pct:.1f}%) | Vectors {b_start} to {b_end}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print("15-VERTICAL SOVEREIGN NEURAL CORE COMPILED")
    print(f"Total Vectors Ingested: {total_chunks} (100% Memory Preserved)")
    print(f"Total Elapsed Time: {elapsed:.2f} seconds")
    print(f"Active Collection: {CONFIG['collection_name']}")
    print("=" * 80)

if __name__ == "__main__":
    build_neural_core()
