import os
import sys
from pathlib import Path
from datetime import datetime, timezone

private_dir = Path(r"C:\HVF_Repos\hvf-media-matrix-private\governance\legal")
public_dir = Path(r"C:\HVF_Repos\hvf-media-matrix-public\governance\legal")
private_dir.mkdir(parents=True, exist_ok=True)
public_dir.mkdir(parents=True, exist_ok=True)

pdf_private = private_dir / "MUTUAL_NDA_VANDERPOOL_ENERGY_DESIGN.pdf"
pdf_public = public_dir / "MUTUAL_NDA_VANDERPOOL_ENERGY_DESIGN.pdf"
html_path = private_dir / "temp_nda.html"

today_str = datetime.now(timezone.utc).strftime('%B %d, %Y')

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Mutual NDA - HVF & Vanderpool Energy Design LLC</title>
<style>
    body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.5; color: #111; margin: 40px; font-size: 13px; }}
    h1 {{ font-size: 18px; text-align: center; text-transform: uppercase; margin-bottom: 5px; }}
    .subtitle {{ text-align: center; font-size: 11px; color: #555; margin-bottom: 25px; }}
    h2 {{ font-size: 13px; text-transform: uppercase; border-bottom: 1px solid #ccc; padding-bottom: 3px; margin-top: 20px; }}
    p, li {{ text-align: justify; }}
    .sig-table {{ width: 100%; margin-top: 40px; border-collapse: collapse; }}
    .sig-table td {{ width: 50%; vertical-align: top; padding: 15px; border: 1px solid #ddd; }}
    .line {{ border-bottom: 1px solid #000; height: 35px; margin-bottom: 5px; }}
</style>
</head>
<body>
    <h1>Mutual Non-Disclosure & Intellectual Property Protection Agreement</h1>
    <div class="subtitle">Effective Date: {today_str} | Governing Jurisdiction: State of Oklahoma</div>

    <p>This Mutual Non-Disclosure and Intellectual Property Protection Agreement ("Agreement") is entered into by and between:</p>
    <p><b>1. Humphrey Virtual Farm & Media Matrix</b> ("HVF"), operating under CAGE Code <b>1AHA8</b>, represented by <b>Jeffery Humphrey</b>, CEO & Founder (Principal Architect, Project Ebony), with corporate address in Oklahoma; and</p>
    <p><b>2. Vanderpool Energy Design LLC</b> ("Company"), a limited liability company organized under the laws of the <b>Commonwealth of Pennsylvania</b>, represented by <b>Richard Vanderpool</b>, Founder, with delivery address at <b>rickyvanderpool15@gmail.com</b>.</p>

    <h2>1. Purpose of Engagement</h2>
    <p>The Parties desire to conduct preliminary exploratory discussions strictly limited to evaluating technical and commercial compatibility between Company's modular physical containment/vault designs and HVF's sovereign bare-metal control layer ("Project Ebony" / "Chronos SCADA" / "Protocol Lambda").</p>

    <h2>2. Strict Carve-Out & Preservation of Pre-Existing IP</h2>
    <p>Company expressly acknowledges and agrees that <b>Project Ebony</b>, <b>Protocol Lambda</b>, <b>Chronos SCADA</b>, the <b>Tri-Brain Bare-Metal Edge Architecture</b>, <b>Sub-Microsecond Kinetic Isolation</b>, <b>Tradewinds Docket 9-26-3703</b>, and all related algorithms, switchgear telemetry, and firmware constitute the sole, exclusive, pre-existing intellectual property of Jeffery Humphrey / HVF. No license, transfer, joint ownership, or implied right is granted under this Agreement.</p>

    <h2>3. Patent Preclusion & Non-Circumvention</h2>
    <p>Company expressly covenants that it shall not incorporate, adapt, reference, or utilize any technical disclosures, logic flows, or architectural models received from HVF into any pending, provisional, continuation, or future patent applications or utility filings. Neither Party shall bypass or circumvent the other regarding proprietary methods disclosed.</p>

    <h2>4. Confidentiality & Non-Disclosure</h2>
    <p>Each Party agrees to hold Confidential Information in strict confidence using no less than reasonable care. Confidentiality obligations endure for five (5) years from disclosure, while trade secret obligations endure indefinitely.</p>

    <h2>5. Governing Law & Jurisdiction</h2>
    <p>This Agreement shall be governed by and construed under the laws of the <b>State of Oklahoma</b>. Any disputes shall be adjudicated exclusively in state or federal courts within Oklahoma.</p>

    <table class="sig-table">
        <tr>
            <td>
                <b>Humphrey Virtual Farm & Media Matrix</b><br><br>
                By: <div class="line"></div>
                Name: Jeffery Humphrey<br>
                Title: Chief Executive Officer & Founder<br>
                Date: {today_str}
            </td>
            <td>
                <b>Vanderpool Energy Design LLC</b><br><br>
                By: <div class="line"></div>
                Name: Richard Vanderpool<br>
                Title: Founder<br>
                Email: rickyvanderpool15@gmail.com<br>
                Date: __________________________________
            </td>
        </tr>
    </table>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[*] HTML source built at: {html_path}")

# Attempt PDF compilation via headless Edge/Chrome
import subprocess

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
]

browser_bin = None
for p in edge_paths:
    if os.path.exists(p):
        browser_bin = p
        break

if browser_bin:
    cmd = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_private}",
        str(html_path)
    ]
    subprocess.run(cmd, check=True)
    import shutil
    shutil.copy2(pdf_private, pdf_public)
    print(f"[+] Successfully compiled PDF across both repos:")
    print(f"    - {pdf_private}")
    print(f"    - {pdf_public}")
else:
    print("[!] No standard browser engine found for PDF compilation.")
