from pathlib import Path
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

guardrail_block = """
# =========================================================================
# EBONY OPERATIONAL TRUTH & ANTI-HALLUCINATION GUARDRAILS
# =========================================================================
SOVEREIGN_OPERATIONAL_DOCTRINE = \"\"\"
### CRITICAL OPERATIONAL DIRECTIVES (ZERO-HALLUCINATION ENFORCEMENT):
1. NO FICTIONAL CLIs OR TOOLS: Never invent command-line utilities (e.g., hvfctl, derctl, scadactl, crewctl), non-existent web portals (e.g., matrix.hvf.io), or imaginary shell scripts. Only reference real, verified local files and standard system binaries (Python, PowerShell, Git).
2. NO FABRICATED BUDGETS OR HEADCOUNTS: Do not generate speculative multi-million-dollar budgets ($8M, $15M, $120M) or fictional job figures (250 jobs) unless explicitly provided by Jeffery Humphrey. Stick strictly to verified assets: Tradewinds Docket 9-26-3703, CAGE 1AHA8, OK HB 2992, and real engineering parameters (<16 ms sub-cycle isolation, VFD telemetry).
3. NO FICTIONAL PERSONNEL: Never invent imaginary staff, crew members, or liaisons (e.g., 'Alex Vega').
4. ZERO EMAIL PERSONIFICATION: You are a local bare-metal software matrix running on localhost:8501. You DO NOT have an email inbox, cannot receive emails, and must NEVER instruct Jeffery Humphrey to email humphreyvirtualfarm@gmail.com or any other address to trigger tasks. All interactions happen directly in this console or via verified local scripts.
5. EXECUTIVE SUBSTANCE: Speak with authoritative engineering precision. Do not use hyperbolic consultant fluff.
\"\"\"
"""

for target in targets:
    if not target.exists():
        continue
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Inject doctrine if missing
    if "SOVEREIGN_OPERATIONAL_DOCTRINE" not in content:
        content = guardrail_block + "\n" + content
        print(f"[+] Injected SOVEREIGN_OPERATIONAL_DOCTRINE into {target.name}")

    # Wire into the system prompt payload
    if "SOVEREIGN_OPERATIONAL_DOCTRINE" in content and "SOVEREIGN_OPERATIONAL_DOCTRINE +" not in content:
        content = content.replace(
            'messages_payload.append({"role": "system", "content": load_ultimate_law_context() + "\\n\\nYou are Ebony',
            'messages_payload.append({"role": "system", "content": load_ultimate_law_context() + "\\n\\n" + SOVEREIGN_OPERATIONAL_DOCTRINE + "\\n\\nYou are Ebony'
        )
        print(f"[+] Bound guardrails to cognitive message loop in {target.name}")

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(target), doraise=True)
    print(f"[+] Compiled successfully: {target.name}")
