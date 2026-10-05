from pathlib import Path
import re
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

sanitizer_code = """
def sanitize_ebony_output(text: str) -> str:
    \"\"\"Hard post-processing filter to strip email hallucinations and fake endpoints.\"\"\"
    import re
    # Strip any instruction telling the user to email humphreyvirtualfarm@gmail.com
    text = re.sub(r'(?i)(?:email|shoot|send|mail)(?:\\s+them|\\s+the\\s+logs|\\s+it)?\\s+(?:over\\s+)?to\\s+humphreyvirtualfarm@gmail\\.com', 'save the output to C:\\\\HVF_Repos\\\\Diagnostics\\\\', text)
    text = re.sub(r'(?i)humphreyvirtualfarm@gmail\\.com', '[LOCAL_STORAGE_ONLY: C:\\\\HVF_Repos\\\\Diagnostics]', text)
    text = re.sub(r'(?i)https?://api\\.ok\\.gov/[^\\s\\)]+', '[STATE_STATUTE: OK_HB_2992_TITLE_61]', text)
    text = re.sub(r'(?i)when the zip lands in my mailbox', 'when the file is saved to your drive', text)
    text = re.sub(r'(?i)New mail → To:.*', 'Review logs locally in PowerShell.', text)
    return text
"""

for target in targets:
    if not target.exists():
        continue
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()

    # Add the sanitizer function if missing
    if "def sanitize_ebony_output" not in code:
        code = sanitizer_code + "\n" + code
        print(f"[+] Added sanitize_ebony_output function to {target.name}")

    # Hook the sanitizer into where the assistant message is saved / displayed
    # Target common Streamlit patterns: st.write(response), st.markdown(response), etc.
    patterns = [
        (r'(\bresponse\s*=\s*.*?\.choices\[0\]\.message\.content)', r'\1\n        response = sanitize_ebony_output(response)'),
        (r'(st\.session_state\.messages\.append\(\{"role":\s*"assistant",\s*"content":\s*)(response)(\}\))', r'\1sanitize_ebony_output(\2)\3'),
        (r'(st\.markdown\(full_response\))', r'st.markdown(sanitize_ebony_output(full_response))'),
        (r'(st\.write\(full_response\))', r'st.write(sanitize_ebony_output(full_response))')
    ]

    for pat, repl in patterns:
        if re.search(pat, code) and "sanitize_ebony_output" not in re.search(pat, code).group(0):
            code, count = re.subn(pat, repl, code, count=1)
            print(f"[+] Applied output sanitizer hook in {target.name} ({count} match)")

    with open(target, "w", encoding="utf-8") as f:
        f.write(code)

    py_compile.compile(str(target), doraise=True)
    print(f"[+] Successfully compiled {target.name}")
