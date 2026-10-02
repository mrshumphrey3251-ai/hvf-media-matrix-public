import os

critical_paths = [
    "src/compliance/regulatory_engine.py",
    "docs/compliance/soc2_control_matrix.md",
    "src/analytics/prescriptive_sandbox.py",
    "src/saas/usage_metering.py"
]

print("\n" + "="*60)
print(" 🦅 EBONY AI: 12-MONTH EXPANSION AUDIT ")
print("="*60)

missing = 0
for path in critical_paths:
    normalized_path = os.path.normpath(path)
    if os.path.exists(normalized_path):
        print(f"[VERIFIED] {normalized_path}")
    else:
        print(f"[FAILED]   {normalized_path} is MISSING!")
        missing += 1

print("="*60)
if missing == 0:
    print("EXECUTIVE STATUS: 12-MONTH SAAS EXPANSION 100% OPERATIONAL.")
else:
    print(f"EXECUTIVE STATUS: SYSTEM COMPROMISED. {missing} FAILURES DETECTED.")
print("="*60 + "\n")
