"""
E.B.O.N.Y. SOVEREIGN COMMAND DIRECTIVE INTERCEPTOR
Authority: CEO Jeffery Humphrey (Level 5 Clearance) // CAGE: 1AHA8
Standard: DFARS 252.227-7018 GPR | Active Docket: 10-26-3976 (TRL 4)

Direct Command Intake:
Ingests natural language executive engineering directives, extracts module scope,
and triggers the closed-loop autonomous synthesis pipeline.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ebony_autonomous_pipeline import EbonyAutonomousPipeline


class EbonyDirectiveEngine:
    def __init__(self):
        self.pipeline = EbonyAutonomousPipeline()

    def receive_ceo_command(self, directive_text: str, ceo_key: str = "HVF-CEO-LEVEL5-AUTH") -> dict:
        print("=" * 70)
        print("E.B.O.N.Y. SOVEREIGN COMMAND INTERCEPT")
        print(f'CEO DIRECTIVE RECEIVED: "{directive_text}"')
        print("=" * 70)

        words = directive_text.lower().replace(",", " ").split()
        module_name = "sovereign_module"
        for w in words:
            if "scada" in w or "battery" in w or "hydro" in w or "energy" in w or "fencing" in w:
                module_name = f"sovereign_{w}"
                break

        return self.pipeline.execute_self_code_cycle(
            module_name=module_name,
            specification=directive_text,
            ceo_key=ceo_key
        )
