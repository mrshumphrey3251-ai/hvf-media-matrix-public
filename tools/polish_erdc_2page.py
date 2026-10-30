from pathlib import Path
import subprocess, sys

p = Path("c2_cockpit/compile_erdc_baa_whitepaper.py")
txt = p.read_text(encoding="utf-8")

# Replace 92-char '====' bars with 84-char bars so zero '====' lines wrap and it fits cleanly on 2 pages
txt = txt.replace("=" * 92, "=" * 84)
txt = txt.replace("\n\n====", "\n====")

p.write_text(txt, encoding="utf-8")
pub_p = Path(r"C:\hvf_c2\hvf-media-matrix-public\c2_cockpit\compile_erdc_baa_whitepaper.py")
if pub_p.parent.exists():
    pub_p.write_text(txt, encoding="utf-8")

subprocess.run([sys.executable, "c2_cockpit/compile_erdc_baa_whitepaper.py"], check=True)
