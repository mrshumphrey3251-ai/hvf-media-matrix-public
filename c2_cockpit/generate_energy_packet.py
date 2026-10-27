"""
HVFNexus Sovereign Industrial C2 — Commerce Energy Briefing Packet Generator
Compiles a polished, print-ready HTML portfolio for physical briefing with Rob Teele.
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit")
manifest_path = cockpit_dir / "compliance_manifest.json"
db_path = cockpit_dir / "matrix_ledger.db"

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
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
<title>HVF Energy Infrastructure Portfolio — Dept of Commerce Briefing</title>
<style>
  @page {{ size: letter; margin: 0.55in; }}
  body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: #1a1a1a; line-height: 1.45; margin: 0; padding: 18px; }}
  .header {{ border-bottom: 3px solid #0b5345; padding-bottom: 10px; margin-bottom: 16px; }}
  .header h1 {{ margin: 0; color: #0b5345; font-size: 23px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .header .subtitle {{ font-size: 13px; color: #444; margin-top: 4px; }}
  .badge-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px; }}
  .badge {{ background: #eafaf1; border: 1px solid #a3e4d7; border-radius: 4px; padding: 8px; text-align: center; }}
  .badge .label {{ font-size: 10px; text-transform: uppercase; color: #555; font-weight: bold; }}
  .badge .val {{ font-size: 14px; color: #0b5345; font-weight: bold; margin-top: 2px; }}
  h2 {{ color: #0b5345; font-size: 15px; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 14px; margin-bottom: 8px; text-transform: uppercase; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 12px; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 8px; text-align: left; }}
  th {{ background-color: #0b5345; color: white; text-transform: uppercase; font-size: 10px; }}
  tr:nth-child(even) {{ background-color: #f4fbf7; }}
  .callout {{ background: #eafaf1; border-left: 4px solid #117a65; padding: 9px 12px; margin: 10px 0; font-size: 11px; }}
  .footer {{ font-size: 9px; color: #777; text-align: center; margin-top: 20px; border-top: 1px solid #eee; padding-top: 6px; }}
</style>
</head>
<body>

<div class="header">
  <h1>Humphrey Virtual Farms LLC</h1>
  <div class="subtitle">Sovereign Industrial Energy Command &amp; Control (C2) | Autonomous Microgrid Optimization | Bare-Metal SCADA Hardening</div>
</div>

<div class="badge-grid">
  <div class="badge"><div class="label">CAGE Code</div><div class="val">{org['cage_code']}</div></div>
  <div class="badge"><div class="label">Unique Entity ID</div><div class="val">{org['uei']}</div></div>
  <div class="badge"><div class="label">Cyber Score</div><div class="val" style="color: #0e6251;">110 / 110 (SPRS)</div></div>
  <div class="badge"><div class="label">DoD UID</div><div class="val">{sprs['dod_unique_identifier']}</div></div>
</div>

<h2>1. Executive Mandate: Department of Commerce Energy Resilience</h2>
<div class="callout">
  <strong>Critical Energy Infrastructure:</strong> Humphrey Virtual Farms LLC operationalizes <em>Ebony</em> (HVFNexus Energy Core), a sovereign, bare-metal autonomous C2 architecture designed to stabilize industrial and agricultural energy loads, automate microgrid failover, and eliminate cloud cyber exposure across regional power networks.
</div>

<table>
  <tr><th>Operational Technology Requirement</th><th>Commercial Cloud Vulnerability</th><th>HVF Sovereign C2 Solution</th></tr>
  <tr><td><strong>Peak Demand Cost Management</strong></td><td>High latency, unable to react to sub-second load spikes</td><td>Local bare-metal edge execution reduces demand charges by 22%â€“38%</td></tr>
  <tr><td><strong>SCADA / OT Cybersecurity</strong></td><td>Third-party cloud APIs exposed to ransomware and foreign vectors</td><td>Enclave compliant with NIST SP 800-171 Rev 2 (TRL 4 Architectural Mapping (Phase-1 OTA Target), 0 open POA&amp;Ms)</td></tr>
  <tr><td><strong>Clean Energy &amp; Carbon Accounting</strong></td><td>Self-reported spreadsheets subject to audit disputes</td><td>Append-only WORM SQLite ledger binding kWh data to SHA-256 proofs</td></tr>
</table>

<h2>2. 4-Phase Commercial Energy Pilot Framework</h2>
<table>
  <tr><th>Phase</th><th>Deployment Window</th><th>Operational Deliverable</th></tr>
  <tr><td><strong>Phase 1: Zero-CAPEX Data Ingest</td><td>Days 1 – 30</td><td>Ingest existing facility smart meter data, SCADA exports, and Green Button utility data. No upfront hardware required.</td></tr>
  <tr><td><strong>Phase 2: Load Profiling</strong></td><td>Days 31 â€“ 60</td><td>Tariff schedule ingestion, demand ratchet modeling, and autonomous threshold calibration.</td></tr>
  <tr><td><strong>Phase 3: Active Peak Shaving</td><td>Days 61 – 120</td><td>Integration with grant-funded or facility-provided edge hardware for sub-second automated dispatch of battery storage and generation to suppress peak charges.</td></tr>
  <tr><td><strong>Phase 4: WORM Certification</strong></td><td>Day 121+</td><td>Continuous cryptographic sealing of energy data and certified utility interconnection audits.</td></tr>
</table>

<h2>3. Key Federal Classifications &amp; Commercialization Focus</h2>
<table>
  <tr><th>Classification Code</th><th>Description</th><th>Commercial Application</th></tr>
  <tr><td><strong>NAICS 541512</strong></td><td>Computer Systems Design Services</td><td>Autonomous Microgrid &amp; Industrial C2 Systems</td></tr>
  <tr><td><strong>NAICS 541715</strong></td><td>R&amp;D in Physical &amp; Engineering Sciences</td><td>Grid Edge Autonomy &amp; Contested Resilience</td></tr>
  <tr><td><strong>NAICS 111998</strong></td><td>All Other Miscellaneous Crop Farming</td><td>Controlled-Environment Agricultural Power Optimization</td></tr>
  <tr><td><strong>NAICS 221122</strong></td><td>Electric Power Distribution</td><td>Utility Co-op Demand Response &amp; SCADA Support</td></tr>
</table>

<div class="footer">
  Humphrey Virtual Farms LLC | Executive Contact: Jeffery Humphrey, CEO | {org['executive_email']} | (580) 677-1055 | Public Portal: github.com/mrshumphrey3251-ai/hvf-media-matrix-public
</div>

</body>
</html>
"""

packet_file = cockpit_dir / "HVF_COMMERCE_ENERGY_PACKET.html"
packet_file.write_text(html_content, encoding="utf-8")
print(f"[+] Commerce Energy Meeting Packet compiled: {packet_file}")
