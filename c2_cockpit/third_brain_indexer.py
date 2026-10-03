import os
from pathlib import Path
import chromadb
from chromadb.config import Settings

def build_vector_vault():
    print("=== INITIALIZING EBONY THIRD BRAIN: VIP OVERRIDE INDEXER ===")
    
    db_path = r"C:\HVF_Repos\HVF_Matrix_Core\vector_vault"
    Path(db_path).mkdir(parents=True, exist_ok=True)
    
    client = chromadb.PersistentClient(path=db_path, settings=Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection(name="hvf_knowledge_base")
    
    root = Path(r"C:\HVF_Repos")
    valid_exts = {".py", ".md", ".txt"}
    
    ignore_dirs = {
        ".git", "__pycache__", "node_modules", "env", "venv", ".venv", 
        "hvf_env", ".streamlit", "GOLD_VERSIONS", "site-packages", 
        "Lib", "Scripts", ".cache", ".vscode", "huggingface"
    }
    
    # VIP FILES: These completely bypass size limits. Add future massive files here.
    vip_files = {"Apocryphal_Texts.txt", "Ultimate_Law_English_66.txt"}
    
    def chunk_text(text, chunk_size=1500, overlap=200):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    doc_id = 0
    batch_docs, batch_metas, batch_ids = [], [], []
    
    print("[*] Commencing VIP-enabled full-spectrum crawl of C:\\HVF_Repos...")
    
    for file_path in root.rglob("*"):
        if file_path.is_file() and file_path.suffix in valid_exts:
            if any(part in ignore_dirs for part in file_path.parts):
                continue
            
            # Check VIP Status vs Size Limit
            is_vip = file_path.name in vip_files
            try:
                if not is_vip and os.path.getsize(file_path) > 100000:
                    print(f"[-] Skipping (Exceeds 100KB limit): {file_path.name}")
                    continue
            except Exception:
                continue
                
            if is_vip:
                print(f"[!] VIP OVERRIDE ACCEPTED: Ingesting massive core file: {file_path.name}...")
            else:
                print(f"[*] Reading: {file_path.parent.name}\\{file_path.name}...")
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                
                if not content.strip():
                    continue
                    
                chunks = chunk_text(content)
                for i, chunk in enumerate(chunks):
                    doc_id += 1
                    batch_docs.append(chunk)
                    batch_metas.append({"source": str(file_path), "chunk": i})
                    batch_ids.append(f"doc_{doc_id}")
                    
                    if len(batch_docs) >= 100:
                        collection.add(documents=batch_docs, metadatas=batch_metas, ids=batch_ids)
                        batch_docs, batch_metas, batch_ids = [], [], []
                        
            except Exception as e:
                print(f"[-] Failed to process {file_path.name}: {e}")

    if batch_docs:
        collection.add(documents=batch_docs, metadatas=batch_metas, ids=batch_ids)

    print(f"\n[+] SUCCESS: {doc_id} cognitive chunks securely embedded in Vector Vault at {db_path}")

if __name__ == "__main__":
    build_vector_vault()
