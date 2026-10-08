"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: MANAGE MARGINS AND COMPILE PDF
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS

    Module: manage_margins_and_compile_pdf.py

    Author: Jeffery Humphrey, Founder & CEO (Apex Architect)

    Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME

    Protocol: DEFENSE DELIVERABLE RIGHT-MARGIN CALIBRATION & PDF COMPILATION

    """



    import os

    import sys

    import sqlite3

    import hashlib

    import subprocess

    from datetime import datetime



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    PROP_DIR = os.path.join(BASE_DIR, "proposals")

    os.makedirs(PROP_DIR, exist_ok=True)

    HTML_FILE = os.path.join(PROP_DIR, "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.html")

    PDF_FILE = os.path.join(PROP_DIR, "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.pdf")

    MD_FILE = os.path.join(PROP_DIR, "TAILORED_BRIEF_DIU-AOI-2026-AUTONOMY.md")

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")



    html_content = """<!DOCTYPE html>

    <html lang="en">

    <head>

    <meta charset="UTF-8">

    <title>DIU Solution Brief | HVF Omni-Industrial Matrix</title>

    <style>

      * {

        box-sizing: border-box;

        margin: 0;

        padding: 0;

      }

      @page {

        size: letter;

        margin-top: 0.75in;

        margin-bottom: 0.75in;

        margin-left: 0.75in;

        margin-right: 0.85in;

        @bottom-center {

          content: "PROPRIETARY & COMPETITION SENSITIVE (DFARS 252.227-7018) | Page " counter(page);

          font-size: 9pt;

          font-family: 'Times New Roman', serif;

        }

      }

      body {

        font-family: 'Times New Roman', Times, serif;

        font-size: 12pt;

        line-height: 1.35;

        color: #000;

        padding-right: 0.1in;

        word-wrap: break-word;

        overflow-wrap: break-word;

      }

      .classification-banner {

        text-align: center;

        font-weight: bold;

        font-size: 10pt;

        letter-spacing: 0.5px;

        padding: 5px;

        background-color: #f2f2f2;

        border: 1px solid #777;

        margin-bottom: 14px;

        width: 100%;

      }

      .header-box {

        border-bottom: 2px solid #000;

        padding-bottom: 8px;

        margin-bottom: 14px;

        width: 100%;

      }

      h1 { font-size: 15pt; margin-bottom: 6px; text-transform: uppercase; line-height: 1.2; }

      h2 { font-size: 12.5pt; margin-top: 14px; margin-bottom: 6px; border-bottom: 1px solid #666; padding-bottom: 2px; }

      p { font-size: 11.5pt; text-align: justify; margin-bottom: 8px; text-justify: inter-word; }

      ul { margin-top: 4px; margin-bottom: 8px; padding-left: 22px; }

      li { font-size: 11.5pt; margin-bottom: 4px; text-align: justify; }

      table {

        width: 100%;

        table-layout: fixed;

        border-collapse: collapse;

        margin: 10px 0;

        font-size: 10pt;

      }

      th, td {

        border: 1px solid #333;

        padding: 5px 6px;

        vertical-align: top;

        word-wrap: break-word;

        overflow-wrap: break-word;

      }

      th { background-color: #e6e6e6; font-weight: bold; text-align: left; }

      col.col-m { width: 22%; }

      col.col-w { width: 14%; }

      col.col-d { width: 49%; }

      col.col-a { width: 15%; }

      .table-total { font-weight: bold; background-color: #f5f5f5; }

      .sig-block {

        margin-top: 20px;

        border-top: 1px solid #000;

        padding-top: 8px;

        font-size: 11pt;

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

      <strong>TARGET AGENCY:</strong> Defense Innovation Unit (DIU) / Office of the Under Secretary of Defense (R&E)<br>

      <strong>PROGRAM TITLE:</strong> Contested Logistics & Edge Autonomy Resiliency<br>

      <strong>ACQUISITION VEHICLE:</strong> 10 U.S.C. § 4022 Commercial Solutions Opening (Prototype Other Transaction)<br>

      <strong>TOTAL PROTOTYPE ALLOCATION:</strong> $1,650,000.00 USD (100% Solo-Prime Allocation)<br>

      <strong>SUBMISSION FORMAT:</strong> 5-Page Commercial Solution Brief

    </div>



    <h2>1. OPERATIONAL ENTITY & PRIME AUTHORITY</h2>

    <ul>

      <li><strong>Prime Contractor:</strong> HVF Omni-Industrial Matrix (100% Unencumbered Prime)</li>

      <li><strong>Corporate Identifiers:</strong> CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Small Business Concern</li>

      <li><strong>Contracting Status:</strong> Nontraditional Defense Contractor pursuant to 10 U.S.C. § 4022(d)(1)(A)</li>

      <li><strong>Primary SME & Principal Investigator:</strong> Jeffery Humphrey, Founder & CEO (Apex Architect)</li>

      <li><strong>Headquarters & Prototyping Laboratory:</strong> Oklahoma City, Oklahoma, USA</li>

      <li><strong>Primary Operational Contact:</strong> humphreyvirtualfarm@gmail.com</li>

    </ul>



    <h2>2. ARCHITECTURAL SOLUTION: PROJECT EBONY</h2>

    <p>

    Project Ebony delivers sovereign, zero-cloud autonomous resilience for tactical logistics, cyber-physical SCADA, and distributed uncrewed platforms in heavily contested Anti-Access/Area Denial (A2/AD) and electronic warfare (EW) environments. Operating entirely on bare-metal silicon with zero external cloud dependencies, Project Ebony decouples physical actuation, cognitive anomaly detection, and cryptographic provenance across an air-gapped <strong>Three-Brain Architecture</strong>:

    </p>

    <ul>

      <li><strong>Brain One (Deterministic Controller & Kinetic Guillotine):</strong> Executes hard-real-time SCADA and kinetic actuation logic on bare-metal ARM Cortex-M7 and RISC-V microcontrollers. Features the 'Kinetic Guillotine'—a hardware-anchored physical interlock that severs actuator power circuits in less than 1.0 microsecond upon boundary threshold breaches (voltage, current, pressure, vibration). Compromised software cannot override an open physical circuit.</li>

      <li><strong>Brain Two (Offline Cognitive Analyst):</strong> Executes edge neural inference locally on dedicated acceleration silicon, identifying multi-spectral anomalies and phenotypic drift in under 5.0ms without RF leakage or cloud queries.</li>

      <li><strong>Brain Three (Local Merkle Arbiter):</strong> Maintains an immutable local Merkle DAG ledger logging every state transition in sub-millisecond cycles (&lt;0.2ms) satisfying NIST SP 800-230 integrity standards with zero external dependencies.</li>

    </ul>



    <h2>3. PERFORMANCE-BASED MILESTONE SCHEDULE ($150,000 MOBILIZATION)</h2>

    <p>

    HVF Omni-Industrial Matrix executes under performance-based payable milestones incorporating a front-loaded mobilization tranche (M1A) to fund long-lead hardware procurement, micro-architecture bench fabrication, and testbed staging within 15–30 days of award:

    </p>



    <table>

      <colgroup>

        <col class="col-m">

        <col class="col-w">

        <col class="col-d">

        <col class="col-a">

      </colgroup>

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

          <td><strong>M1A: Mobilization</strong></td>

          <td><strong>Days 15–30</strong></td>

          <td>Systems Engineering Plan (SEP), Post-Award Kickoff, Long-Lead Silicon Procurement Plan, and Prototyping Lab Initialization.</td>

          <td><strong>$150,000.00</strong></td>

        </tr>

        <tr>

          <td><strong>M1B: HW Integration</strong></td>

          <td>Month 3</td>

          <td>Bare-metal deployment of Brain One & Three; sub-0.15ms SHA-256 Merkle DAG state validation on ARM/RISC-V hardware.</td>

          <td>$200,000.00</td>

        </tr>

        <tr>

          <td><strong>M2: Hardening</strong></td>

          <td>Month 6</td>

          <td>Hardware-in-the-Loop (HIL) stress-testing across 10,000 fault-injection cycles; &lt;1.0us Kinetic Guillotine circuit cutoff verification.</td>

          <td>$450,000.00</td>

        </tr>

        <tr>

          <td><strong>M3: AI Optimization</strong></td>

          <td>Month 9</td>

          <td>Brain Two offline neural inference deployment; multi-spectral sensor spoofing detection (&lt;5.0ms) with zero outbound RF emissions.</td>

          <td>$450,000.00</td>

        </tr>

        <tr>

          <td><strong>M4: Field Demo</strong></td>

          <td>Month 12</td>

          <td>48-hour continuous air-gapped operational field demonstration on live pumping testbed under simulated EW denial; TRL-7 data package.</td>

          <td>$400,000.00</td>

        </tr>

        <tr class="table-total">

          <td colspan="3"><strong>TOTAL PROTOTYPE CONTRACT EFFORT (10 U.S.C. § 4022)</strong></td>

          <td><strong>$1,650,000.00</strong></td>

        </tr>

      </tbody>

    </table>



    <h2>4. INTELLECTUAL PROPERTY & DATA RIGHTS (DFARS 252.227-7018)</h2>

    <p>

    HVF Omni-Industrial Matrix asserts 100% exclusive, unencumbered ownership of all Background Intellectual Property, bare-metal source code, hardware schematics, firmware architectures, and neural models developed prior to or outside of this agreement pursuant to DFARS 252.227-7018. The Government receives negotiated commercial prototype evaluation rights strictly for testing and evaluation during the Prototype OT. HVF retains absolute commercial title, sole licensing authority, and exclusive follow-on production rights under 10 U.S.C. § 4022(f).

    </p>



    <div class="sig-block">

      <strong>SUBMITTED ON BEHALF OF PRIME CONTRACTOR:</strong><br>

      <strong>Jeffery Humphrey</strong>, Founder & Chief Executive Officer<br>

      Apex Architect & Principal Investigator | HVF Omni-Industrial Matrix<br>

      CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Oklahoma City, Oklahoma, USA

    </div>



    </body>

    </html>

    """



    # Write HTML with calibrated margins

    with open(HTML_FILE, "w", encoding="utf-8") as f:

        f.write(html_content)



    # Render to PDF using Microsoft Edge headless engine

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

        print(f"[SUCCESS] PDF re-compiled with calibrated margins ({pdf_size:,} bytes)")



    # Read Markdown brief and pipe to clipboard buffer

    if os.path.exists(MD_FILE):

        with open(MD_FILE, "r", encoding="utf-8") as f:

            md_text = f.read()

        p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)

        p.communicate(md_text.strip().encode("utf-8"))

        print("[SUCCESS] Full Markdown brief loaded into Windows clipboard buffer.")



    doc_hash = hashlib.sha256(html_content.encode("utf-8")).hexdigest()



    conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)

    conn.execute("""

        INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)

        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        "Jeffery Humphrey, CEO",

        "Defense Innovation Unit (DIU)",

        "RIGHT_MARGINS_CALIBRATED_AND_SEALED",

        f"Calibrated right-side margins (0.85in margin + fixed table layout). Hash: {doc_hash[:16]}",

        datetime.now().isoformat(),

        "MARGINS_CALIBRATED_AND_SEALED"

    ))

    conn.close()



    print(f"[SUCCESS] Right-side margins managed (0.85in right boundary + fixed table layout).")

    print(f"  HTML Artifact : {HTML_FILE}")

    print(f"  PDF Artifact  : {PDF_FILE}")

    print(f"  Digest        : {doc_hash[:16]} (Sealed in memory vault)")




if __name__ == "__main__":
    render()
