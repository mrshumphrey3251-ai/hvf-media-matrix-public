#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HUMPHREY VIRTUAL FARMS LLC // USACE ERDC CERL CSO (2026) 4-DOCUMENT PDF SUITE COMPILER
Generates the 4 mandatory ERDCWERX CERL CSO (2026) PDF artifacts with exact naming conventions:
1. Solution-CoverLetter-Humphrey Virtual Farms LLC.pdf
2. Solution-Brief-Humphrey Virtual Farms LLC.pdf
3. Solution-PitchDeck-Humphrey Virtual Farms LLC.pdf
4. Solution-Price-Humphrey Virtual Farms LLC.pdf
"""

import hashlib
import json
import textwrap
from pathlib import Path
from typing import Dict, List, Tuple

ROOT_PRIV = Path(r"C:\hvf_c2\hvf-media-matrix-private")
ROOT_PUB  = Path(r"C:\hvf_c2\hvf-media-matrix-public")
DESKTOP   = Path(r"C:\Users\mrshu\OneDrive\Desktop")


def _escape_pdf_text(s: str) -> str:
    clean = s.encode("ascii", "replace").decode("ascii")
    return clean.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_times_12pt_pdf(paragraphs: List[Tuple[str, str]]) -> bytes:
    wrapped_lines: List[Tuple[str, str]] = []
    for style, para in paragraphs:
        width = 74 if style == "B" else 78
        lines = textwrap.wrap(para, width=width) or [""]
        if style == "B" and wrapped_lines:
            wrapped_lines.append(("N", ""))
        for ln in lines:
            wrapped_lines.append((style, ln))

    lines_per_page = 40
    pages = [
        wrapped_lines[i : i + lines_per_page]
        for i in range(0, len(wrapped_lines), lines_per_page)
    ] or [[("N", "")]]
    total_pages = len(pages)

    objects: List[bytes] = []

    def add_obj(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font_reg_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >>")
    font_bold_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>")

    page_ids: List[int] = []
    content_ids: List[int] = []

    for p_idx, p_lines in enumerate(pages, start=1):
        cmds = ["BT", "72 708 Td", "14.4 TL"]
        for style, ln in p_lines:
            font_tag = "/F2 12 Tf" if style == "B" else "/F1 12 Tf"
            cmds.append(f"{font_tag} ({_escape_pdf_text(ln)}) Tj T*")
        cmds.append("ET")
        cmds.append("BT")
        cmds.append(f"/F1 12 Tf 285 72 Td ({p_idx} of {total_pages}) Tj")
        cmds.append("ET")
        stream_bytes = "\n".join(cmds).encode("ascii")
        c_id = add_obj(
            f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii")
            + stream_bytes
            + b"\nendstream"
        )
        content_ids.append(c_id)

    pages_tree_id = len(objects) + len(pages) + 1
    for c_id in content_ids:
        p_obj = (
            f"<< /Type /Page /Parent {pages_tree_id} 0 R "
            f"/MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_reg_id} 0 R /F2 {font_bold_id} 0 R >> >> "
            f"/Contents {c_id} 0 R >>"
        ).encode("ascii")
        page_ids.append(add_obj(p_obj))

    kids_str = " ".join(f"{pid} 0 R" for pid in page_ids)
    actual_pages_id = add_obj(
        f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_ids)} >>".encode("ascii")
    )
    catalog_id = add_obj(f"<< /Type /Catalog /Pages {actual_pages_id} 0 R >>".encode("ascii"))

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{idx} 0 obj\n".encode("ascii"))
        out.extend(obj)
        out.extend(b"\nendobj\n")

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode(
            "ascii"
        )
    )
    return bytes(out)


COVER_LETTER_PARAS = [
    ("B", "USACE ERDC CONSTRUCTION & ENGINEERING RESEARCH LABORATORY (CERL) COMMERCIAL SOLUTIONS OPENING (CSO 2026) - EXECUTIVE COVER LETTER"),
    ("N", "Date: October 30, 2026"),
    ("N", "Primary Offeror: Humphrey Virtual Farms LLC (701 E Drew St., Madill, OK 73446)"),
    ("N", "Business Status: Non-Traditional Defense Contractor (NTDC), Small Disadvantaged Business (SDB), Minority-Owned Small Business"),
    ("N", "SAM.gov UEI: S1M4ENLHTDH5 | CAGE Code: 1AHA8 | NAICS: 541715, 541511, 541330"),
    ("N", "Authorized Representative: Jeffery Humphrey, Founder, President & CEO | (572) 358-9978 | humphreyvirtualfarm@gmail.com"),
    ("N", "Proposed Solution Title: Project Ebony v8.0.0: Air-Gapped Tri-Brain OT/SCADA Safety Interlock, Automated Bridge/Pavement NDE & WORM Merkle Provenance Testbed"),
    ("N", "CERL Areas of Interest: Operational Energy; Sustainment Management System; Robotics for Engineering Operations"),
    ("N", "Cross-Referenced Federal Filings: Active DoD CDAO Tradewinds Solutions Marketplace Docket 10-26-4046 (Status: Received | Video SHA-256: c597865785eae6fdad6fdf6803a2710aaa0fb5c2fa28fe512b6ed76ef8b7a7fd | Merkle Root: bb39eeaa66a39ad2e0c0ab74ba4a5c4faac2bf0d98babc0362482b97607151a1) and USACE ERDC BAA Filings (CERL, ITL-4, GSL-19)."),
    ("B", "1. Executive Purpose & Statutory Eligibility (10 U.S.C. 4022 / 10 U.S.C. 3458)"),
    ("N", "Humphrey Virtual Farms LLC respectfully submits this complete four-part Commercial Solutions Opening (CSO) package to the U.S. Army Engineer Research and Development Center (ERDC) Construction and Engineering Research Laboratory (CERL). As a verified U.S. Non-Traditional Defense Contractor (NTDC) and Small Disadvantaged Business (SDB) actively registered in SAM.gov (UEI: S1M4ENLHTDH5 | CAGE: 1AHA8), Humphrey Virtual Farms LLC qualifies for streamlined commercial and prototype Other Transaction Authority (OTA) or FAR/DFARS award with 0% required cost sharing."),
    ("B", "2. Summary of Operational Impact for CERL Installations & Facilities"),
    ("N", "Per U.S. GAO reports GAO-21-81 and GAO-24-106137 and Joint CISA/DoD Volt Typhoon advisories (AA23-144A / AA24-038A), DoD's 500+ installations, 300,000+ buildings, and $4.2B+ in operational energy and utility assets rely on commercial PLCs scanning at 50 to 200ms, whereas arc-flash faults destroy switchgear in <4.16ms and thermal excursions occur in 6.0ms. Project Ebony v8.0.0 provides a live TRL 4 air-gapped software emulation testbed on local loopback 127.0.0.1 (0% cloud dependency, 0 external retrieval APIs, 637 C2 modules, 85/85 passing unit test suites, 52 SQLite WORM tables) modeling a <50us safety loop and 36.75ns SiC MOSFET cutoff target (Brain 1), isolated ASTM D6433 structural/pavement NDE diagnostics cutting $4,600/day inspections to $250/sortie (Brain 2), and SHA-256 WORM Merkle provenance (Brain 3)."),
    ("B", "3. Non-Proprietary & Unclassified Compliance Statement"),
    ("N", "In strict compliance with ERDCWERX CSO instructions, this submission contains no classified, confidential, or restricted proprietary markings and may be shared across ERDC teams. Background commercial software modules developed at private expense are governed by standard DFARS 252.227-7018 / FAR 52.227-14 provisions upon award. Respectfully submitted by Jeffery Humphrey, Founder, President & CEO, Humphrey Virtual Farms LLC."),
]

SOLUTION_BRIEF_PARAS = [
    ("B", "USACE ERDC CERL COMMERCIAL SOLUTIONS OPENING (CSO 2026) - SOLUTION BRIEF"),
    ("B", "Title: Project Ebony v8.0.0: Air-Gapped Tri-Brain OT/SCADA Safety Interlock, Automated Bridge/Pavement NDE & WORM Merkle Provenance Testbed"),
    ("N", "Offeror: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Madill, OK 73446"),
    ("N", "POC: Jeffery Humphrey, CEO | (572) 358-9978 | humphreyvirtualfarm@gmail.com | Public Repo: https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public"),
    ("B", "1. Problem Identification & CERL Operational Energy / Infrastructure Gap"),
    ("N", "Per GAO-21-81 and GAO-24-106137, the Department of Defense and USACE operate 500+ military installations, 300,000+ buildings, and $4.2B+ in operational energy microgrids and facility control systems relying on digital PLCs scanning at 50 to 200 milliseconds. Per Joint CISA/NSA/FBI/DoD Advisories AA23-144A and AA24-038A (Volt Typhoon) and TRISIS, state-sponsored actors pre-position inside installation energy, water, and utility OT networks to corrupt PLC logic while spoofing operator HMIs. Because arc-flash faults destroy switchgear in <4.16ms and thermal excursions occur in 6.0ms, 50-200ms PLC scans react 8x to 33x too late. Simultaneously, conventional facility, bridge, and pavement condition assessments require manual crews and snooper trucks costing $4,600+/day without tamper-evident telemetry logs."),
    ("B", "2. Technical Solution: Air-Gapped Tri-Brain Architecture (TRL 4 Baseline to TRL 6)"),
    ("N", "Project Ebony v8.0.0 is an active TRL 4 laboratory software emulation testbed running 100% offline on local workstation loopback 127.0.0.1 with 0% commercial cloud dependency, 0 external retrieval APIs, 0 third-party vector DBs, and 0 open WAN ports:"),
    ("N", "- Brain 1 (Operational Energy & Microgrid Safety Interlock): Executes deterministic physical boundary mathematics in software and models our Phase-1 hardware target: a <50us bare-metal Cortex-M7/RISC-V control loop, 2.04us RS-485 Modbus FC05 trip, and a 36.75ns Silicon-Carbide (SiC) MOSFET Analog Kinetic Guillotine gate cutoff—1,360,544x faster than a 50ms PLC at a 28.5W target power draw on a 24V DC bus."),
    ("N", "- Brain 2 (Robotics & Sustainment Management NDE Diagnostics): Operates across a unidirectional read-only hardware buffer with zero electrical actuator wire. Performs offline automated ASTM D6433 Pavement Condition Index (PCI) distress classification, crack-width mensuration, and structural health monitoring, modeling a 94.6% cost reduction ($250/sortie autonomous NDE vs. $4,600/day manual closures)."),
    ("N", "- Brain 3 (52-Table SQLite WORM Enclave & Merkle Provenance): Executes all data retrieval locally inside an air-gapped 52-table bare-metal SQLite WORM enclave (matrix_ledger.db + hvf_memory_vault.db) and seals a SHA-256 Merkle DAG (Root: bb39eeaa66a39ad2e0c0ab74ba4a5c4faac2bf0d98babc0362482b97607151a1) in <0.15ms across 637 compiled C2 Python modules, 85/85 passing unit test suites, 17/17 blocked Red-Team vectors, and a 110-control NIST SP 800-171 / 800-82 mapping."),
    ("B", "3. 5-Vendor Quantitative Analysis of Alternatives (6 of 6 Mission Gates Passed)"),
    ("N", "Project Ebony v8.0.0 passes 6/6 gates (sub-ms cutoff, zero-cloud air-gap, WORM provenance, isolated NDE, <30W SWaP-C, tamper zeroization), outperforming Siemens S7-1500/Rockwell ControlLogix (50-200ms, 150-450W), Schneider Triconex SIS (10-50ms, 200-600W, breached by TRISIS), passive IDS Dragos/Nozomi (0 cutoff authority, 300-1,200W), and commercial cloud AI wrappers (>250ms RTT, fails under EMCON)."),
    ("B", "4. Proposed 12-Month Phase-1 Prototype Plan & Dual-Use Commercial Viability"),
    ("N", "Humphrey Virtual Farms LLC proposes a 12-Month, $1,200,000.00 Fixed-Price Phase-1 Prototype Effort ($150,000.00 Mobilization) advancing Project Ebony from TRL 4 to TRL 6, or modular dual-use licensing starting at CLIN 0001 ($2,450/mo) and CLIN 1004-A ($895,000/yr). Non-proprietary submission; background IP retained under DFARS 252.227-7018."),
]

PITCH_DECK_PARAS = [
    ("B", "SLIDE 1 OF 5: EXECUTIVE OVERVIEW & CERL MISSION ALIGNMENT"),
    ("N", "- Solution: Project Ebony v8.0.0: Air-Gapped Tri-Brain OT/SCADA Safety Interlock, Automated Bridge/Pavement NDE & WORM Merkle Provenance Testbed"),
    ("N", "- Offeror: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Madill, OK 73446)"),
    ("N", "- Status: Non-Traditional Defense Contractor (NTDC) & Small Disadvantaged Business (SDB)"),
    ("N", "- CERL Alignment: Operational Energy (Microgrids/Switchgear), Sustainment Management System (SMS/BUILDER Sensor Analytics), Robotics for Engineering Operations (Autonomous NDE)"),
    ("N", "- Verified Federal Docket: DoD CDAO Tradewinds Docket 10-26-4046 (Status: Received | 04:24 Video SHA-256: c597865785eae6fdad6fdf6803a2710aaa0fb5c2fa28fe512b6ed76ef8b7a7fd)"),
    ("B", "SLIDE 2 OF 5: THE <4.16ms INSTALLATION OT/SCADA & SUSTAINMENT PHYSICS GAP"),
    ("N", "- GAO-21-81 & GAO-24-106137: DoD operates 500+ installations, 300,000+ buildings, and $4.2B+ in OT energy systems on legacy PLCs scanning at 50 to 200ms."),
    ("N", "- CISA AA23-144A / AA24-038A (Volt Typhoon) & TRISIS: Adversaries corrupt PLC safety logic while spoofing operator displays."),
    ("N", "- Physics Gap: High-voltage arc-flash faults destroy switchgear in <4.16ms and thermal excursions occur in 6.0ms—meaning 50-200ms PLCs react 8x to 33x too late."),
    ("N", "- Sustainment Gap: Manual bridge, pavement, and facility inspections cost $4,600+/day with snooper-truck closures and lack cryptographic chain-of-custody verification."),
    ("B", "SLIDE 3 OF 5: LIVE TRL 4 AIR-GAPPED TRI-BRAIN ARCHITECTURE (127.0.0.1 LOOPBACK)"),
    ("N", "- Baseline Maturity: TRL 4 laboratory software emulation testbed (0% cloud, 0 external retrieval APIs, 0 open WAN ports, 637 C2 Python modules, 85/85 passing unit test suites, 17/17 blocked Red-Team vectors, 52 bare-metal SQLite WORM tables)."),
    ("N", "- Brain 1 (Safety Interlock): Models <50us Cortex-M7/RISC-V bare-metal loop, 2.04us RS-485 Modbus FC05 trip, and 36.75ns SiC MOSFET cutoff target at 28.5W on 24V DC."),
    ("N", "- Brain 2 (Isolated NDE): Read-only buffer (0 actuator wire) executing offline ASTM D6433 PCI and structural crack mensuration ($250/sortie vs. $4,600/day manual)."),
    ("N", "- Brain 3 (WORM Provenance): Seals SHA-256 Merkle DAG (Root: bb39eeaa66a39ad2e0c0ab74ba4a5c4faac2bf0d98babc0362482b97607151a1) in <0.15ms."),
    ("B", "SLIDE 4 OF 5: 5-VENDOR QUANTITATIVE ANALYSIS OF ALTERNATIVES (6/6 GATES PASSED)"),
    ("N", "- Project Ebony v8.0.0 (CAGE 1AHA8): 6/6 Gates Passed | Modeled 36.75ns cutoff (1,360,544x faster than 50ms PLC) | 28.5W target draw | 100% air-gapped SQLite WORM."),
    ("N", "- Siemens S7-1500 / Rockwell ControlLogix: 0/6 Gates | 50-200ms scan | 150-450W draw."),
    ("N", "- Schneider Triconex SIS: 0/6 Gates | 10-50ms scan | 200-600W draw | Breached by TRISIS."),
    ("N", "- Dragos / Nozomi Passive IDS: 0/6 Gates | 0 physical cutoff authority | 300-1,200W draw."),
    ("N", "- Cloud AI Wrappers (Jev AI): 0/6 Gates | >250ms cloud RTT | Fails under EMCON."),
    ("B", "SLIDE 5 OF 5: TRACTION, DUAL-USE CLIN PRICING & 12-MONTH PHASE-1 PROTOTYPE PLAN"),
    ("N", "- Verified Traction: Active CDAO Tradewinds Docket 10-26-4046; USACE ERDC BAA filings (CERL, ITL-4, GSL-19); 11-artifact Microgrid SOW suite; 110-control NIST 800-171/800-82 map."),
    ("N", "- Phase-1 Prototype ROM: $1,200,000.00 (12 Months; TRL 4 to TRL 6; $150,000.00 Mobilization) or 26-Module Commercial CLINs (CLIN 0001 $2,450/mo; CLIN 1004-A $895K/yr)."),
]

PRICE_SCHEDULE_PARAS = [
    ("B", "USACE ERDC CERL COMMERCIAL SOLUTIONS OPENING (CSO 2026) - PRICE & ROM SCHEDULE"),
    ("N", "Primary Offeror: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | SAM.gov UEI: S1M4ENLHTDH5)"),
    ("N", "Address: 701 E Drew St., Madill, OK 73446 | POC: Jeffery Humphrey, CEO | (572) 358-9978 | humphreyvirtualfarm@gmail.com"),
    ("N", "Solution Title: Project Ebony v8.0.0: Air-Gapped Tri-Brain OT/SCADA Safety Interlock, Automated Bridge/Pavement NDE & WORM Merkle Provenance Testbed"),
    ("N", "Contracting Vehicles Supported: Commercial Solutions Opening (CSO) Fixed-Price Agreement, 10 U.S.C. 4022 Prototype OTA (0% Cost Share for NTDC/SDB), or FAR Part 12/13 Commercial Award."),
    ("B", "1. Option A: 12-Month Fixed-Price Phase-1 Prototype Effort (TRL 4 to TRL 6) - $1,200,000.00 Total ROM"),
    ("N", "Humphrey Virtual Farms LLC proposes a 12-Month, $1,200,000.00 Firm-Fixed-Price Milestone Schedule to fabricate, calibrate, and field-validate the TRL 6 CERL Operational Energy & Sustainment Management Prototype (0% Cost Share required per NTDC status):"),
    ("N", "- Milestone 1 (Months 1-2 | Days 15-30 Mobilization): $150,000.00 — CERL Operational Energy & Sustainment Management Interface Control Document (ICD), 52-Table SQLite WORM Enclave Baseline & Test Plan."),
    ("N", "- Milestone 2 (Months 3-6): $350,000.00 — Brain 1 Bare-Metal Cortex-M7 + SiC MOSFET Safety Interlock PCB Fabrication & <50us Loop / 36.75ns Cutoff Oscilloscope Verification."),
    ("N", "- Milestone 3 (Months 7-9): $350,000.00 — Brain 2 Isolated Read-Only ASTM D6433 Pavement, Bridge & Facility Sensor Analytics Calibration with ERDC CERL Datasets."),
    ("N", "- Milestone 4 (Months 10-12): $350,000.00 — TRL 6 Integrated CERL Hardware-in-the-Loop (HIL) Demonstration, 110-Control NIST SP 800-171 / 800-82 C3PAO Package & Final Report."),
    ("N", "- Total 12-Month Phase-1 Prototype Price: $1,200,000.00 USD (Inclusive of Engineering Labor, PCB/SiC Hardware Fabrication, HIL Test Equipment, and Technical Data Deliverables)."),
    ("B", "2. Option B: Extended 5-Node Installation Microgrid & SMS Field Pilot OTA - $1,485,000.00 (12 Months)"),
    ("N", "For installations requiring a multi-bay 5-Node Hardware-in-the-Loop microgrid and Sustainment Management System deployment (matching CDAO Tradewinds Docket 10-26-4046), total 12-month fixed price is $1,485,000.00 ($150,000.00 Mobilization; $445,000.00 Month 4; $445,000.00 Month 8; $445,000.00 Month 12)."),
    ("B", "3. Option C: Unbundled Dual-Use Commercial Software Licensing Schedule (26-Module C2 Console)"),
    ("N", "- CLIN 0001 (Base Single-Node TRL 4 Software Testbed & WORM Enclave Pilot): $2,450.00 / Month ($29,400.00 / Year)."),
    ("N", "- CLIN 0002 through CLIN 0026 (Individual Specialized OT, NDE, Microgrid & Cryptographic Add-On Modules): $20,000.00 to $185,000.00 / Year per module."),
    ("N", "- CLIN 1004-A (Full 26-Module 1-Node Tactical Operations Center Bundle): $895,000.00 / Year."),
    ("N", "- CLIN 1004-B (Enterprise 25-Node Installation / Base Fleet License): $2,450,000.00 / Year."),
    ("B", "4. Intellectual Property & Data Rights Statement"),
    ("N", "This price schedule contains no classified or restricted proprietary markings. All 637 core C2 software modules and WORM schemas developed exclusively at private expense are retained by Humphrey Virtual Farms LLC under DFARS 252.227-7018 / FAR 52.227-14, with standard Government Purpose Rights granted for funded Phase-1 deliverables."),
]


def compile_cerl_cso_suite() -> Dict[str, dict]:
    specs = {
        "Solution-CoverLetter-Humphrey Virtual Farms LLC.pdf": COVER_LETTER_PARAS,
        "Solution-Brief-Humphrey Virtual Farms LLC.pdf": SOLUTION_BRIEF_PARAS,
        "Solution-PitchDeck-Humphrey Virtual Farms LLC.pdf": PITCH_DECK_PARAS,
        "Solution-Price-Humphrey Virtual Farms LLC.pdf": PRICE_SCHEDULE_PARAS,
    }
    manifest: Dict[str, dict] = {}
    for fname, paras in specs.items():
        pdf_bytes = build_times_12pt_pdf(paras)
        sha = hashlib.sha256(pdf_bytes).hexdigest().lower()
        destinations = [
            DESKTOP / fname,
            ROOT_PRIV / "c2_cockpit" / "proposals" / "cerl_cso_2026" / fname,
            ROOT_PUB / "c2_cockpit" / "proposals" / "cerl_cso_2026" / fname,
        ]
        for dst in destinations:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(pdf_bytes)
        manifest[fname] = {
            "sha256": sha,
            "size_bytes": len(pdf_bytes),
            "desktop_path": str(DESKTOP / fname),
            "pdf_header_valid": pdf_bytes.startswith(b"%PDF-1.4"),
        }
    return manifest


if __name__ == "__main__":
    res = compile_cerl_cso_suite()
    print(json.dumps(res, indent=2))
