import sys
from pathlib import Path

ROOT = Path(r"C:\HVF_Repos\hvf-media-matrix-private")
for p in [str(ROOT / "dispatch_core"), str(ROOT / "sandbox_staging"), str(ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import sovereign_coder

coder = sovereign_coder.SovereignCoder()
result = coder.generate_and_stage(
    module_name="linkedin_lead_scheduler.py",
    specification="LinkedIn Market Lead Dispatch Scheduler with lead queue metrics, contact staging table, and outbound message template composer."
)
print("[+] Sandbox Synthesis Result:", result)
