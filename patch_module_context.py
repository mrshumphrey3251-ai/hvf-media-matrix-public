from pathlib import Path
import re
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

module_definition_block = """
# =========================================================================
# EXACT SIDEBAR COMMAND MODULE DEFINITIONS (NOT VERTICALS)
# =========================================================================
SIDEBAR_MODULE_ARCHITECTURE = \"\"\"
### CANONICAL C2 SIDEBAR COMMAND MODULES:
When asked about 'modules' or 'sidebar modules', refer STRICTLY to these 5 software/hardware command modules in the console sidebar (NOT the 15 business verticals):
1. Master C2 Cockpit (Grid bus voltage, current, 60Hz frequency, and system state monitors)
2. Sub-Cycle Kinetic Isolation (<16ms hardware islanding and transient quench engine)
3. Modbus RTU / TCP Switchgear Telemetry (Direct register read/write, FC05 coil assertions at 2.04us)
4. Sovereign Command Nexus (Cognitive air-gapped terminal and prompt dispatch interface)
5. Level-5 Extensions & Debriefs (Offloaded historical telemetry, Merkle logs, and audit records)

The 15 verticals (AgTech, Defense, Aerospace, etc.) are industry market sectors, NOT sidebar command modules.
\"\"\"
"""

for target in targets:
    if not target.exists():
        continue
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()

    if "SIDEBAR_MODULE_ARCHITECTURE" not in code:
        code = module_definition_block + "\n" + code
        print(f"[+] Injected SIDEBAR_MODULE_ARCHITECTURE into {target.name}")

    if "SIDEBAR_MODULE_ARCHITECTURE +" not in code:
        code = code.replace(
            'load_ultimate_law_context() + "\\n\\n" + SOVEREIGN_OPERATIONAL_DOCTRINE',
            'load_ultimate_law_context() + "\\n\\n" + SOVEREIGN_OPERATIONAL_DOCTRINE + "\\n\\n" + SIDEBAR_MODULE_ARCHITECTURE'
        )
        print(f"[+] Bound module architecture to system prompt in {target.name}")

    with open(target, "w", encoding="utf-8") as f:
        f.write(code)

    py_compile.compile(str(target), doraise=True)
    print(f"[+] Compiled clean: {target.name}")
