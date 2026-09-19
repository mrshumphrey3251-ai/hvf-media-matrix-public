"""
================================================================================
HVF SOVEREIGN MEDIA MATRIX - DUAL-TIER STRATEGIC MEMORY VAULT (PUBLIC BLUEPRINT)
System: Project Ebony - Continuous Episodic & Semantic Memory Engine
Authority: Jeffery Humphrey, Founder & CEO
Compliance: DFARS 252.227-7018 Data Rights Protection (Sanitized Architecture)
================================================================================
"""

import os
import time
import sqlite3
import threading
from datetime import datetime
import chromadb
from chromadb.utils import embedding_functions

SQLITE_DB_PATH = os.getenv("HVF_VAULT_SQLITE", "./hvf_memory_vault_public.db")
CHROMA_DB_PATH = os.getenv("HVF_CHROMA_DIR", "./chroma_db_public")
COLLECTION_NAME = "hvf_iron_dome_public_blueprint"

_lock = threading.Lock()

def get_chroma_collection():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
        metadata={"system": "Project Ebony", "classification": "Sanitized Public Architecture"}
    )

def init_vault():
    os.makedirs(os.path.dirname(os.path.abspath(SQLITE_DB_PATH)), exist_ok=True)
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

    try:
        col = get_chroma_collection()
        col.upsert(
            ids=[f"directive_{directive_id}_{int(time.time())}"],
            documents=[f"DIRECTIVE [{category}]: {directive}"],
            metadatas=[{
                "source": "directive",
                "pillar_id": "governance",
                "category": category,
                "timestamp": timestamp
            }]
        )
    except Exception:
        pass

def log_conversation_turn(role: str, content: str):
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

    try:
        col = get_chroma_collection()
        col.upsert(
            ids=[f"conv_{role}_{msg_id}_{int(time.time())}"],
            documents=[f"[{role.upper()}]: {content}"],
            metadatas=[{
                "source": "conversation",
                "pillar_id": "episodic_memory",
                "timestamp": timestamp
            }]
        )
    except Exception:
        pass

if __name__ == "__main__":
    init_vault()