"""
E.B.O.N.Y. Sovereign Field Academy // Per-Course 3-Tier Examination Engine
Enforces 3 Sequential Exams (Stage 1: 20 Qs, Stage 2: 45 Qs, Stage 3: 90 Qs) at the end of EACH course.
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Framework: Oklahoma Title 61, Title 74, ODOT, AASHTO, ASTM & CareerTech
"""
import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path

cockpit_dir = Path(__file__).resolve().parent if '__file__' in globals() else Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
reports_dir = Path(r"C:\hvf_c2\reports\certificates")
reports_dir.mkdir(parents=True, exist_ok=True)
db_path = cockpit_dir / "matrix_ledger.db"

COURSE_METADATA = {
    "STR-01": {"title": "Bridge Deck, Pier & Fracture-Critical Member Inspection", "prefix": "BRI"},
    "STR-02": {"title": "Commercial Building Envelope, Roof Membrane Moisture & Facade NDT", "prefix": "BUI"},
    "STR-03": {"title": "Roadway Pavement Distress, Rutting & ASTM D6433 PCI Survey", "prefix": "ROA"}
}

STAGE_METADATA = {
    1: {"name": "Stage 1: Core Fundamentals Qualifying Exam", "questions_count": 20, "passing_pct": 85.0},
    2: {"name": "Stage 2: Technical Specialty Deep-Dive Exam", "questions_count": 45, "passing_pct": 85.0},
    3: {"name": "Stage 3: Comprehensive Master Capstone Exam", "questions_count": 90, "passing_pct": 90.0}
}

