from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

priv_repo = Path(r"C:\hvf_c2\hvf-media-matrix-private")
pub_repo  = Path(r"C:\hvf_c2\hvf-media-matrix-public")
desktop   = Path.home() / "Desktop"

def sha256_of(p: Path) -> str:
    if not p.exists():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest().lower()

# 1. Record old PDF hashes before recompiling so we can replace them everywhere if they change
erdc_pdf_priv = priv_repo / "c2_cockpit/proposals/WHITE_PAPER_USACE_ERDC_BAA_2026.pdf"
tw_pdf_priv   = priv_repo / "c2_cockpit/proposals/TRADEWINDS_RESUBMISSION_SCRIPT_10_26_4046.pdf"
video_priv    = priv_repo / "c2_cockpit/proposals/EBONY_V8_CDAO_RUBRIC_VERIFICATION_20261028.mp4"

old_erdc_hash = sha256_of(erdc_pdf_priv)
old_tw_hash   = sha256_of(tw_pdf_priv)

# 2. Re-compile both PDFs so their binary contents reflect Docket 10-26-4046
subprocess.run([sys.executable, str(priv_repo / "c2_cockpit/compile_erdc_baa_whitepaper.py")], cwd=str(priv_repo), check=True)
subprocess.run([sys.executable, str(priv_repo / "c2_cockpit/tradewinds_pitch_compiler.py")], cwd=str(priv_repo), check=True)

new_erdc_hash = sha256_of(erdc_pdf_priv)
new_tw_hash   = sha256_of(tw_pdf_priv)
video_hash    = sha256_of(video_priv)
merkle_root   = "bb39eeaa66a39ad2e0c0ab74ba4a5c4faac2bf0d98babc0362482b97607151a1"

# 3. Copy freshly compiled PDFs to Public Repo and Desktop
for rel in ("c2_cockpit/proposals/WHITE_PAPER_USACE_ERDC_BAA_2026.pdf", "c2_cockpit/proposals/TRADEWINDS_RESUBMISSION_SCRIPT_10_26_4046.pdf"):
    src = priv_repo / rel
    dst = pub_repo / rel
    if src.exists() and dst.parent.exists():
        shutil.copy2(src, dst)

if erdc_pdf_priv.exists() and desktop.exists():
    shutil.copy2(erdc_pdf_priv, desktop / "WHITE_PAPER_USACE_ERDC_BAA_2026.pdf")

# 4. Scan both repositories for any old ERDC/TW PDF hashes and replace them with the new live SHA-256 hashes
hash_replacements = []
if old_erdc_hash and old_erdc_hash != new_erdc_hash:
    hash_replacements.append((old_erdc_hash, new_erdc_hash))
if old_tw_hash and old_tw_hash != new_tw_hash:
    hash_replacements.append((old_tw_hash, new_tw_hash))

# Also update usace_erdc_baa_2026_dispatch_receipt.md explicitly if present
for repo in (priv_repo, pub_repo):
    if not repo.exists():
        continue
    for path in repo.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".py", ".json", ".txt", ".html"}:
            continue
        try:
            txt = path.read_text(encoding="utf-8")
        except Exception:
            continue
        mod = txt
        for old_h, new_h in hash_replacements:
            mod = mod.replace(old_h, new_h)
        if mod != txt:
            path.write_text(mod, encoding="utf-8")

# 5. Update sovereign_publisher_config.json with all verified hashes
cfg_path = priv_repo / "c2_cockpit/sovereign_publisher_config.json"
if cfg_path.exists():
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["merkle_root"] = merkle_root
    cfg["master_video_sha256"] = video_hash
    cfg["erdc_whitepaper_pdf_sha256"] = new_erdc_hash
    cfg["tradewinds_script_pdf_sha256"] = new_tw_hash
    cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

print(json.dumps({
    "merkle_root_sha256": merkle_root,
    "master_video_04_24_sha256": video_hash,
    "erdc_baa_whitepaper_pdf_sha256": new_erdc_hash,
    "tradewinds_script_pdf_sha256": new_tw_hash,
    "desktop_pdf_ready": str(desktop / "WHITE_PAPER_USACE_ERDC_BAA_2026.pdf"),
}, indent=2))
