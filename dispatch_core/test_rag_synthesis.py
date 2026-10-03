import os
import sys
import chromadb
from groq import Groq
from dotenv import load_dotenv

# ==============================================================================
# HVF Omni-Industrial Matrix | RAG SYNTHESIS VERIFICATION PROBE
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Groq (openai/gpt-oss-120b) + ChromaDB Iron Dome Verification
# ==============================================================================

load_dotenv(override=True)
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("[FAIL] GROQ_API_KEY not found in environment or .env file.")
    sys.exit(1)

client = Groq(api_key=groq_key)
db_path = r"C:\HVF_Repos\hvf-media-matrix-private\chroma_db"
chroma_client = chromadb.PersistentClient(path=db_path)

try:
    collection = chroma_client.get_collection("hvf_iron_dome_core")
except Exception as e:
    print(f"[FAIL] Unable to access hvf_iron_dome_core: {e}")
    sys.exit(1)

query = "Explain HVF Omni-Industrial Matrix prime defense capabilities and AF_XDP sensor hypervisor under CAGE 1AHA8"
print(f"1. Querying 20,244 vectors for: \"{query}\"")

results = collection.query(
    query_texts=[query],
    n_results=2
)

docs = results.get("documents", [[]])[0]
metas = results.get("metadatas", [[]])[0]

print(f"2. Retrieved {len(docs)} relevant vector chunks.")
for idx, meta in enumerate(metas):
    print(f"   * Match {idx + 1}: Source={meta.get('source')} | Pillar={meta.get('pillar_name')}")

context = "\n\n".join(docs)

prompt = f"""You are Ebony, the executive AI for HVF Omni-Industrial Matrix. 
You write with supreme authority, addressing CEO Jeffery Humphrey as Boss.
Use the following retrieved sovereign intelligence from the Iron Dome to answer the prompt.

--- RETRIEVED CONTEXT ---
{context}
-------------------------

Boss's Query: {query}
"""

print("\n3. Generating RAG response via Groq (openai/gpt-oss-120b)...")
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

print("\n" + "=" * 80)
print("LIVE RAG INFERENCE OUTPUT:")
print("=" * 80)
print(response.choices[0].message.content)
print("=" * 80)
