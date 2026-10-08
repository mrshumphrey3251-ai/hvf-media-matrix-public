"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: INGEST CHUNKED
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import json

    import chromadb

    from pathlib import Path



    json_path = Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\SOVEREIGN_CORPUS.json")

    db_path = r"C:\HVF_Repos\HVF_Matrix_Core\vector_vault"



    print("[*] Initiating Semantic Fragmentation and Ingestion...")



    if not json_path.exists():

        print(f"[-] CRITICAL ERROR: Corpus not found at {json_path}")

        exit(1)



    try:

        client = chromadb.PersistentClient(path=db_path)

        collection = client.get_or_create_collection(name="hvf_knowledge_base")

    except Exception as e:

        print(f"[-] FATAL: Could not connect to Vector Vault. {e}")

        exit(1)



    with open(json_path, "r", encoding="utf-8") as f:

        try:

            data = json.load(f)

        except json.JSONDecodeError as e:

            print(f"[-] JSON Parsing Error: {e}")

            exit(1)



    docs = []

    metadatas = []

    ids = []

    chunk_id = 0



    axioms = data.get("ultimate_law_axioms", [])

    for axiom in axioms:

        content = axiom.get("content", "")

        repo = axiom.get("repo", "unknown")



        # Shatter the monolith into individual verses/paragraphs

        chunks = [c.strip() for c in content.split('\n') if len(c.strip()) > 10]



        for chunk in chunks:

            docs.append(chunk)

            metadatas.append({

                "repo": repo,

                "is_law": "true"

            })

            ids.append(f"law_chunk_{chunk_id}")

            chunk_id += 1



    print(f"[*] Monolith shattered into {len(docs)} tactical vectors.")



    # Ingest in batches to prevent database overload

    batch_size = 1000

    for i in range(0, len(docs), batch_size):

        end = min(i + batch_size, len(docs))

        collection.upsert(

            documents=docs[i:end],

            metadatas=metadatas[i:end],

            ids=ids[i:end]

        )

        print(f"[+] Locked batch {i} to {end} into the Iron Dome...")



    print(f"[+] TOTAL INGESTION COMPLETE. {len(docs)} highly-targeted vectors active in memory.")


if __name__ == "__main__":
    render()
