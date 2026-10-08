"""
================================================================================
HVF SOVEREIGN MEDIA MATRIX - DUAL-TIER STRATEGIC MEMORY VAULT
System: Project Ebony - Continuous Episodic & Semantic Memory Engine
Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
Compliance: DFARS 252.227-7018 Data Rights Protection
================================================================================
"""

import os
import sys
import time
import sqlite3
import threading
from datetime import datetime
import chromadb
from chromadb.utils import embedding_functions

SQLITE_DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"
CHROMA_DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db"
COLLECTION_NAME = "hvf_iron_dome_core"

_lock = threading.Lock()

def get_chroma_collection():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
        metadata={"system": "Project Ebony", "prime_cage": "1AHA8"}
    )

def init_vault():
    os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
    with _lock, sqlite3.connect(SQLITE_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ceo_directives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                category TEXT NOT NULL,
                directive TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conversation_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        conn.commit()

def log_directive(category: str, directive: str, status: str = "ACTIVE"):
    """Logs directive to SQLite and immediately embeds into ChromaDB vector memory."""
    init_vault()
    timestamp = datetime.utcnow().isoformat()
    
    with _lock, sqlite3.connect(SQLITE_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ceo_directives (timestamp, category, directive, status) VALUES (?, ?, ?, ?)",
            (timestamp, category, directive, status)
        )
        directive_id = cur.lastrowid
        conn.commit()

    # Real-time atomic upsert into ChromaDB
    try:
        col = get_chroma_collection()
        col.upsert(
            ids=[f"directive_{directive_id}_{int(time.time())}"],
            documents=[f"CEO DIRECTIVE [{category}]: {directive}"],
            metadatas=[{
                "source": "ceo_directive",
                "pillar_id": "governance_legal",
                "pillar_name": "Executive Directives & Governance",
                "category": category,
                "status": status,
                "timestamp": timestamp,
                "prime_cage": "1AHA8"
            }]
        )
    except Exception as e:
        print(f"[WARN] Vector memory injection failed for directive: {e}")

def log_conversation_turn(role: str, content: str):
    """Logs conversation turn to SQLite and embeds into ChromaDB episodic memory."""
    init_vault()
    timestamp = datetime.utcnow().isoformat()

    with _lock, sqlite3.connect(SQLITE_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO conversation_memory (timestamp, role, content) VALUES (?, ?, ?)",
            (timestamp, role, content)
        )
        msg_id = cur.lastrowid
        conn.commit()

    # Real-time atomic upsert into ChromaDB
    try:
        col = get_chroma_collection()
        col.upsert(
            ids=[f"conv_{role}_{msg_id}_{int(time.time())}"],
            documents=[f"[{role.upper()}]: {content}"],
            metadatas=[{
                "source": "episodic_conversation",
                "pillar_id": "episodic_conversations",
                "pillar_name": "Continuous Conversational History",
                "role": role,
                "timestamp": timestamp,
                "prime_cage": "1AHA8"
            }]
        )
    except Exception as e:
        print(f"[WARN] Vector memory injection failed for conversation turn: {e}")

def ingest_future_document(filepath: str, pillar_id: str = "core_hypervisor", pillar_name: str = "Dynamic Ingestion"):
    """
    Dynamically embeds new documents, proposals, or memos in seconds
    without rebuilding or wiping the existing 20,244-vector database.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Target document {filepath} not found.")

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    chunk_size = 1000
    overlap = 150
    chunks = []
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap

    rel_path = os.path.basename(filepath)
    doc_ids = [f"dynamic_{rel_path}_{i}_{int(time.time())}" for i in range(len(chunks))]
    metas = [{
        "source": rel_path,
        "pillar_id": pillar_id,
        "pillar_name": pillar_name,
        "chunk_index": i,
        "prime_cage": "1AHA8",
        "timestamp": str(time.time())
    } for i in range(len(chunks))]

    col = get_chroma_collection()
    col.upsert(ids=doc_ids, documents=chunks, metadatas=metas)
    print(f"[SUCCESS] Atomically indexed {len(chunks)} vectors from {rel_path} into {COLLECTION_NAME}.")

if __name__ == "__main__":
    init_vault()
    print("HVF Dual-Tier Strategic Memory Vault initialized successfully.")