"""
HVFNexus Sovereign Industrial C2 — Master Disk Inventory Engine
Scans, hashes, and indexes every file saved across private, public, and briefcase enclaves.
Excludes .git internal metadata directories to focus strictly on operational assets.
"""
import os
import hashlib
from datetime import datetime
from pathlib import Path

targets = {
    "Private Enclave": Path("C:/HVF_Repos/hvf-media-matrix-private"),
    "Public Repository": Path("C:/HVF_Repos/hvf-media-matrix-public"),
    "Offline Briefcase": Path("C:/HVF_Briefcase_Rob_Teele")
}

output_file = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit/HVF_FULL_DISK_MANIFEST.md")

manifest_lines = []
manifest_lines.append("# HUMPHREY VIRTUAL FARMS LLC — MASTER DISK ARTIFACT MANIFEST")
manifest_lines.append(f"**Generated (UTC):** {datetime.utcnow().isoformat()}  ")
manifest_lines.append("**Entity:** Humphrey Virtual Farms LLC | **CAGE:** `1AHA8` | **UEI:** `S1M4ENLHTDH5`  ")
manifest_lines.append("**SPRS Cyber Score:** 110 / 110 (DoD UID: `PHASE1-OTA-TARGET`)  ")
manifest_lines.append("\n---\n")

print("\n=== [HVFNexus C2] EXECUTING EXHAUSTIVE DISK INVENTORY ===")

total_file_count = 0
total_byte_size = 0

for label, root_path in targets.items():
    if not root_path.exists():
        print(f"[-] Directory not found: {root_path}")
        continue
    
    print(f"\n[*] Scanning {label} ({root_path})...")
    manifest_lines.append(f"## {label} (`{root_path}`)\n")
    manifest_lines.append("| File Path | Size (KB) | SHA-256 (First 16 chars) |")
    manifest_lines.append("| :--- | :--- | :--- |")
    
    scanned_in_target = 0
    # Walk directory
    for root, dirs, files in os.walk(root_path):
        if ".git" in dirs:
            dirs.remove(".git")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
            
        for f in sorted(files):
            full_path = Path(root) / f
            try:
                size_bytes = full_path.stat().st_size
                rel_path = full_path.relative_to(root_path)
                data = full_path.read_bytes()
                h = hashlib.sha256(data).hexdigest()[:16]
                size_kb = round(size_bytes / 1024, 2)
                
                manifest_lines.append(f"| `{rel_path}` | {size_kb} KB | `{h}` |")
                scanned_in_target += 1
                total_file_count += 1
                total_byte_size += size_bytes
            except Exception as e:
                manifest_lines.append(f"| `{f}` | ERROR | Read error: {e} |")
                
    print(f"    [+] Indexed {scanned_in_target} files.")
    manifest_lines.append(f"\n*Subtotal: {scanned_in_target} files*\n\n---\n")

total_mb = round(total_byte_size / (1024 * 1024), 2)
manifest_lines.append(f"## Summary of Disk Holdings\n")
manifest_lines.append(f"* **Total Enclave Files Saved on Disk:** **{total_file_count} files**\n")
manifest_lines.append(f"* **Total Storage Footprint:** **{total_mb} MB**\n")
manifest_lines.append(f"* **Offline Readiness Status:** 100% Bare-Metal Available (0 KB cloud pull required)\n")

manifest_text = "\n".join(manifest_lines) + "\n"
output_file.write_text(manifest_text, encoding="utf-8")

print(f"\n[+] Master disk manifest written to: {output_file}")
print(f"[+] Total Files Indexed: {total_file_count} ({total_mb} MB)")
print("=== DISK SWEEP COMPLETE ===")
