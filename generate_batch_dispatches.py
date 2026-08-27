import os
import json
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(BASE_DIR, "knowledge_vault")
OUTPUT_DIR = os.path.join(BASE_DIR, "ebony_dashboard", "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "weekly_dispatch_queue.json")
REPO_URL = "https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public"

def load_vault():
    docs = {}
    if os.path.exists(VAULT_DIR):
        for f in os.listdir(VAULT_DIR):
            if f.endswith(".txt") or f.endswith(".md"):
                with open(os.path.join(VAULT_DIR, f), "r", encoding="utf-8") as vf:
                    docs[f] = vf.read().strip()
    return docs

def generate_weekly_queue():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.datetime.now()
    
    dispatches = [
        {
            "id": 1,
            "platform": "LinkedIn",
            "schedule": (now + datetime.timedelta(days=1)).strftime("%A, %B %d, %Y at 09:00 AM"),
            "topic": "Autonomous Digital Infrastructure & AgTech",
            "content": f"Humphrey Virtual Farm (HVF) is deploying zero-latency automated pipelines to bridge industrial ag-systems with real-time federal environmental telemetry.\n\nExplore our open-source blueprints: {REPO_URL}\n\n#AgTech #AI #HumphreyVirtualFarm #DigitalTransformation"
        },
        {
            "id": 2,
            "platform": "Technical Bulletin",
            "schedule": (now + datetime.timedelta(days=3)).strftime("%A, %B %d, %Y at 02:00 PM"),
            "topic": "Operational Security & Geofenced Telemetry",
            "content": f"Security Briefing: Precision Doppler radar integration with 2-decimal OPSEC geofencing enables real-time weather analytics without exposing physical node coordinates.\n\nPublic Architecture: {REPO_URL}\n\n#CyberSecurity #OPSEC #IoT #HVF"
        },
        {
            "id": 3,
            "platform": "Executive Update",
            "schedule": (now + datetime.timedelta(days=5)).strftime("%A, %B %d, %Y at 10:00 AM"),
            "topic": "Proprietary RAG & Knowledge Vault Deployment",
            "content": f"Executive Overview: On-premise knowledge vault architectures allow instant multi-document context retrieval while eliminating external API dependency risk.\n\nVerified Blueprint: {REPO_URL}\n\n#ExecutiveLeadership #AutonomousSystems #Innovation"
        }
    ]
    
    payload = {"generated_at": now.strftime("%Y-%m-%d %H:%M:%S"), "queue": dispatches}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(payload, out, indent=4)
        
    print(f"[*] Generated 3 Scheduled Dispatches -> {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_weekly_queue()
