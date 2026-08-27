import os
import chromadb
from chromadb.utils import embedding_functions

MASTER_DIR = r"C:\HVF_Repos"
DB_DIR = os.path.join(MASTER_DIR, "hvf-media-matrix-private", "chroma_db")

print("Initializing HVF Neural Core...")
client = chromadb.PersistentClient(path=DB_DIR)
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(name="hvf_master_vault", embedding_function=embed_fn)

ignore_dirs = {'.git', '.venv', 'venv', '__pycache__', 'chroma_db', 'logs'}
valid_exts = {'.py', '.txt', '.md', '.json', '.cpp'}

doc_ids = []
documents = []
metadatas = []

print("Scanning your 6 bare-metal repositories...")
for root, dirs, files in os.walk(MASTER_DIR):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for file in files:
        if os.path.splitext(file)[1].lower() in valid_exts:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.strip(): continue
                    
                    # Chop files into exact mathematical vectors
                    chunk_size = 1000
                    for i in range(0, len(content), chunk_size):
                        doc_ids.append(f"{filepath}_chunk_{i}")
                        documents.append(content[i:i+chunk_size])
                        metadatas.append({"source": filepath})
            except: pass

if documents:
    print(f"Ingesting {len(documents)} vectors into the local Iron Dome...")
    for i in range(0, len(documents), 5000):
        collection.upsert(
            ids=doc_ids[i:i+5000],
            documents=documents[i:i+5000],
            metadatas=metadatas[i:i+5000]
        )
    print("Neural Core is ONLINE. Master vault is permanently memorized.")
else:
    print("Scan complete. No readable files detected.")
