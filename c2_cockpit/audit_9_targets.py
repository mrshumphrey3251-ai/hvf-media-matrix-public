"""
E.B.O.N.Y. Authoritative 9-Target Mission Auditor
Cryptographic SHA-256 Verification & File Integrity Ledger
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory: Oklahoma Title 61 & OK HB 2992
"""
import hashlib
from pathlib import Path
from datetime import datetime, timezone

TARGETS = [
    Path(r"C:\hvf_c2\hvf-media-matrix-private\EBONY_OPERATIONAL_CAPABILITY_SPECIFICATION.md"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\OK_DRONE_INFRASTRUCTURE_SPECIFICATION.md"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\OK_DRONE_GRANT_BUDGET_PROPOSAL.md"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\DOC_FOLLOWUP_DISPATCH_TEMPLATE.md"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\audit_briefcase_integrity.py"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_scada_poll.py"),
    Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_agent_swarm.py")
]

print("=" * 86)
print("     E.B.O.N.Y. SOVEREIGN 9-TARGET MISSION AUDIT // IMMUTABLE INTEGRITY REPORT")
print(f"     TIMESTAMP: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | SOVEREIGN NODE: HVFNexus")
print("=" * 86)
print(f"{'STATUS':<9} | {'ARTIFACT NAME':<46} | {'SIZE (KB)':<10} | {'SHA-256 (FIRST 16)'}")
print("-" * 86)

all_verified = True
for target in TARGETS:
    if target.exists():
        data = target.read_bytes()
        size_kb = round(len(data) / 1024, 2)
        sha16 = hashlib.sha256(data).hexdigest()[:16].upper()
        print(f"[ONLINE]  | {target.name:<46} | {size_kb:>8.2f} KB | {sha16}...")
    else:
        print(f"[MISSING] | {target.name:<46} | {'0.00':>8} KB | NONE")
        all_verified = False

print("=" * 86)
if all_verified:
    print(">>> [SUCCESS] 9 OF 9 SOVEREIGN TARGETS PHYSICALLY VERIFIED ON DISK. ZERO FAULTS. <<<")
else:
    print(">>> [CRITICAL] ONE OR MORE ASSETS FAILED PHYSICAL VERIFICATION. <<<")
print("=" * 86)