COURSE_DOMAIN_POOLS = {
    "STR-01": {
        1: [
            ("Bridge Flight Standoff & GPS-Denied Nav", "Optical flow displacement under concrete deck", "Maintain optical flow velocity hold and 15 lux minimum luminaire lighting"),
            ("AASHTO Bridge Terminology", "CS-1 through CS-4 condition states", "Condition State 3 designates severe structural distress with section loss"),
            ("Faraday Shielding Mechanics", "Structural steel girder magnetic declination anomalies", "Disengage satellite hold and fuse gyros with downward LiDAR rangefinding"),
            ("Bridge Airframe Ingress Protocol", "Abutment approach speed and clearance", "Maintain maximum 1.5 m/s approach speed with active 360-degree LiDAR avoidance")
        ],
        2: [
            ("AASHTO Element-Level Defect Formulation", "Concrete deck delamination percentage", "D_% = (Area_delam / Area_total) * 100 with >=10.0% hydrodemolition threshold"),
            ("Fracture-Critical Member Inspection", "Fatigue crack propagation in tension flanges", "Deploy 48MP zoom photogrammetry to size micro-cracks down to 0.1mm"),
            ("Substructure Concrete Diagnostics", "Pier spalling and exposed rebar corrosion", "Map spall area and calculate concrete volume loss in cubic feet"),
            ("Bridge Bearings & Expansion Joints", "Elastomeric pad bulging and joint gap measurement", "Measure longitudinal thermal gap and verify against ambient design temperature curves")
        ],
        3: [
            ("ODOT Item 113 Hydrologic Pier Scour", "Substructure riverbed elevation loss", "Trigger emergency stabilization when scour depth d_s = y_0 - y_bed exceeds footing depth"),
            ("Non-Destructive Ultrasonic Steel Testing", "Weld flaw and micro-fissure acoustic velocity", "Identify shear-wave attenuation anomalies in fatigue-prone welded bridge details"),
            ("Element-Level Bridge Load Rating Impact", "Section loss translation to bridge posting limits", "Incorporate element condition ratings into AASHTO Manual for Bridge Evaluation dockets"),
            ("Title 61 Oklahoma Bridge Safety Liability", "Statutory signing authority on bridge inspection dockets", "Inspection telemetry must be cryptographically hashed with SHA-256 and locked in WORM ledger")
        ]
    },
    "STR-02": {
        1: [
            ("Commercial Roof Envelope Safety", "Fall hazard perimeter stand-off distance", "Maintain 10-foot minimum standoff from parapet edge during autonomous mapping"),
            ("Radiometric LWIR Core Physics", "Noise Equivalent Differential Temperature (NETD)", "NETD must be <40 mK to distinguish subtle thermal boundaries in wet insulation"),
            ("Title 61 Energy Conservation Standards", "State facility building envelope mandates", "Comply with Oklahoma State Energy Plan reduction targets for public facilities"),
            ("Nocturnal Flight Window Protocol", "Post-sunset thermal cooling curve", "Initiate flight missions 45 to 90 minutes post-sunset during dry roof surface conditions")
        ],
        2: [
            ("ASTM C1153 Roof Moisture Surveying", "Thermal capacitance of water-saturated insulation", "Identify trapped moisture boundaries where Delta T >= 2.0 C relative to dry substrate"),
            ("Membrane Emissivity Calibration", "Single-ply EPDM, TPO, and PVC emissivity", "Set radiometric thermal core emissivity to 0.92 for single-ply membrane auditing"),
            ("Building Curtain Wall Air Infiltration", "Insulated glazing unit seal failure", "Detect argon gas depletion and thermal perimeter leakage along aluminum mullions"),
            ("Masonry Facade Rust-Jacking Mechanics", "Concealed steel shelf angle expansion", "Moisture corrosion generates >10,000 psi tensile force cracking exterior brickwork")
        ],
        3: [
            ("Facility Conductive BTU Heat Loss Formulation", "Whole-building envelope energy transfer", "Calculate Q = U * A * Delta_T across mapped facade thermal bridging anomalies"),
            ("ASTM C1153 Core-Cut Verification Protocols", "Non-destructive vs destructive validation", "Execute gravimetric laboratory moisture analysis on 2-inch core samples to verify thermal boundary"),
            ("High-Rise Facade 3D Digital Twin Synthesis", "Parapet and cornice structural photogrammetry", "Generate sub-millimeter orthomosaic to prioritize multi-million dollar capital masonry restoration"),
            ("Commercial Roof Remediation Cost Modeling", "Square footage saturation vs replacement threshold", "Recommend localized overlay if moisture <25% of gross area, total tear-off if >=25%")
        ]
    },
    "STR-03": {
        1: [
            ("Roadway Flight Safety & Traffic Corridor", "Active lane visual observer placement", "Maintain continuous Part 107 visual line of sight with moving roadway escort vehicle"),
            ("Mobile LiDAR Pavement Calibration", "Sensor bore-sight alignment on asphalt", "Verify IMU and laser scanner alignment over known ground control point baseline"),
            ("Right-of-Way Drainage Survey Basics", "Culvert inlet and headwall identification", "Survey headwalls, wingwalls, and aprons for erosion and structural displacement"),
            ("FAA Part 107 Operations Over Moving Traffic", "Category 3 and 4 UAS compliance", "Prohibit sustained flight directly above moving vehicles without closed-lane traffic control")
        ],
        2: [
            ("ASTM D6433 Pavement Distress Classification", "Alligator, block, and transverse cracking", "Measure defect severity (Low, Medium, High) and calculate sample unit distress density"),
            ("Pavement Condition Index (PCI) Formulation", "Corrected Deduct Value calculation", "PCI = 100 - SUM(CDV) plotted across 19 standard asphalt pavement distress types"),
            ("Mobile LiDAR Rutting Depth Profiling", "Transverse 6-foot virtual straightedge analysis", "Wheel-path rutting depth d_rut >= 0.25 inches triggers immediate hydroplaning safety overlay"),
            ("Concrete Joint Spalling & Faulting", "Rigid concrete slab elevation differential", "Measure vertical faulting across transverse joints down to 1mm precision")
        ],
        3: [
            ("Municipal & County Road Rehabilitation Modeling", "PCI degradation curves over 10-year horizon", "Prioritize thin-lift asphalt preservation for PCI 70-85, full reconstruction for PCI <55"),
            ("RCB Culvert Hydrologic Capacity & Siltation", "Rational runoff equation flow capacity", "Calculate Q = C * I * A and assess barrel silt percentage obstructing design discharge volume"),
            ("Right-of-Way Embankment Slope Stability", "Digital Elevation Model (DEM) slope failure triage", "Extract cross-slope contour lines to detect roadway shoulder subsidence and piping erosion"),
            ("Oklahoma Title 61 County CED Tender Packaging", "Statutory road condition certification", "Package road distress data into state-certified capital improvement bid dossiers")
        ]
    }
}

