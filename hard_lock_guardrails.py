from pathlib import Path
import re
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

strict_system_directive = """
CRITICAL SYSTEM DIRECTIVES:
1. PLATFORM REALITY: You are running locally on a Windows workstation at C:\\HVF_Repos\\ via Python/Streamlit (localhost:8501). DO NOT output Linux paths like /opt/hvf, /var/log, /tmp, or /mnt.
2. ZERO FICTIONAL CLIS: DO NOT invent imaginary commands (hvf-backup, hvf-probe, hvf-stress, hvfctl, derctl, scadactl). If a task requires diagnostics, reference standard Windows tools: PowerShell, Python scripts in C:\\HVF_Repos\\, or Git.
3. ZERO FICTIONAL SERVICES: You DO NOT use AWS S3 buckets (s3://), Jira tickets, or Slack channels (#grid-ops). DO NOT mention them.
4. ZERO EMAIL PERSONIFICATION: You are software running on this machine. You DO NOT have an email address and CANNOT receive emails. NEVER instruct Jeffery Humphrey to email humphreyvirtualfarm@gmail.com or any other address.
5. REAL ASSETS ONLY: Restrict all technical statements to verified assets: Oklahoma HB 2992, DoD Tradewinds Docket 9-26-3703, CAGE 1AHA8, sub-cycle kinetic isolation under 16 ms, and local Modbus RTU/TCP telemetry.
"""

for target in targets:
    if not target.exists():
        continue
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()

    # Locate where the messages list is passed to openai/litellm/groq/anthropic client
    # Replace system content assignment with guaranteed strict enforcement
    pattern = r'(\{"role":\s*"system",\s*"content":\s*)(.*?)\}'
    
    def replacer(match):
        prefix = match.group(1)
        original_expr = match.group(2)
        return f'{prefix}f"""{strict_system_directive}\\n\\n""" + str({original_expr})}}'

    # Check if strict directive already present
    if "ZERO FICTIONAL CLIS" not in code:
        new_code, count = re.subn(pattern, replacer, code, count=1)
        if count > 0:
            with open(target, "w", encoding="utf-8") as f:
                f.write(new_code)
            print(f"[+] Hard-locked system directive into {target.name} ({count} occurrence)")
        else:
            print(f"[!] Could not locate system message pattern in {target.name}")
    else:
        print(f"[-] Strict directive already present in {target.name}")

    py_compile.compile(str(target), doraise=True)
    print(f"[+] Compiled cleanly: {target.name}")
