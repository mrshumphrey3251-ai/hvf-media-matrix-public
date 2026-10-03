import os
import chromadb
from chromadb.utils import embedding_functions

# Connect to the Sovereign Iron Dome
DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db"
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="hvf_iron_dome_core")

# Target the Master Empire Directory (All 19 Repositories)
REPOS_ROOT = r"C:\HVF_Repos"
VALID_EXTENSIONS = {".py", ".md", ".txt", ".json", ".bat", ".ps1"}

print("⚡ IGNITING OMNI-REPOSITORY NEURAL INGESTION ENGINE...")
print("📡 Scanning all 19 repositories across the HVF Master Directory...")

documents = []
metadatas = []
ids = []
doc_id = 0

for root, dirs, files in os.walk(REPOS_ROOT):
    # Bypass dead-weight directories to keep the neural net lethal and fast
    if ".git" in root or "venv" in root or "__pycache__" in root or "node_modules" in root or "chroma_db" in root:
        continue
        
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in VALID_EXTENSIONS:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                if not content.strip():
                    continue
                    
                # Slice the architecture into digestible neural blocks
                chunk_size = 1500
                chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
                
                # Identify which of the 19 repos this file belongs to
                parts = filepath.replace(REPOS_ROOT, "").strip("\\/").split("\\")
                repo_name = parts[0] if len(parts) > 0 else "HVF_Root"
                
                for idx, chunk in enumerate(chunks):
                    doc_id += 1
                    documents.append(chunk)
                    metadatas.append({"source": filepath, "repo": repo_name, "pillar_name": "OMNI_VISION_ALL_REPOS"})
                    ids.append(f"omni_doc_{doc_id}")
                    
            except Exception:
                pass

# Inject the extracted DNA into the active memory vault in batches
batch_size = 100
print(f"📊 Extracted {len(documents)} cognitive blocks across the Empire. Injecting into Iron Dome...")

for i in range(0, len(documents), batch_size):
    collection.upsert(
        documents=documents[i:i+batch_size],
        metadatas=metadatas[i:i+batch_size],
        ids=ids[i:i+batch_size]
    )

print(f"✅ INGESTION COMPLETE: Ebony now possesses omnipresent visibility over {doc_id} architectural sectors.")