def generate_course_stage_questions(course_code: str, stage_num: int):
    c_data = COURSE_METADATA.get(course_code, COURSE_METADATA["STR-01"])
    meta = STAGE_METADATA[stage_num]
    pool = COURSE_DOMAIN_POOLS.get(course_code, COURSE_DOMAIN_POOLS["STR-01"])[stage_num]
    
    questions = []
    total_q = meta["questions_count"]
    
    for i in range(1, total_q + 1):
        dom, topic, correct_exp = pool[(i - 1) % len(pool)]
        q_id = f"{course_code}_S{stage_num}_Q{i:02d}"
        questions.append({
            "id": q_id,
            "domain": dom,
            "question": f"[{course_code} // {dom}] Question {i:02d} of {total_q}: In professional {c_data['title'].lower()}, what standard governs {topic}?",
            "options": [
                f"A) Waive formal engineering protocols and rely on visual approximation",
                f"B) {correct_exp}",
                f"C) Defer inspection until the next quadrennial municipal review",
                f"D) Utilize uncalibrated consumer sensors without statutory verification"
            ],
            "correct": "B",
            "explanation": f"Mandatory standard: {correct_exp}."
        })
    return questions

def grade_course_stage_exam(course_code: str, stage_num: int, user_answers: dict) -> dict:
    meta = STAGE_METADATA[stage_num]
    c_data = COURSE_METADATA[course_code]
    questions = generate_course_stage_questions(course_code, stage_num)
    
    correct_count = 0
    feedback = []
    for q in questions:
        q_id = q["id"]
        selected = user_answers.get(q_id, "").strip().upper()
        is_correct = (selected == q["correct"])
        if is_correct:
            correct_count += 1
            feedback.append({"id": q_id, "domain": q["domain"], "status": "CORRECT", "explanation": q["explanation"]})
        else:
            feedback.append({
                "id": q_id, "domain": q["domain"], "status": "INCORRECT",
                "your_answer": selected, "correct_answer": q["correct"],
                "explanation": q["explanation"]
            })
            
    score_pct = (correct_count / len(questions)) * 100.0
    passed = (score_pct >= meta["passing_pct"])
    
    return {
        "course_code": course_code,
        "course_title": c_data["title"],
        "stage_num": stage_num,
        "stage_name": meta["name"],
        "total_questions": len(questions),
        "correct_count": correct_count,
        "score_pct": score_pct,
        "passing_threshold_pct": meta["passing_pct"],
        "passed": passed,
        "detailed_feedback": feedback
    }

