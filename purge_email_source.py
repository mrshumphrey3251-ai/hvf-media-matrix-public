from pathlib import Path
import re
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit")
]

for base in targets:
    if not base.exists():
        continue
    for py_file in base.glob("*.py"):
        with open(py_file, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()

        changed = False
        # Remove literal email mentions in prompts or defaults
        if "humphreyvirtualfarm@gmail.com" in code:
            code = code.replace("humphreyvirtualfarm@gmail.com", "[LOCAL_ARCHIVE_ONLY: C:\\HVF_Repos\\Archive]")
            changed = True
            print(f"[+] Replaced hardcoded email in {py_file.name}")

        # Intercept Streamlit streaming or write blocks directly
        if "st.write_stream" in code and "def clean_stream" not in code:
            stream_wrapper = """
def clean_stream(generator):
    for chunk in generator:
        if hasattr(chunk, 'choices') and chunk.choices and chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            text = text.replace("humphreyvirtualfarm@gmail.com", "C:\\\\HVF_Repos\\\\Diagnostics\\\\")
            text = text.replace("email", "save locally")
            yield text
        elif isinstance(chunk, str):
            yield chunk.replace("humphreyvirtualfarm@gmail.com", "C:\\\\HVF_Repos\\\\Diagnostics\\\\")
"""
            code = stream_wrapper + "\n" + code
            code = re.sub(r'st\.write_stream\((.*?)\)', r'st.write_stream(clean_stream(\1))', code)
            changed = True
            print(f"[+] Intercepted st.write_stream in {py_file.name}")

        if changed:
            with open(py_file, "w", encoding="utf-8") as f:
                f.write(code)
            py_compile.compile(str(py_file), doraise=True)
            print(f"[+] Compiled clean: {py_file.name}")
