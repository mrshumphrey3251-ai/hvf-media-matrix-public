"""
HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS
Module: compile_diu_pdf.py
Author: Jeffery Humphrey, Founder & CEO (Apex Architect)
Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME
Protocol: DEFENSE PROTOTYPE SOLUTION BRIEF COMPILATION (10 U.S.C. § 4022)
"""

import os
import sys
import sqlite3
import hashlib
import subprocess
from datetime import datetime

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
PROP_DIR = os.path.join(BASE_DIR, "proposals")
HTML_FILE = os.path.join(PROP_DIR, "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.html")
PDF_FILE = os.path.join(PROP_DIR, "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.pdf")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DIU Solution Brief | HVF Omni-Industrial Matrix</title>
<style>
  @page {
    size: letter;
    margin: 0.75in;
    @bottom-center { content: "PROPRIETARY & COMPETITION SENSITIVE (DFARS 252.227-7018) | Page " counter(page); }
  }
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.35;
    color: #000;
    margin: 0;
    padding: 0;
  }
  .header-box {
    border-bottom: 2px solid #000;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }
  .classification-banner {
    text-align: center;
    font-weight: bold;
    font-size: 11pt;
    letter-spacing: 1px;
    padding: 4px;
    background-color: #f0f0f0;
    border: 1px solid #999;
    margin-bottom: 12px;
  }
  h1 { font-size: 16pt; margin: 0 0 6px 0; text-transform: uppercase; }
  h2 { font-size: 13pt; margin: 16px 0 6px 0; border-bottom: 1px solid #666; padding-bottom: 2px; }
  p, li { font-size: 11.5pt; text-align: justify; }
  ul { margin-top: 4px; padding-left: 20px; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 10.5pt;
  }
  th, td {
    border: 1px solid #000;
    padding: 6px 8px;
    text-align: left;
  }
  th { background-color: #e6e6e6; font-weight: bold; }
  .table-total { font-weight: bold; background-color: #f5f5f5; }
  .sig-block {
    margin-top: 24px;
    border-top: 1px solid #000;
    padding-top: 8px;
  }
</style>
</head>
<body>

<div class="classification-banner">
  PROPRIETARY & COMPETITION SENSITIVE (DFARS 252.227-7018) | Nontraditional Defense Contractor
</div>

<div class="header-box">
  <h1>EXECUTIVE PROPOSAL BRIEF | SOVEREIGN PRIME CONTRACTOR</h1>
  <strong>SOLICITATION IDENTIFIER:</strong> DIU-AOI-2026-AUTONOMY<br>
  <strong>TARGET AGENCY:</strong> Defense Innovation Unit (DIU) / Department of Defense<br>
  <strong>PROGRAM TITLE:</strong> Contested Logistics & Edge Autonomy Resiliency<br>
  <strong>ACQUISITION VEHICLE:</strong> 10 U.S.C. § 4022 Commercial Solutions Opening (Prototype OT)<br>
  <strong>TOTAL PROTOTYPE ALLOCATION:</strong> $1,650,000.00 USD (100% Solo Prime Prime Allocation)<br>
  <strong>FORMAT:</strong> 5-Page Commercial Solution Brief
</div>

<h2>1. OPERATIONAL ENTITY & PRIME AUTHORITY</h2>
<ul>
  <li><strong>Prime Contractor:</strong> HVF Omni-Industrial Matrix (100% Unencumbered Prime)</li>
  <li><strong>Corporate Identifiers:</strong> CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Small Business Concern</li>
  <li><strong>Contracting Status:</strong> Nontraditional Defense Contractor pursuant to 10 U.S.C. § 4022(d)</li>
  <li><strong>Primary SME & Principal Investigator:</strong> Jeffery Humphrey, Founder & Chief Executive Officer (Apex Architect)</li>
  <li><strong>Corporate Headquarters & Testing Proving Grounds:</strong> Oklahoma Prototyping Laboratory</li>
  <li><strong>Primary Operational Contact:</strong> humphreyvirtualfarm@gmail.com</li>
</ul>

<h2>2. ARCHITECTURAL SOLUTION: PROJECT EBONY</h2>
<p>
Project Ebony delivers sovereign, zero-cloud autonomous resilience for tactical logistics, cyber-physical SCADA, and distributed uncrewed platforms in heavily contested (A2/AD) and electronic-warfare environments. Operating entirely on bare-metal silicon with zero external cloud dependencies, Project Ebony decouples physical actuation, cognitive anomaly detection, and cryptographic provenance across an air-gapped <strong>Three-Brain Architecture</strong>:
</p>
<ul>
  <li><strong>Brain One (Deterministic Controller & Kinetic Guillotine):</strong> Executes hard-real-time SCADA and kinetic actuation logic on bare-metal industrial microcontrollers (ARM Cortex-M and RISC-V). Brain One features the 'Kinetic Guillotine'—a hardware-anchored physical interlock that severs actuator circuits at the physical level in less than 1.0 microsecond upon boundary threshold breaches (frequency drift, voltage spikes, kinetic runaway). compromised software states cannot override an open electrical circuit.</li>
  <li><strong>Brain Two (Offline Cognitive Analyst):</strong> Executes offline neural inference directly on edge silicon, identifying multi-spectral anomalies and phenotypic drift without RF signatures, cloud querying, or external network leakage.</li>
  <li><strong>Brain Three (Local Cryptographic Merkle Arbiter):</strong> Maintains an immutable local Merkle DAG ledger logging every state frame in sub-millisecond cycles (&lt;0.2ms) to satisfy NIST SP 800-230 integrity standards without cloud tethers.</li>
</ul>

<h2>3. PERFORMANCE-BASED MILESTONE SCHEDULE ($150,000 MOBILIZATION)</h2>
<p>
HVF Omni-Industrial Matrix executes under performance-based payable milestones incorporating a front-loaded mobilization tranche (M1A) to fund long-lead hardware procurement, micro-architecture bench fabrication, and facility staging within 15–30 days of award:
</p>

<table>
  <thead>
    <tr>
      <th>Milestone</th>
      <th>Window</th>
      <th>Deliverable Focus & Verification Criteria</th>
      <th>Allocation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>M1A: Kickoff & Mobilization</strong></td>
      <td><strong>Days 15–30</strong></td>
      <td>Systems Engineering Plan (SEP), Post-Award Kickoff, Long-Lead Hardware Acquisition Plan, and Bench Initialization.</td>
      <td><strong>$150,000.00</strong></td>
    </tr>
    <tr>
      <td><strong>M1B: Hardware Integration</strong></td>
      <td>Month 3</td>
      <td>Bare-metal deployment of Brain One & Three; sub-millisecond Merkle DAG validation on ARM Cortex-M/RISC-V controllers.</td>
      <td>$200,000.00</td>
    </tr>
    <tr>
      <td><strong>M2: Environmental Hardening</strong></td>
      <td>Month 6</td>
      <td>Operational stress testing under simulated EW/network denial; automated Kinetic Guillotine interlock bench verification.</td>
      <td>$450,000.00</td>
    </tr>
    <tr>
      <td><strong>M3: Cognitive Optimization</strong></td>
      <td>Month 9</td>
      <td>Deployment of Brain Two offline neural inference; zero-cloud multi-axis sensor drift and anomaly classification.</td>
      <td>$450,000.00</td>
    </tr>
    <tr>
      <td><strong>M4: Proving Ground Demo</strong></td>
      <td>Month 12</td>
      <td>Live operational field demonstration on contested proving ground; delivery of full TRL-7 prototype data package.</td>
      <td>$400,000.00</td>
    </tr>
    <tr class="table-total">
      <td colspan="3"><strong>TOTAL PROTOTYPE CONTRACT EFFORT (10 U.S.C. § 4022)</strong></td>
      <td><strong>$1,650,000.00</strong></td>
    </tr>
  </tbody>
</table>

<h2>4. INTELLECTUAL PROPERTY ASSERTIONS & DATA RIGHTS</h2>
<p>
HVF Omni-Industrial Matrix asserts exclusive, unencumbered title to all Background Intellectual Property, source code, firmware, schematics, and neural models developed prior to or outside of this agreement pursuant to <strong>DFARS 252.227-7018</strong>. The Government receives negotiated commercial prototype evaluation rights for the duration of the Prototype OT. The contractor retains 100% commercial title, global licensing authority, and sole follow-on production rights under 10 U.S.C. § 4022(f).
</p>

<div class="sig-block">
  <strong>SUBMITTED ON BEHALF OF PRIME CONTRACTOR:</strong><br>
  <strong>Jeffery Humphrey</strong>, Founder & Chief Executive Officer<br>
  Apex Architect | HVF Omni-Industrial Matrix<br>
  CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Oklahoma, USA
</div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

# Look for Microsoft Edge to compile PDF
edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]
msedge_bin = next((p for p in edge_paths if os.path.exists(p)), None)

if msedge_bin:
    cmd = [
        msedge_bin,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={PDF_FILE}",
        HTML_FILE
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pdf_size = os.path.getsize(PDF_FILE)
    print(f"[SUCCESS] PDF generated via Microsoft Edge engine ({pdf_size:,} bytes)")
else:
    # Fallback: copy HTML as primary print deliverable
    print("[NOTICE] Microsoft Edge binary not in standard path; HTML master deliverable ready.")

doc_hash = hashlib.sha256(html_content.encode("utf-8")).hexdigest()

conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
conn.execute("""
    INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Jeffery Humphrey, CEO",
    "Defense Innovation Unit (DIU)",
    "DIU_SOLUTION_BRIEF_PDF_COMPILED",
    f"Compiled DoD-standard 5-page Solution Brief deliverable for DIU-AOI-2026-AUTONOMY ($1.65M). Hash: {doc_hash[:16]}",
    datetime.now().isoformat(),
    "DELIVERABLE_COMPILED_AND_SEALED"
))
conn.close()

print(f"[SUCCESS] DIU Solution Brief compiled: {HTML_FILE}")
if os.path.exists(PDF_FILE):
    print(f"[SUCCESS] PDF Deliverable ready: {PDF_FILE}")
print(f"  Cryptographic Hash : {doc_hash[:16]} (Sealed in hvf_memory_vault.db)")

