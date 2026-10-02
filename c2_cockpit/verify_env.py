import os
import sys

print("=" * 80)
print("PROJECT EBONY: RUNTIME ENVIRONMENT & TOML VERIFICATION")
print("=" * 80)

# 1. Test Local Repository TOML Configuration
local_toml = os.path.join(".streamlit", "config.toml")
if os.path.exists(local_toml):
    try:
        import toml
        with open(local_toml, "r", encoding="utf-8") as f:
            data = toml.loads(f.read())
        primary = data.get("theme", {}).get("primaryColor", "Not Specified")
        print(f"[SUCCESS] Local {local_toml} parsed cleanly.")
        print(f"          Theme Primary Color: {primary}")
    except Exception as e:
        print(f"[FAIL] Local config.toml syntax error: {e}")
else:
    print(f"[WARN] Local {local_toml} not found.")

# 2. Test User Home Directory TOML Configuration
user_toml = os.path.expanduser(os.path.join("~", ".streamlit", "config.toml"))
if os.path.exists(user_toml):
    try:
        import toml
        with open(user_toml, "r", encoding="utf-8") as f:
            u_data = toml.loads(f.read())
        print(f"[SUCCESS] User Home {user_toml} parsed cleanly.")
    except Exception as e:
        print(f"[WARN] User Home config.toml syntax error: {e}")
        print("       (Recommend deleting or replacing ~/.streamlit/config.toml if errors persist)")

# 3. Verify ChromaDB 15-Vertical Vector Core Health
print("\nVerifying ChromaDB Core Connection...")
try:
    import chromadb
    db_path = os.path.join(os.getcwd(), "chroma_db")
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection("hvf_iron_dome_core")
    count = collection.count()
    print(f"[SUCCESS] ChromaDB Iron Dome online.")
    print(f"          Active Collection: hvf_iron_dome_core")
    print(f"          Total Verified Vectors: {count}")
except Exception as e:
    print(f"[FAIL] ChromaDB retrieval error: {e}")

print("=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)