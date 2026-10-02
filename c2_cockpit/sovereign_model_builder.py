import os
from huggingface_hub import snapshot_download

def build_sovereign_model():
    print("[SYSTEM] Engaging direct Python model download to sovereign vault...")
    model_path = snapshot_download(repo_id="Lykon/dreamshaper-8-lcm", local_dir="sovereign_model")
    
    index_file = os.path.join(model_path, "model_index.json")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        patched_content = content.replace("CLIPFeatureExtractor", "CLIPImageProcessor")
        
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(patched_content)
        print("[SYSTEM] Model cloned and legacy blueprint patched successfully.")
    else:
        print("[SYSTEM ERROR] model_index.json not found in local vault.")

if __name__ == "__main__":
    build_sovereign_model()
