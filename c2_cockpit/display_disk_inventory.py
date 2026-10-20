"""
HVFNexus Sovereign Industrial C2 — Disk Inventory Terminal Viewer
Groups and prints all saved disk files by operational domain.
"""
from pathlib import Path

manifest_path = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit/HVF_FULL_DISK_MANIFEST.md")

if not manifest_path.exists():
    print("[-] Manifest not found.")
    exit(1)

lines = manifest_path.read_text(encoding="utf-8").splitlines()

print("\n" + "=" * 80)
print("     HUMPHREY VIRTUAL FARMS LLC — COMPREHENSIVE ON-DISK FILE CATALOG     ")
print("=" * 80)

for line in lines:
    if line.startswith("## ") or line.startswith("*Subtotal") or line.startswith("* **Total"):
        print("\n" + line.replace("**", "").replace("##", ">>>"))
    elif line.startswith("| `"):
        # Format table line nicely for terminal display
        parts = [p.strip().replace("`", "") for p in line.split("|")[1:-1]]
        if len(parts) >= 3:
            print(f"  - {parts[0]:<45} | {parts[1]:<10} | SHA: {parts[2]}")

print("\n" + "=" * 80 + "\n")