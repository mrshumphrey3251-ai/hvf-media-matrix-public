"""
HVFNexus Sovereign Industrial C2 — Printable Executive Meeting Packet Generator
Compiles a polished, print-ready HTML portfolio for physical briefing with Rob Teele.
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit")
manifest_path = cockpit_dir / "compliance_manifest.json"
pipeline_path = cockpit_dir / "solicitation_pipeline.json"
db_path = cockpit_dir / "matrix_ledger.db"

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
pipeline = json.loads(pipeline_path.read_text(encoding="utf-8"))

org = manifest["organization"]
sprs = manifest["defense_portals"]["sprs"]

# Ledger stats
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("SELECT count(*) FROM executive_authorizations")
event_count = cursor.fetchone()[0]
cursor.execute("SELECT proof_hash FROM executive_authorizations WHERE artifact_hash = 'PHASE1-OTA-TARGET' LIMIT 1")
sprs_proof = cursor.fetchone()[0]
conn.close()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HVF Defense Executive Portfolio — Rob Teele Briefing</title>
<style>
  @page {{ size: letter; margin: 0.6in; }}
  body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: #1a1a1a; line-height: 1.45; margin: 0; padding: 20px; }}
  .header {{ border-bottom: 3px solid #003366; padding-bottom: 12px; margin-bottom: 20px; }}
  .header h1 {{ margin: 0; color: #003366; font-size: 24px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .header .subtitle {{ font-size: 13px; color: #555; margin-top: 4px; }}
  .badge-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }}
  .badge {{ background: #f0f4f8; border: 1px solid #c0d0e0; border-radius: 4px; padding: 8px; text-align: center; }}
  .badge .label {{ font-size: 10px; text-transform: uppercase; color: #666; font-weight: bold; }}
  .badge .val {{ font-size: 14px; color: #003366; font-weight: bold; margin-top: 2px; }}
  h2 {{ color: #003366; font-size: 16px; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 18px; margin-bottom: 8px; text-transform: uppercase; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 12px; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 8px; text-align: left; }}
  th {{ background-color: #003366; color: white; text-transform: uppercase; font-size: 10px; }}
  tr:nth-child(even) {{ background-color: #f9fbfd; }}
  .callout {{ background: #eef5fc; border-left: 4px solid #0055aa; padding: 10px; margin: 12px 0; font-size: 11px; }}
  .page-break {{ page-break-after: always; }}
  .footer {{ font-size: 9px; color: #888; text-align: center; margin-top: 25px; border-top: 1px solid #eee; padding-top: 6px; }}
</style>
</head>
<body>

<div class="header">
  <h1>Humphrey Virtual Farms LLC</h1>
  <div class="subtitle">Sovereign Industrial Command &amp; Control (C2) | Autonomous Systems | Cryptographic WORM Architecture</div>
</div>

<div class="badge-grid">
  <div class="badge"><div class="label">CAGE Code</div><div class="val">{org['cage_code']}</div></div>
  <div class="badge"><div class="label">Unique Entity ID</div><div class="val">{org['uei']}</div></div>
  <div class="badge"><div class="label">SPRS Score</div><div class="val" style="color: #007700;">110 / 110</div></div>
  <div class="badge"><div class="label">DoD UID</div><div class="val">{sprs['dod_unique_identifier']}</div></div>
</div>

<h2>1. Executive Summary &amp; Statutory Defense Posture</h2>
<div class="callout">
  <strong>Contractor Readiness:</strong> Humphrey Virtual Farms LLC satisfies all pre-award Department of Defense cybersecurity requirements pursuant to DFARS 252.204-7019/7020 with zero open POA&amp;M items. Fully qualified for prime bidding and Tier-1 prime subcontracting.
</div>

<table>
  <tr><th>Governance Parameter</th><th>Attested Metric</th><th>Verification Standard</th></tr>
  <tr><td>SAM.gov Registration</td><td>Active Small Business</td><td>GSA Federal Registry</td></tr>
  <tr><td>DoD PIEE Account</td><td>Active Contractor Administrator (CAM)</td><td>DISA Enterprise System</td></tr>
  <tr><td>SPRS Cyber Assessment</td><td>110 / 110 (Maximum BASIC Confidence)</td><td>DoD Unique ID: {sprs['dod_unique_identifier']}</td></tr>
  <tr><td>System Security Plan</td><td>{sprs['ssp_document']} (v{sprs['ssp_version']})</td><td>NIST SP 800-171 Rev 2 Enclave</td></tr>
  <tr><td>Cryptographic Ledger</td><td>{event_count} Immutable WORM Events</td><td>SHA-256 Proof: {sprs_proof[:32]}...</td></tr>
</table>

<h2>2. Core Competencies &amp; Federal Codes</h2>
<table>
  <tr><th>NAICS Code</th><th>Domain Classification</th><th>HVF Sovereign Capability</th></tr>
  <tr><td><strong>541512</strong></td><td>Computer Systems Design Services</td><td>Bare-Metal Autonomous C2 Architecture (HVFNexus)</td></tr>
  <tr><td><strong>541519</strong></td><td>Other Computer Related Services</td><td>Cryptographic WORM Audit Ledgers &amp; Zero-Trust Logging</td></tr>
  <tr><td><strong>541511</strong></td><td>Custom Computer Programming</td><td>Deterministic Edge Telemetry &amp; Real-Time Data Ingest</td></tr>
  <tr><td><strong>541715</strong></td><td>R&amp;D in Physical &amp; Engineering Sciences</td><td>Contested Logistics &amp; Resilient Edge Autonomy</td></tr>
  <tr><td><strong>111998</strong></td><td>Miscellaneous Crop Farming</td><td>Controlled-Environment Agricultural Telemetry</td></tr>
</table>

<h2>3. APEX Bid Match Criteria for Rob Teele</h2>
<table>
  <tr><th>Parameter</th><th>Targeted Configuration</th></tr>
  <tr><td><strong>Target PSC/FSC Codes</strong></td><td>D302 (Systems Dev), D307 (IT Strategy), D310 (Cybersecurity), AC11 (Autonomous R&amp;D), AC21 (C2 R&amp;D)</td></tr>
  <tr><td><strong>Match Keywords</strong></td><td>"Command and Control", "C2", "Autonomous Systems", "Bare-Metal", "WORM Ledger", "NIST 800-171"</td></tr>
  <tr><td><strong>Target Procuring Agencies</strong></td><td>Dept of the Army, Defense Innovation Unit (DIU), DARPA, Defense Logistics Agency (DLA)</td></tr>
  <tr><td><strong>Action Items Requested</strong></td><td>1. Provision DLA Automated Bid Match. 2. Warm intro to Prime SBLOs. 3. SBIR/STTR alignment.</td></tr>
</table>

<div class="footer">
  Humphrey Virtual Farms LLC | Executive Contact: Jeffery Humphrey, CEO | {org['executive_email']} | (580) 677-1055 | Public Dossier: github.com/mrshumphrey3251-ai/hvf-media-matrix-public
</div>

</body>
</html>
"""

output_path = cockpit_dir / "HVF_EXECUTIVE_MEETING_PACKET.html"
output_path.write_text(html_content, encoding="utf-8")
print(f"[+] Printable Executive Packet compiled: {output_path}")
