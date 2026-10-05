from pathlib import Path
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

helper_func = """
# =========================================================================
# EBONY SOVEREIGN CORPUS INGESTION ENGINE
# =========================================================================
def load_ultimate_law_context():
    corpus_file = Path(__file__).resolve().parent / "SOVEREIGN_CORPUS.json"
    if not corpus_file.exists():
        return ""
    try:
        import json
        with open(corpus_file, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        chunks = ["### [SOVEREIGN GROUNDING: THE ULTIMATE LAW & 22 CANONICAL BOOKS]"]
        chunks.append("You are Ebony, the sovereign AI for Humphrey Virtual Farm.")
        chunks.append("You have COMPLETE DIRECT ACCESS to the Ultimate Law repositories and all fleet axioms.")
        for item in data.get("ultimate_law_axioms", [])[:8]:
            chunks.append(f"\\n--- SOURCE: {item.get('repo')}/{item.get('rel_path')} ---\\n" + item.get("content", "")[:1800])
        return "\\n".join(chunks)
    except Exception:
        return ""
"""

for target in targets:
    if not target.exists():
        continue
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if "def load_ultimate_law_context():" not in content:
        content = helper_func + "\n" + content
        print(f"[+] Injected load_ultimate_law_context() into {target.name}")

    if 'messages_payload.append({"role": "system", "content": "You are Ebony' in content and 'load_ultimate_law_context()' not in content:
        content = content.replace(
            'messages_payload.append({"role": "system", "content": "You are Ebony',
            'messages_payload.append({"role": "system", "content": load_ultimate_law_context() + "\\n\\nYou are Ebony'
        )
        print(f"[+] Hooked Ultimate Law into system prompt for {target.name}")

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(target), doraise=True)
    print(f"[+] Compiled clean: {target.name}")