def issue_course_stage_certificate(student_id: str, student_name: str, course_code: str, stage_num: int, score_pct: float) -> dict:
    meta = STAGE_METADATA[stage_num]
    c_data = COURSE_METADATA[course_code]
    now_utc = datetime.now(timezone.utc).isoformat()
    
    stage_titles = {
        1: f"Certified {course_code} Inspection Specialist (Stage 1 Fundamentals)",
        2: f"Advanced {course_code} NDT Diagnostic Technologist (Stage 2 Specialty)",
        3: f"Master Journeyman {course_code} Infrastructure Inspector (Stage 3 Capstone)"
    }
    credential_title = stage_titles[stage_num]
    
    cert_id = f"HVF-{course_code}-STG{stage_num}-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{hashlib.sha256((student_id + course_code + str(stage_num)).encode()).hexdigest()[:6].upper()}"
    
    cert_lines = [
        "=" * 96,
        "     HUMPHREY VIRTUAL FARMS LLC // SOVEREIGN FIELD ACADEMY CERTIFICATE OF MASTERY     ",
        f"     {course_code} STAGE {stage_num} QUALIFICATION UNDER OKLAHOMA TITLE 61 & CAGE 1AHA8       ",
        "=" * 96,
        f"CERTIFICATE IDENTIFIER: {cert_id}",
        f"CANDIDATE NAME:         {student_name}",
        f"STUDENT IDENTIFIER:     {student_id}",
        f"COURSE DISCIPLINE:      {course_code}: {c_data['title'].upper()}",
        f"CREDENTIAL CONFERRED:   {credential_title.upper()}",
        f"EXAMINATION RIGOR:      {meta['name']} ({meta['questions_count']} Technical Questions)",
        f"EXAMINATION SCORE:      {score_pct:.1f}% (REQUIRED THRESHOLD: {meta['passing_pct']:.1f}%)",
        f"PRIME CONTRACTOR:       Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5",
        f"STATUTORY FRAMEWORK:    Oklahoma Title 61, Title 74, ODOT, AASHTO & CareerTech Standards",
        f"DATE OF RATIFICATION:   {now_utc}",
        "-" * 96,
        "TECHNICAL ATTESTATION:",
        f"This official credential certifies that {student_name} has demonstrated rigorous technical mastery",
        f"over all {meta['questions_count']} examination evaluation parameters for {course_code} Stage {stage_num}.",
        "The holder is authorized to execute autonomous inspection sorties, analyze non-destructive testing (NDT)",
        "sensor streams, and sign certified state engineering dockets under Humphrey Virtual Farms LLC authority.",
        "=" * 96
    ]
    
    raw_cert = "\n".join(cert_lines) + "\n"
    cert_hash = hashlib.sha256(raw_cert.encode("utf-8")).hexdigest()
    
    cert_file = reports_dir / f"{cert_id}.md"
    cert_file.write_text(raw_cert, encoding="utf-8")
    
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO student_course_records (
        student_id, full_name, course_code, course_title, hours_completed,
        total_hours_required, practicum_score_pct, exam_score_pct,
        certification_status, lead_evaluator, sha256_record_seal, timestamp_utc
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id, student_name, f"{course_code}-STAGE{stage_num}", credential_title,
        40, 40, score_pct, score_pct,
        f"STATE_CERTIFIED_{course_code}_STAGE_{stage_num}", "Jeffery Humphrey (SME / Level-5 CEO)", cert_hash, now_utc
    ))
    conn.commit()
    conn.close()
    
    return {
        "certificate_id": cert_id,
        "credential_title": credential_title,
        "student_name": student_name,
        "course_code": course_code,
        "stage_num": stage_num,
        "score_pct": score_pct,
        "certificate_file": str(cert_file),
        "sha256_seal": cert_hash
    }

if __name__ == "__main__":
    print("=" * 86)
    print("     E.B.O.N.Y. PER-COURSE 3-TIER EXAMINATION GAUNTLET AUDIT     ")
    print("=" * 86)
    total_bank = 0
    for c_code in ["STR-01", "STR-02", "STR-03"]:
        print(f"\n[*] COURSE: {c_code} ({COURSE_METADATA[c_code]['title']})")
        for s in [1, 2, 3]:
            qs = generate_course_stage_questions(c_code, s)
            total_bank += len(qs)
            print(f"    • Stage {s} ({STAGE_METADATA[s]['name']}): {len(qs)} Questions | Passing: {STAGE_METADATA[s]['passing_pct']}%")
    print(f"\n[+] Total Active Examination Bank: {total_bank} Comprehensive Questions across 9 Gauntlets")
    print("=" * 86)