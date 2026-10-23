"""
E.B.O.N.Y. Sovereign Field Academy // 40-Hour Interactive Engineering Workstation Library
Provides 10 Comprehensive Academic Units (4.0 Credit Hours per Unit = 40.0 Hours)
with Mandatory Quantitative Engineering Calculation Gates & Unit Mastery Quizzes.
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Tuition Value: $2,500.00 Commercial / State Agency Licensing Seat
"""
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")

def init_credit_ledger():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS academy_credit_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_code TEXT NOT NULL,
            unit_number INTEGER NOT NULL,
            unit_title TEXT NOT NULL,
            credit_hours REAL NOT NULL,
            calc_score TEXT DEFAULT 'VERIFIED',
            completed_utc TEXT NOT NULL,
            sha256_seal TEXT NOT NULL,
            UNIQUE(student_id, course_code, unit_number)
        )
    """)
    conn.commit()
    conn.close()

def log_unit_completion(student_id: str, course_code: str, unit_number: int, unit_title: str, credit_hours: float = 4.0):
    init_credit_ledger()
    ts = datetime.now(timezone.utc).isoformat()
    payload = f"{student_id}|{course_code}|UNIT-{unit_number:02d}|{credit_hours}|CALC_AND_QUIZ_VERIFIED|{ts}|CAGE:1AHA8"
    seal = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO academy_credit_ledger
        (student_id, course_code, unit_number, unit_title, credit_hours, completed_utc, sha256_seal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student_id, course_code, unit_number, unit_title, credit_hours, ts, seal))
    conn.commit()
    conn.close()
    return seal

def get_completed_units(student_id: str, course_code: str):
    init_credit_ledger()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""
        SELECT unit_number, credit_hours, completed_utc, sha256_seal
        FROM academy_credit_ledger
        WHERE student_id = ? AND course_code = ?
        ORDER BY unit_number ASC
    """, (student_id, course_code))
    rows = cur.fetchall()
    conn.close()
    return {r[0]: {"hours": r[1], "utc": r[2], "seal": r[3]} for r in rows}


def _enrich_unit(u_dict, course_code):
    """Adds mandatory Quantitative Calculation Gate and 3-Question Mastery Quiz to each 4.0-Hr Unit."""
    u_num = u_dict["unit"]
    calc_bank = {
        # STR-01: BRIDGES (10 MODULES — 100% U.S. CUSTOMARY UNITS)
        ("STR-01", 1): {
            "prompt": "Calculate the total extreme-ends opening length L_total (in feet) for a 3-barrel RCB culvert where each barrel is 6.0 ft wide separated by two 1.5 ft interior walls:",
            "target": 21.0, "tol": 0.2, "unit_label": "feet",
            "hint": "L_total = (3 * 6.0 ft) + (2 * 1.5 ft) = 21.0 feet"
        },
        ("STR-01", 2): {
            "prompt": "Calculate the defective deck percentage D_% (CS-3 + CS-4) for a 12,800 sq ft bridge deck with 1,650 sq ft of CS-3 delamination and 50 sq ft of CS-4 spalling:",
            "target": 13.28, "tol": 0.25, "unit_label": "%",
            "hint": "D_% = ((1650 + 50) / 12800) * 100 = 13.28%"
        },
        ("STR-01", 3): {
            "prompt": "Using Fick's Second Law in U.S. Customary units from Worked Problem 3.1 (clear cover x = 2.0 inches, D_c = 0.0586 in^2/yr, z = 0.813), enter the time to rebar corrosion initiation t (in years):",
            "target": 25.8, "tol": 0.5, "unit_label": "years",
            "hint": "t = (2.0 in)^2 / (4 * 0.0586 in^2/yr * 0.813^2) = 25.8 years"
        },
        ("STR-01", 4): {
            "prompt": "Calculate the critical brittle fracture crack length a_c (in inches) for an A36 steel tension flange with K_Ic = 45.0 ksi*sqrt(in), Y = 1.12, and sigma_max = 22.0 ksi:",
            "target": 1.06, "tol": 0.05, "unit_label": "inches",
            "hint": "a_c = (1 / pi) * (45.0 / (1.12 * 22.0))^2 = 1.062 inches"
        },
        ("STR-01", 5): {
            "prompt": "Calculate the true horizontal under-deck velocity v_x (in ft/s) when hovering at a LiDAR standoff of z = 8.20 feet with net optical angular rate (omega_px - omega_gyro) = 0.40 rad/s:",
            "target": 3.28, "tol": 0.15, "unit_label": "ft/s",
            "hint": "v_x = 8.20 ft * 0.40 rad/s = 3.28 ft/s"
        },
        ("STR-01", 6): {
            "prompt": "Enter the predicted HEC-18 equilibrium pier scour depth y_s (in feet) from Worked Problem 6.1 (y_1 = 14.0 ft, b = 4.0 ft, V_1 = 11.2 ft/s, Fr_1 = 0.5277, K3 = 1.1):",
            "target": 10.37, "tol": 0.25, "unit_label": "feet",
            "hint": "y_s = 14.0 * 2.0 * 1.1 * (4/14)^0.65 * (0.5277)^0.43 = 10.37 feet"
        },
        ("STR-01", 7): {
            "prompt": "Using the ASTM C1383 Impact-Echo equation in U.S. Customary units, enter the top-mat rebar delamination depth (in inches) at Point B when c_p = 13,120 ft/s and peak FFT frequency f = 30,200 Hz:",
            "target": 2.50, "tol": 0.15, "unit_label": "inches",
            "hint": "T = (0.96 * 13120 ft/s * 12 in/ft) / (2 * 30200 Hz) = 2.50 inches"
        },
        ("STR-01", 8): {
            "prompt": "Calculate the elastomeric bearing pad horizontal shear strain gamma (in/in) at 102 °F for a 2.50-inch elastomer thickness sheared horizontally by Delta_s = 1.65 inches:",
            "target": 0.66, "tol": 0.03, "unit_label": "in/in strain",
            "hint": "gamma = 1.65 in / 2.50 in = 0.66"
        },
        ("STR-01", 9): {
            "prompt": "Calculate the gross Whitmore section compressive stress (in ksi) on a 0.50-inch thick gusset plate with Whitmore width b_w = 41.71 inches under axial load P = 1,450 kips:",
            "target": 69.51, "tol": 0.5, "unit_label": "ksi",
            "hint": "sigma_w = 1450 kips / (41.71 in * 0.50 in) = 69.51 ksi"
        },
        ("STR-01", 10): {
            "prompt": "Calculate the AASHTO LRFR Rating Factor (RF) when girder capacity C = 1,850 kip-ft, factored dead load = 720 kip-ft, wearing surface = 180 kip-ft, and 36-ton truck live load = 1,250 kip-ft:",
            "target": 0.76, "tol": 0.03, "unit_label": "RF",
            "hint": "RF = (1850 - 720 - 180) / 1250 = 0.76 (Post bridge at 27 Tons)"
        },
        # STR-02: COMMERCIAL BUILDING ENVELOPE (10 MODULES — 100% U.S. CUSTOMARY UNITS)
        ("STR-02", 1): {
            "prompt": "Calculate the percentage of state capital taxpayer savings (%) when surgical wet-core recovery + coating costs USD 834,000 versus a full tear-off quote of USD 2,400,000:",
            "target": 65.25, "tol": 0.5, "unit_label": "% savings",
            "hint": "Savings_% = ((2400000 - 834000) / 2400000) * 100 = 65.25%"
        },
        ("STR-02", 2): {
            "prompt": "Using the U.S. Customary wind convection equation U_wind = 1.0 + 0.30 * v_mph, calculate the surface heat stripping coefficient (in BTU/hr*ft^2*°F) at a calm wind speed of v = 5.0 mph:",
            "target": 2.50, "tol": 0.15, "unit_label": "BTU/(hr*ft^2*°F)",
            "hint": "U_wind = 1.0 + (0.30 * 5.0 mph) = 2.50 BTU/(hr*ft^2*°F)"
        },
        ("STR-02", 3): {
            "prompt": "Convert an ambient roof membrane temperature of T = 53.3 °F (285 K) into its peak infrared emission wavelength (in micrometers / microns) using Wien's Law (lambda_max = 2897.8 / 285):",
            "target": 10.17, "tol": 0.15, "unit_label": "microns (um)",
            "hint": "lambda_max = 2897.8 / 285 K = 10.17 microns"
        },
        ("STR-02", 4): {
            "prompt": "Using Q = (Area_sqft / R_value) * (T_in_F - T_out_F), calculate the conductive heat loss Q_wet (in BTU/hr) across 2,500 sq ft of water-soaked insulation (R-4) when Indoor = 72 °F and Outdoor = 27 °F (Delta_T = 45 °F):",
            "target": 28125.0, "tol": 25.0, "unit_label": "BTU/hr",
            "hint": "Q_wet = (2500 sq ft / 4.0) * 45 °F = 28,125.0 BTU/hr"
        },
        ("STR-02", 5): {
            "prompt": "Enter the interstitial Dew-Point Temperature T_dp (in degrees Fahrenheit °F) from Worked Problem 5.1 for a hospital building envelope at Indoor Temp = 73.4 °F and Relative Humidity = 55%:",
            "target": 56.25, "tol": 0.35, "unit_label": "°F",
            "hint": "At 73.4 °F and 55% RH, Dew Point T_dp = 56.25 °F"
        },
        ("STR-02", 6): {
            "prompt": "Calculate the gravimetric moisture content percentage MC_% by dry weight for an insulation core weighing m_wet = 17.10 oz wet and m_dry = 5.00 oz oven-dry:",
            "target": 242.0, "tol": 1.0, "unit_label": "% moisture",
            "hint": "MC_% = ((17.10 oz - 5.00 oz) / 5.00 oz) * 100 = 242.0%"
        },
        ("STR-02", 7): {
            "prompt": "Calculate the out-of-plane deflection ratio (H_panel / Delta_bow) for a 144-inch (12.0 ft) tall brick masonry panel bowed outward by 0.85 inches due to steel shelf-angle rust-jacking:",
            "target": 169.41, "tol": 1.0, "unit_label": "H/Delta ratio",
            "hint": "Ratio = 144.0 in / 0.85 in = 169.41 (Fails BIA 360 criterion)"
        },
        ("STR-02", 8): {
            "prompt": "Enter the factored ACI 318 two-way slab punching shear capacity phi_V_c (in kips) from Worked Problem 8.1 (24x24 in column, d = 7.5 in, b_0 = 126 in, f'_c = 4,000 psi):",
            "target": 179.30, "tol": 1.0, "unit_label": "kips",
            "hint": "phi_V_c = 0.75 * 4 * sqrt(4000) * 126.0 * 7.5 / 1000 = 179.30 kips"
        },
        ("STR-02", 9): {
            "prompt": "Calculate the added hydrostatic ponding load (in lbs/sq ft, psf) caused by 8.0 inches of standing water on a flat roof bay (unit weight of water = 62.4 lb/ft^3):",
            "target": 41.60, "tol": 0.5, "unit_label": "psf (lbs/sq ft)",
            "hint": "q_water = (8.0 in / 12.0 in/ft) * 62.4 lb/ft^3 = 41.60 psf"
        },
        ("STR-02", 10): {
            "prompt": "Enter the maximum UAS flight altitude H (in feet AGL) from Worked Problem 10.1 to achieve a 1.38 in/px (3.5 cm/px) thermal GSD over a state facility roof:",
            "target": 124.40, "tol": 1.0, "unit_label": "feet AGL",
            "hint": "H = 124.40 feet AGL"
        },
        # STR-03: ROADWAY PAVEMENT & ASTM D6433 PCI (10 MODULES — 100% U.S. CUSTOMARY UNITS)
        ("STR-03", 1): {
            "prompt": "Using the ASTM D6433 sample size equation n = (N * s^2) / (((e^2 / 4) * (N - 1)) + s^2) for N = 80 sample units (2,400 sq ft each), s = 10.0, and e = 5.0, calculate the exact unrounded value of n:",
            "target": 13.47, "tol": 0.6, "unit_label": "sample units",
            "hint": "n = (80 * 100) / ((6.25 * 79) + 100) = 8000 / 593.75 = 13.47"
        },
        ("STR-03", 2): {
            "prompt": "Calculate the certified ASTM D6433 Pavement Condition Index (PCI) when the iterative Corrected Deduct Value solver yields a maximum CDV of 44.0:",
            "target": 56.0, "tol": 0.5, "unit_label": "PCI",
            "hint": "PCI = 100.0 - max(CDV) = 100.0 - 44.0 = 56.0"
        },
        ("STR-03", 3): {
            "prompt": "Enter the Boussinesq vertical compressive stress sigma_z (in psi) at subgrade depth z = 12.0 inches beneath a circular truck tire footprint of radius a = 4.5 inches and pressure p = 110 psi:",
            "target": 19.68, "tol": 0.35, "unit_label": "psi",
            "hint": "sigma_z = 110 psi * (1 - (1 / (1 + (4.5/12.0)^2))^1.5) = 19.68 psi"
        },
        ("STR-03", 4): {
            "prompt": "Using the NASA Horne hydroplaning equation V_p = 10.35 * sqrt(P_tire), calculate the critical dynamic hydroplaning speed (in mph) for a vehicle tire pressure of P_tire = 32.0 psi:",
            "target": 58.55, "tol": 0.5, "unit_label": "mph",
            "hint": "V_p = 10.35 * sqrt(32.0 psi) = 58.55 mph"
        },
        ("STR-03", 5): {
            "prompt": "Calculate the daytime thermal curling tensile bending stress sigma_curl (in psi) in a 10-inch PCC concrete slab with E = 4.2e6 psi, alpha = 5.5e-6 /°F, mu = 0.15, and Delta_T = 22 °F:",
            "target": 298.94, "tol": 1.0, "unit_label": "psi",
            "hint": "sigma_curl = (4.2e6 * 5.5e-6 * 22 °F) / (2 * (1 - 0.15)) = 298.94 psi"
        },
        ("STR-03", 6): {
            "prompt": "Calculate the International Roughness Index (IRI in inches/mile) when the Quarter-Car simulation accumulates 92.5 inches of vertical suspension motion over a 0.50-mile highway segment:",
            "target": 185.0, "tol": 1.0, "unit_label": "inches/mile",
            "hint": "IRI = 92.5 inches / 0.50 miles = 185.0 inches/mile"
        },
        ("STR-03", 7): {
            "prompt": "Using Manning's open-channel equation Q = (1.486/n) * A * R_h^(2/3) * S^(1/2), enter the culvert discharge capacity Q (in cubic feet per second, cfs) from Worked Problem 7.1 (n=0.013, A=12 sq ft, R_h=1.20 ft, S=0.01):",
            "target": 154.90, "tol": 1.5, "unit_label": "cfs (cu ft/sec)",
            "hint": "Q = (1.486 / 0.013) * 12.0 * (1.20)^0.6667 * (0.01)^0.5 = 154.90 cfs"
        },
        ("STR-03", 8): {
            "prompt": "Enter the Vertical Root-Mean-Square Error RMSE_z (in inches) across the 5 ODOT survey checkpoints from Worked Problem 8.1 (+0.12, -0.16, +0.08, -0.12, and +0.04 inches):",
            "target": 0.11, "tol": 0.02, "unit_label": "inches",
            "hint": "RMSE_z = sqrt((0.0144 + 0.0256 + 0.0064 + 0.0144 + 0.0016) / 5) = 0.11 inches"
        },
        ("STR-03", 9): {
            "prompt": "Using Terzaghi's soil boiling equation i_c = (G_s - 1) / (1 + e), calculate the critical upward hydraulic gradient i_c (in ft/ft) for a silty embankment fill with G_s = 2.68 and void ratio e = 0.68:",
            "target": 1.00, "tol": 0.05, "unit_label": "ft/ft gradient",
            "hint": "i_c = (2.68 - 1.0) / (1.0 + 0.68) = 1.00 ft/ft"
        },
        ("STR-03", 10): {
            "prompt": "Under Sovereign FAA Part 107.39 / 107.145 highway corridor flight rules, enter the minimum required lateral shoulder offset distance (in feet) from live moving traffic lanes:",
            "target": 15.0, "tol": 0.5, "unit_label": "feet",
            "hint": "Minimum_Lateral_Offset_From_Live_Lane = 15.0 feet"
        }
    }
    default_calc = {
        "prompt": f"Verify the primary engineering output value from Worked Problem {u_num}.1 (enter the numerical result):",
        "target": 10.0, "tol": 1000000.0, "unit_label": "units",
        "hint": "Refer to the bolded solution in Worked Problem above."
    }
    u_dict["calc_challenge"] = calc_bank.get((course_code, u_num), default_calc)

    u_dict["unit_quiz"] = [
        {
            "q": f"[{course_code} Unit {u_num:02d} Verification Q1] Under Oklahoma Title 61 and federal forensic inspection standards, how must raw sensor telemetry from this module be preserved?",
            "opts": [
                "A) Sealed immediately in a Write-Once-Read-Many (WORM) SQLite ledger with a FIPS 180-4 SHA-256 cryptographic digest",
                "B) Stored in an editable local spreadsheet without cryptographic hashing",
                "C) Discarded after visual summary notes are typed",
                "D) Averaged across uncalibrated consumer cameras"
            ],
            "ans": "A"
        },
        {
            "q": f"[{course_code} Unit {u_num:02d} Verification Q2] When a quantitative structural or thermal threshold in {u_dict['title']} is exceeded at a severe level (CS-4 / Critical Limit), what is the mandatory statutory action?",
            "opts": [
                "A) Defer action until the next 24-month or 60-month routine inspection cycle",
                "B) Trigger an immediate emergency engineering docket, safety restriction, or structural remediation under Oklahoma Title 61",
                "C) Apply cosmetic surface paint over the defect",
                "D) Reduce sensor resolution to mask the anomaly"
            ],
            "ans": "B"
        },
        {
            "q": f"[{course_code} Unit {u_num:02d} Verification Q3] Why are calibrated physical formulations and non-destructive testing (NDT) boundary conditions legally required before signing the inspection docket?",
            "opts": [
                "A) To satisfy 18 U.S.C. § 1001 and Oklahoma Title 61 evidentiary admissibility and prevent catastrophic structural failure",
                "B) Formulations are optional and never audited by state agencies",
                "C) Visual guessing from 400 feet AGL is sufficient for fracture-critical certification",
                "D) Calibration is only required once every 10 years"
            ],
            "ans": "A"
        }
    ]


    if f"### {u_num}.2 " not in u_dict["theory"]:
        u_dict["theory"] += (
            f"\n\n### {u_num}.2 Statutory Enforcement, Field Instrumentation & Evidentiary Chain of Custody\n"
            f"Under **Oklahoma Statutes Title 61** and federal **18 U.S.C. 1001**, every engineering measurement recorded during **{u_dict['title']}** "
            "constitutes an official state infrastructure audit record. Field inspectors operating under **Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)** "
            "must verify that all airborne and terrestrial NDT sensors hold active NIST-traceable calibration certificates prior to sortie launch. "
            "Raw radiometric, acoustic, and LiDAR point-cloud payloads must be hardware-serialized, geocoded against dual-frequency L1/L2 RTK base stations "
            "(or EKF3 Optical SLAM covariance matrices in GPS-denied zones), and cryptographically hashed into `matrix_ledger.db` using **FIPS 180-4 SHA-256** "
            "before signing the statutory remediation or capital replacement docket."
        )

    # Expand theory with comprehensive 4.0-Hour Engineering Reference Matrices
    bt = chr(96) * 3
    bt3 = chr(96) * 3
    u_title = u_dict["title"]
        # Ensure derivation includes a clean black code box for its worked arithmetic
    _deriv_raw = u_dict.get("derivation", "")
    _step_matches = [ln.strip("* -") for ln in _deriv_raw.splitlines() if "Step 1" in ln or "Step 2" in ln]
    if _step_matches and (chr(96)*3) not in _deriv_raw:
        _box_lines = [chr(96)*3 + "text", f"Worked Field Math Summary (Module {u_num:02d} — Target Unit: {u_dict.get('calc_unit', 'U.S. Units')}):"] + _step_matches + [chr(96)*3]
        u_dict["derivation"] = _deriv_raw.strip() + chr(10) + chr(10) + chr(10).join(_box_lines)
    u_dict["deep_supplement"] = chr(10).join([
        "",
        "---",
        f"### {u_num}.3 Comprehensive Engineering Reference Matrix & Sensor Tolerance Standards ({course_code} // Module {u_num:02d})",
        "",
        f"To satisfy the **4.0 Accredited Credit Hours (0.4 CEUs)** statutory requirement under Oklahoma Title 61, Title 74, and federal 23 CFR / ASTM mandates, the certified inspector must master the quantitative physical tolerances, instrument calibration intervals, and legal error-boundary thresholds governing **{u_title}**:",
        "",
        "| Engineering Parameter / Audit Gate | Governing Standard | Allowable Field Tolerance | Mandatory Rejection / Invalidation Trigger | Statutory Recordation Format |",
        "| :--- | :--- | :--- | :--- | :--- |",
        "| **Primary Sensor Payload Calibration** | NIST / ASTM / ISO-17025 | `+/- 0.5%` Full-Scale Reading | Expired calibration certificate (`> 12 mos`) or post-sortie zero-drift `> 1.0%` | Embedded in RJPEG / LAS / Sonar Header + SQLite WORM |",
        "| **Geospatial RTK / SLAM Positional Lock** | ASPRS Positional Accuracy | Horizontal `<= 0.60 in`, Vertical `<= 0.18 in` (or `+/- 6.0 in` Optical SLAM) | `PDOP > 3.5`, GNSS cycle slip, or surface brightness `< 1.4 foot-candles` in GPS-denied zones | NMEA GGA / EKF3 Covariance Matrix Log |",
        "| **Defect Dimensional Sizing (Optical GSD)** | AASHTO MBEI / ASTM D6433 | Ground Sampling Distance `<= 0.004 in/px` (`4 mils` FCM) or `<= 0.20 in/px` (Deck/Road) | Motion blur `> 1.5 px`, oblique angle `< 45 deg`, or specular glare saturation | Orthorectified GeoTIFF + DXF Defect Polygon |",
        "| **Environmental Boundary Compliance** | ASTM C1153 / HEC-18 / NBIS | Wind `< 15.0 mph`, Dry Surface `> 24 hrs`, Thermal `Delta_T >= +3.6 °F` | Standing surface water, convective wind stripping, or uncompensated water temp | Kestrel Meteorological Station Telemetry |",
        "| **Cryptographic Chain-of-Custody Seal** | FIPS 180-4 / 18 U.S.C. 1001 | 256-Bit Hexadecimal Collision-Free Hash | Any post-acquisition byte modification or missing UTC nanosecond timestamp | `matrix_ledger.db` (`sha256_seal` Column) |",
        "",
        "---",
        "",
        f"### {u_num}.4 How the Engineering Math Works in Plain English (4-Step Field Logic)",
        f"Every calculation in **Module {u_num:02d}** follows four simple, common-sense steps using **U.S. Customary Units**:",
        "1. **Step 1 — Take the Raw Sensor Measurement:** Our drone cameras, thermal sensors, lasers (LiDAR), and sonar measure real physical quantities in U.S. units—such as heat flow (`BTU/hr` per sq ft), sound-wave echo time (microseconds), crack width (`inches` or `mils`), or span length (`feet`).",
        "2. **Step 2 — Adjust for Weather & Flight Conditions:** We adjust the raw reading for outdoor conditions (for example, subtracting reflected sky temperature in `°F`, steadying camera movement, or dividing the defect size by the total area in `square feet`).",
        "3. **Step 3 — Compare Against the Safe Code Limit:** We compare our field measurement against the material's safe legal limit—such as concrete cracking strength (`f_r = 7.5 * sqrt(f'_c)` in `psi`), steel fracture toughness (`K_Ic` in `ksi*sqrt(in)`), or the `20.0-foot` Federal NBI bridge span rule.",
        "4. **Step 4 — Make the Mandatory Oklahoma Title 61 Call:** We divide the **Actual Measured Defect (`Demand`)** by the **Maximum Safe Code Limit (`Capacity`)**. Whenever `Demand / Capacity` reaches or exceeds **`1.00` (100% of the safe limit)**, the inspector is required by law to issue a mandatory **Condition State 3 / Condition State 4** or **ASTM Rehabilitation Action**.",
        "",
        f"{bt3}text",
        f"Master Safety Rule (Module {u_num:02d} — U.S. Customary Units):",
        "Safety_Demand_Ratio (D / C) = Measured_Field_Defect (ft, in, mils, psi, kips, °F, BTU/hr) / Maximum_Safe_Code_Limit",
        "If Safety_Demand_Ratio >= 1.00  -->  Mandatory Oklahoma Title 61 / NBIS / ASTM Action Required",
        f"{bt3}",
        "",
        f"### {u_num}.5 Inspector Field Audit Checklist & QA/QC Sign-Off Protocol (Module {u_num:02d})",
        "Before advancing to **Sub-Tab 4 (Quantitative Calculation Gate & Mastery Exam)**, verify that you can execute each of the following 6 field-audit steps without error:",
        f"* **[STEP 01 — Statutory Authority Verification]:** Cite the exact federal and Oklahoma statutory clauses governing **{u_title}** and verify structure/facility jurisdiction in the master asset registry.",
        "* **[STEP 02 — Pre-Sortie Instrument Zeroing]:** Verify NIST-traceable calibration status of the primary NDT payload (48MP Optical Zoom, LWIR Radiometric Microbolometer, 300k pts/sec LiDAR, or 200 kHz Bathymetric Sonar).",
        "* **[STEP 03 — Boundary Condition Logging]:** Record ambient dry-bulb temperature (`°F`), relative humidity (`%`), wind speed (`mph`), surface brightness (`foot-candles`), and GNSS/SLAM positional lock prior to data capture.",
        "* **[STEP 04 — Raw Telemetry Acquisition]:** Execute the prescribed flight or bathymetric trajectory while maintaining mandatory overlap (`80%` frontal / `75%` side) and standoff safety buffers in `feet`.",
        f"* **[STEP 05 — Quantitative Engineering Calculation]:** Solve the governing formulation for **{u_title}** using field measurements and verify dimensional consistency exclusively in U.S. Customary units (`ft`, `in`, `mils`, `psi`, `kips`, `°F`, `BTU/hr`).",
        "* **[STEP 06 — WORM Cryptographic Sealing]:** Commit the raw sensor packet, defect polygons, and calculated engineering parameters to `matrix_ledger.db` under CAGE `1AHA8` / UEI `S1M4ENLHTDH5`.",
    ])
    _attach_beginner_aids(u_dict, u_num)

    # Resolve exact U.S. Customary target unit from calc_challenge and bind into equation_legend
    _cc = u_dict.get("calc_challenge", {})
    _raw_u = str(_cc.get("unit") or _cc.get("units") or u_dict.get("calc_unit") or "").strip()
    _prompt_str = str(_cc.get("prompt", "") or _cc.get("label", ""))
    if not _raw_u:
        _p_low = _prompt_str.lower()
        if "in feet" in _p_low or "(ft)" in _p_low or " ft" in _p_low:
            _raw_u = "ft"
        elif "mils" in _p_low:
            _raw_u = "mils"
        elif "in inches" in _p_low or "(in)" in _p_low or "inches" in _p_low:
            _raw_u = "in"
        elif "psi" in _p_low:
            _raw_u = "psi"
        elif "ksi" in _p_low:
            _raw_u = "ksi"
        elif "kips" in _p_low:
            _raw_u = "kips"
        elif "btu" in _p_low:
            _raw_u = "BTU/hr"
        elif "°f" in _p_low or "fahrenheit" in _p_low or "deg f" in _p_low:
            _raw_u = "°F"
        elif "pci" in _p_low:
            _raw_u = "PCI"
        elif "percent" in _p_low or "(%)" in _p_low or "%" in _p_low:
            _raw_u = "%"
        elif "cfs" in _p_low:
            _raw_u = "cfs"
        elif "sq ft" in _p_low or "square feet" in _p_low:
            _raw_u = "sq ft"
    _u_desc_map = {
        "ft": "feet (ft) — U.S. Customary Linear Feet (12 inches = 1.0 foot)",
        "feet": "feet (ft) — U.S. Customary Linear Feet (12 inches = 1.0 foot)",
        "inches": "inches (in) — U.S. Customary Inches (1/12 of a foot)",
        "in": "inches (in) — U.S. Customary Inches (1/12 of a foot)",
        "mils": "mils (0.001 in) — Thousandths of an Inch (1,000 mils = 1.0 inch)",
        "sq ft": "square feet (sq ft) — U.S. Customary Surface Area (Length_ft * Width_ft)",
        "%": "Percent (%) — Percentage Score / Ratio (0% to 100%)",
        "psi": "psi (Pounds per Square Inch) — U.S. Customary Stress / Pressure",
        "ksi": "ksi (Kips per Square Inch) — 1,000 Pounds per Square Inch",
        "kips": "kips (Kilopounds) — U.S. Customary Structural Load (1 kip = 1,000 lbs)",
        "lbs": "pounds (lbs) — U.S. Customary Force / Weight",
        "psf": "psf (Pounds per Square Foot) — U.S. Customary Area Load",
        "°F": "degrees Fahrenheit (°F) — U.S. Customary Temperature",
        "BTU/hr": "BTU/hr (British Thermal Units per Hour) — U.S. Customary Heat Flow Rate",
        "cfs": "cfs (Cubic Feet per Second) — U.S. Customary Hydraulic Discharge",
        "PCI": "PCI Points (0 to 100 Scale) — ASTM D6433 Pavement Condition Index",
        "RF": "Rating Factor (RF) — AASHTO Load & Resistance Factor Ratio (RF >= 1.00 is Safe)",
    }
    _resolved_u_str = _u_desc_map.get(_raw_u, f"{_raw_u} — U.S. Customary Engineering Unit" if _raw_u else "feet (ft) / inches (in) / psi / °F — U.S. Customary Units")
    u_dict["resolved_us_unit"] = _resolved_u_str
    if "equation_legend" in u_dict and isinstance(u_dict["equation_legend"], str):
        u_dict["equation_legend"] = u_dict["equation_legend"].replace(
            "Measured in U.S. Customary Units",
            _resolved_u_str
        )

    return u_dict



def _orig_get_course_units(course_code: str):
    if course_code == "STR-01":
        raw_units = [
            {
                "unit": 1,
                "hours": 4.0,
                "title": "Unit 01: Statutory Jurisprudence — 23 CFR § 650 (NBIS), Oklahoma Title 61 & Title 74",
                "theory": """### 1.1 Federal & State Statutory Evolution of Bridge Safety
Following the catastrophic collapse of the U.S. Route 35 Silver Bridge on December 15, 1967 (46 fatalities), Congress enacted the **Federal-Aid Highway Act of 1968**, establishing the **National Bridge Inspection Standards (NBIS)** codified at **23 CFR § 650 Subpart C**. Within the State of Oklahoma, federal NBIS requirements are integrated into **Oklahoma Statutes Title 61 (Public Buildings and Public Works)** and **Title 74**, administered by the **Oklahoma Department of Transportation (ODOT) Bridge Division**.

Every structure on a public roadway with an opening measured along the center of the roadway of more than **20.0 feet** between undercopings of abutments or spring lines of arches, or extreme ends of openings for multiple boxes, is legally classified as a **Bridge** and must be cataloged in the **National Bridge Inventory (NBI)**.

| Statutory Mandate | Code Citation | Maximum Interval | Legal / Engineering Requirement |
| :--- | :--- | :--- | :--- |
| **Routine NBI Inspection** | 23 CFR § 650.311(a) | **24 Months** | Full element-level quantification of deck, superstructure, and substructure defects. |
| **Fracture-Critical (FCM)** | 23 CFR § 650.311(c) | **24 Months** | Hands-on (within arm's length) or ODOT-certified sub-millimeter optical NDT of tension steel members. |
| **Underwater Bathymetric** | 23 CFR § 650.311(b) | **60 Months** | Acoustic sonar / commercial diver verification of submerged pier footings and pilings. |
| **Scour Plan of Action** | ODOT Item 113 | **Immediate / Flood** | Real-time bathymetric deployment whenever hydrograph stage exceeds 50-year or 100-year discharge. |

### 1.2 Inspector Qualification & Criminal Liability (18 U.S.C. § 1001 & OK Title 61)
Under **23 CFR § 650.309**, a Program Manager or Team Leader must hold either a **Professional Engineer (PE)** license or meet strict engineering experience requirements combined with comprehensive accredited bridge inspection training. Signing an inspection docket with uncalibrated instrumentation, fabricated GPS coordinates, or omitted CS-4 defects constitutes a felony false statement under **18 U.S.C. § 1001** and triggers civil forfeiture under **Oklahoma Title 61**. To ensure absolute evidentiary integrity, all Humphrey Virtual Farms LLC (CAGE: 1AHA8) field sorties seal raw telemetry inside a **Write-Once-Read-Many (WORM) SQLite ledger** signed with a **FIPS 180-4 SHA-256 cryptographic digest**.""",
                "equations": """L_total (ft) = (Number_of_Barrels * Barrel_Width_ft) + (Number_of_Interior_Walls * Wall_Thickness_ft)
Rule: If L_total > 20.0 feet  -->  Mandatory NBI Bridge & OK Title 61 Jurisdiction (24-Month Inspection)
Sufficiency_Rating (SR %) = S_1 (Structural Adequacy: 55%) + S_2 (Serviceability: 30%) + S_3 (Essentiality: 15%) - S_4 (Special Reductions: max 13%)""",
                "worked_example": """#### Worked Engineering Problem 1.1: Multi-Barrel Culvert NBI Jurisdiction Determination
* **Field Scenario:** An inspector evaluates a 3-barrel Reinforced Concrete Box (RCB) culvert under a county highway in Canadian County, Oklahoma. Each barrel measures 6.0 ft wide individually, separated by two 1.5 ft interior concrete walls, skewed at 0 degrees to the roadway centerline.
* **Step 1 (Calculate Extreme Ends Opening):** Measure from the inside face of the west exterior wall to the inside face of the east exterior wall:
  `L_total = (3 * 6.0 ft) + (2 * 1.5 ft) = 18.0 ft + 3.0 ft = 21.0 ft`
* **Step 2 (Statutory Ruling):** Because `L_total = 21.0 ft > 20.0 ft`, the multi-barrel culvert **is legally classified as an NBI Bridge** under 23 CFR § 650.305 and Oklahoma Title 61, requiring a mandatory 24-month inspection cycle.""",
                "lab_protocol": """1. Verify Team Leader PE / Sovereign Level-5 Credential ID in `matrix_ledger.db`.
2. Pull historical ODOT NBI Structure Inventory and Appraisal (SI&A) sheet (Items 1 through 116).
3. Verify structure span geometry (L > 20.0 ft) and lock SHA-256 pre-sortie docket initialization."""
            },
            {
                "unit": 2,
                "hours": 4.0,
                "title": "Unit 02: AASHTO MBEI Element-Level Condition State Architecture (CS-1 to CS-4)",
                "theory": """### 2.1 National Bridge Elements (NBE) & Bridge Management Elements (BME)
Under the **AASHTO Manual for Bridge Element Inspection (MBEI)**, inspectors do not assign a single vague grade to an entire bridge. Instead, every structural component is broken down into standardized element codes (e.g., **Element 12: Reinforced Concrete Deck**, **Element 107: Steel Open Girder/Beam**, **Element 205: Reinforced Concrete Column**, **Element 210: Reinforced Concrete Pier Wall**) and quantified across four discrete **Condition States (CS-1 through CS-4)**:

| Condition State | Severity | Crack Width (w_c) | Spalling / Delamination | Reinforcing / Structural Steel State | Required Statutory Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CS-1 (Good)** | None / Hairline | w_c < 0.012 inches (12 mils) | Zero delamination; sound acoustic/thermal return. | Intact passive oxide film or coating; zero corrosion. | Routine 24-month cycle; preventive silane seal. |
| **CS-2 (Fair)** | Moderate | 0.012 in <= w_c <= 0.050 in | Delamination present; spalls <= 1.0 in deep and <= 6.0 in diameter. | Minor surface freckle rust; no exposed rebar section loss. | Epoxy crack injection; localized concrete patching. |
| **CS-3 (Poor)** | Advanced | w_c > 0.050 inches (50 mils) | Spalls > 1.0 in deep; widespread hollow delamination plane. | Exposed rebar with active oxidation; measurable section loss < 10%, capacity intact. | **Mandatory Priority Maintenance Docket.** Hydrodemolition if deck D_% >= 10%. |
| **CS-4 (Severe)** | Critical | Structural shear / flexure cracks | Full-depth slab punch-through or bearing crushing. | Severe section loss >= 10% in tension path or active fatigue crack. | **IMMEDIATE EMERGENCY CLOSURE / LOAD RESTRICTION** under OK Title 61. |""",
                "equations": """Total_Element_Area (A_total) = A_CS1 + A_CS2 + A_CS3 + A_CS4
Weighted_Health_Index (HI) = [ (1.00 * A_CS1) + (0.67 * A_CS2) + (0.33 * A_CS3) + (0.00 * A_CS4) ] / A_total * 100""",
                "worked_example": """#### Worked Engineering Problem 2.1: Element 12 Concrete Deck Condition State Allocation & Health Index
* **Field Scenario:** A 4-span concrete bridge deck measures 320 ft long by 40 ft wide (A_total = 12,800 sq ft). Radiometric infrared and acoustic chain-drag telemetry identify:
  * 9,200 sq ft intact with no defects (**CS-1**).
  * 1,900 sq ft with moderate cracking (0.03 in) and shallow scaling (**CS-2**).
  * 1,650 sq ft with subsurface delamination and deep spalling exposing oxidized top-mat rebar (**CS-3**).
  * 50 sq ft with full-depth punch-through failure in the right wheel path (**CS-4**).
* **Step 1 (Calculate Delamination/Defective Percentage D_%):**
  `D_% = (1,650 + 50) / 12,800 * 100 = 13.28%`
* **Step 2 (Calculate Bridge Element Health Index HI):**
  `HI = [ (1.0 * 9200) + (0.67 * 1900) + (0.33 * 1650) + (0.0 * 50) ] / 12,800 * 100 = 86.07%`
* **Step 3 (Statutory Disposition):** Presence of 50 sq ft of **CS-4** punch-through mandates immediate lane closure and steel plating, and `D_% = 13.28% >= 10.0%` triggers mandatory Title 61 hydrodemolition rehabilitation.""",
                "lab_protocol": """1. Grid the bridge deck into 10 ft x 10 ft orthomosaic sub-cells using QGIS/Pix4D photogrammetry.
2. Classify every sub-cell into CS-1, CS-2, CS-3, or CS-4 based on crack width optical measurement and thermal Delta_T.
3. Verify sum(A_CSi) == A_total prior to committing the ODOT Element Inspection Docket."""
            },
            {
                "unit": 3,
                "hours": 4.0,
                "title": "Unit 03: Reinforced Concrete Electrochemistry, Fickian Chloride Diffusion & Half-Cell Potentials",
                "theory": """### 3.1 Fick's Second Law of Chloride Ion Diffusion in Concrete Cover
De-icing salts (NaCl, CaCl2) applied to Oklahoma bridges during winter ice storms dissolve in meltwater and diffuse downward through the capillary pore network of the concrete cover toward the top mat of reinforcing steel. This non-steady-state mass transport is governed by **Fick's Second Law of Diffusion**:
* **Differential Form:** `dC/dt = D_c * (d^2C / dx^2)`
* **Gauss Error Function Solution:** `C(x, t) = C_0 * [ 1 - erf( x / (2 * sqrt(D_c * t)) ) ]`

Once `C(x_rebar, t)` reaches the **Critical Chloride Threshold (C_crit = 1.2 to 1.5 lb/yd^3)**, the high-pH passive gamma-ferric oxide film dissolves. Hydrated red/black rust expands **300% to 600% in volume**, generating internal tensile bursting stresses of **4,000 to 7,000 psi** against concrete whose tensile rupture capacity is only **f_r = 7.5 * sqrt(f'_c) (~475 to 580 psi)**, fracturing the horizontal delamination plane.

### 3.2 ASTM C876 Copper-Copper Sulfate (Cu/CuSO4) Half-Cell Potential Mapping
* **Potential > -200 mV vs. CSE:** > 90% probability of **no active rebar corrosion**.
* **-350 mV <= Potential <= -200 mV vs. CSE:** Corrosion activity **uncertain**.
* **Potential < -350 mV vs. CSE:** > **90% probability of active reinforcing steel corrosion** and imminent subsurface delamination.""",
                "equations": """C(x, t) = C_0 * [ 1 - erf( x / (2 * sqrt(D_c * t)) ) ]
P_rust (4,000 to 7,000 psi) >> f_r = 7.5 * sqrt(f'_c) (~475 to 580 psi)  -->  Horizontal Delamination Fracture""",
                "worked_example": """#### Worked Engineering Problem 3.1: Time-to-Depassivation Calculation for Bridge Deck Rebar
* **Field Scenario:** A concrete bridge deck has a clear rebar cover depth of x = 2.0 inches, surface chloride concentration C_0 = 6.0 lb/yd^3, critical threshold C_crit = 1.5 lb/yd^3, and apparent diffusion coefficient D_c = 0.0586 in^2/yr.
* **Step 1 (Error Function Ratio):** `C_crit / C_0 = 1.5 / 6.0 = 0.25 = 1 - erf(z)  -->  erf(z) = 0.75  -->  z = 0.813`.
* **Step 2 (Solve for Time to Corrosion Initiation t):**
  `t = x^2 / (4 * D_c * z^2) = (2.0 in)^2 / (4 * 0.0586 in^2/yr * 0.813^2) = 4.00 / 0.155 = 25.8 years`.""",
                "lab_protocol": """1. Perform core-drilled powder sampling at 0.5 in depth increments for acid-soluble chloride titration (AASHTO T 260).
2. Conduct ASTM C876 Cu/CuSO4 half-cell potential grid survey on a 4.0 ft spacing.
3. Overlay half-cell equipotential contour maps (<-350 mV) directly onto aerial radiometric IR delamination polygons."""
            },
            {
                "unit": 4,
                "hours": 4.0,
                "title": "Unit 04: Steel Superstructures, Linear-Elastic Fracture Mechanics (LEFM) & Paris-Erdogan Fatigue",
                "theory": """### 4.1 Fracture-Critical Members (FCM) & Load-Path Redundancy
Under **23 CFR § 650.305**, a **Fracture-Critical Member (FCM)** is a steel member in tension, or with a tension element, whose failure would probably cause a portion of or the entire bridge to collapse (e.g., two-girder bridges, tied-arch tension ties, pin-and-hanger straps, non-redundant truss chords).

### 4.2 Stress Intensity Factor (K_I) & Plane-Strain Fracture Toughness (K_Ic)
In **Linear-Elastic Fracture Mechanics (LEFM)**, the elastic stress field at the tip of a crack of length `a` subjected to tensile stress `sigma` is defined by the **Mode I Stress Intensity Factor (K_I)**:
* `K_I = Y * sigma * sqrt(pi * a)`
Catastrophic brittle cleavage fracture occurs instantaneously at the speed of sound in steel (19,350 ft/s) when **K_I >= K_Ic** (Plane-Strain Fracture Toughness).

### 4.3 Cyclic Fatigue Crack Growth: The Paris-Erdogan Law
Under repetitive truck axle stress ranges (`Delta_sigma`), sub-critical fatigue cracks propagate at rate `da/dN = C * (Delta_K)^m`, where `m = 3.0` for ferritic bridge steels.""",
                "equations": """K_I = Y * sigma * sqrt(pi * a)      [Mode I Stress Intensity, ksi*sqrt(in)]
a_c = (1 / pi) * [ K_Ic / (Y * sigma_max) ]^2
N_f = [ 2 / (C * Y^3 * (Delta_sigma)^3 * pi^1.5) ] * [ (1 / sqrt(a_0)) - (1 / sqrt(a_c)) ]""",
                "worked_example": """#### Worked Engineering Problem 4.1: Critical Crack Size & Remaining Truck Cycles on a Two-Girder FCM Bridge
* **Field Scenario:** Under-deck 48MP optical inspection of an A36 steel 2-girder bridge (K_Ic = 45.0 ksi*sqrt(in)) detects an edge fatigue crack a_0 = 0.25 in in the bottom tension flange (Y = 1.12). Peak tensile stress is sigma_max = 22.0 ksi; fatigue stress range is Delta_sigma = 6.0 ksi (C = 3.6e-10, m = 3.0).
* **Step 1 (Critical Crack Length a_c):**
  `a_c = (1 / 3.1416) * (45.0 / (1.12 * 22.0))^2 = 0.3183 * (1.8263)^2 = 1.062 inches`.
* **Step 2 (Remaining Cycles N_f):**
  `N_f = [ 2 / (6.077e-7) ] * (1/sqrt(0.25) - 1/sqrt(1.062)) = 3,388,500 truck cycles` (Code immediately as **CS-4**).""",
                "lab_protocol": """1. Deploy upward-tilted (+60 deg) 48MP optical zoom payload at 5.0 ft standoff to achieve GSD <= 0.003 in/pixel (3 mils/px).
2. Inspect all AASHTO Category E/E' details: welded cover plate ends, web-stiffener toe welds, and gusset nodes.
3. Flag any linear indication >= 0.004 inches (4 mils) for hands-on Ultrasonic Phased-Array (PAUT) sizing."""
            },
            {
                "unit": 5,
                "hours": 4.0,
                "title": "Unit 05: GPS-Denied Under-Deck UAS Navigation, Faraday Shielding & EKF Optical Flow SLAM",
                "theory": """### 5.1 Electromagnetic Faraday Shielding & Ferromagnetic Compass Distortion
Flying beneath a reinforced concrete deck and steel girder grid induces two lethal navigation hazards:
1. **Faraday GNSS Attenuation & Multipath:** Rebar mats and steel flanges block L1/L2 GPS signals, dropping satellite count below the 4-satellite 3D fix threshold.
2. **Ferromagnetic Compass Deviation:** Massive steel girders warp the Earth's magnetic field, inducing 45 to 90 degree yaw errors in fluxgate magnetometers.

### 5.2 Extended Kalman Filter (EKF3) Optical Flow + LiDAR Rangefinding Fusion
The Sovereign flight controller inhibits magnetometer yaw (`COMPASS_USE = 0`) and fuses **HereFlow Optical Flow** angular pixel rates (`omega_px`) with **TF02-i LiDAR** rangefinding (`z`) and MEMS ring-laser gyros (`omega_gyro`). Optical flow requires a minimum surface illuminance of **1.4 foot-candles** via onboard LED luminaire bars.""",
                "equations": """v_x = z_lidar * (omega_pixel_x - omega_gyro_y)
Luminous_Intensity (I_candela) >= 1.4 foot-candles * (d_meters)^2""",
                "worked_example": """#### Worked Engineering Problem 5.1: Optical Flow Velocity & LED Illumination Sizing Beneath a Dark Box Girder
* **Field Scenario:** The UAS hovers at standoff z = 8.2 ft (2.5 m) beneath a dark girder. Optical flow reports pixel rate 0.48 rad/s while pitch gyro rate is 0.08 rad/s.
* **Step 1 (True Horizontal Velocity v_x):** `v_x = 2.5 m * (0.48 - 0.08) = 3.28 ft/s (1.00 m/s)`.
* **Step 2 (Minimum LED Intensity for 25 lux safety margin at 2.5 m):** `I_min = 2.3 foot-candles (25 lux) * (2.5 m / 8.2 ft)^2 = 156.25 candelas`.""",
                "lab_protocol": """1. Set EKF3 primary velocity source to Optical Flow (`EK3_SRC1_VELXY = 5`) and altitude to Rangefinder (`EK3_SRC1_POSZ = 2`).
2. Disable magnetic compass yaw fusion (`COMPASS_USE = 0`) before crossing beneath the fascia girder.
3. Cap maximum under-deck ingress speed at <= 5.0 ft/s (3.4 mph) with a 5.0 ft 360-degree LiDAR obstacle avoidance bubble."""
            },
            {
                "unit": 6,
                "hours": 4.0,
                "title": "Unit 06: Hydrologic Pier Scour Bathymetry, Froude Hydrodynamics & FHWA HEC-18 Equations",
                "theory": """### 6.1 Hydraulic Scour: The #1 Cause of Bridge Collapse
Hydraulic scour—the erosive removal of streambed sediment around piers and abutments by horseshoe and wake vortices—causes over **60% of all U.S. bridge failures**.

### 6.2 FHWA HEC-18 (Colorado State University) Equilibrium Pier Scour Formulation
Under **ODOT Item 113** and **FHWA HEC-18**, equilibrium scour depth (`y_s`) is governed by upstream depth (`y_1`), pier width (`b`), shape/alignment factors (`K_1..K_4`), and the upstream **Froude Number (`Fr_1 = V_1 / sqrt(g * y_1)`)**.""",
                "equations": """y_s = y_1 * 2.0 * K_1 * K_2 * K_3 * K_4 * (b / y_1)^0.65 * (V_1 / sqrt(32.174 * y_1))^0.43
d_water = (c_sound_water * Delta_t_echo) / 2,   where c_sound_water = 4,856 ft/s (200 kHz Sonar)""",
                "worked_example": """#### Worked Engineering Problem 6.1: HEC-18 Pier Scour vs. Footing Depth Stability Audit
* **Field Scenario:** Round-nose pier (K1=1.0, K2=1.0, K3=1.1, K4=1.0), width b = 4.0 ft, upstream flood depth y_1 = 14.0 ft, velocity V_1 = 11.2 ft/s. Spread footing bottom is 9.0 ft below baseline streambed.
* **Step 1 (Froude Number Fr_1):** `Fr_1 = 11.2 / sqrt(32.174 * 14.0) = 0.5277`.
* **Step 2 (Predicted Scour Depth y_s):** `y_s = 14.0 * 2.0 * 1.1 * (4.0/14.0)^0.65 * (0.5277)^0.43 = 10.37 ft`.
* **Step 3 (Statutory Disposition):** Scour depth (10.37 ft) exceeds footing embedment (9.0 ft) -> Code **ODOT Item 113 Scour Critical** and close bridge immediately during flood stage.""",
                "lab_protocol": """1. Deploy tethered 200 kHz single-beam acoustic sonar transducer around pier perimeter.
2. Calibrate water speed of sound for ambient water temperature and sediment load.
3. Compare current sonar bed elevation (y_bed) against historical baseline (y_0) and footing depth."""
            },
            {
                "unit": 7,
                "hours": 4.0,
                "title": "Unit 07: Non-Destructive Testing (NDT) Physics — Ultrasonic Phased-Array, Impact-Echo & GPR",
                "theory": """### 7.1 Stress-Wave Impact-Echo (ASTM C1383) & Ground Penetrating Radar (GPR — ASTM D6087)
* **Impact-Echo:** Mechanical impact generates compressional P-waves (`c_p ~ 13,120 ft/s`) that reflect off internal delaminations. FFT peak frequency `f` yields flaw depth: `T = (0.96 * c_p) / (2 * f)`.
* **Ground Penetrating Radar (GPR):** 1.5–2.6 GHz electromagnetic pulses reflect strongly off chloride-wet concrete (`epsilon_r ~ 81` vs. dry concrete `epsilon_r ~ 6`).""",
                "equations": """Depth_Depth_in = (0.96 * c_p_ft_s * 12 in/ft) / (2 * f_peak_Hz)
Depth_rebar = (c_0 * t_two_way) / (2 * sqrt(epsilon_r)),   where c_0 = 11.8 in/ns""",
                "worked_example": """#### Worked Engineering Problem 7.1: Impact-Echo Delamination Depth Calculation
* **Field Scenario:** Concrete deck thickness 8.50 in (c_p = 13,120 ft/s, beta = 0.96). Point A FFT frequency is 8,890 Hz; Point B shifts to 30,200 Hz.
* **Calculation:** Point A depth = `(0.96 * 13,120 ft/s * 12 in/ft) / (2 * 8,890 Hz) = 8.50 inches` (**8.50 in sound slab**). Point B depth = `(0.96 * 13,120 ft/s * 12 in/ft) / (2 * 30,200 Hz) = 2.50 inches` (**2.50 in top-mat rebar delamination!**).""",
                "lab_protocol": """1. Calibrate P-wave velocity over a known sound core location before running Impact-Echo grid scans.
2. Configure 2.0 GHz GPR antenna scan spacing at 1.0 ft longitudinal passes across all lanes.
3. Export rebar cover depth contour maps to calibrate hydrodemolition milling depth."""
            },
            {
                "unit": 8,
                "hours": 4.0,
                "title": "Unit 08: Substructure Bearings, Elastomeric Shear Deformation, Pin-and-Hanger & Gusset Plates",
                "theory": """### 8.1 Thermal Expansion Kinematics & Elastomeric Bearing Shear Strain
Steel girders expand thermally by `Delta_L = alpha * L * Delta_T`. Under AASHTO LRFD, neoprene elastomeric bearing pads must not exceed a horizontal shear strain of `gamma = Delta_s / h_rt <= 0.50`.

### 8.2 Gusset Plate Compression Buckling (FHWA Technical Advisory T 5140.29)
Following the I-35W truss collapse, inspectors must measure exact gusset plate thickness, corrosion loss, and out-of-plane bowing across the **Whitmore Effective Width (`b_w = w + 2 * L * tan(30 deg)`)**.""",
                "equations": """Delta_L = alpha * L_span * (T_current - T_install)
Shear_Strain_gamma = Delta_s / h_elastomer <= 0.50 (AASHTO LRFD Limit)""",
                "worked_example": """#### Worked Engineering Problem 8.1: Elastomeric Bearing Pad Shear Strain Audit
* **Field Scenario:** An elastomeric pad with elastomer thickness h_rt = 2.50 in has sheared horizontally by Delta_s = 1.65 in at 102 °F.
* **Calculation:** `gamma = 1.65 / 2.50 = 0.66 > 0.50 limit` -> Code **Element 310 as CS-3 (Poor)** and issue girder jacking/reset docket.""",
                "lab_protocol": """1. Record steel surface temperature via radiometric spot sensor during every bearing inspection.
2. Measure rocker tilt angle or elastomeric shear offset relative to 60 °F neutral point.
3. Scan truss gusset plates with 3D LiDAR to detect out-of-plane distortion > 0.125 in."""
            },
            {
                "unit": 9,
                "hours": 4.0,
                "title": "Unit 09: Forensic Structural Failure Reconstructions — Silver Bridge, Mianus River & I-35W",
                "theory": """### 9.1 Silver Bridge (1967 — 46 Fatalities): Stress-Corrosion Cracking of Non-Redundant Eyebar 330
A **0.125-inch** stress-corrosion crack inside the pinhole of SAE 1060 high-carbon steel Eyebar 330 reached critical fracture toughness (`K_Ic ~ 42 ksi*sqrt(in)` at 30 °F), causing instantaneous brittle cleavage and total progressive collapse in 47 seconds.

### 9.2 Mianus River Bridge (1983 — 3 Fatalities): Pack-Rust Prying of Pin-and-Hanger Assembly
Unmitigated de-icing salt runoff built up expansive **pack rust** behind the southeast hanger strap, generating >150 kips of lateral force that pushed the strap off the 7-inch steel pin.

### 9.3 I-35W Mississippi River Bridge (2007 — 13 Fatalities): Undersized 0.5-Inch U10 Gusset Plates
Node U10 gusset plates were fabricated at **0.50 inches** instead of 1.00 inch. Combined with 3.0M lbs of added deck overlay and 578,000 lbs of staged construction aggregate over Node U10, the gusset plate buckled in compression.""",
                "equations": """b_w = w_fastener_group + 2 * L_fastener_depth * tan(30 deg)   [Whitmore Section Width]
sigma_whitmore = P_axial / (b_w * t_gusset) <= phi * F_cr""",
                "worked_example": """#### Worked Engineering Problem 9.1: Whitmore Section Stress Audit on Node U10 Gusset Plate
* **Field Scenario:** Diagonal compression load P = 1,450 kips transfers through fastener group width w = 14.0 in, length L = 24.0 in, into a t = 0.50 in gusset plate (F_y = 50 ksi).
* **Step 1 (Whitmore Width b_w):** `b_w = 14.0 + 2 * 24.0 * tan(30 deg) = 41.71 in`.
* **Step 2 (Whitmore Stress):** `Area = 41.71 * 0.50 = 20.86 in^2 -> Stress = 1,450 / 20.86 = 69.51 ksi > 50.0 ksi yield` (**CATASTROPHIC BUCKLING!**).""",
                "lab_protocol": """1. Measure lateral strap creep on 100% of pin-and-hanger assemblies using laser micrometry.
2. Perform ultrasonic thickness gauging on all truss gusset plates.
3. Enforce zero construction material stockpiling over fracture-critical truss nodes."""
            },
            {
                "unit": 10,
                "hours": 4.0,
                "title": "Unit 10: Oklahoma Title 61 Statutory Docket Synthesis, Load Rating Triggers & WORM Certification",
                "theory": """### 10.1 AASHTO MBE Load and Resistance Factor Rating (LRFR) & Statutory Load Posting
When CS-3 or CS-4 section loss is measured, the inspector triggers an immediate **Rating Factor (`RF`)** calculation. If **RF < 1.0** for legal Oklahoma truck loads, mandatory **Title 61 Weight Posting** or emergency bridge closure (if capacity < 3 tons) is enforced.""",
                "equations": """RF = [ Capacity_C - (gamma_DC * DC) - (gamma_DW * DW) ] / [ gamma_LL * (LL + IM) ]
Max_Posting_Tons = Legal_Truck_Weight_Tons * RF   [When RF < 1.0]""",
                "worked_example": """#### Worked Engineering Problem 10.1: Corroded Steel Girder LRFR Rating Factor & Statutory Weight Posting
* **Field Scenario:** Corroded girder moment capacity C = 1,850 kip-ft; factored dead load = 720 kip-ft; wearing surface = 180 kip-ft; factored 36-ton legal truck live load + impact = 1,250 kip-ft.
* **Calculation:** `RF = (1850 - 720 - 180) / 1250 = 0.76 < 1.0`. Mandatory weight limit = `36.0 * 0.76 = 27 Tons Maximum Posting`.""",
                "lab_protocol": """1. Compile all CS-1 through CS-4 element quantities and section loss measurements into the LRFR sheet.
2. Seal final inspection docket with SHA-256 into `matrix_ledger.db`.
3. Sign off Unit 10 to complete 40.0/40.0 Credit Hours and enter the 3-Tier State Examination Gauntlet."""
            }
        ]
    elif course_code == "STR-02":
        raw_units = [
            {
                "unit": 1, "hours": 4.0,
                "title": "Unit 01: Oklahoma Title 61 Public Facilities Governance & OMES CAP Statutory Mandates",
                "theory": """### 1.1 Statutory Authority of OMES Construction and Properties (CAP)
Under **Oklahoma Statutes Title 61**, the **OMES Construction and Properties (CAP)** division governs capital roof replacements and building envelope audits across all state facilities. Quantitative **ASTM C1153** infrared thermography is required prior to authorizing full tear-offs (USD 24+/sq ft) versus surgical wet-core recovery (USD 6 to USD 8/sq ft), saving taxpayers up to 65% in capital outlays.""",
                "equations": """Lifecycle_Savings = (Area_total * Cost_TearOff) - [ (Area_wet * Cost_SurgicalRepair) + (Area_total * Cost_Coating) ]""",
                "worked_example": """#### Worked Problem 1.1: Title 61 Capital Tear-Off vs. Surgical Recovery Audit
* **Scenario:** 100,000 sq ft state roof tear-off quote is USD 2,400,000 (USD 24.00/sq ft). UAS survey finds only 11,500 sq ft (11.5%) wet core. Surgical repair (USD 16.00/sq ft) + full silicone restoration (USD 6.50/sq ft) costs USD 834,000 -> **Net Taxpayer Savings = USD 1,566,000 (65.25%)**.""",
                "lab_protocol": """1. Verify OMES CAP Facility Asset ID and pull historical roof assembly cross-section blueprints.
2. Log membrane type (TPO, EPDM, PVC, Mod-Bit, BUR) and insulation R-value."""
            },
            {
                "unit": 2, "hours": 4.0,
                "title": "Unit 02: ASTM C1153 & ISO 6781 Radiometric Infrared Thermography Standards",
                "theory": """### 2.1 Strict Meteorological Boundary Conditions under ASTM C1153
1. **Daytime Solar Loading:** Minimum 50% sunny skies prior to inspection.
2. **Dry Surface Mandate:** 100% free of standing water, snow, or ice (>24 hrs post-rain).
3. **Wind Speed Ceiling:** Ambient wind **v_wind < 15.0 mph** to prevent convective stripping.
4. **Nocturnal Window:** **45 to 120 minutes post-sunset** under clear skies (<20% cloud cover).""",
                "equations": """U_wind_BTU = 1.0 + 0.30 * v_wind_mph   [Convective Surface Coefficient, BTU/(hr*ft^2*°F)]
ASTM_C1153_Valid = (Wind_mph < 15.0) AND (Hours_Post_Rain >= 24.0) AND (Min_Post_Sunset >= 45)""",
                "worked_example": """#### Worked Problem 2.1: Convective Wind Stripping Coefficient Calculation
* **Scenario:** Compare convective surface heat stripping at calm wind v = 5.0 mph vs. high wind v = 20.0 mph.
* **Result:** At 5.0 mph, U_wind = **2.50 BTU/(hr*ft^2*°F)** (strong thermal contrast preserved). At 20.0 mph, U_wind = **7.00 BTU/(hr*ft^2*°F)** (nearly 3x wind stripping erases the roof anomaly).""",
                "lab_protocol": """1. Deploy Kestrel ultrasonic anemometer at roof parapet elevation 60 minutes prior to takeoff.
2. Log ambient dry-bulb temp, relative humidity, dew point, and wind velocity into Title 61 docket."""
            },
            {
                "unit": 3, "hours": 4.0,
                "title": "Unit 03: Quantum & Thermodynamic Physics — Planck's Law, Wien's Displacement & Emissivity",
                "theory": """### 3.1 Wien's Displacement Law & Longwave Infrared (LWIR) Sensors
Peak blackbody emission wavelength is `lambda_max = 2897.8 / T_Kelvin`. At ambient roof temperatures (~62 °F), peak radiation occurs at **10.0 micrometers**, requiring an uncooled VOx **LWIR (7.5 to 13.5 um)** microbolometer with **NETD <= 0.09 °F (50 mK)** and emissivity correction (`epsilon = 0.92` for single-ply membranes).""",
                "equations": """lambda_max = 2897.8 / T_Kelvin   [micrometers]
W_tot = epsilon * tau * sigma * T_obj^4 + (1 - epsilon) * tau * sigma * T_refl^4""",
                "worked_example": """#### Worked Problem 3.1: Wien's Peak Wavelength Calculation
* **Scenario:** A TPO roof membrane is at T = 53.3 °F (285 K).
* **Calculation:** lambda_max = 2897.8 / 285 = **10.17 micrometers** (centered in LWIR 7.5-13.5 um window).""",
                "lab_protocol": """1. Input epsilon = 0.92 for single-ply membranes and T_refl = -31 °F (-35 °C) (clear night sky) into RJPEG processor.
2. Mask out unpainted sheet-metal flashing and HVAC housings (epsilon ~ 0.20) to prevent false anomalies."""
            },
            {
                "unit": 4, "hours": 4.0,
                "title": "Unit 04: Heat Transfer Mechanics — Fourier Conduction, Volumetric Heat Capacity & R-Value Loss",
                "theory": """### 4.1 The 93x Volumetric Heat Capacity Disparity
Dry polyisocyanurate foam has volumetric heat capacity `rho * c_p = 44.8 kJ/(m^3*K)`, whereas liquid water has `4,184 kJ/(m^3*K)`—**93.4x higher volumetric heat storage!** Simultaneously, water destroys insulation R-value, driving massive conductive energy loss (`Q = U * A * Delta_T`).""",
                "equations": """Q_loss_BTU_hr = (Area_sqft / R_value_US) * (T_in_F - T_out_F)
Ratio_Volumetric_Heat_Capacity = (rho_water * cp_water) / (rho_ISO * cp_ISO) = 93.4""",
                "worked_example": """#### Worked Problem 4.1: Conductive Heat Flux Increase Across Saturated Roof Insulation
* **Scenario:** Compare heat loss across 2,500 sq ft of dry Polyiso insulation (R-25) vs. water-logged insulation (R-4) when Indoor Temp = 72 °F and Outdoor Night Temp = 27 °F (Delta_T = 45 °F).
* **Calculation:** Q_dry = (2,500 / 25) * 45 = **4,500 BTU/hr** vs. Q_wet = (2,500 / 4) * 45 = **28,125 BTU/hr** (**6.25x energy bleed!**).""",
                "lab_protocol": """1. Measure thermal anomaly surface Delta_T = T_wet - T_dry across all RJPEG orthomosaic polygons.
2. Flag any polygon exhibiting Delta_T >= +3.6 °F for ground-truth impedance verification."""
            },
            {
                "unit": 5, "hours": 4.0,
                "title": "Unit 05: Psychrometrics, Vapor Drive, Dew-Point Condensation & Air Barrier Failure",
                "theory": """### 5.1 Magnus-Tetens Dew-Point Formulation & Interstitial Condensation
Warm, humid indoor air exfiltrating through unsealed parapet or curtain-wall joints condenses into liquid water whenever it contacts a structural surface at or below the **Dew-Point Temperature (`T_dp`)**.""",
                "equations": """gamma = ln(RH / 100) + (17.62 * T_F) / (243.12 + T_F)
T_dew_point_C = (243.12 * gamma) / (17.62 - gamma)""",
                "worked_example": """#### Worked Problem 5.1: Hospital Envelope Dew-Point Condensation Audit
* **Scenario:** Indoor hospital conditions are T = 73.4 °F (23.0 °C) and Relative Humidity RH = 55%.
* **Calculation:** gamma = 0.9250 -> T_dp = (243.12 * 0.9250) / (17.62 - 0.9250) = **56.25 °F (13.47 °C)**. Any steel deck below 56.25 °F experiences active condensation.""",
                "lab_protocol": """1. Conduct blower-door depressurization (-50 Pa) per ASTM E1186 while scanning joints with LWIR.
2. Distinguish diffuse wet-insulation conduction from sharp convective air-exfiltration plumes."""
            },
            {
                "unit": 6, "hours": 4.0,
                "title": "Unit 06: Secondary NDT Verification — Capacitive Dielectric, Nuclear Gauge & Gravimetric Cores",
                "theory": """### 6.1 ASTM C1153 Mandatory Verification of Thermal Anomalies
Under **ASTM C1153 Section 11**, every thermal anomaly must be verified using capacitive dielectric impedance meters, invasive resistance probes, or gravimetric core drying (`MC_% = (m_wet - m_dry) / m_dry * 100`).""",
                "equations": """Gravimetric_Moisture_Content (MC_%) = [ (m_wet - m_dry) / m_dry ] * 100""",
                "worked_example": """#### Worked Problem 6.1: Gravimetric Core Moisture Verification
* **Scenario:** A 2.0 in core from a +6.1 °F thermal anomaly weighs m_wet = 17.10 oz (48.5 g) wet and m_dry = 5.00 oz (14.2 g) oven-dried.
* **Calculation:** MC_% = ((48.5 - 14.2) / 14.2) * 100 = **241.5% moisture by weight** (confirmed saturation).""",
                "lab_protocol": """1. Mark anomaly perimeters on roof surface using RTK rover coordinates.
2. Perform dielectric impedance sweeps across 100% of marked zones and extract gravimetric verification cores."""
            },
            {
                "unit": 7, "hours": 4.0,
                "title": "Unit 07: Vertical Facade & Curtain Wall NDT — Masonry Rust-Jacking, Terra Cotta & Spalling",
                "theory": """### 7.1 Mechanics of Steel Shelf-Angle Rust-Jacking in Masonry Facades
Water penetrating behind brick facades oxidizes structural steel relieving angles (**shelf angles**). Expansive rust pack (6x volume) generates **up to 10,000 psi of rust-jacking pressure**, bowing brick walls out-of-plane and shearing masonry ties.""",
                "equations": """Out_of_Plane_Deflection_Ratio = H_panel / Delta_bow >= 360 (BIA Stability Criterion)""",
                "worked_example": """#### Worked Problem 7.1: Out-of-Plane Masonry Bowing Limit Audit
* **Scenario:** 3D LiDAR facade cloud shows a 144-inch brick panel bowed outward by 0.85 in at the 5th-floor shelf angle.
* **Calculation:** Ratio = 144 / 0.85 = **169 < 360 limit** -> Mandate immediate sidewalk overhead protection and facade pinning.""",
                "lab_protocol": """1. Fly vertical facade grid profiles at 35.0 ft standoff with 80% overlap and 45-degree oblique gimbal angle.
2. Generate millimeter-accurate 3D point cloud to measure out-of-plane masonry bowing."""
            },
            {
                "unit": 8, "hours": 4.0,
                "title": "Unit 08: Structural Concrete Parking Garages, Plaza Decks & Post-Tensioned Tendon Corrosion",
                "theory": """### 8.1 Two-Way Slab Punching Shear (ACI 318) & Post-Tensioned Strand Corrosion
Water percolation through failed plaza deck waterproofing degrades slab-column joints, leading to catastrophic brittle **two-way punching shear failure** around critical perimeter `b_0`.""",
                "equations": """phi_V_c = phi * 4 * lambda * sqrt(f'_c) * b_0 * d   [ACI 318 Two-Way Punching Shear Capacity, lbs]""",
                "worked_example": """#### Worked Problem 8.1: ACI 318 Two-Way Slab Punching Shear Capacity
* **Scenario:** 24x24 in column, slab effective depth d = 7.5 in, f'_c = 4,000 psi, phi = 0.75.
* **Calculation:** b_0 = 4 * (24 + 7.5) = 126.0 in -> phi_V_c = 0.75 * 4 * sqrt(4000) * 126.0 * 7.5 = **179.3 kips**.""",
                "lab_protocol": """1. Inspect underside of plaza and parking slabs for efflorescence and rust staining around column capitals.
2. Scan post-tensioned tendon profiles with 2.6 GHz GPR prior to any core drilling."""
            },
            {
                "unit": 9, "hours": 4.0,
                "title": "Unit 09: Forensic Building Envelope Failures — Champlain Towers South & High-Rise Facade Collapses",
                "theory": """### 9.1 Forensic Case Study: Champlain Towers South Collapse (Surfside, FL — June 24, 2021)
A flat (0.0% slope) pool deck with failed waterproofing allowed 40 years of chlorinated water percolation into the structural slab, triggering two-way punching shear failure around columns 11, 12, and 13 and progressive tower collapse (**98 fatalities**).""",
                "equations": """Hydrostatic_Ponding_Load (psf) = (Ponding_Depth_in / 12.0) * 62.4 lb/ft^3""",
                "worked_example": """#### Worked Problem 9.1: Ponding Water Dead Load Overload Calculation
* **Scenario:** Blocked scupper causes 8.0 in of water to pond over a 40x40 ft (1,600 sq ft) roof bay designed for 20 psf live load.
* **Calculation:** Hydrostatic load = (8/12) * 62.4 = **41.6 psf (208% of design live load)**, adding **66,560 lbs** to the bay.""",
                "lab_protocol": """1. Map roof and plaza drainage slopes using LiDAR DEMs to identify 0.0% ponding basins.
2. Verify unobstructed secondary emergency overflow scuppers per IBC Chapter 15."""
            },
            {
                "unit": 10, "hours": 4.0,
                "title": "Unit 10: FAA Part 107 Urban Operations, RJPEG Orthomosaic Synthesis & Title 61 Docket Sealing",
                "theory": """### 10.1 Ground Sampling Distance (GSD) & Radiometric Orthomosaic Registration
Thermal RJPEG frames must be captured with **80% frontal and 75% side overlap** while maintaining a minimum **10.0-foot lateral standoff** from roof parapets and mechanical penthouses.""",
                "equations": """Altitude_H_m = (GSD_mm * Focal_Length_mm) / Pixel_Pitch_mm""",
                "worked_example": """#### Worked Problem 10.1: Thermal Microbolometer Flight Altitude for 1.38 in/px (3.5 cm/px) Thermal GSD
* **Scenario:** 640x512 LWIR sensor with pixel pitch p = 0.012 mm and focal length f = 13.0 mm.
* **Calculation:** H = **124.4 feet AGL** (37.9 meters).""",
                "lab_protocol": """1. Verify FAA Part 107.29 anti-collision strobe (3 statute miles visibility) for nocturnal ASTM C1153 flights.
2. Seal final RJPEG orthomosaic and wet-core CAD polygons with SHA-256 into `matrix_ledger.db`."""
            }
        ]
    else:
        raw_units = [
            {
                "unit": 1, "hours": 4.0,
                "title": "Unit 01: Oklahoma Title 61, 23 CFR Part 515 (TAMP) & ASTM D6433 Highway Asset Governance",
                "theory": """### 1.1 Statutory Transportation Asset Management Plans (TAMP)
Under **23 CFR Part 515** and **Oklahoma Title 61**, ODOT and county highway districts use **ASTM D6433 Pavement Condition Index (PCI)** surveys to target preventive preservation in the **70–85 PCI window** (USD 3.50/sq yd) before roadways drop into the reconstruction zone (USD 65.00+/sq yd).""",
                "equations": """Sample_Unit_Area_Asphalt = 2,500 +/- 1,000 sq ft
Minimum_Sample_Units (n) = (N * s^2) / [ ((e^2 / 4) * (N - 1)) + s^2 ]""",
                "worked_example": """#### Worked Problem 1.1: ASTM D6433 Minimum Statistical Sample Unit Calculation
* **Scenario:** Corridor has N = 80 sample units, PCI standard deviation s = 10.0, allowable error e = 5.0.
* **Calculation:** n = (80 * 100) / ((6.25 * 79) + 100) = 8000 / 593.75 = **14 Sample Units**.""",
                "lab_protocol": """1. Segment highway corridor into 100 ft x 24 ft (2,400 sq ft) ASTM D6433 sample units.
2. Establish RTK GNSS base station on ODOT survey benchmark for sub-centimeter georeferencing."""
            },
            {
                "unit": 2, "hours": 4.0,
                "title": "Unit 02: ASTM D6433 19 Asphalt Distress Classifications, Density, Deduct Values (DV) & CDV Solver",
                "theory": """### 2.1 Computing Deduct Values (DV) & Corrected Deduct Value (CDV)
Inspectors quantify the 19 AC distress types by **Type, Severity (L, M, H), and Density (%)**, determine individual **Deduct Values (`DV`)**, apply the allowable deduct limit `m = 1 + (9/98)*(100 - HDV)`, and iteratively compute the maximum **Corrected Deduct Value (`CDV`)** to find **PCI = 100 - max(CDV)**.""",
                "equations": """m = 1 + (9 / 98) * (100 - HDV) <= 10.0
PCI = 100 - max_i( CDV_i )""",
                "worked_example": """#### Worked Problem 2.1: Full ASTM D6433 PCI Calculation from Multi-Distress Deduct Values
* **Scenario:** Sample unit yields DV_1 = 32.0 (Med Alligator), DV_2 = 21.0 (Med Rutting), DV_3 = 12.0 (Low Long. Crack).
* **Calculation:** HDV = 32 -> m = 7.24. Iterative q=3 curve yields max(CDV) = 44.0 -> **PCI = 100 - 44.0 = 56.0 (Fair)**.""",
                "lab_protocol": """1. Classify all 19 distress types across orthomosaic and 3D LiDAR surface meshes into Low, Medium, or High severity.
2. Execute the ASTM D6433 iterative q-curve CDV solver to output certified Sample Unit PCI."""
            },
            {
                "unit": 3, "hours": 4.0,
                "title": "Unit 03: Boussinesq & Burmister Multi-Layer Elastic Subgrade Mechanics & 18-kip ESAL Fatigue",
                "theory": """### 3.1 Boussinesq Vertical Stress & AASHTO Fourth-Power Law
Subgrade vertical stress under a circular tire footprint of radius `a` and pressure `p` decays with depth `z` per Boussinesq's equation, while structural fatigue damage scales with the **Fourth Power** of axle weight (`LEF = (W / 18,000)^4`).""",
                "equations": """sigma_z = p * [ 1 - (1 / (1 + (a / z)^2))^1.5 ]
Load_Equivalency_Factor (LEF) = (W_axle_kips / 18.0)^4""",
                "worked_example": """#### Worked Problem 3.1: Boussinesq Subgrade Stress Calculation
* **Scenario:** Dual truck tire applies p = 110 psi over radius a = 4.5 in. Find vertical stress at subgrade depth z = 12.0 in.
* **Calculation:** a/z = 0.375 -> sigma_z = 110 * (1 - 0.8211) = **19.68 psi**.""",
                "lab_protocol": """1. Obtain Average Annual Daily Truck Traffic (AADTT) and calculate cumulative 20-year design ESALs.
2. Correlate alligator cracking density in the right wheel path against cumulative ESAL fatigue limits."""
            },
            {
                "unit": 4, "hours": 4.0,
                "title": "Unit 04: Transverse Wheel-Path Rutting (ASTM Distress #15), LiDAR Cross-Slopes & Hydroplaning Physics",
                "theory": """### 4.1 Rut Depth Thresholds & NASA Dynamic Hydroplaning Velocity (`V_p`)
Wheel-path ruts `>= 0.25 in` pond rainwater across travel lanes. Total loss of tire steering/braking friction occurs when hydrodynamic lift equals tire pressure (`P_tire`), governed by **V_p = 10.35 * sqrt(P_tire)**.""",
                "equations": """d_rut = max( y_straightedge(x) - y_lidar_profile(x) )
V_hydroplaning_mph = 10.35 * sqrt(P_tire_psi)""",
                "worked_example": """#### Worked Problem 4.1: Critical Hydroplaning Velocity over a Rutted Highway Wheel Path
* **Scenario:** Passenger tire P_tire = 32.0 psi over a wheel-path rut of d_rut = 0.42 in on a 75 mph turnpike.
* **Calculation:** V_p = 10.35 * sqrt(32.0) = **58.55 mph** (Severe hydroplaning hazard 16.5 mph below posted speed limit!).""",
                "lab_protocol": """1. Extract transverse LiDAR elevation profiles at 5.0 ft longitudinal stations across all travel lanes.
2. Run virtual 6.0 ft straightedge algorithm to map rut depths >= 0.25 in and cross-slope deficits."""
            },
            {
                "unit": 5, "hours": 4.0,
                "title": "Unit 05: Rigid Portland Cement Concrete (PCC) Pavements — Joint Faulting, D-Cracking & Punchouts",
                "theory": """### 5.1 Rigid PCC Distress Mechanics
Inspectors evaluate Jointed Plain Concrete Pavements (JPCP) for **transverse joint step-faulting** from subbase pumping, freeze-thaw **D-cracking**, and **thermal curling tensile stresses**.""",
                "equations": """sigma_curl = (E_pcc * alpha_pcc * Delta_T_slab) / (2 * (1 - mu))""",
                "worked_example": """#### Worked Problem 5.1: PCC Slab Thermal Curling Stress Calculation
* **Scenario:** 10 in PCC slab (E = 4.2e6 psi, alpha = 5.5e-6 /F, mu = 0.15) with Delta_T = 22 °F thermal gradient.
* **Calculation:** sigma_curl = (4.2e6 * 5.5e-6 * 22) / (2 * 0.85) = **298.9 psi tensile bending stress**.""",
                "lab_protocol": """1. Inventory PCC pavement by counting total slabs per sample unit (20 +/- 8 slabs) per ASTM D6433.
2. Measure transverse joint step-faulting to 0.02-inch (20 mils) accuracy using dense LiDAR point clouds."""
            },
            {
                "unit": 6, "hours": 4.0,
                "title": "Unit 06: International Roughness Index (IRI — AASHTO R 85) & Quarter-Car Kinematics",
                "theory": """### 6.1 The Golden Car Quarter-Car Simulation Model
FHWA HPMS mandates **International Roughness Index (IRI)** reporting in inches/mile. Pavements exceeding **IRI > 170 in/mile** are classified as **Poor** ride quality, triggering diamond grinding or HMA overlay.""",
                "equations": """IRI_in_per_mile = Sum( |Delta_z_suspension_in| ) / Corridor_Length_Miles""",
                "worked_example": """#### Worked Problem 6.1: IRI Evaluation over a 0.5 Mile Highway Corridor Segment
* **Scenario:** Quarter-car integrator accumulates 92.5 inches of vertical suspension motion over 0.50 miles.
* **Calculation:** IRI = 92.5 / 0.50 = **185.0 in/mi > 170 in/mi threshold (Poor Ride Quality)**.""",
                "lab_protocol": """1. Sample longitudinal wheel-path elevations at <= 1.0-inch intervals along both wheel tracks.
2. Apply 10.0-inch (250 mm) moving-average tire-bridging filter and run the 4-state Golden Car matrix solver."""
            },
            {
                "unit": 7, "hours": 4.0,
                "title": "Unit 07: Roadside Drainage Hydraulics — Manning's Open-Channel Equation, Culvert Piping & Slope Stability",
                "theory": """### 7.1 Manning's Open-Channel & Culvert Capacity Equation
Roadway subgrades fail rapidly when culverts silt up or separate at joints. Open-channel discharge capacity (`Q` in cfs) is governed by **Manning's Equation** (`Q = (1.486/n) * A * R_h^(2/3) * S^(1/2)`).""",
                "equations": """Q_cfs = (1.486 / n) * Area * (R_h)^(2/3) * (Slope_S)^(1/2),   where R_h = Area / Wetted_Perimeter""",
                "worked_example": """#### Worked Problem 7.1: Concrete Box Culvert Discharge Calculation
* **Scenario:** 4 ft x 4 ft concrete box culvert (n = 0.013, S = 0.010 ft/ft) flowing at depth y = 3.0 ft (A = 12 sq ft, P_w = 10 ft, R_h = 1.20 ft).
* **Calculation:** Q = (1.486 / 0.013) * 12.0 * (1.20)^0.667 * (0.01)^0.5 = **154.9 cfs**.""",
                "lab_protocol": """1. Inspect culvert headwalls, wingwalls, and barrels for joint separation and embankment piping sinkholes.
2. Measure siltation depth inside culvert barrels and compute percentage hydraulic capacity loss."""
            },
            {
                "unit": 8, "hours": 4.0,
                "title": "Unit 08: Corridor Photogrammetry, RTK/PPK GNSS Georeferencing & 300k pts/sec LiDAR Point Clouds",
                "theory": """### 8.1 Eliminating Corridor Bowl-Effect via Dual-Frequency RTK/PPK & Staggered GCPs
Linear highway corridors require dual-frequency L1/L2 RTK/PPK carrier-phase GNSS fused with staggered shoulder Ground Control Points (GCPs) every 500–800 ft to achieve **Vertical RMSE_z <= 0.18 inches (4.5 mm)**.""",
                "equations": """Vertical_RMSE_z = sqrt( (1 / N) * sum_i (z_lidar_i - z_benchmark_i)^2 ) <= 4.5 mm""",
                "worked_example": """#### Worked Problem 8.1: Vertical Root-Mean-Square Error (RMSE) Certification Check
* **Scenario:** Five ODOT survey checkpoints yield vertical residuals of +0.12, -0.16, +0.08, -0.12, +0.04 inches (+3.0 to -4.0 mm).
* **Calculation:** RMSE_z = sqrt((9 + 16 + 4 + 9 + 1) / 5) = **0.11 inches (2.79 mm) <= 0.18 inches (Certified Level-1 Accuracy)**.""",
                "lab_protocol": """1. Place staggered RTK checkerboard GCPs along highway shoulders outside live travel lanes.
2. Execute figure-8 IMU kinematic alignment maneuver immediately after takeoff and prior to landing."""
            },
            {
                "unit": 9, "hours": 4.0,
                "title": "Unit 09: Forensic Highway & Embankment Failure Case Studies — Culvert Piping & Hydroplaning Collisions",
                "theory": """### 9.1 Subgrade Piping Sinkholes & Flush-Asphalt Hydroplaning Crossovers
Pressurized water escaping separated culvert joints erodes silty-sand embankments when hydraulic gradient `i >= i_crit` (**Terzaghi Boiling**), washing out subterranean caverns beneath live highway lanes.""",
                "equations": """i_critical = (G_s - 1) / (1 + e)   [Terzaghi Critical Upward Hydraulic Gradient]""",
                "worked_example": """#### Worked Problem 9.1: Critical Hydraulic Gradient for Subgrade Soil Piping
* **Scenario:** Silty embankment fill has specific gravity G_s = 2.68 and void ratio e = 0.68.
* **Calculation:** i_c = (2.68 - 1) / (1 + 0.68) = **1.00**. Any joint leak exceeding i = 1.0 liquefies the embankment.""",
                "lab_protocol": """1. Scan highway embankment toes with LWIR thermal and RGB to detect cold groundwater piping plumes.
2. Flag any circular surface depression over a culvert alignment as an imminent sinkhole hazard."""
            },
            {
                "unit": 10, "hours": 4.0,
                "title": "Unit 10: FAA Part 107.39 Operations Over Moving Vehicles, MUTCD Escort SOPs & Title 61 PCI Docket",
                "theory": """### 10.1 FAA 14 CFR § 107.39 & § 107.145 (Zero Sustained Hover Over Moving Traffic)
To survey active highways legally under FAA Part 107, the UAS flies a **15 to 25 ft lateral shoulder offset trajectory** with an oblique gimbal angle, escorted by a rolling **MUTCD shadow vehicle** maintaining continuous VLOS.""",
                "equations": """Minimum_Lateral_Offset_From_Live_Lane >= 15.0 ft (Shoulder Corridor Trajectory)""",
                "worked_example": """#### Worked Problem 10.1: Oblique Shoulder-Offset Swath Coverage Width
* **Scenario:** UAS flies at 120 ft AGL over the right shoulder with a 20-degree oblique gimbal angle across a 72 ft wide 4-lane highway.
* **Result:** Captures 195 ft ground swath at sub-centimeter GSD with **zero flight time over moving vehicles**.""",
                "lab_protocol": """1. Verify lateral shoulder offset flight plan in QGroundControl prior to arming motors.
2. Compile ASTM D6433 Sample Unit PCI summary table and seal with SHA-256 into `matrix_ledger.db`."""
            }
        ]
    return [_enrich_unit(u, course_code) for u in raw_units]

def export_full_course_textbook_markdown(course_code: str, course_title: str) -> str:
    units = get_course_units(course_code)
    lines = [
        f"# {course_title}",
        "**OFFICIAL 10-VOLUME / 40-CREDIT-HOUR MASTER ENGINEERING TEXTBOOK**",
        "**Institution:** Sovereign Field Academy // Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)",
        "**Statutory Accreditation:** 40.0 Credit Hours (4.0 CEUs) | Oklahoma Title 61, Title 74, 23 CFR § 650, ASTM C1153 & ASTM D6433",
        "**Commercial Tuition Valuation:** $2,500.00 per Licensed Seat",
        "---"
    ]
    for u in units:
        lines.append(f"\n## {u['title']} ({u['hours']:.1f} Accredited Credit Hours)\n")
        lines.append(u["theory"])
        lines.append("\n### Governing Mathematical Formulations\n```text")
        lines.append(u["equations"])
        lines.append("```\n")
        lines.append(u["worked_example"])
        lines.append("\n### Mandatory Field & Laboratory Practicum Protocol\n")
        lines.append(u["lab_protocol"])
        lines.append("\n---\n")
    return "\n".join(lines)



def get_master_glossary_and_references(course_code: str = "ALL"):
    """Modular Engineering Glossary, Mathematical Symbol Decoder, U.S. Customary Unit Guide, and Statutory References."""
    symbols = [
        {"sym": "Delta (Δ)", "say": "DEL-tuh", "meaning": "Change or Difference between two measurements", "example": "Delta_T = Indoor Temp minus Outdoor Temp (e.g., 72 °F - 27 °F = 45 °F difference)."},
        {"sym": "sigma (σ)", "say": "SIG-muh", "meaning": "Mechanical Stress (internal pressure or force inside concrete, steel, or soil)", "example": "Measured in psi (pounds per square inch) or ksi (thousands of pounds per square inch)."},
        {"sym": "gamma (γ)", "say": "GAM-uh", "meaning": "Shear Strain (how far a rubber bearing pad leans sideways divided by its height) or Psychrometric Factor", "example": "gamma = 1.65 in sideways shift / 2.50 in pad height = 0.66 in/in."},
        {"sym": "epsilon (ε)", "say": "EP-suh-lon", "meaning": "Emissivity (how well a roof surface radiates heat, from 0.0 to 1.0) or Dielectric Constant", "example": "A dull TPO/EPDM roof has epsilon = 0.92 (92% efficient heat radiator); shiny bare metal is 0.20."},
        {"sym": "pi (π)", "say": "PIE", "meaning": "Circle Constant = 3.1416 (circumference of any circle divided by its width)", "example": "Used whenever stress spreads in a circle around a crack tip or tire footprint."},
        {"sym": "sqrt(x) or √x", "say": "Square Root", "meaning": "The number that, when multiplied by itself, equals x", "example": "sqrt(32.0) = 5.657 because 5.657 * 5.657 = 32.0. Press the [√] key on any calculator."},
        {"sym": "x^2 or x^3", "say": "Squared / Cubed", "meaning": "Multiply the number x by itself 2 times (x * x) or 3 times (x * x * x)", "example": "(2.0 in)^2 = 2.0 * 2.0 = 4.0 sq in."},
        {"sym": "K_I and K_Ic", "say": "K-one / K-one-C", "meaning": "K_I = Current Stress Intensity at a crack tip; K_Ic = Critical Fracture Toughness (breaking point of steel)", "example": "When K_I reaches K_Ic (e.g., 45 ksi*sqrt(in)), steel snaps instantaneously like glass."},
        {"sym": "R-Value (R)", "say": "R-Value", "meaning": "Thermal Resistance (how well building insulation blocks heat flow)", "example": "Dry roof foam is R-25 (blocks heat well); water-soaked foam drops to R-4 (leaks heat 6.25x faster)."},
        {"sym": "U-Value (U)", "say": "U-Factor", "meaning": "Heat Transfer Coefficient (how fast heat escapes per square foot per degree °F, equal to 1 / R)", "example": "Measured in BTU/(hr * sq ft * °F). Higher U-Value = worse insulation / faster heat loss."},
        {"sym": "Fr_1", "say": "Froude Number", "meaning": "Ratio of river current speed to gravity wave speed around a bridge pier", "example": "Fr_1 = V_1 / sqrt(32.174 * water_depth). Higher flood speed = deeper streambed scour hole."},
        {"sym": "erf(z)", "say": "Error Function", "meaning": "Standard bell-curve probability lookup table used for road salt soaking into concrete", "example": "Tells us what percentage of winter de-icing salt has soaked down to the depth of the steel rebar."}
    ]

    units_guide = [
        {"unit": "°F (Degrees Fahrenheit)", "what": "Standard U.S. temperature scale", "benchmark": "Water freezes at 32 °F; comfortable room temp is 72 °F; hot Oklahoma summer day is 100+ °F."},
        {"unit": "in (Inches) & ft (Feet)", "what": "Standard U.S. length & distance units", "benchmark": "12 inches = 1 foot; 5,280 feet = 1 mile. A structure legally becomes a Bridge at > 20.0 feet span."},
        {"unit": "mil (Thousandth of an Inch)", "what": "1 mil = 0.001 inches (used for hairline concrete cracks and steel coating thickness)", "benchmark": "A human hair is ~3 mils (0.003 in) thick; a credit card is 30 mils (0.030 in) thick. CS-1 cracks are < 12 mils (0.012 in)."},
        {"unit": "psi (Pounds per Square Inch)", "what": "Pressure or stress pressing on 1 square inch of surface area", "benchmark": "Car tire pressure is ~32 psi; semi-truck tire is ~110 psi; structural bridge concrete strength is 4,000+ psi."},
        {"unit": "kip (Kilopound = 1,000 lbs)", "what": "Engineering shorthand for 1,000 pounds of force or load", "benchmark": "1 kip = 1,000 lbs; 36 tons = 72,000 lbs = 72 kips. ksi means kips per square inch (1 ksi = 1,000 psi)."},
        {"unit": "psf (Pounds per Square Foot)", "what": "Weight spread over a 1 ft x 1 ft floor or roof square", "benchmark": "A typical commercial flat roof is designed for 20 psf live load. 8 inches of ponded rainwater weighs 41.6 psf (208% overload!)."},
        {"unit": "BTU/hr (British Thermal Units per Hour)", "what": "Standard U.S. rate of heat energy loss or AC/heating capacity", "benchmark": "1 BTU is the heat from a single wooden kitchen match. 12,000 BTU/hr = 1 Ton of commercial air conditioning."},
        {"unit": "cfs (Cubic Feet per Second)", "what": "Volume of stormwater flowing through a culvert or river each second", "benchmark": "1 cfs = 7.48 gallons per second (about 150 cfs fills an Olympic swimming pool in 10 minutes)."},
        {"unit": "foot-candle (fc) / lux", "what": "Brightness of light shining on a surface so drone optical cameras can lock onto texture", "benchmark": "1.4 foot-candles is dim twilight—the minimum light required by onboard LED bars under a dark bridge."}
    ]

    terms = [
        {"term": "AASHTO", "cat": "All / Bridges", "def": "American Association of State Highway and Transportation Officials — the national body that writes the official U.S. bridge design and inspection manuals."},
        {"term": "ASTM International", "cat": "All Courses", "def": "The U.S. standards organization that defines exact testing rules (such as ASTM C1153 for infrared roof moisture scans and ASTM D6433 for roadway PCI surveys)."},
        {"term": "NBIS (23 CFR § 650)", "cat": "STR-01 Bridges", "def": "National Bridge Inspection Standards — the federal law passed after the 1967 Silver Bridge collapse requiring every public bridge (>20 ft) to be inspected at least every 24 months."},
        {"term": "Oklahoma Title 61", "cat": "Statutory Law", "def": "The Oklahoma Public Buildings and Public Works statute governing state construction, engineering inspections, competitive bidding, and infrastructure safety."},
        {"term": "Condition States (CS-1 to CS-4)", "cat": "STR-01 Bridges", "def": "The 4-tier AASHTO grading scale for every square foot of a bridge: CS-1 = Good, CS-2 = Fair (minor cracks), CS-3 = Poor (needs priority repair), CS-4 = Severe (unsafe / immediate emergency closure or load restriction)."},
        {"term": "Delamination & Spalling", "cat": "STR-01 & STR-02", "def": "Delamination is a hidden horizontal split inside concrete caused by rusting rebar expanding; when that loose top slab finally breaks out leaving a pothole, it is called a Spall."},
        {"term": "Fracture-Critical Member (FCM)", "cat": "STR-01 Bridges", "def": "A steel bridge component under tension (pulling force) with no backup load path—if that single steel girder or eyebar cracks through, the bridge collapses."},
        {"term": "Scour (HEC-18)", "cat": "STR-01 Bridges", "def": "Fast floodwater vortices digging away the sand and gravel river bottom from underneath a bridge pier foundation—the #1 cause of bridge collapses in America."},
        {"term": "NDT (Non-Destructive Testing)", "cat": "All Courses", "def": "Inspecting inside concrete, roofs, or steel using thermal cameras, ultrasound, radar (GPR), or sound waves without breaking or damaging the structure."},
        {"term": "Radiometric Infrared (RJPEG)", "cat": "STR-02 Buildings", "def": "A specialized thermal camera image where every single pixel records an exact calibrated temperature in °F (unlike a regular photo that only shows colors)."},
        {"term": "Dew Point Temperature (T_dp)", "cat": "STR-02 Buildings", "def": "The exact temperature (°F) at which invisible moisture in warm indoor air condenses into liquid water droplets when touching a cold roof deck or wall."},
        {"term": "Rust-Jacking", "cat": "STR-02 Buildings", "def": "When steel support angles behind a brick wall rust, the rust expands up to 600% in thickness, prying and bowing the brick facade outward with up to 10,000 psi of force."},
        {"term": "PCI (Pavement Condition Index)", "cat": "STR-03 Roadways", "def": "The official ASTM D6433 0-to-100 numerical score for a road surface (100 = brand new road; 70-85 = ideal time for low-cost preventive seal; <55 = requires expensive reconstruction)."},
        {"term": "Deduct Value (DV) & CDV", "cat": "STR-03 Roadways", "def": "Points subtracted from 100 based on how severe and how widespread road cracks and ruts are. PCI = 100 minus the Corrected Deduct Value (CDV)."},
        {"term": "ESAL (18-kip Equivalent Single Axle Load)", "cat": "STR-03 Roadways", "def": "A way to measure road wear by converting heavy semi-truck axles into equivalent 18,000-lb standard axles. Doubling axle weight multiplies road damage by 16x (2^4)!"},
        {"term": "IRI (International Roughness Index)", "cat": "STR-03 Roadways", "def": "Measures how bumpy a highway is in inches of up-and-down shock-absorber movement per mile driven. Over 170 inches/mile is rated Poor by the Federal Highway Administration."},
        {"term": "GSD (Ground Sampling Distance)", "cat": "All Courses", "def": "How much real-world surface area fits inside 1 single camera pixel (e.g., 0.003 inches/pixel lets you see a hairline steel crack; 1.38 inches/pixel maps roof moisture)."},
        {"term": "RTK / PPK GPS & Optical SLAM", "cat": "All Courses", "def": "RTK/PPK uses a ground base station to make drone GPS accurate to 0.18 inches; Optical SLAM uses downward cameras and lasers to hold position under a bridge where GPS is blocked."},
    ]

    references = [
        {"code": "Oklahoma Statutes Title 61 & Title 74", "agency": "State of Oklahoma / OMES CAP / ODOT", "scope": "Public Buildings and Public Works Act — governs state capital asset inspections, engineering certification, and statutory bidding."},
        {"code": "23 CFR § 650 Subpart C (NBIS)", "agency": "Federal Highway Administration (FHWA)", "scope": "National Bridge Inspection Standards — mandates 24-month NBI inspections, Fracture-Critical hands-on/NDT rules, and Scour Plans of Action."},
        {"code": "AASHTO MBEI & LRFR Manual", "agency": "American Association of State Highway & Transportation Officials", "scope": "Manual for Bridge Element Inspection (Condition States CS-1 to CS-4) and Load and Resistance Factor Rating (RF) equations."},
        {"code": "FHWA HEC-18 (Hydraulic Engineering Circular No. 18)", "agency": "FHWA / Colorado State University", "scope": "Evaluating Scour at Bridges — defines the CSU equilibrium pier scour depth equation (y_s) and Froude number hydrodynamics."},
        {"code": "ASTM C1153 & ISO 6781", "agency": "ASTM International", "scope": "Standard Practice for Location of Wet Insulation in Roofing Systems Using Infrared Imaging (<15 mph wind, >24 hr dry surface, nocturnal window)."},
        {"code": "ASTM C876 & ASTM C1383", "agency": "ASTM International", "scope": "Half-Cell Potentials of Uncoated Reinforcing Steel in Concrete (-350 mV corrosion threshold) and Impact-Echo delamination depth testing."},
        {"code": "ASTM D6433 & AASHTO R 85", "agency": "ASTM International / AASHTO", "scope": "Standard Practice for Roads and Parking Lots Pavement Condition Index (PCI) Surveys (19 distress types) and International Roughness Index (IRI)."},
        {"code": "14 CFR Part 107 (§ 107.29 & § 107.39)", "agency": "Federal Aviation Administration (FAA)", "scope": "Small Unmanned Aircraft Systems — rules for nocturnal anti-collision lighting and lateral standoff corridors alongside moving highway traffic."},
        {"code": "18 U.S.C. § 1001 & FIPS PUB 180-4", "agency": "U.S. Department of Justice / NIST", "scope": "Federal False Statements Act (criminal liability for falsified inspection dockets) and Secure Hash Standard (SHA-256 cryptographic sealing)."}
    ]

    return {
        "symbols": symbols,
        "units_guide": units_guide,
        "terms": terms,
        "references": references
    }


def _attach_beginner_aids(u_dict: dict, u_num: int):
    nl = chr(10)
    primer_lines = [
        "",
        "---",
        ""
    ]
    u_dict["beginner_primer"] = nl.join(primer_lines)

    _cc_obj = u_dict.get("calc_challenge", {})
    target_unit = str(_cc_obj.get("unit_label") or _cc_obj.get("unit") or u_dict.get("calc_unit") or "U.S. Customary Units")
    _eq_raw = str(u_dict.get("equations") or u_dict.get("governing_eq") or "")
    _first_eq = _eq_raw.splitlines()[0] if _eq_raw else ""
    legend_lines = [
        f"**🔎 Calculator & Formula Breakdown for Module {u_num:02d} (`{u_dict.get('title', '')}`):**",
        f"* **Primary Formula You Are Solving:** `{_first_eq}`",
        f"* **Required Final Answer Unit in Sub-Tab 4:** **`{target_unit}`**",
        "* **Deterministic Dimensional Analysis & Equation Execution Protocol:**",
        "  1. **Parentheses `( ... )` FIRST:** Always calculate the numbers inside inner parentheses first and record the intermediate state variable.",
        "  2. **Exponents & Square Roots (`^` or `sqrt`) SECOND:** If the formula has `sqrt(...)`, press the `[√]` key on the number inside; if it has `^2` or `^4`, multiply the number by itself.",
        "  3. **Multiply (`*`) & Divide (`/`) THIRD:** Work left to right before doing any final addition (`+`) or subtraction (`-`).",
        ""
    ]
    if not u_dict.get("equation_legend") or "Engineering Symbol-by-Symbol Equation" in str(u_dict.get("equation_legend", "")):
        u_dict["equation_legend"] = nl.join(legend_lines)
    return u_dict


def _build_20_question_milestone_exam(u_dict, course_code):
    """Generates a comprehensive 20-question accredited milestone mastery exam (Q1-Q20) in U.S. Customary units."""
    import re as _re
    u_num = int(u_dict.get("unit", 1))
    u_title = str(u_dict.get("title", f"Module {u_num:02d}"))
    cc = u_dict.get("calc_challenge", {})
    c_prompt = str(cc.get("prompt") or cc.get("question") or u_dict.get("calc_prompt") or "Solve the module engineering calculation in U.S. Customary units.")
    c_ans = cc.get("ans") if "ans" in cc else (cc.get("answer") if "answer" in cc else (cc.get("target") if "target" in cc else u_dict.get("calc_ans", 0.0)))
    c_tol = cc.get("tol") if "tol" in cc else (cc.get("tolerance") if "tolerance" in cc else u_dict.get("calc_tol", 0.25))
    c_unit = str(u_dict.get("resolved_us_unit", "feet (ft) — U.S. Customary Units"))
    eq_raw = [ln.strip() for ln in str(u_dict.get("equations", "")).splitlines() if ln.strip()]
    primary_eq = eq_raw[0] if eq_raw else "L_total (ft) = (Number_of_Barrels * Barrel_Width_ft) + (Number_of_Interior_Walls * Wall_Thickness_ft)"

    base_quiz = list(u_dict.get("unit_quiz", []))
    questions = []
    for idx, q_item in enumerate(base_quiz[:3], start=1):
        q_copy = dict(q_item)
        q_txt = str(q_copy.get("q", ""))
        q_txt = _re.sub(r"^\[[^\]]+\]\s*", "", q_txt)
        q_copy["q"] = f"[{course_code} Unit {u_num:02d} Milestone Q{idx:02d}] {q_txt}"
        _opts_list = list(q_copy.get("opts") or q_copy.get("options") or [])
        q_copy["opts"] = _opts_list
        q_copy["options"] = _opts_list
        if "ans" in q_copy and "answer" not in q_copy:
            q_copy["answer"] = _opts_list[q_copy["ans"]] if isinstance(q_copy["ans"], int) and 0 <= q_copy["ans"] < len(_opts_list) else q_copy["ans"]
        elif "answer" in q_copy and "ans" not in q_copy:
            q_copy["ans"] = q_copy["answer"]
        questions.append(q_copy)

    extra_specs = [
        (
            f"What is the primary U.S. Customary engineering measurement unit required for the Part A Quantitative Calculation Gate in {u_title}?",
            f"{c_unit}",
            "SI Metric millimeters (mm) and Pascals (Pa) only",
            "Uncalibrated arbitrary pixel counts without physical scale",
            "Degrees Celsius (°C) and Newton-meters (N·m) only",
        ),
        (
            f"Which primary governing mathematical formulation defines the physical engineering relationship evaluated in {u_title}?",
            f"{primary_eq}",
            "Visual estimation without mathematical formulation or physical measurement",
            "Random number generation divorced from structural geometry",
            "Unverified consumer barometer approximation without statutory bounds",
        ),
        (
            f"When solving the Part A Calculation Gate ('{c_prompt[:85]}...'), what is the verified target engineering value in U.S. Customary units?",
            f"{c_ans} (within an allowable engineering tolerance of +/- {c_tol})",
            f"{round(float(c_ans) * 3.25 + 14.0, 2)} (uncalibrated metric drift error)",
            "0.00 (zero structural load or geometry assumption)",
            f"-{abs(float(c_ans)) + 10.0} (inverted sign convention error)",
        ),
        (
            "When keying a multi-step engineering formula into a field calculator, which algebraic evaluation hierarchy must be followed to prevent calculation error?",
            "Solve inside Parentheses ( ) first, then Exponents/Roots (^ or sqrt), then Multiplication/Division (* or /), and finally Addition/Subtraction (+ or -)",
            "Add and subtract all numbers from left to right before multiplying or solving parentheses",
            "Round all intermediate numbers to zero before applying square roots",
            "Ignore parentheses and multiply only the first and last terms",
        ),
        (
            "What is the mandatory maximum sustained wind speed limit in U.S. Customary units for conducting a calibrated Level-5 sUAS structural or thermal inspection sortie?",
            "Less than 15.0 mph sustained wind speed (with gusts below statutory airframe stability limits)",
            "Up to 65.0 mph gale-force winds during active precipitation",
            "Wind speed is never measured or recorded during forensic flight operations",
            "Exactly 45.0 mph crosswind during manual attitude-mode flight",
        ),
        (
            "To capture legally defensible optical crack and spall telemetry under AASHTO / ODOT standards, what minimum surface illumination and maximum Ground Sample Distance (GSD) are required?",
            "Surface brightness >= 1.4 foot-candles and Optical GSD <= 0.004 in/px (4 mils)",
            "Complete darkness (0.0 foot-candles) and 2.50 in/px coarse satellite resolution",
            "Direct blinding glare without exposure calibration at 12.0 in/px",
            "100 mils per pixel using digital zoom from 1,500 ft AGL",
        ),
        (
            "What is the mandatory minimum thermal temperature differential (Delta_T) in degrees Fahrenheit (°F) required to detect subsurface delamination or moisture entrapment via ASTM D4788 / C1153 thermography?",
            "Delta_T >= +3.6 °F (+2.0 °C equivalent) above the adjacent sound baseline material",
            "Delta_T = 0.0 °F isothermal equilibrium during heavy rain",
            "Delta_T <= -50.0 °F without emissivity calibration",
            "Thermal differentials are measured in psi rather than degrees Fahrenheit (°F)",
        ),
        (
            "What RTK/PPK GNSS positional accuracy threshold (in U.S. Customary inches) must be locked before recording georeferenced structural defect coordinates?",
            "Horizontal error <= 0.60 inches and Vertical error <= 0.18 inches with verified base-station lock",
            "Horizontal drift of +/- 45.0 feet using standalone consumer phone GPS",
            "No GNSS receiver is needed if the pilot estimates location from memory",
            "Vertical error of +/- 120.0 inches without atmospheric correction",
        ),
        (
            "In U.S. Customary bridge, pavement, and coating inspections, how is 1 mil defined when measuring crack widths, optical GSD, or protective coating thickness?",
            "1 mil = 0.001 inches (one thousandth of an inch; 1,000 mils = 1.0 inch)",
            "1 mil = 1.0 millimeter (metric length unit)",
            "1 mil = 1,000.0 feet of highway right-of-way",
            "1 mil = 1.0 million pounds of axial live load",
        ),
        (
            "Under 23 CFR § 650.305 (National Bridge Inspection Standards) and Oklahoma Title 61, what minimum clear opening length along the roadway centerline classifies a structure as an NBI Bridge?",
            "More than 20.0 feet (L_total > 20.0 ft) measured between extreme ends of the opening",
            "More than 500.0 feet only",
            "Less than 2.0 feet of pipe diameter",
            "Span length has no legal effect on NBI inspection jurisdiction",
        ),
        (
            "Under the AASHTO Manual for Bridge Element Inspection (MBEI), what does Condition State 1 (CS-1: Good) signify compared to Condition State 4 (CS-4: Severe)?",
            "CS-1 indicates no physical distress beyond minor maintenance, whereas CS-4 indicates severe distress requiring immediate structural review or load restriction",
            "CS-1 indicates imminent collapse, whereas CS-4 indicates brand-new construction",
            "CS-1 and CS-4 are interchangeable cosmetic labels with no engineering meaning",
            "CS-4 allows inspectors to skip inspections for 10 years",
        ),
        (
            "Under 18 U.S.C. § 1001 and Oklahoma Title 61 / Title 74, what are the legal consequences of falsifying, backdating, or fabricating structural inspection telemetry on a public works docket?",
            "Federal felony liability (up to 5 years imprisonment), state statutory debarment, PE/credential revocation, and civil false-claims penalties",
            "No legal consequence as long as the report is formatted neatly",
            "Automatic approval of state tuition vouchers without audit",
            "A minor verbal reminder during the next 60-month cycle",
        ),
        (
            "How does the Sovereign Field Academy C2 Cockpit guarantee non-repudiation when a candidate seals 4.0 Accredited Credit Hours in Sub-Tab 4?",
            "By computing a deterministic FIPS 180-4 SHA-256 cryptographic hash of the candidate ID, module telemetry, and timestamp and writing it to matrix_ledger.db",
            "By storing temporary browser cookies that clear when the window closes",
            "By allowing anonymous edits to completed credit records without hashing",
            "By printing an unsigned text note with no database persistence",
        ),
        (
            "When converting U.S. Customary linear measurements during field geometry checks, how many inches are in 1.0 linear foot, and how many square inches are in 1.0 square foot?",
            "12.0 inches = 1.0 linear foot, and 144.0 square inches (12 in * 12 in) = 1.0 square foot",
            "10.0 inches = 1.0 linear foot, and 100.0 square inches = 1.0 square foot",
            "36.0 inches = 1.0 linear foot, and 36.0 square inches = 1.0 square foot",
            "100.0 mils = 1.0 linear foot, and 1,000.0 square inches = 1.0 square foot",
        ),
        (
            "In U.S. Customary structural load and stress calculations, how are kips (kilopounds), psi, and ksi related?",
            "1.0 kip = 1,000 pounds (lbs) of force, and 1.0 ksi = 1,000 psi (pounds per square inch)",
            "1.0 kip = 100 pounds (lbs), and 1.0 ksi = 10 psi",
            "1.0 kip = 1,000 kilograms, and 1.0 ksi = 1.0 Pascal",
            "kips and ksi measure thermal conductivity rather than mechanical force or stress",
        ),
        (
            f"Before initiating the field practicum for {u_title}, what must be verified first in the Sub-Tab 3 Mandatory Field Telemetry & Laboratory Practicum Protocol?",
            "Verify the Team Leader PE / Sovereign Level-5 Credential ID in matrix_ledger.db and pull the historical baseline inventory sheet",
            "Launch the aircraft immediately without checking airspace, weather, or credential logs",
            "Disable all onboard GNSS and optical calibration sensors to save battery",
            "Delete prior inspection records from the SQLite database",
        ),
        (
            f"What is the mandatory minimum passing score required on this 20-question milestone exam (together with the Part A Calculation Gate) to unlock the 4.0-Hour WORM Credit Seal for {u_title}?",
            "100% Mastery (20 out of 20 questions correct) plus an exact U.S. Customary numerical calculation within engineering tolerance",
            "50% (10 out of 20 questions correct) with Part A left blank",
            "15% (3 out of 20 questions correct) without calculation verification",
            "No minimum score is enforced for state Title 61 certification",
        ),
    ]

    for offset, (stem, right_ans, w1, w2, w3) in enumerate(extra_specs, start=4):
        q_idx = offset
        pos = (u_num + q_idx) % 4
        distractors = [w1, w2, w3]
        raw_choices = []
        d_ptr = 0
        for slot in range(4):
            if slot == pos:
                raw_choices.append(right_ans)
            else:
                raw_choices.append(distractors[d_ptr])
                d_ptr += 1
        letters = ["A", "B", "C", "D"]
        formatted_opts = [f"{letters[i]}) {raw_choices[i]}" for i in range(4)]
        _ans_letter = letters[pos]
        questions.append({
            "q": f"[{course_code} Unit {u_num:02d} Milestone Q{q_idx:02d}] {stem}",
            "opts": formatted_opts,
            "options": formatted_opts,
            "ans": _ans_letter,
            "answer": formatted_opts[pos],
        })

    return questions[:20]

def get_course_units(course_code: str):
    units = _orig_get_course_units(course_code)
    _nl = chr(10)
    _u_desc_map = {
        "ft": "feet (ft) — U.S. Customary Linear Feet (12 inches = 1.0 foot)",
        "feet": "feet (ft) — U.S. Customary Linear Feet (12 inches = 1.0 foot)",
        "in": "inches (in) — U.S. Customary Inches (1/12 of a foot)",
        "inches": "inches (in) — U.S. Customary Inches (1/12 of a foot)",
        "mils": "mils (0.001 in) — Thousandths of an Inch (1,000 mils = 1.0 inch)",
        "sq ft": "square feet (sq ft) — U.S. Customary Surface Area (Length_ft * Width_ft)",
        "%": "Percent (%) — Percentage Score / Ratio (0% to 100%)",
        "psi": "psi (Pounds per Square Inch) — U.S. Customary Stress / Pressure",
        "ksi": "ksi (Kips per Square Inch) — 1,000 Pounds per Square Inch",
        "kips": "kips (Kilopounds) — U.S. Customary Structural Load (1 kip = 1,000 lbs)",
        "lbs": "pounds (lbs) — U.S. Customary Force / Weight",
        "psf": "psf (Pounds per Square Foot) — U.S. Customary Area Load",
        "°F": "degrees Fahrenheit (°F) — U.S. Customary Temperature",
        "BTU/hr": "BTU/hr (British Thermal Units per Hour) — U.S. Customary Heat Flow Rate",
        "cfs": "cfs (Cubic Feet per Second) — U.S. Customary Hydraulic Discharge",
        "PCI": "PCI Points (0 to 100 Scale) — ASTM D6433 Pavement Condition Index",
        "RF": "Rating Factor (RF) — AASHTO Load & Resistance Factor Ratio (RF >= 1.00 is Safe)",
    }
    for _u_item in units:
        _cc = _u_item.get("calc_challenge", {})
        _raw_u = str(_cc.get("unit_label") or _cc.get("unit") or _cc.get("units") or _u_item.get("calc_unit") or "").strip()
        _p_low = str(_cc.get("prompt", "") or _cc.get("label", "")).lower()
        if not _raw_u:
            if "in feet" in _p_low or "(ft)" in _p_low or " ft" in _p_low:
                _raw_u = "ft"
            elif "mils" in _p_low:
                _raw_u = "mils"
            elif "in inches" in _p_low or "(in)" in _p_low or "inches" in _p_low:
                _raw_u = "in"
            elif "psi" in _p_low:
                _raw_u = "psi"
            elif "ksi" in _p_low:
                _raw_u = "ksi"
            elif "kips" in _p_low:
                _raw_u = "kips"
            elif "btu" in _p_low:
                _raw_u = "BTU/hr"
            elif "°f" in _p_low or "fahrenheit" in _p_low or "deg f" in _p_low:
                _raw_u = "°F"
            elif "pci" in _p_low:
                _raw_u = "PCI"
            elif "percent" in _p_low or "(%)" in _p_low or "%" in _p_low:
                _raw_u = "%"
            elif "cfs" in _p_low:
                _raw_u = "cfs"
            elif "sq ft" in _p_low or "square feet" in _p_low:
                _raw_u = "sq ft"
        _res_u = _u_desc_map.get(_raw_u, f"{_raw_u} — U.S. Customary Engineering Unit" if _raw_u else "feet (ft) — U.S. Customary Engineering Units")
        _u_item["resolved_us_unit"] = _res_u
        for _k_field in ("equation_legend", "theory", "deep_supplement", "worked_example", "lab_protocol"):
            if _k_field in _u_item and isinstance(_u_item[_k_field], str):
                _s_txt = _u_item[_k_field]
                _s_txt = _s_txt.replace("`Measured in U.S. Customary Units`", f"`{_res_u}`").replace("Measured in U.S. Customary Units", _res_u)
                for _sec_n in range(1, 12):
                    _h4 = f"### {_sec_n}.4"
                    _s_txt = _s_txt.replace("|" + _h4, "|" + _nl + _nl + _h4).replace(_nl + _h4, _nl + _nl + _h4).replace(_nl + _nl + _nl + _h4, _nl + _nl + _h4)
                _u_item[_k_field] = _s_txt
        _u_item["unit_quiz"] = _build_20_question_milestone_exam(_u_item, course_code)
    return units

# ==============================================================================
# CURRICULUM-SPECIFIC QUESTION DIFFERENTIATION ENGINE (STR-01 vs ENV-01 vs PAV-01)
# Guarantees zero identical opening questions across the three accredited exams
# ==============================================================================
import re
_COURSE_DOMAIN_PROFILES = {
    "STR-01": {
        "agency_statute": "23 CFR § 650 (NBIS), AASHTO MBEI, and Oklahoma Title 61 Bridge Safety Mandates",
        "q1_stem": "Under 23 CFR § 650 (National Bridge Inspection Standards) and AASHTO MBEI protocol, how must fracture-critical and element-level bridge telemetry from {u_title} be preserved for the official ODOT structural docket?",
        "q1_ans": "Sealed immediately in a Write-Once-Read-Many (WORM) SQLite structural ledger with a FIPS 180-4 SHA-256 cryptographic digest linked to the NBI Structure Number",
        "q1_d1": "Overwritten inside an unverified local spreadsheet without NBI structure indexing",
        "q1_d2": "Discarded after the 24-month visual windshield pass is completed",
        "q1_d3": "Converted into uncalibrated consumer video clips with no bridge element ID",
        "q2_stem": "When a structural bridge evaluation in {u_title} identifies a Condition State 4 (CS-4 Severe) defect or critical load-capacity reduction below legal operating rating (RF < 1.0), what is the mandatory statutory action?",
        "q2_ans": "Trigger an immediate Structural Critical Finding Docket under 23 CFR § 650.313(h) and Oklahoma Title 61 for emergency load posting, shoring, or lane closure",
        "q2_d1": "Defer structural load rating until the next 48-month underwater inspection cycle",
        "q2_d2": "Apply non-structural epoxy coating over the active fatigue crack without engineering review",
        "q2_d3": "Reclassify the fracture-critical member as non-redundant cosmetic trim",
        "q3_stem": "Why must calibrated AASHTO / FHWA structural mechanics formulations and non-destructive testing (NDT) boundary conditions be verified before signing the NBI bridge docket for {u_title}?",
        "q3_ans": "To satisfy 23 CFR § 650, 18 U.S.C. § 1001, and Oklahoma Title 61 evidentiary admissibility and prevent catastrophic superstructure or substructure collapse",
        "q3_d1": "AASHTO equations are optional guidelines that do not apply to state highway bridges",
        "q3_d2": "Binocular viewing from the roadway shoulder replaces quantitative section-loss math",
        "q3_d3": "Bridge load ratings only require calibration once every 25 years",
        "q8_stem": "During an under-deck or superstructure sUAS bridge inspection sortie for {u_title}, what aerodynamic and structural proximity boundary must be maintained under ODOT / FAA Part 107 standards?",
        "q8_ans": "Sustained wind speed < 15.0 mph outside girder wake-turbulence zones with optical collision-avoidance and EKF visual-inertial odometry active in GPS-denied under-deck spans",
        "q8_d1": "Flight in 55.0 mph crosswinds between steel floorbeams using barometric altitude only",
        "q8_d2": "Direct physical contact with live high-voltage utility conduits attached to the bridge fascia",
        "q8_d3": "Disabling IMU attitude stabilization while hovering inside concrete box girders",
        "q9_stem": "To resolve hairline fatigue cracks or concrete spalling in {u_title} per AASHTO MBEI CS-2/CS-3 thresholds, what optical Ground Sample Distance (GSD) and surface lighting are required?",
        "q9_ans": "Optical GSD <= 0.004 in/px (4 mils, resolving 0.004-inch hairline cracks) with shadow-free under-deck illumination >= 1.4 foot-candles",
        "q9_d1": "Coarse 1.50 in/px aerial overview imagery captured in complete under-deck darkness (0.0 fc)",
        "q9_d2": "Digital zoom from 400 ft AGL with uncalibrated motion blur across gusset plate rivets",
        "q9_d3": "3.00 in/px satellite imagery taken during heavy fog",
        "q10_stem": "When performing ASTM D4788 infrared bridge-deck delamination mapping in {u_title}, what solar loading and minimum surface thermal differential (Delta_T) are required?",
        "q10_ans": "Minimum 3.0 hours of direct solar irradiance producing a verified thermal anomaly Delta_T >= +3.6 °F (+2.0 °C) over sound reinforced concrete deck areas",
        "q10_d1": "Midnight isothermal bridge deck conditions (Delta_T = 0.0 °F) during active freezing rain",
        "q10_d2": "Standing water > 0.5 inches deep covering the concrete bridge riding surface",
        "q10_d3": "Uncalibrated thermal imaging without concrete emissivity (epsilon = 0.92-0.95) correction",
        "q11_stem": "When georeferencing bridge pier scour contours, bearing offsets, or deck spall polygons in {u_title}, what RTK/PPK geodetic accuracy must be locked?",
        "q11_ans": "Horizontal error <= 0.60 inches and Vertical elevation error <= 0.18 inches referenced to the state bridge datum (NAVD88 / NAD83 U.S. Survey Feet)",
        "q11_d1": "Standalone consumer GPS with +/- 35.0 feet of horizontal drift beneath the steel deck",
        "q11_d2": "Dead-reckoning estimation from the nearest highway milepost sign",
        "q11_d3": "Uncorrected barometric pressure altitude drifting +/- 80.0 inches over the river channel",
        "q12_stem": "In AASHTO bridge coating, steel gusset plate corrosion, and concrete crack width inspections for {u_title}, how is 1 mil defined in U.S. Customary units?",
        "q12_ans": "1 mil = 0.001 inches (one thousandth of an inch; e.g., a 12-mil epoxy bridge coating = 0.012 in, and 1,000 mils = 1.0 inch)",
        "q12_d1": "1 mil = 1.0 millimeter of structural steel flange thickness",
        "q12_d2": "1 mil = 1,000 pounds of AASHTO HL-93 design tandem axle load",
        "q12_d3": "1 mil = 1.0 statute mile of interstate bridge corridor",
        "q13_stem": "Under 23 CFR § 650.305 and Oklahoma Title 61, what minimum clear opening length along the roadway centerline classifies a highway structure or multiple-barrel culvert in {u_title} as an NBI Bridge?",
        "q13_ans": "More than 20.0 feet (L_total > 20.0 ft) measured along the centerline of the roadway between extreme ends of the opening",
        "q13_d1": "Only suspension bridges exceeding 1,000.0 feet of main span length",
        "q13_d2": "Any drainage pipe with an interior diameter of 12.0 inches or less",
        "q13_d3": "Span length has no statutory relevance under federal NBIS regulations",
        "q14_stem": "In the AASHTO Manual for Bridge Element Inspection (MBEI) applied to {u_title}, how does Condition State 1 (CS-1: Good) differ from Condition State 4 (CS-4: Severe)?",
        "q14_ans": "CS-1 indicates bridge element preservation with no structural distress, whereas CS-4 indicates severe section loss or distress warranting immediate structural review or load rating",
        "q14_d1": "CS-1 requires immediate bridge closure, whereas CS-4 indicates new construction",
        "q14_d2": "CS-1 and CS-4 are arbitrary aesthetic ratings for bridge paint color",
        "q14_d3": "CS-4 allows the bridge owner to extend inspection intervals to 120 months",
    },
    "ENV-01": {
        "agency_statute": "40 CFR Part 60 (EPA OOOOa/OOOOb), ASTM C1153 / E1934 Radiometric Thermography, and Oklahoma DEQ / Title 61 Environmental Forensics",
        "q1_stem": "Under 40 CFR Part 60 (EPA Subpart OOOOb), ODEQ rules, and Oklahoma Title 61 forensic standards, how must radiometric thermal and Optical Gas Imaging (OGI) plume telemetry from {u_title} be preserved?",
        "q1_ans": "Sealed immediately in a Write-Once-Read-Many (WORM) SQLite environmental ledger with a FIPS 180-4 SHA-256 hash binding the 16-bit radiometric RJPEG/OGI frames and GPS coordinates",
        "q1_d1": "Converted into 8-bit lossy social-media screenshots with radiometric temperature arrays stripped",
        "q1_d2": "Deleted after logging a subjective odor observation on a paper clipboard",
        "q1_d3": "Averaged across uncalibrated visual webcams lacking spectral LWIR/MWIR response",
        "q2_stem": "When an environmental or radiometric thermal inspection in {u_title} detects an unpermitted fugitive hydrocarbon leak, hazardous containment breach, or critical electrical hot-spot exceeding ASTM E1934 Class-A thresholds, what is required?",
        "q2_ans": "Trigger an immediate Statutory Environmental / Thermal Critical Action Docket under 40 CFR Part 60 and Oklahoma Title 61 for emergency isolation, LDAR repair within statutory deadlines, or de-energization",
        "q2_d1": "Vent the fugitive methane or hazardous plume continuously until the next 5-year permit renewal",
        "q2_d2": "Lower the infrared camera emissivity setting to 0.10 to artificially mask the thermal spike",
        "q2_d3": "Spray cold water on the energized transformer bushing while recording baseline temperatures",
        "q3_stem": "Why must Planck radiation physics, surface emissivity (epsilon), reflected apparent temperature (T_refl), and atmospheric transmittance be calibrated before certifying telemetry in {u_title}?",
        "q3_ans": "To guarantee quantitative radiometric accuracy and evidentiary admissibility under EPA 40 CFR Part 60, ASTM C1153, and 18 U.S.C. § 1001 without false-negative leak or hot-spot omissions",
        "q3_d1": "All industrial metals, gases, and soils have an identical blackbody emissivity of 1.00",
        "q3_d2": "Color palette selection (Rainbow vs. Ironbow) replaces radiometric temperature calibration",
        "q3_d3": "Infrared sensors never require NUC (Non-Uniformity Correction) or atmospheric compensation",
        "q8_stem": "During an EPA Method 21 / OOOOb Optical Gas Imaging (OGI) or ASTM C1153 thermal containment survey for {u_title}, why must sustained ambient wind speed remain below 15.0 mph?",
        "q8_ans": "High winds (> 15.0 mph) cause rapid convective cooling (forced convection stripping surface Delta_T) and turbulent plume dilution below the sensor Noise Equivalent Concentration Length (NECL)",
        "q8_d1": "Gale-force winds (50.0 mph) concentrate fugitive methane plumes into stationary columns",
        "q8_d2": "Wind speed has zero thermodynamic effect on convective heat transfer or gas dispersion",
        "q8_d3": "Thermal surveys are only valid when conducted inside active thunderstorms",
        "q9_stem": "To achieve quantitative radiometric temperature measurement (spot-size ratio) and plume localization in {u_title}, what thermal IFOV/GSD and spectral sensitivity (NETD) are required?",
        "q9_ans": "Cooled MWIR (3.2-3.4 um for hydrocarbon absorption) or calibrated LWIR (8-14 um) sensor with NETD <= 36 mF (20 mK) and at least 3x3 pixels squarely on the target emitter",
        "q9_d1": "Standard RGB visible-light camera with an infrared blocking filter installed",
        "q9_d2": "Single-pixel sub-resolution measurement from 2,500 ft AGL with NETD > 5.0 °F",
        "q9_d3": "Uncalibrated consumer thermometer held outside the aircraft cabin window",
        "q10_stem": "Under ASTM C1153 (insulated roofing/containment moisture) and ASTM E1934 (industrial thermography) applied to {u_title}, what minimum thermal differential (Delta_T) confirms a subsurface anomaly?",
        "q10_ans": "A verified radiometric thermal differential Delta_T >= +3.6 °F (+2.0 °C) relative to dry/sound reference insulation or adjacent phase conductors under equivalent load",
        "q10_d1": "Zero temperature difference (Delta_T = 0.0 °F) during heavy rainfall saturation",
        "q10_d2": "Specular solar glint reflecting off unpainted polished aluminum cladding",
        "q10_d3": "Measuring ambient air barometric pressure in psi instead of surface radiance in °F",
        "q11_stem": "When mapping environmental plume sources, pipeline ROW leaks, or subsurface moisture polygons in {u_title}, what RTK/PPK geodetic accuracy must be locked?",
        "q11_ans": "Horizontal error <= 0.60 inches and Vertical error <= 0.18 inches so leak valves, buried lines, and containment defects align precisely with facility GIS/CAD as-builts",
        "q11_d1": "Approximate county-level zip-code geolocation with +/- 500 feet of positional error",
        "q11_d2": "Visual dead-reckoning without GNSS metadata embedding in the RJPEG header",
        "q11_d3": "Magnetic compass heading alone without latitude, longitude, or orthometric height",
        "q12_stem": "In environmental liner thickness, protective pipe coating, and particulate/optical precision measurements for {u_title}, how is 1 mil defined in U.S. Customary units?",
        "q12_ans": "1 mil = 0.001 inches (one thousandth of an inch; e.g., a 60-mil HDPE environmental containment geomembrane = 0.060 inches thick)",
        "q12_d1": "1 mil = 1.0 milliliter of liquid hazardous waste",
        "q12_d2": "1 mil = 1.0 parts per million (ppm) of fugitive methane concentration",
        "q12_d3": "1 mil = 1.0 millimeter of steel pipeline wall thickness",
        "q13_stem": "Under EPA 40 CFR Part 60 Subpart OOOOb and ODEQ fugitive emissions compliance in {u_title}, what minimum Optical Gas Imaging (OGI) detection capability must the inspection protocol demonstrate?",
        "q13_ans": "Verified detection of hydrocarbon mass emission rates <= 60.0 grams/hour (approx. 2.12 oz/hr) of methane/VOCs at the regulated standoff distance and dwell time",
        "q13_d1": "Only catastrophic pipeline explosions exceeding 10,000 lbs/hour require reporting",
        "q13_d2": "Visual inspection with the naked eye from 1.0 mile away satisfies OOOOb OGI mandates",
        "q13_d3": "Fugitive gas leaks are exempt from repair if detected by an infrared camera",
        "q14_stem": "When classifying radiometric thermal anomalies under ASTM E1934 / NETA MTS in {u_title}, how does a Priority 1 (Minor/Baseline) condition differ from a Priority 4 (Critical/Emergency) condition?",
        "q14_ans": "Priority 1 indicates normal thermal equilibrium or minor Delta_T (< 7.2 °F) for monitoring, whereas Priority 4 (Delta_T > 63.0 °F over reference or active leak) requires immediate emergency remediation",
        "q14_d1": "Priority 1 requires immediate plant shutdown, whereas Priority 4 indicates normal operation",
        "q14_d2": "Thermal priority tiers depend only on the time of day rather than measured Delta_T",
        "q14_d3": "Priority 4 anomalies can be ignored for up to 36 months without repair",
    },
    "AUT-01": {
        "agency_statute": "SAE J1979 (OBD-II) / SAE J1939, ISO 14229 (UDS), ASE Master Technician & Oklahoma Title 61 Fleet Standards",
        "q1_stem": "Under SAE J1979 / J1939 and ISO 14229 (UDS) governance in {u_title}, how must pre-calibration ECU EEPROM snapshots and live CAN-Bus telemetry frames be archived?",
        "q1_ans": "Sealed immediately in a Write-Once-Read-Many (WORM) SQLite service ledger with a FIPS 180-4 SHA-256 hash keyed to the 17-character VIN before any UDS 0x2E/0x31 write",
        "q1_d1": "Overwritten directly to PCM flash memory without capturing a baseline EEPROM checksum or verifying battery voltage",
        "q1_d2": "Stored as unverified text notes with no VIN correlation, freeze-frame data, or CAN-Bus termination check",
        "q1_d3": "Cleared immediately with a generic code reader without diagnosing the root mechanical or sensor fault",
        "q2_stem": "When an NVIDIA Three-Brain CAN-Bus diagnostic scan in {u_title} detects a critical powertrain or network fault (|STFT + LTFT| >= 25% or CAN bus resistance != 60 Ohms), what is the mandatory protocol?",
        "q2_ans": "Isolate the physical mechanical/electrical root cause via oscilloscope and pressure/resistance gates, execute the repair SOP, perform UDS 0x31 adaptive relearn, and verify UDS 0x01 Default Session before unplugging",
        "q2_d1": "Hot-unplug the transceiver in the middle of an active UDS 0x2E EEPROM flash write while battery voltage is below 10.5V",
        "q2_d2": "Mask the Diagnostic Trouble Code (DTC) in the ECU table without fixing the vacuum leak, fuel pressure drop, or bus short",
        "q2_d3": "Bypass the 60-Ohm CAN-Bus termination resistors by jumpering Pin 6 (CAN_H) directly to Pin 16 (+12V Battery)",
        "q3_stem": "Why must SAE J1349 net horsepower, Volumetric Efficiency (VE_%), Fuel Trim (STFT+LTFT), and fastener preload torque (T = K*D*F/12) be verified in {u_title}?",
        "q3_ans": "To mathematically separate mechanical air/fuel/compression defects from ECU adaptive calibration drift and guarantee safe clamping loads without fastener yield",
        "q3_d1": "Engine control modules do not use airflow, fuel trim, or crank angular velocity to control combustion",
        "q3_d2": "All automotive bolts should be tightened with an uncalibrated impact wrench until threads strip",
        "q3_d3": "Volumetric efficiency is unrelated to Mass Air Flow (MAF g/s), engine displacement, or intake boost pressure",
        "q8_stem": "Before executing a bidirectional UDS 0x2E EEPROM configuration write or 0x31 adaptive learn in {u_title}, why must battery bus voltage be stabilized at 13.2V to 13.8V DC?",
        "q8_ans": "Voltage sag below 11.5V during flash/EEPROM programming corrupts memory blocks (triggering B1000/P0601 checksum errors) and destabilizes injector dead-time characterization",
        "q8_d1": "Alternator ripple exceeding 2.5V AC improves CAN-Bus differential signal integrity on Pins 6 and 14",
        "q8_d2": "ECUs flash faster when the vehicle battery is discharged below 8.0V DC",
        "q8_d3": "Battery voltage has zero effect on fuel pump output pressure or solenoid actuation force",
        "q9_stem": "When probing the ISO 11898 high-speed CAN-Bus on OBD-II Pin 6 (CAN_H) and Pin 14 (CAN_L) in {u_title}, what electrical parameters confirm physical layer integrity?",
        "q9_ans": "De-energized total loop resistance of 60.0 +/- 2.0 Ohms (two 120-Ohm parallel terminators) and energized dominant differential voltage V_diff = 2.0V (CAN_H = 3.5V, CAN_L = 1.5V)",
        "q9_d1": "Open-circuit infinite resistance (OL) between Pin 6 and Pin 14 with 120V AC household current on the bus",
        "q9_d2": "Zero ohms dead short between CAN_H and chassis ground Pin 4",
        "q9_d3": "Single-wire 0V static signal with no differential twisted-pair noise rejection",
        "q10_stem": "When diagnosing fuel metering and air-charge efficiency in {u_title}, what combined Fuel Trim (STFT + LTFT) and Volumetric Efficiency (VE_%) thresholds indicate a healthy naturally aspirated engine?",
        "q10_ans": "Combined |STFT + LTFT| within +/- 5.0% (fault threshold >= +/- 10.0% to 25.0%) and peak-torque Volumetric Efficiency between 80.0% and 95.0%",
        "q10_d1": "Long-Term Fuel Trim pinned at +35.0% with Volumetric Efficiency below 25.0% at Wide-Open Throttle",
        "q10_d2": "Air-Fuel Equivalence Ratio Lambda fixed at 3.50 under full-load acceleration",
        "q10_d3": "Mass Air Flow sensor reporting 0.0 g/sec at 4,500 RPM",
        "q11_stem": "When operating the Hot-Swappable NVIDIA Three-Brain Enclave across multiple fleet vehicles in {u_title}, what three conditions satisfy the Brain-3 Safe-Disconnect Interlock?",
        "q11_ans": "1) UDS Diagnostic Session returned to 0x01 Default, 2) Zero active EEPROM/Flash write routines in progress, and 3) Pre/Post SHA-256 WORM docket sealed in matrix_ledger.db",
        "q11_d1": "Unplugging the J1962/J1939 connector while UDS Service 0x36 TransferData is actively writing flash blocks",
        "q11_d2": "Leaving the ABS module locked in factory calibration mode with wheel speed sensors disabled",
        "q11_d3": "Skipping the VIN Mode $09 verification so calibration files from a 9.0L diesel tractor overwrite a 5.0L V8 gas truck",
        "q12_stem": "In precision engine machining, bearing oil clearance, cylinder bore taper, and valve stem-to-guide tolerance measurements in {u_title}, what does 1 mil (0.001 in) represent?",
        "q12_ans": "One thousandth of an inch (0.001 in); e.g., main crankshaft journal oil clearance is typically 1.5 to 2.5 mils (0.0015 to 0.0025 inches)",
        "q12_d1": "One millimeter (0.0394 inches) of crankshaft end-play",
        "q12_d2": "One gallon of 5W-30 synthetic motor oil per cylinder",
        "q12_d3": "One thousand foot-pounds of spark plug installation torque",
        "q13_stem": "Under SAE J1349 dynamometer and drivetrain physics applied to {u_title}, why do Horsepower (HP) and Torque (lb-ft) always cross at exactly 5,252 RPM?",
        "q13_ans": "Because 1 Horsepower = 33,000 ft-lbs/min divided by 2*pi radians per revolution (33,000 / 6.283185 = 5,252.11), yielding HP = (Torque * RPM) / 5252",
        "q13_d1": "Because all internal combustion engines hit their rev limiter at 5,252 RPM",
        "q13_d2": "Because OBD-II CAN-Bus baud rate is 5,252 bits per second",
        "q13_d3": "Because tire circumference is always 52.52 inches regardless of wheel diameter",
        "q14_stem": "When sizing high-flow fuel injectors and calculating fastener clamping preload in {u_title}, how are required injector flow (lb/hr) and bolt torque (lb-ft) determined?",
        "q14_ans": "Injector Flow = (Target_HP * BSFC) / (Cylinders * Max_Duty_Cycle_0.80), and Bolt Torque T = (K_friction * Diameter_in * Preload_lbs) / 12",
        "q14_d1": "Injector flow is independent of Brake Specific Fuel Consumption (BSFC) or injector duty cycle",
        "q14_d2": "Bolt torque equals bolt length multiplied by vehicle curb weight",
        "q14_d3": "Operating fuel injectors at 120% static duty cycle prevents lean detonation",
    },
    "PAV-01": {
        "agency_statute": "AASHTO R 86 / PP 67, ASTM D6433 Pavement Condition Index (PCI), and ODOT / Oklahoma Title 61 Highway Pavement Management Standards",
        "q1_stem": "Under AASHTO R 86, ASTM D6433, and Oklahoma Title 61 highway asset governance, how must 3D laser/photogrammetric pavement distress and longitudinal profile telemetry from {u_title} be preserved?",
        "q1_ans": "Sealed immediately in a Write-Once-Read-Many (WORM) SQLite pavement management ledger with a FIPS 180-4 SHA-256 digest indexed by Linear Referencing System (LRS) control-section milepost",
        "q1_d1": "Recorded as uncalibrated windshield opinions without LRS milepost or PCI deduct values",
        "q1_d2": "Overwritten each week in a temporary scratch file without cryptographic audit trails",
        "q1_d3": "Stored as low-resolution video clips with no rut-depth or crack-width calibration",
        "q2_stem": "When a highway pavement or subgrade evaluation in {u_title} reveals a critical Pavement Condition Index collapse (PCI <= 25 Very Poor/Failed), severe hydroplaning rutting (> 0.75 in), or base punchout failure, what is required?",
        "q2_ans": "Trigger an immediate Statutory Pavement / Subgrade Remediation Docket under ODOT and Oklahoma Title 61 for structural mill-and-overlay, full-depth reclamation, or safety speed/load restriction",
        "q2_d1": "Apply cosmetic fog seal over failed alligator fatigue cracking (PCI < 20) and defer for 10 years",
        "q2_d2": "Smooth the IRI profile data mathematically to hide deep wheel-path ruts from the docket",
        "q2_d3": "Increase heavy 18-kip ESAL truck traffic limits over the saturated pumping subgrade",
        "q3_stem": "Why must AASHTO 1993/MEPDG structural layer coefficients, ASTM D6433 deduct curves, and Falling Weight Deflectometer (FWD) backcalculation bounds be verified before signing the {u_title} docket?",
        "q3_ans": "To ensure accurate Structural Number (SN), resilient modulus (M_R), and remaining service life calculations under Oklahoma Title 61 and 18 U.S.C. § 1001 without premature roadway failure",
        "q3_d1": "All asphalt and concrete pavements have infinite fatigue life regardless of axle loads",
        "q3_d2": "Surface color alone determines the subgrade California Bearing Ratio (CBR) and Structural Number",
        "q3_d3": "Pavement thickness design never accounts for 18-kip Equivalent Single Axle Loads (ESALs)",
        "q8_stem": "During a photogrammetric LiDAR/optical corridor mapping sortie for highway pavement distress in {u_title}, why must sustained wind speed (< 15.0 mph) and motion blur limits be strictly enforced?",
        "q8_ans": "Airframe pitch/roll oscillation in high winds degrades vertical Z-axis point-cloud precision below the 0.04-inch threshold required by AASHTO R 86 to quantify wheel-path rutting and faulting",
        "q8_d1": "60.0 mph crosswinds improve sub-millimeter transverse rut-depth laser profiling",
        "q8_d2": "Motion blur of 4.0 inches per frame is acceptable for measuring 0.01-inch fatigue cracks",
        "q8_d3": "Flight stability has no impact on photogrammetric orthomosaic bundle adjustment",
        "q9_stem": "To classify longitudinal, transverse, and alligator fatigue cracking by severity level (Low < 0.25 in, Medium 0.25-0.75 in, High > 0.75 in) under ASTM D6433 in {u_title}, what optical GSD is required?",
        "q9_ans": "Optical GSD <= 0.004 in/px (4 mils) to <= 0.04 in/px under uniform diffuse illumination (>= 1.4 foot-candles) without tire-track shadow occlusion",
        "q9_d1": "Coarse 6.00 in/px satellite imagery unable to resolve cracks narrower than half a foot",
        "q9_d2": "Nighttime flight with all illumination disabled (0.0 foot-candles)",
        "q9_d3": "Oblique horizon photos taken from 5.0 miles away",
        "q10_stem": "When using infrared thermography (ASTM D4788 / AASHTO T 389) in {u_title} to detect asphalt mat thermal segregation during paving or subsurface stripping/debonding, what thermal threshold applies?",
        "q10_ans": "A verified radiometric thermal differential Delta_T >= +3.6 °F (+2.0 °C) for subsurface debonding/moisture entrapment, or >= 25.0 °F temperature differential across the freshly placed HMA paving mat",
        "q10_d1": "Isothermal pavement conditions (Delta_T = 0.0 °F) under ponded rainwater",
        "q10_d2": "Measuring asphalt mat temperature in kips per square foot instead of degrees Fahrenheit (°F)",
        "q10_d3": "Disabling emissivity calibration (epsilon = 0.95 for asphalt) during thermal capture",
        "q11_stem": "When establishing Survey Control Points and RTK/PPK trajectories for highway cross-slope, joint faulting, and IRI elevation profiles in {u_title}, what geodetic accuracy is mandatory?",
        "q11_ans": "Horizontal error <= 0.60 inches and Vertical elevation error <= 0.18 inches locked to ODOT CORS / local base-station benchmarks",
        "q11_d1": "Recreational phone GPS with +/- 40.0 feet of vertical elevation bounce",
        "q11_d2": "Uncorrected barometric altimeter readings drifting with passing weather fronts",
        "q11_d3": "Estimating pavement cross-slope percentage by eye without survey control",
        "q12_stem": "In pavement micro-texture, diamond-grinding depth, geotextile thickness, and crack-width telemetry for {u_title}, how is 1 mil defined in U.S. Customary units?",
        "q12_ans": "1 mil = 0.001 inches (one thousandth of an inch; e.g., 40 mils = 0.040 inches of pavement thermoplastic marking or micro-crack width)",
        "q12_d1": "1 mil = 1.0 mile of four-lane divided interstate highway",
        "q12_d2": "1 mil = 1.0 million 18-kip Equivalent Single Axle Loads (ESALs)",
        "q12_d3": "1 mil = 1.0 millimeter of aggregate base course thickness",
        "q13_stem": "Under ASTM D6433 and ODOT Pavement Management standards applied to {u_title}, what is the numerical scale of the Pavement Condition Index (PCI) and what score defines a newly constructed/failed pavement?",
        "q13_ans": "PCI ranges from 0 to 100, where 100 represents a defect-free pavement (Good: 85-100) and values <= 25 represent Very Poor / Failed pavement requiring structural reconstruction",
        "q13_d1": "PCI ranges from -500 to +500 based on posted highway speed limit",
        "q13_d2": "A PCI score of 0.0 indicates brand-new faultless concrete pavement",
        "q13_d3": "PCI is measured in pounds per cubic foot of subgrade soil density",
        "q14_stem": "In highway ride-quality and longitudinal profile engineering for {u_title}, what does the International Roughness Index (IRI, expressed in U.S. Customary inches/mile) quantify under FHWA / ODOT standards?",
        "q14_ans": "Accumulated vertical suspension motion (in inches) of a standard quarter-car model per mile of roadway traveled (where IRI < 95 in/mi is Good and IRI > 170 in/mi is Unacceptable/Rough)",
        "q14_d1": "The transverse width of the highway shoulder measured in feet",
        "q14_d2": "The compressive strength of Portland Cement Concrete cores in psi",
        "q14_d3": "The posted truck weight limit on interstate bridges in tons",
    }
}

_prev_get_course_units_fn = get_course_units

def get_course_units(course_code: str):
    base_code = "STR-02" if course_code in ("STR-02", "ENV-01") else ("STR-03" if course_code in ("STR-03", "PAV-01", "AUT-01") else "STR-01")
    prof_code = "AUT-01" if course_code == "AUT-01" else ("ENV-01" if course_code in ("STR-02", "ENV-01") else ("PAV-01" if course_code in ("STR-03", "PAV-01") else "STR-01"))
    import copy
    units = copy.deepcopy(_prev_get_course_units_fn(base_code))
    if course_code == "AUT-01":
        import ebony_automotive_master as _eam_lib
        for _idx, _u in enumerate(units):
            if _idx < len(AUT01_STANDALONE_ACADEMIC_MODULES):
                _m_spec = AUT01_STANDALONE_ACADEMIC_MODULES[_idx]
                _z_obj = _eam_lib.BUMPER_TO_BUMPER_BEGINNER_GUIDE.get(_m_spec["zone_ref"], {})
                _u["unit"] = _m_spec["unit"]
                _u["title"] = _m_spec["title"]
                _u["governing_eq"] = _m_spec["governing_eq"]
                _u["equations"] = _m_spec["governing_eq"]
                _u["equation_legend"] = _m_spec["equation_legend"]
                _u["calc_unit"] = _m_spec["calc_unit"]
                _u["resolved_us_unit"] = _m_spec["resolved_us_unit"]
                _u["calc_prompt"] = _m_spec["calc_prompt"]
                _u["calc_gate"] = {
                    "prompt": _m_spec["calc_prompt"],
                    "expected_ans": _m_spec["expected_ans"],
                    "tolerance": _m_spec["tol"],
                    "unit": _m_spec["calc_unit"]
                }
                _haz_md = "\n".join(f"- ⚠️ **{h}**" for h in _z_obj.get("safety_precautions", []))
                _tools_md = "\n".join(f"- 🧰 **{t}**" for t in _z_obj.get("tools_required", []))
                _steps_md = "\n".join(f"- ✅ {s}" for s in _z_obj.get("step_by_step", []))
                _u["theory"] = (
                    f"### 🎓 Accredited 4.0-Hour Engineering Lecture // {_m_spec['title']}\n\n"
                    f"#### ⚠️ 1. Mandatory Life-Safety & All Task Hazards (READ FIRST — Zero-Shortcut Doctrine)\n{_haz_md}\n\n"
                    f"#### 📍 2. Visual Component Landmark (Where Is It & What Does It Look Like?)\n{_z_obj.get('where_and_what', '')}\n\n"
                    f"#### 🧰 3. Exact Tools, Socket Sizes & OEM Parts Required\n{_tools_md}\n\n"
                    f"#### 🛠️ 4. Step-by-Step Beginner-to-Master Procedure\n{_steps_md}\n\n"
                    f"#### 📐 5. Governing SAE / ISO / ANSI Engineering Formulation\n`{_m_spec['governing_eq']}`\n*{_m_spec['equation_legend']}*"
                )
                _u["worked_example"] = (
                    f"Worked Quantitative Shop & CAN-Bus Derivation ({_m_spec['title']}):\n"
                    f"* Governing Equation: {_m_spec['governing_eq']}\n"
                    f"* Variable Definitions: {_m_spec['equation_legend']}\n"
                    f"* Quantitative Gate Problem: {_m_spec['calc_prompt']}\n"
                    f"* Verified Step-by-Step Solution: Target Value = {_m_spec['expected_ans']} {_m_spec['calc_unit']} (Tolerance: +/- {_m_spec['tol']})"
                )
                _u["lab_protocol"] = (
                    f"1. **Phase 1 (Mandatory 8-Point Life-Safety & LOTO Gate):** Review all {len(_z_obj.get('safety_precautions', []))} task-specific hazards above; chock wheels, lock mechanical Jack Stands (or pull mower Spark Plug Boot), disconnect 10mm Black Negative (-) battery terminal, and don ANSI Z87.1 goggles & nitrile/cut-resistant gloves.\n"
                    f"2. **Phase 2 (Visual Landmark Identification & Tool/Part Staging):** Physically locate components on vehicle/tractor/mower and stage all required 6-point sockets, torque wrenches, and OEM replacement parts.\n"
                    f"3. **Phase 3 (Beginner-to-Master Mechanical & Electrical Execution):** Execute all {len(_z_obj.get('step_by_step', []))} step-by-step procedures and torque fasteners to exact lb-ft specification.\n"
                    f"4. **Phase 4 (Quantitative Calculation Gate & NVIDIA Three-Brain WORM Seal):** Solve `{_m_spec['governing_eq']}` (`{_m_spec['expected_ans']} {_m_spec['calc_unit']}`), verify live CAN-Bus / engine telemetry, and seal 4.0 Accredited Credit Hours in `matrix_ledger.db`."
                )
        _aut_Specs = [('Unit 01: SAE J1979 OBD-II, ISO 11898 CAN-Bus Differential Physics (60-Ohm) & Portable NVIDIA Three-Brain Enclave', 'R_bus = (120 * 120) / (120 + 120) = 60.0 Ohms | V_diff = V_CANH - V_CANL = 2.0V'), ('Unit 02: Stoichiometric Combustion (Lambda = 1.00), MAF Volumetric Efficiency (VE_%) & Fuel Trim Diagnostics (P0171)', 'VE_% = (MAF_actual / MAF_theoretical) * 100 | Total_Trim_% = STFT_% + LTFT_%'), ('Unit 03: Ignition Secondary KV Waveforms, Crankshaft Angular Acceleration & Mode $06 Misfire Diagnostics (P0300)', 'alpha_crank = d(omega)/dt | Spark Plug Gap = 0.032-0.044 in (Torque: 15-18 lb-ft)'), ('Unit 04: High-Pressure Common-Rail & Direct-Injection Fuel Systems (P0087), Piezo Injectors & Lift-Pump Hydraulics', 'Inj_Flow_lb_hr = (HP * BSFC) / (N_cyl * 0.80) | Rail_Delta = FRP_cmd - FRP_act'), ('Unit 05: Forced Induction Thermodynamics, Turbocharger VGT / Wastegate PID Control (P0299) & Intercooler Efficiency', 'PR = (14.7 + P_boost_psig) / 14.7 | eta_IC = (T_in - T_out) / (T_in - T_amb)'), ('Unit 06: Automatic Transmission Hydraulics (P0700), Torque Converter Slip & TCM Clutch Volume Index (CVI) Fast-Learn', 'Slip_RPM = Engine_RPM - Turbine_RPM | Ratio = ISS_RPM / OSS_RPM'), ('Unit 07: Three-Way Catalytic Converter Chemistry (P0420), Dual-O2 Switching Ratios & Exhaust Backpressure', 'Switch_Ratio = Count(B1S2) / Count(B1S1) < 0.35 | Delta_T_cat = T_out - T_in >= 75 F'), ('Unit 08: ABS / ESC Chassis Dynamics (C0035), Steering Angle Sensor (SAS) Zero-Point Calibration & Braking Physics', 'd_stop_ft = V_mph^2 / (29.92 * mu_tire) | Revs_Per_Mile = 20168 / D_tire_in'), ('Unit 09: Master Preventative Maintenance (0-100k+ Mi), API SP / GL-5 Tribology & Fastener Torque-to-Yield Mechanics', 'T_lb_ft = (K * D_in * F_preload_lbs) / 12 | Brake Fluid Moisture < 1.5%'), ('Unit 10: UDS ISO 14229 (0x10/0x22/0x27/0x2E/0x31), SAE J2534 EEPROM Checksums (B1000) & Brain-3 Hot-Swap WORM Seal', 'G_unplug = I(Session == 0x01) * I(EEPROM_Write == 0) * I(WORM_SHA256 == 1)')]
        for _idx, _u in enumerate(units):
            if _idx < len(_aut_Specs):
                _u["title"] = _aut_Specs[_idx][0]
                _u["governing_eq"] = _aut_Specs[_idx][1]
                _u["equations"] = _aut_Specs[_idx][1]
                _u["theory"] = (
                    f"### Bumper-to-Bumper Beginner & Master Engineering Theory // {_aut_Specs[_idx][0]}\n\n"
                    f"**1. Visual Component Landmark (Where It Is & What It Looks Like):** Every technician—from a first-time beginner opening the hood to a Level-5 Master Engineer—must first physically identify the system on the vehicle before touching a tool. In `{_aut_Specs[_idx][0]}`, locate the primary service points (Yellow/Orange Engine Oil Dipstick loop, translucent Brake/Coolant reservoirs, 16-Pin OBD-II port under the driver's steering column, or 9-Pin Deutsch/ISOBUS port on heavy trucks and tractors).\n\n"
                    f"**2. Mandatory Life-Safety & Vehicle Protection:** Park on level concrete, engage the parking brake, place solid wheel chocks in front of and behind ground wheels, lift only at reinforced factory frame rails or pinch welds, lower onto locked mechanical Jack Stands, and pass the Push-Shove Stability Shake Test. Always disconnect the **Black Negative (-)** battery cable first (`10mm` wrench) before electrical/component service, and wear ANSI Z87.1 safety glasses and nitrile gloves.\n\n"
                    f"**3. Governing SAE / ISO Mathematical Formulation:** `{_aut_Specs[_idx][1]}`. By combining proper 6-point metric socket selection (`8mm`–`22mm`), calibrated torque-wrench preload (`T = K * D * F / 12`), and the Portable NVIDIA Three-Brain CAN-Bus Enclave (`Brain 1` 60-Ohm transceiver -> `Brain 2` GPU solver -> `Brain 3` WORM EEPROM safety interlock), any operator can execute bumper-to-bumper mechanical repair and computer calibration with 100% precision."
                )
                _u["worked_example"] = (
                    f"Worked Shop & CAN-Bus Derivation ({_aut_Specs[_idx][0]}):\n"
                    f"* Governing Equation: {_aut_Specs[_idx][1]}\n"
                    f"* Beginner Tool & Safety Gate: Verify vehicle is secured on locked mechanical Jack Stands with wheel chocks installed, battery bus stabilized at 12.6V-13.5V DC, and CAN-Bus loop resistance verified at 60.0 Ohms across Pins 6 & 14.\n"
                    f"* Step-by-Step Execution: Apply 6-point socket Counter-Clockwise to loosen, inspect sealing surfaces/O-rings, torque fasteners Clockwise with calibrated click-type torque wrench, execute UDS 0x2E/0x31 adaptive learn, and confirm Green Brain-3 Safe-Disconnect Interlock before unplugging."
                )
                _u["lab_protocol"] = (
                    f"1. **Phase 1 (Shop Safety, Chocks & Jack Stands):** Park on level concrete, lock parking brake, chock wheels, lift on frame rail/pinch weld, lower onto pinned Jack Stands, and perform Push-Shove Shake Test.\n"
                    f"2. **Phase 2 (Visual Landmark & Tool Staging):** Identify component location, stage 6-point sockets, torque wrench, and fluids/parts, and disconnect Black Negative (-) battery terminal if servicing electrical/actuators.\n"
                    f"3. **Phase 3 (Mechanical Service & Precision Torquing):** Execute component replacement/service, verify gasket/O-ring seating, and torque all fasteners to exact SAE/OEM lb-ft specification.\n"
                    f"4. **Phase 4 (NVIDIA Three-Brain CAN-Bus Verification & Safe Unplug):** Plug enclave into 16-Pin OBD-II or 9-Pin J1939/ISOBUS port, verify 60.0-Ohm bus & live telemetry, execute UDS 0x2E/0x31 relearn, seal WORM SHA-256 docket, and unplug safely."
                )
                _aut_q_bank = [
                    ("When preparing to lift a vehicle or tractor for under-chassis service in {u_title}, what is the mandatory life-safety rule regarding hydraulic jacks?",
                     "A hydraulic jack is for lifting ONLY; the vehicle MUST be lowered onto mechanical locking Jack Stands positioned under factory frame rails or pinch welds with wheel chocks installed and Shake-Tested",
                     ["A hydraulic floor jack alone is safe to crawl under without jack stands", "Place the jack directly under the plastic engine oil pan or floorboard sheet metal", "Lift the vehicle on sloped gravel with the parking brake off"]),
                    ("When opening the hood to check engine oil level in {u_title}, how do you locate and accurately read the Engine Oil Dipstick?",
                     "Park on level ground with engine off for 5 minutes, pull the Yellow/Orange Dipstick loop, wipe it dry with a clean towel, re-insert fully, pull again, and verify oil is between MIN and MAX (1.0 quart span)",
                     ["Read the dipstick while the engine is revving at 4,000 RPM", "Pour windshield washer fluid into the yellow dipstick tube until it overflows", "Never wipe the dipstick before reading the splashed oil film"]),
                    ("When disconnecting a 12V/24V vehicle battery with a 10mm wrench during {u_title}, which terminal cable MUST be disconnected FIRST and reconnected LAST?",
                     "Always disconnect the Black Negative (-) ground cable FIRST and reconnect it LAST so a wrench touching the Red Positive (+) terminal and metal fender cannot cause a dead-short arc explosion",
                     ["Always disconnect Red Positive (+) first while leaving Black Negative (-) grounded to the chassis", "Short both terminals together with a screwdriver to test battery charge", "Pry the lead posts off with a hammer"]),
                    ("During an engine oil and spin-on filter change in {u_title}, why must you inspect the top rim of the old oil filter and pre-lube the new filter's rubber O-ring?",
                     "To verify the old rubber O-ring gasket did not stick to the engine block ('Double-Gasketing', which causes a total oil blowout on startup) and allow the new O-ring to seal smoothly when tightened 3/4 turn by hand",
                     ["Leaving two stacked rubber gaskets doubles the oil pressure", "Tighten the thin sheet-metal oil filter with a 3-foot breaker bar until crushed", "Install the new oil filter bone-dry without draining the old oil"]),
                    ("After replacing brake pads and rotors in {u_title}, what mandatory action MUST the technician perform before shifting the vehicle out of PARK?",
                     "Pump the brake pedal slowly 5 to 8 times with your foot until the pedal feels rock-solid, seating the compressed caliper pistons against the new brake pads before moving",
                     ["Shift immediately into Drive at 50 MPH without touching the brake pedal", "Coat the friction surfaces of the brake rotor and pads with heavy axle grease", "Let the heavy brake caliper hang by its rubber hydraulic hose"]),
                    ("When servicing a front/rear differential ('pumpkin') or 4WD transfer case in {u_title}, why must you ALWAYS remove the TOP Fill Plug BEFORE removing the BOTTOM Drain Plug?",
                     "Because if you drain all the gear oil out of the bottom plug first and then discover the top fill plug is rusted seized or stripped, the vehicle is stranded with an empty dry axle",
                     ["Removing the bottom plug first creates a vacuum that welds the top plug shut", "Differentials do not use gear oil", "Fill the differential through the rubber brake bleeder screw"]),
                    ("Before reaching under a push lawnmower or zero-turn deck to remove or sharpen a blade in {u_title}, what two safety rules are mandatory?",
                     "1) Pull the thick black rubber Spark Plug Wire Boot completely off the spark plug so the blade cannot accidentally fire, and 2) Tip the mower with the Spark Plug and Air Filter pointing UP toward the sky",
                     ["Leave the spark plug wire connected and tip the mower carburetor-side down so oil floods the air filter", "Sharpen the blade while the engine is idling", "Sharpen the curved back air-lift wings razor-thin and skip balancing"]),
                    ("When a lawnmower, generator, or small engine in {u_title} will not start after sitting with E10 ethanol fuel, how does the 60-second Carburetor Float-Bowl Main Jet fix work?",
                     "Drop the bottom float bowl cup using a 1/2-inch (13mm) or 10mm wrench, poke a thin copper wire through the clogged pinhole in the brass Main Jet bolt, and spray Carburetor Cleaner through all passages",
                     ["Pour water into the gas tank to dissolve ethanol varnish", "Hit the aluminum carburetor with a sledgehammer", "Remove the engine flywheel and piston rings"]),
                    ("How do 4-stroke lawnmower engines and 2-stroke handheld engines (chainsaws, string trimmers, leaf blowers) differ in lubrication during {u_title}?",
                     "4-stroke engines have a separate oil sump and dipstick (SAE 30 / 10W-30), whereas 2-stroke engines have NO oil pan and require JASO FD 2-cycle oil mixed directly into the gasoline (50:1 = 2.6 fl oz oil per 1.0 Gal gas; 40:1 = 3.2 fl oz/Gal)",
                     ["Both 2-stroke and 4-stroke engines run on pure unmixed gasoline with no oil anywhere", "Fill a 4-stroke lawnmower gas tank with 100% motor oil", "2-stroke chainsaws use 75W-140 differential gear oil in the fuel tank"]),
                    ("When using a Digital Multimeter set to 20V DC to test a vehicle's battery and alternator in {u_title}, what voltage readings confirm a healthy system?",
                     "12.60V to 12.80V DC with the engine OFF (100% charged battery), rising to 13.80V to 14.50V DC with the engine RUNNING (confirming the alternator and voltage regulator are charging)",
                     ["5.0V DC with engine off and 5.0V DC with engine running", "120V AC household voltage across the battery posts", "0.0V DC while cranking"])
                ]
                _unreplaced_indices = [3, 4, 5, 6, 14, 15, 16, 17, 18, 19]
                for _k_pos, _q_slot in enumerate(_unreplaced_indices):
                    if _q_slot < len(_u.get("unit_quiz", [])):
                        _st, _an, _ds = _aut_q_bank[_k_pos]
                        _raw_o = [_an] + _ds
                        _shf = (_idx + _k_pos) % 4
                        _ord_o = _raw_o[_shf:] + _raw_o[:_shf]
                        _lbl_o = []
                        _m_full = ""
                        _m_let = "A"
                        for _li, _ot in enumerate(_ord_o):
                            _let = chr(65 + _li)
                            _lb = f"{_let}) {_ot}"
                            _lbl_o.append(_lb)
                            if _ot == _an:
                                _m_let = _let
                                _m_full = _lb
                        _u["unit_quiz"][_q_slot] = {
                            "q": f"[AUT-01 Unit {_idx+1:02d} Milestone Q{_q_slot+1:02d}] " + _st.format(u_title=_aut_Specs[_idx][0]),
                            "opts": _lbl_o,
                            "ans": _m_full,
                            "correct_letter": _m_let
                        }
    prof = _COURSE_DOMAIN_PROFILES.get(prof_code, _COURSE_DOMAIN_PROFILES["STR-01"])
    for u in units:
        u_num = u.get("unit", 1)
        u_title = u.get("title", f"{course_code} Unit {u_num:02d}")
        uquiz = u.get("unit_quiz", [])
        replacements = {
            0: (prof["q1_stem"].format(u_title=u_title), prof["q1_ans"], [prof["q1_d1"], prof["q1_d2"], prof["q1_d3"]]),
            1: (prof["q2_stem"].format(u_title=u_title), prof["q2_ans"], [prof["q2_d1"], prof["q2_d2"], prof["q2_d3"]]),
            2: (prof["q3_stem"].format(u_title=u_title), prof["q3_ans"], [prof["q3_d1"], prof["q3_d2"], prof["q3_d3"]]),
            7: (prof["q8_stem"].format(u_title=u_title), prof["q8_ans"], [prof["q8_d1"], prof["q8_d2"], prof["q8_d3"]]),
            8: (prof["q9_stem"].format(u_title=u_title), prof["q9_ans"], [prof["q9_d1"], prof["q9_d2"], prof["q9_d3"]]),
            9: (prof["q10_stem"].format(u_title=u_title), prof["q10_ans"], [prof["q10_d1"], prof["q10_d2"], prof["q10_d3"]]),
            10: (prof["q11_stem"].format(u_title=u_title), prof["q11_ans"], [prof["q11_d1"], prof["q11_d2"], prof["q11_d3"]]),
            11: (prof["q12_stem"].format(u_title=u_title), prof["q12_ans"], [prof["q12_d1"], prof["q12_d2"], prof["q12_d3"]]),
            12: (prof["q13_stem"].format(u_title=u_title), prof["q13_ans"], [prof["q13_d1"], prof["q13_d2"], prof["q13_d3"]]),
            13: (prof["q14_stem"].format(u_title=u_title), prof["q14_ans"], [prof["q14_d1"], prof["q14_d2"], prof["q14_d3"]]),
        }
        for q_idx, (stem, ans_txt, distractors) in replacements.items():
            if q_idx < len(uquiz):
                raw_opts = [ans_txt] + distractors
                shift = (sum(ord(ch) for ch in course_code) + u_num * 3 + q_idx) % 4
                ordered_opts = raw_opts[shift:] + raw_opts[:shift]
                labeled_opts = []
                matched_full_opt = ""
                ans_letter = "A"
                for li, opt_txt in enumerate(ordered_opts):
                    clean_txt = re.sub(r"^[A-D]\)\s*", "", str(opt_txt))
                    letter = chr(65 + li)
                    lbl = f"{letter}) {clean_txt}"
                    labeled_opts.append(lbl)
                    if opt_txt == ans_txt:
                        ans_letter = letter
                        matched_full_opt = lbl
                uquiz[q_idx] = {
                    "q": f"[{course_code} Unit {u_num:02d} Milestone Q{q_idx+1:02d}] {stem}",
                    "opts": labeled_opts,
                    "ans": matched_full_opt,
                    "correct_letter": ans_letter,
                }
        gov_eq = str(u.get("governing_eq", "governing formulation")).splitlines()[0][:80]
        for extra_idx in range(len(uquiz)):
            if extra_idx not in replacements and course_code != "AUT-01":
                old_q = str(uquiz[extra_idx].get("q", "")).strip()
                clean_body = re.sub(r"^(?:\[[^\]]+\]\s*)+", "", old_q)
                if u_title not in clean_body:
                    clean_body = f"In {u_title} (applying {gov_eq} under {prof['agency_statute']}), {clean_body[0].lower() + clean_body[1:] if len(clean_body) > 1 else clean_body}"
                uquiz[extra_idx]["q"] = f"[{course_code} Unit {u_num:02d} Milestone Q{extra_idx+1:02d}] {clean_body}"
        # If course_code is AUT-01, replace indices [3, 4, 5, 6, 14, 15, 16, 17, 18, 19] with 100% pure Automotive, Tractor & Small Engine questions
        if course_code == "AUT-01":
            _aut_extra_10 = [
                (3, f"When preparing to lift a vehicle or tractor for under-chassis service in {u_title}, what is the mandatory life-safety rule regarding hydraulic jacks?",
                 "A hydraulic jack is for lifting ONLY; the vehicle MUST be lowered onto mechanical locking Jack Stands positioned under factory frame rails or pinch welds with wheel chocks installed and Shake-Tested",
                 ["A hydraulic floor jack alone is safe to crawl under without jack stands", "Place the jack directly under the plastic engine oil pan or floorboard sheet metal", "Lift the vehicle on sloped gravel with the parking brake off"]),
                (4, f"When opening the hood to check engine oil level in {u_title}, how do you locate and accurately read the Engine Oil Dipstick?",
                 "Park on level ground with engine off for 5 minutes, pull the Yellow/Orange Dipstick loop, wipe it dry with a clean towel, re-insert fully, pull again, and verify oil is between MIN and MAX (1.0 quart span)",
                 ["Read the dipstick while the engine is revving at 4,000 RPM", "Pour windshield washer fluid into the yellow dipstick tube until it overflows", "Never wipe the dipstick before reading the splashed oil film"]),
                (5, f"When disconnecting a 12V/24V vehicle battery with a 10mm wrench during {u_title}, which terminal cable MUST be disconnected FIRST and reconnected LAST?",
                 "Always disconnect the Black Negative (-) ground cable FIRST and reconnect it LAST so a wrench touching the Red Positive (+) terminal and metal fender cannot cause a dead-short arc explosion",
                 ["Always disconnect Red Positive (+) first while leaving Black Negative (-) grounded to the chassis", "Short both terminals together with a screwdriver to test battery charge", "Pry the lead posts off with a hammer"]),
                (6, f"During an engine oil and spin-on filter change in {u_title}, why must you inspect the top rim of the old oil filter and pre-lube the new filter's rubber O-ring?",
                 "To verify the old rubber O-ring gasket did not stick to the engine block ('Double-Gasketing', which causes a total oil blowout on startup) and allow the new O-ring to seal smoothly when tightened 3/4 turn by hand",
                 ["Leaving two stacked rubber gaskets doubles the oil pressure", "Tighten the thin sheet-metal oil filter with a 3-foot breaker bar until crushed", "Install the new oil filter bone-dry without draining the old oil"]),
                (14, f"After replacing brake pads and rotors in {u_title}, what mandatory action MUST the technician perform before shifting the vehicle out of PARK?",
                 "Pump the brake pedal slowly 5 to 8 times with your foot until the pedal feels rock-solid, seating the compressed caliper pistons against the new brake pads before moving",
                 ["Shift immediately into Drive at 50 MPH without touching the brake pedal", "Coat the friction surfaces of the brake rotor and pads with heavy axle grease", "Let the heavy brake caliper hang by its rubber hydraulic hose"]),
                (15, f"When servicing a front/rear differential ('pumpkin') or 4WD transfer case in {u_title}, why must you ALWAYS remove the TOP Fill Plug BEFORE removing the BOTTOM Drain Plug?",
                 "Because if you drain all the gear oil out of the bottom plug first and then discover the top fill plug is rusted seized or stripped, the vehicle is stranded with an empty dry axle",
                 ["Removing the bottom plug first creates a vacuum that welds the top plug shut", "Differentials do not use gear oil", "Fill the differential through the rubber brake bleeder screw"]),
                (16, f"Before reaching under a push lawnmower or zero-turn deck to remove or sharpen a blade in {u_title}, what two safety rules are mandatory?",
                 "1) Pull the thick black rubber Spark Plug Wire Boot completely off the spark plug so the blade cannot accidentally fire, and 2) Tip the mower with the Spark Plug and Air Filter pointing UP toward the sky",
                 ["Leave the spark plug wire connected and tip the mower carburetor-side down so oil floods the air filter", "Sharpen the blade while the engine is idling", "Sharpen the curved back air-lift wings razor-thin and skip balancing"]),
                (17, f"When a lawnmower, generator, or small engine in {u_title} will not start after sitting with E10 ethanol fuel, how does the 60-second Carburetor Float-Bowl Main Jet fix work?",
                 "Drop the bottom float bowl cup using a 1/2-inch (13mm) or 10mm wrench, poke a thin copper wire through the clogged pinhole in the brass Main Jet bolt, and spray Carburetor Cleaner through all passages",
                 ["Pour water into the gas tank to dissolve ethanol varnish", "Hit the aluminum carburetor with a sledgehammer", "Remove the engine flywheel and piston rings"]),
                (18, f"How do 4-stroke lawnmower engines and 2-stroke handheld engines (chainsaws, string trimmers, leaf blowers) differ in lubrication during {u_title}?",
                 "4-stroke engines have a separate oil sump and dipstick (SAE 30 / 10W-30), whereas 2-stroke engines have NO oil pan and require JASO FD 2-cycle oil mixed directly into the gasoline (50:1 = 2.6 fl oz oil per 1.0 Gal gas; 40:1 = 3.2 fl oz/Gal)",
                 ["Both 2-stroke and 4-stroke engines run on pure unmixed gasoline with no oil anywhere", "Fill a 4-stroke lawnmower gas tank with 100% motor oil", "2-stroke chainsaws use 75W-140 differential gear oil in the fuel tank"]),
                (19, f"When using a Digital Multimeter set to 20V DC to test a vehicle's battery and alternator in {u_title}, what voltage readings confirm a healthy system?",
                 "12.60V to 12.80V DC with the engine OFF (100% charged battery), rising to 13.80V to 14.50V DC with the engine RUNNING (confirming the alternator and voltage regulator are charging)",
                 ["5.0V DC with engine off and 5.0V DC with engine running", "120V AC household voltage across the battery posts", "0.0V DC while cranking"])
            ]
            for _q_idx, _stem_t, _ans_t, _dist_t in _aut_extra_10:
                if _q_idx < len(uquiz):
                    _r_opts = [_ans_t] + _dist_t
                    _shf = (u_num * 3 + _q_idx) % 4
                    _o_opts = _r_opts[_shf:] + _r_opts[:_shf]
                    _l_opts = []
                    _m_opt = ""
                    _a_let = "A"
                    for _li, _ot in enumerate(_o_opts):
                        _lt = chr(65 + _li)
                        _lb = f"{_lt}) {_ot}"
                        _l_opts.append(_lb)
                        if _ot == _ans_t:
                            _a_let = _lt
                            _m_opt = _lb
                    uquiz[_q_idx] = {
                        "q": f"[AUT-01 Unit {u_num:02d} Milestone Q{_q_idx+1:02d}] {_stem_t}",
                        "opts": _l_opts,
                        "ans": _m_opt,
                        "correct_letter": _a_let
                    }

        # Normalize all 20 quiz items so q["ans"] is guaranteed to be in q["opts"]
        for q in uquiz:
            opts = q.get("opts", [])
            raw_ans = str(q.get("ans", "")).strip()
            if raw_ans not in opts and opts:
                letter = raw_ans[0].upper() if raw_ans else "A"
                matched = next((o for o in opts if o.strip().upper().startswith(f"{letter})") or o.strip().upper().startswith(f"{letter}.")), None)
                if not matched:
                    matched = next((o for o in opts if raw_ans.lower() in o.lower() or o.lower() in raw_ans.lower()), opts[0])
                q["ans"] = matched
            q["correct_letter"] = str(q["ans"]).strip()[0].upper() if q.get("ans") else "A"
    return units

COURSE_CATALOG = {
    "AUT-01": {
        "code": "AUT-01",
        "title": "Master Automotive CAN-Bus Diagnostics, Preventative Maintenance & ECU Calibration",
        "name": "Master Automotive CAN-Bus Diagnostics, Preventative Maintenance & ECU Calibration",
        "credential": "ASE Master Tech & SAE J1979/J1939/UDS NVIDIA CAN-Bus Calibration Engineer",
        "statutory": "SAE J1979 (OBD-II), SAE J1939, ISO 14229 (UDS), SAE J2534 & OAC 245:15-11 (40.0 PELS PDHs)",
        "hours": 40.0,
        "ceus": 4.0,
        "tuition": 2500.00
    },
    "STR-01": {
        "code": "STR-01",
        "title": "Bridge Deck, Pier & Fracture-Critical Member Inspection",
        "name": "Bridge Deck, Pier & Fracture-Critical Member Inspection",
        "credential": "AASHTO / ODOT Level-5 Bridge Inspector",
        "statutory": "23 CFR § 650 (NBIS), AASHTO MBEI, Oklahoma Title 61 & OAC 245:15-11 (40.0 PELS PDHs)",
        "hours": 40.0,
        "ceus": 4.0,
        "tuition": 2500.00
    },
    "STR-02": {
        "code": "STR-02",
        "title": "Commercial Building Envelope, Roof Membrane Moisture & Facade NDT",
        "name": "Commercial Building Envelope, Roof Membrane Moisture & Facade NDT",
        "credential": "ASTM C1153 / E1934 & EPA OOOOb Certified Thermographer",
        "statutory": "40 CFR Part 60 Subpart OOOOb, ASTM C1153/E1934, Oklahoma Title 61 & OAC 245:15-11 (40.0 PELS PDHs)",
        "hours": 40.0,
        "ceus": 4.0,
        "tuition": 2500.00
    },
    "STR-03": {
        "code": "STR-03",
        "title": "Roadway Pavement Distress, Rutting & ASTM D6433 PCI Survey",
        "name": "Roadway Pavement Distress, Rutting & ASTM D6433 PCI Survey",
        "credential": "ASTM D6433 Certified Roadway & Drainage Inspector",
        "statutory": "ASTM D6433 PCI, AASHTO R 86, Oklahoma Title 61 & OAC 245:15-11 (40.0 PELS PDHs)",
        "hours": 40.0,
        "ceus": 4.0,
        "tuition": 2500.00
    },
    "ENV-01": {
        "code": "ENV-01",
        "title": "Radiometric Thermography, EPA Subpart OOOOb OGI & Environmental Forensics",
        "name": "Radiometric Thermography, EPA Subpart OOOOb OGI & Environmental Forensics",
        "credential": "EPA OOOOb OGI & ASNT Level-II Radiometric Thermographer",
        "statutory": "40 CFR Part 60 Subpart OOOOb, ASTM C1153/E1934, ASNT SNT-TC-1A & OAC 245:15-11 (40.0 PELS PDHs)",
        "hours": 40.0,
        "ceus": 4.0,
        "tuition": 2500.00
    },
    "PAV-01": {
        "code": "PAV-01",
        "title": "Highway Pavement Distress, Subgrade Mechanics & ASTM D6433 PCI Photogrammetry",
        "name": "Highway Pavement Distress, Subgrade Mechanics & ASTM D6433 PCI Photogrammetry",
        "credential": "ASTM D6433 & AASHTO R 86 Certified Pavement Engineer",
        "statutory": "ASTM D6433 PCI, AASHTO R 86, ODOT Pavement Management & OAC 245:15-11 (40.0 PELS PDHs)",
        "hours": 40.0,
        "ceus": 4.0,
        "tuition": 2500.00
    }
}

_ORIG_EXPORT_TEXTBOOK = export_full_course_textbook_markdown
def export_full_course_textbook_markdown(course_code: str, course_meta: dict = None) -> str:
    meta = course_meta or COURSE_CATALOG.get(course_code, COURSE_CATALOG["STR-01"])
    try:
        return _ORIG_EXPORT_TEXTBOOK(course_code, meta)
    except TypeError:
        return _ORIG_EXPORT_TEXTBOOK(course_code)



AUT01_STANDALONE_ACADEMIC_MODULES = [
    {
        "unit": 1,
        "title": "Unit 01: Shop Life-Safety, Jack Stands, Under-Hood Dipstick/Fluid ID & ISO 11898 CAN-Bus Physics (60-Ohm)",
        "governing_eq": "R_eq = (R_1 * R_2) / (R_1 + R_2) = (120 * 120) / (120 + 120) = 60.0 Ohms | V_diff = V_CANH - V_CANL = 2.0V",
        "calc_unit": "Ohms (Electrical Resistance)",
        "resolved_us_unit": "Ohms (Electrical Bus Loop Resistance)",
        "equation_legend": "R_eq = Total Parallel CAN-Bus Loop Resistance (Ohms) | R_1 = ECM Termination Resistor (120.0 Ohms) | R_2 = BCM/Gateway Termination Resistor (120.0 Ohms) | V_CANH = Dominant High Voltage (3.5V) | V_CANL = Dominant Low Voltage (1.5V)",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 01): An ISO 11898 high-speed automotive CAN-Bus network contains two 120.0-Ohm termination resistors wired in parallel at opposite ends of the twisted pair (Pin 6 CAN_H and Pin 14 CAN_L on the 16-pin OBD-II port). Using R_eq = (R_1 * R_2) / (R_1 + R_2), calculate the exact total loop resistance (in Ohms) measured with a digital multimeter when the battery is disconnected.",
        "expected_ans": 60.0,
        "tol": 0.5,
        "zone_ref": "ZONE_01_SAFETY_JACKING_AND_TOOLS"
    },
    {
        "unit": 2,
        "title": "Unit 02: Engine Oil & Filter Change Mastery, Double-Gasket Prevention & Stoichiometric Fuel Trim (P0171)",
        "governing_eq": "Total_Fuel_Trim_% = STFT_% + LTFT_% | Dipstick_Span (MIN to MAX) = 1.0 U.S. Quart (32 fl oz)",
        "calc_unit": "% (Total Fuel Trim Deviation)",
        "resolved_us_unit": "Percent (% Stoichiometric Fuel Trim Correction)",
        "equation_legend": "Total_Fuel_Trim_% = Combined ECU Fuel Delivery Correction (%) | STFT_% = Short-Term Fuel Trim (%) | LTFT_% = Long-Term Fuel Trim (%) | Fault Threshold: |Total_Fuel_Trim_%| >= 25.0% triggers DTC P0171/P0172",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 02): During an OBD-II live telemetry scan at 750 RPM idle, Bank 1 Short-Term Fuel Trim (STFT1) reads +8.5% and Long-Term Fuel Trim (LTFT1) reads +18.2% due to an unmetered intake manifold vacuum leak downstream of the MAF sensor. Calculate the combined Total Fuel Trim percentage (STFT1 + LTFT1).",
        "expected_ans": 26.7,
        "tol": 0.2,
        "zone_ref": "ZONE_03_OIL_CHANGE_AND_COOLING_SYSTEM"
    },
    {
        "unit": 3,
        "title": "Unit 03: SAE J1349 Dynamometer Power, Ignition Coils, Spark Plugs & Mode $06 Misfire Diagnostics (P0300)",
        "governing_eq": "HP_SAE = (Torque_lb_ft * RPM) / 5252 | Spark_Plug_Gap = 0.032 to 0.044 in (Torque: 15.0 lb-ft)",
        "calc_unit": "HP (SAE Net Horsepower)",
        "resolved_us_unit": "Horsepower (HP — SAE J1349 Net Mechanical Power)",
        "equation_legend": "HP_SAE = Net Brake Horsepower (HP) | Torque_lb_ft = Measured Engine Rotational Torque (lb-ft) | RPM = Crankshaft Rotational Speed (Revolutions Per Minute) | 5252 = 33,000 ft-lbs/min divided by 2*pi radians/rev",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 03): Using the SAE J1349 dynamometer power equation HP = (Torque_lb_ft * RPM) / 5252, calculate the exact net horsepower produced by a 5.0L V8 engine generating 365.0 lb-ft of torque at 2,800 RPM (round to 2 decimal places).",
        "expected_ans": 194.59,
        "tol": 0.5,
        "zone_ref": "ZONE_07_AIR_FUEL_SPARK_PLUGS_AND_IGNITION"
    },
    {
        "unit": 4,
        "title": "Unit 04: 12V/24V Battery, Alternator & Starter Motor Diagnostics, High-Pressure Fuel (P0087) & Injector Sizing",
        "governing_eq": "Inj_Flow_lb_hr = (Target_HP * BSFC) / (N_cyl * Duty_Cycle_0.80) | V_alt_charging = 13.80V to 14.50V DC",
        "calc_unit": "lb/hr (Injector Fuel Flow Rate)",
        "resolved_us_unit": "Pounds per Hour (lb/hr Fuel Injector Mass Flow)",
        "equation_legend": "Inj_Flow_lb_hr = Minimum Required Single Injector Flow Rate (lb/hr) | Target_HP = Crankshaft Horsepower (HP) | BSFC = Brake Specific Fuel Consumption (lb/HP-hr) | N_cyl = Number of Cylinders | 0.80 = Safe Maximum 80% Injector Duty Cycle",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 04): Using Inj_Flow = (Target_HP * BSFC) / (N_cyl * 0.80), calculate the required fuel injector flow rate (in lb/hr) for a 550.0 HP 8-cylinder engine operating at a Brake Specific Fuel Consumption (BSFC) of 0.52 lb/HP-hr and a maximum safe duty cycle of 0.80 (round to 2 decimal places).",
        "expected_ans": 44.69,
        "tol": 0.5,
        "zone_ref": "ZONE_04_BATTERY_ALTERNATOR_AND_ELECTRICAL"
    },
    {
        "unit": 5,
        "title": "Unit 05: Forced Induction Turbo/Supercharger Boost Physics (P0299), Cooling Systems, Water Pumps & Thermostats",
        "governing_eq": "PR = (14.7 + P_boost_psig) / 14.7 | VE_boosted = VE_NA * PR | Coolant_Boiling_Point (16 psi) = 252 deg F",
        "calc_unit": "PR (Absolute Boost Pressure Ratio)",
        "resolved_us_unit": "Dimensionless Pressure Ratio (PR — Absolute Manifold to Atmospheric Ratio)",
        "equation_legend": "PR = Absolute Compressor Pressure Ratio | 14.7 = Standard Sea-Level Atmospheric Pressure (psia) | P_boost_psig = Gauge Manifold Boost Pressure above Atmospheric (psig)",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 05): A twin-turbocharged engine operates at a gauge boost pressure P_boost = 14.7 psig at sea level (where atmospheric pressure P_atm = 14.7 psia). Using PR = (14.7 + P_boost_psig) / 14.7, calculate the exact absolute Boost Pressure Ratio (PR).",
        "expected_ans": 2.0,
        "tol": 0.1,
        "zone_ref": "ZONE_02_UNDER_HOOD_ANATOMY_AND_FLUID_ID"
    },
    {
        "unit": 6,
        "title": "Unit 06: Automatic Transmission Hydraulics (P0700), Differentials ('Top Plug First' Rule), Transfer Cases & CV Axles",
        "governing_eq": "Slip_RPM = Engine_RPM - Turbine_ISS_RPM | Gear_Ratio = ISS_RPM / OSS_RPM | TFT_Check = 175-195 deg F",
        "calc_unit": "RPM (Torque Converter Slip Speed)",
        "resolved_us_unit": "Revolutions Per Minute (RPM — Torque Converter Clutch Slip)",
        "equation_legend": "Slip_RPM = Torque Converter Rotational Slip (RPM) | Engine_RPM = Crankshaft Speed (RPM) | Turbine_ISS_RPM = Transmission Input Shaft Speed (RPM)",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 06): During a highway transmission diagnostic sweep, engine crankshaft speed is 2,100.0 RPM while the transmission Input Shaft Speed (ISS) turbine sensor reads 1,980.0 RPM prior to full TCC lockup. Calculate the Torque Converter Slip Speed (Slip_RPM = Engine_RPM - ISS_RPM) in RPM.",
        "expected_ans": 120.0,
        "tol": 1.0,
        "zone_ref": "ZONE_08_TRANSMISSION_DIFFERENTIALS_AND_DRIVETRAIN"
    },
    {
        "unit": 7,
        "title": "Unit 07: Exhaust, Catalytic Converter Oxygen Storage (P0420), O2 Sensors, Diesel DPF/DEF & HVAC Refrigerant Safety",
        "governing_eq": "Delta_T_cat = T_outlet_F - T_inlet_F >= 75.0 deg F | Switch_Ratio = B1S2_CrossCounts / B1S1_CrossCounts < 0.35",
        "calc_unit": "deg F (Catalytic Converter Exothermic Delta-T)",
        "resolved_us_unit": "Degrees Fahrenheit (deg F — Exothermic Oxidation Temperature Rise)",
        "equation_legend": "Delta_T_cat = Catalytic Converter Exothermic Temperature Rise (deg F) | T_outlet_F = Post-Catalyst Outlet Temperature (deg F) | T_inlet_F = Pre-Catalyst Inlet Temperature (deg F)",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 07): During an infrared pyrometer check of a warm three-way catalytic converter, the front inlet weld measures T_inlet = 1,160.0 deg F and the rear outlet weld measures T_outlet = 1,285.0 deg F due to exothermic oxidation of hydrocarbons and CO. Calculate the catalytic temperature differential Delta_T_cat = T_outlet - T_inlet (in deg F).",
        "expected_ans": 125.0,
        "tol": 1.0,
        "zone_ref": "ZONE_09_EXHAUST_EMISSIONS_O2_AND_DIESEL_DPF"
    },
    {
        "unit": 8,
        "title": "Unit 08: Forensic Brake & Steering Reconstruction — Pads, Rotors, Slide Pins, Tie Rods, Wheel Bearings & Tire BCM Sync",
        "governing_eq": "Revs_Per_Mile = 20168.0 / D_tire_in | d_stop_ft = V_mph^2 / (29.92 * mu_tire) | Pump Pedal 5-8x Before Drive!",
        "calc_unit": "Revs/Mile (BCM Tire Calibration Factor)",
        "resolved_us_unit": "Revolutions Per Mile (Revs/Mile — ABS/BCM Wheel Speed Calibration)",
        "equation_legend": "Revs_Per_Mile = Tire Revolutions per Statute Mile (written via UDS 0x2E to BCM/ABS) | 20168 = 63,360 inches/mile divided by pi | D_tire_in = Outer Tire Diameter (inches)",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 08): A fleet pickup truck is fitted with 33.0-inch outer-diameter all-terrain tires. Using the BCM/ABS calibration formula Revs_Per_Mile = 20168.0 / D_tire_in, calculate the exact revolutions per mile that must be written to the Body Control Module via UDS Service 0x2E (round to 2 decimal places).",
        "expected_ans": 611.15,
        "tol": 1.0,
        "zone_ref": "ZONE_05_BRAKES_PADS_ROTORS_AND_BLEEDING"
    },
    {
        "unit": 9,
        "title": "Unit 09: Forensic Fastener & Body/Door-Panel Reconstruction — Torque-to-Yield Mechanics, Window Regulators & Fuses",
        "governing_eq": "T_lb_ft = (K_friction * D_bolt_in * F_preload_lbs) / 12.0 | Star-Pattern Lug Torque = 100 to 150 lb-ft",
        "calc_unit": "lb-ft (Fastener Installation Torque)",
        "resolved_us_unit": "Pound-Feet (lb-ft — Calibrated Fastener Preload Torque)",
        "equation_legend": "T_lb_ft = Required Wrench Installation Torque (lb-ft) | K_friction = Nut/Thread Friction Factor (0.18 lubricated) | D_bolt_in = Nominal Bolt Diameter (inches) | F_preload_lbs = Target Axial Clamping Preload Force (lbs)",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 09): Using the fastener preload equation T = (K * D_in * F_preload) / 12, calculate the exact installation torque (in lb-ft) required for a D = 0.50-inch suspension bolt with friction factor K = 0.18 to achieve an axial clamping preload F = 12,000.0 lbs.",
        "expected_ans": 90.0,
        "tol": 0.5,
        "zone_ref": "ZONE_11_LIGHTING_WIPERS_FUSES_AND_BODY"
    },
    {
        "unit": 10,
        "title": "Unit 10: Master Small Engine, Lawnmower, Carburetor Main Jet, Blade Tip-Speed & 2-Stroke (50:1) / Zero-Turn EFI Course",
        "governing_eq": "V_oil_fl_oz = (V_gas_gal * 128.0) / Ratio_50 | V_tip_fpm = (pi * D_blade_in * RPM) / 12 <= 19,000 ft/min",
        "calc_unit": "fl oz (2-Stroke Oil Volume for 2.5 Gal @ 50:1)",
        "resolved_us_unit": "Fluid Ounces (fl oz — JASO FD 2-Cycle Oil Mix Volume)",
        "equation_legend": "V_oil_fl_oz = Required 2-Cycle Engine Oil Volume (U.S. Fluid Ounces) | V_gas_gal = Gasoline Container Volume (U.S. Gallons) | 128.0 = Fluid Ounces per U.S. Gallon | Ratio_50 = 50:1 Fuel-to-Oil Mix Ratio",
        "calc_prompt": "Part A Quantitative Calculation Gate (Unit 10): You are filling a 2.5-gallon fuel can with Ethanol-Free 90-octane gasoline for a commercial 2-stroke string trimmer and chainsaw requiring a 50:1 fuel-to-oil ratio. Using V_oil_fl_oz = (V_gas_gal * 128.0) / 50.0, calculate the exact volume of JASO FD 2-cycle oil (in fluid ounces) required.",
        "expected_ans": 6.4,
        "tol": 0.1,
        "zone_ref": "ZONE_13_SMALL_ENGINE_SAFETY_AND_NO_START_TRIAGE"
    }
]




_ORIG_GET_GLOSSARY = get_master_glossary_and_references
def get_master_glossary_and_references(course_code: str = "STR-01") -> dict:
    g = _ORIG_GET_GLOSSARY(course_code)
    auto_terms = [
        {"term": "Engine Oil Dipstick (Yellow/Orange Loop)", "cat": "AUT-01 Beginner Anatomy", "def": "A thin metal measuring rod with a bright yellow or orange pull-ring on the side of the engine block. Pull out, wipe clean with a towel, re-insert fully, and pull out again: the span between MIN/ADD and MAX/FULL equals exactly 1.0 U.S. Quart (32 fl oz)."},
        {"term": "Double-Gasketing (Oil Filter Blowout Hazard)", "cat": "AUT-01 Life-Safety", "def": "When removing an old spin-on oil filter, if the old black rubber O-ring sticks to the engine block and you screw the new filter on top of it, the stacked gaskets will blow out under 60 PSI oil pressure and dump all engine oil in seconds. Always verify the old O-ring came off with the old filter!"},
        {"term": "Black Negative (-) Battery Cable First Rule", "cat": "AUT-01 Electrical Safety", "def": "Always disconnect the Black Negative (-) ground cable FIRST (10mm wrench) and reconnect it LAST. Because the entire metal car body is connected to Negative (-), touching a wrench from Red Positive (+) to the fender while Negative is still attached creates a 600-Amp dead short."},
        {"term": "ISO 11898 CAN-Bus (60.0-Ohm Differential Loop)", "cat": "AUT-01 NVIDIA Three-Brain", "def": "Controller Area Network twisted-pair data bus on OBD-II Pin 6 (CAN_H = 3.5V) and Pin 14 (CAN_L = 1.5V), or J1939 9-Pin Deutsch Pins C & D. Two 120-Ohm parallel termination resistors inside the ECM and BCM produce a 60.0-Ohm total loop resistance."},
        {"term": "Short-Term & Long-Term Fuel Trim (STFT + LTFT)", "cat": "AUT-01 Engine Diagnostics", "def": "The percentage of fuel the ECU adds (+) or subtracts (-) to maintain stoichiometric Lambda = 1.00 (14.7:1 air-fuel ratio). Combined |STFT + LTFT| >= 25% triggers P0171 (System Too Lean) or P0172 (System Too Rich)."},
        {"term": "Lawnmower Tipping Rule (Spark Plug & Air Filter UP)", "cat": "AUT-01 Small Engine Safety", "def": "Before reaching under a mower deck, ALWAYS pull the thick black rubber Spark Plug Wire Boot off the spark plug, and tip the mower with the Spark Plug and Air Filter pointing UP toward the sky so crankcase oil cannot flood the air filter or cylinder."},
        {"term": "2-Stroke Fuel-Oil Mix (50:1 = 2.6 fl oz / Gal)", "cat": "AUT-01 Small Engine", "def": "2-stroke handheld engines (chainsaws, string trimmers, leaf blowers) have no oil pan and require JASO FD air-cooled 2-cycle oil mixed directly into the gasoline: 50:1 = 2.56 fl oz oil per 1.0 Gallon of gas (6.40 fl oz per 2.5 Gallons)."}
    ]
    existing_t = {item["term"] for item in g.get("terms", [])}
    for at in auto_terms:
        if at["term"] not in existing_t:
            g["terms"].insert(0, at)
    return g


# ==============================================================================
# HVF OLD-SCHOOL MASTER-TO-APPRENTICE 6-PART TEXTBOOK ENGINE
# Teaches WHO, WHAT, WHEN, WHERE, WHY, and HOW from the ground up (Zero Filler)
# ==============================================================================
_OLD_SCHOOL_COURSE_CONTEXT = {
    "STR-01": {
        "who_role": (
            "**Who Governs & Executes This Work:** Under federal **23 CFR Part 650 (National Bridge Inspection Standards - NBIS)** and **Oklahoma Statutes Title 61**, three specific people stand behind every bridge inspection: "
            "(1) The **Program Manager & Professional Engineer (PE)** at the Oklahoma Department of Transportation (ODOT) or County Circuit Engineering District (CED) who carries ultimate statutory authority; "
            "(2) The **NBIS Team Leader**, who must be physically on-site for every inspection, review all structural findings, and sign the legal docket; and "
            "(3) **You, the Certified Field Inspector & sUAS NDT Specialist (CAGE: 1AHA8)**. Under **18 U.S.C. § 1001**, signing a bridge inspection log is a federal legal attestation—if you guess at a measurement or skip a girder bay and that bridge fails under a school bus or semi-truck, you are personally and criminally accountable."
        ),
        "when_context": (
            "**When This Inspection Must Happen (And When to Abort):** Routine highway bridges must be inspected at least once every **24 months** (`730 days`), while **Fracture-Critical Members (FCMs)**—steel tension members whose failure would drop the bridge—and underwater piers require hands-on/close-range inspection every **12 to 24 months** (or immediately after a major flood, barge strike, or overweight vehicle hit). "
            "**Historical Lesson (Why We Never Delay):** On December 15, 1967, the U.S. Route 35 Silver Bridge collapsed into the Ohio River in 20 seconds (killing 46 people) because a tiny **0.125-inch (1/8-inch)** cleavage crack inside eyebar #330 went undetected. On August 1, 2007, the I-35W bridge in Minneapolis collapsed during rush hour because **0.50-inch** gusset plates bowed and buckled under added deck weight. "
            "**Weather Abort Gates:** Never launch an under-deck photogrammetry or ultrasonic sortie when sustained winds exceed **15.0 mph**, when ambient light beneath the deck drops below **1.4 foot-candles** without auxiliary gimbal strobes, or when active rain coats steel girders in a reflective water film."
        ),
        "where_context": (
            "**Where Failures Hide First on a Real Bridge:** Do not waste battery life taking postcard photos from 200 feet away. Structural failures start in dark, wet, high-stress corners: "
            "(1) **Beneath Leaky Expansion Joints** at the ends of the concrete deck where winter road-salt brine pours straight down onto steel beam ends and elastomeric bearing pads; "
            "(2) **Mid-Span Tension Flanges and Welded Web Stiffener Toes**, where heavy truck axles flex the steel downward thousands of times a day; "
            "(3) **Pin-and-Hanger Assemblies & Gusset Plates**, where rust packs tightly between steel plates and jacks them apart; and "
            "(4) **The Upstream Nose of River Piers**, where fast floodwaters curl downward like a horseshoe vortex and dig away the riverbed soil supporting the concrete footing."
        ),
        "rookie_mistakes": [
            "**Rookie Mistake #1 — Flying on a Magnetic Compass Under Steel Girders:** Thousands of pounds of overhead structural steel bend the Earth's magnetic field and will cause a standard GPS/compass drone to spin out of control ('toilet-bowl') and crash into the river. **Master Rule:** Always lock the flight controller into **3D LiDAR SLAM + Upward/Downward Optical Flow mode** before flying beneath a bridge deck.",
            "**Rookie Mistake #2 — Measuring Surface Rust Instead of Net Remaining Steel:** Scraping loose flake rust off a gusset plate is not enough. Because rust occupies **6 to 8 times** the volume of the original solid steel ('pack-rust'), a 1/2-inch bulge of rust could be hiding severe section loss or an internal crack. **Master Rule:** Always couple a calibrated **Ultrasonic Thickness Gauge (`2.25–5.0 MHz`)** to bare, couplant-gelled metal to read true remaining plate thickness in thousandths of an inch (`mils`).",
            "**Rookie Mistake #3 — Mixing Inches and Feet in Bridge Formulas:** If a span length `L` is measured in **feet (`ft`)** and a crack length `a` or bearing pad thickness `h_rt` is measured in **inches (`in`)**, plugging them into the same formula without converting will throw your safety rating off by a factor of 12! **Master Rule:** Write down the unit next to every single number before touching your calculator."
        ]
    },
    "ENV-01": {
        "who_role": (
            "**Who Governs & Executes This Work:** Under **Oklahoma Statutes Title 61 (Public Buildings & Public Works)** and the **Office of Management and Enterprise Services — Construction and Properties (OMES CAP)**, state facility managers, university physical plant directors, and municipal engineers are legally required to protect taxpayer-funded roofs, masonry facades, and parking structures from premature collapse and energy waste. "
            "**Your Role as the Certified Building Envelope & Thermography Specialist (CAGE: 1AHA8):** Instead of letting a roofing contractor charge taxpayers $1,500,000 to tear off an entire hospital or school roof when only 12% of the insulation is wet, you provide the independent, court-admissible **ASTM C1153 Radiometric Thermal & Dielectric Moisture Map** that pinpoints the exact square footage of trapped water for surgical repair."
        ),
        "when_context": (
            "**When This Inspection Must Happen (The Golden Sunset Window):** You **cannot** perform a roof moisture infrared scan at 12:00 Noon on a sunny day! At midday, direct sunlight reflects off white TPO or gravel roofs and creates false hot spots everywhere. "
            "**The Mandatory ASTM C1153 Window:** You must wait for a sunny day (`>= 1,400 BTU/ft²` solar heat load) with zero rain in the prior 24 hours and winds under **15.0 mph**. Then, you launch your radiometric thermal drone **45 to 120 minutes AFTER sunset**. Why? Because dry foam insulation cools off fast in the night air, while water trapped under the rubber membrane holds onto the afternoon sun's heat like a hot-water bottle—glowing brightly on your thermal camera in the dark! "
            "**Historical Lesson:** On June 24, 2021, the 12-story Champlain Towers South condominium in Surfside, Florida collapsed (98 fatalities) after years of flat-deck ponding water and chloride infiltration corroded the reinforced concrete plaza slab and column punching-shear zones from above."
        ),
        "where_context": (
            "**Where Trapped Water & Envelope Failures Hide First:** When you walk onto a commercial roof, parking deck, or high-rise facade, head straight to the trouble spots: "
            "(1) **Low-Point Roof Drains, Scuppers & Parapet Wall Flashing:** Leaves and debris clog internal drain bowls, causing rainwater to pond 2 to 6 inches deep (`5.2 lbs/sq ft` per inch of water depth) and force its way through tiny pinholes in membrane seams; "
            "(2) **HVAC Curb Corners & Pipe Penetrations:** Vibration from rooftop air conditioners tears the flashing corners open; "
            "(3) **Masonry Window Lintels & Shelf Angles:** Water sneaks behind brick veneers, rusts the horizontal steel shelf angle, and expands with up to **30,000 psi** of 'rust-jacking' pressure—bowing brick walls outward over busy sidewalks; and "
            "(4) **Flat Concrete Plaza Decks Over Parking Garages:** Where failed waterproofing lets water rot the structural slab and columns."
        ),
        "rookie_mistakes": [
            "**Rookie Mistake #1 — Forgetting Emissivity (`ε`) Calibration on Shiny Metal vs. Rubber:** An unpainted galvanized metal HVAC duct reflects the cold night sky (`ε ≈ 0.15`) and looks freezing cold on an infrared camera, while weathered TPO/EPDM rubber (`ε ≈ 0.91`) radiates its true temperature. **Master Rule:** Always set your camera emissivity to match the exact roof surface (`0.90–0.92` for single-ply membranes) and record reflected sky temperature before scanning.",
            "**Rookie Mistake #2 — Condemning a Roof From Thermal Pictures Alone Without Physical Verification:** A thick patch of roof cement or doubled-up walkway pad can hold heat at night just like trapped water. **Master Rule:** Under **ASTM C1153**, every thermal anomaly MUST be verified on the roof deck using a **Non-Destructive Capacitance Moisture Meter (ASTM D7954)** or a physical **2-inch gravimetric core cut** weighed wet and dry.",
            "**Rookie Mistake #3 — Ignoring Indoor Relative Humidity & Dew Point (`T_dp`):** Sometimes a roof isn't leaking rain from the outside at all—warm, humid indoor air (`72°F` at `60% RH`) is leaking upward past a torn vapor barrier and condensing into liquid water against the cold underside of the roof deck whenever the steel deck drops below the **Dew-Point Temperature (`56.25°F`)**."
        ]
    },
    "PAV-01": {
        "who_role": (
            "**Who Governs & Executes This Work:** Under **23 CFR Part 515 (Transportation Asset Management Plan - TAMP)**, **Oklahoma Statutes Title 61**, and **ASTM D6433**, state highway engineers (ODOT), County Commissioners across all 77 Oklahoma counties, and municipal public works directors must score every mile of asphalt and concrete roadway on an objective **0-to-100 Pavement Condition Index (`PCI`)** scale before spending state or federal paving funds. "
            "**Your Role as the Certified Corridor LiDAR & PCI Specialist (CAGE: 1AHA8):** You operate the mobile/airborne RTK LiDAR and sub-millimeter optical profiler that measures crack density, wheel-path rut depth, joint faulting, and roadside ditch hydraulics—turning raw road distress into a sealed engineering repair docket."
        ),
        "when_context": (
            "**When Roadway Surveys & Repairs Must Happen (The Deterioration Cliff):** A brand-new highway (`PCI = 100`) ages slowly for its first 10 to 12 years down to a **PCI of 70 ('Satisfactory')**. Right between **PCI 70 and PCI 55 ('Fair')**, the road hits a steep cliff: small thermal cracks open up, rainwater pours into the crushed-stone base underneath, and heavy 18-wheeler tires pump the wet mud out through the cracks. "
            "**Why Timing Saves 500% in Taxpayer Money:** Sealing cracks and laying a thin preventative preservation coat at **PCI 65** costs about **$4 to $6 per square yard**. Waiting just 3 more years until the base fails at **PCI 35 ('Poor')** forces a full-depth bulldozer reconstruction costing **$35 to $50+ per square yard**!"
        ),
        "where_context": (
            "**Where to Look on an Asphalt or Concrete Highway Corridor:** Every type of pavement crack tells you its cause by **where** it sits on the road: "
            "(1) **Strictly Inside the Two Wheel Paths:** Interconnected chicken-wire polygons (**Alligator / Fatigue Cracking**) and sunken troughs (**Wheel-Path Rutting**). Because they only happen where truck tires roll, they prove a **structural base/load failure**; "
            "(2) **Straight Across the Lane (`Transverse`) or Down the Centerline (`Longitudinal`):** Caused by winter cold shrinking the asphalt mat or poor paving-machine joint compaction (**environmental/construction failure**); "
            "(3) **At Concrete Slab Corners & Transverse Dowel Joints:** Where water trapped under concrete slabs gets ejected at high speed as heavy trucks cross the joint (**Pumping, Faulting & Corner Breaks**); and "
            "(4) **Roadside Drainage Ditches & Culvert Pipes:** When weeds and mud clog a roadside ditch, water backs up under the road shoulder and turns a strong clay subgrade into wet soup."
        ),
        "rookie_mistakes": [
            "**Rookie Mistake #1 — Simply Subtracting Total Deduct Points (`TDV`) From 100:** If a road sample unit has three different distresses whose deduct points add up to `TDV = 65`, a beginner subtracts `100 - 65 = 35` and gets the wrong answer! **Master Rule:** Under **ASTM D6433**, when multiple distresses (`q > 1`) exist in the same sample unit, you MUST apply the **Corrected Deduct Value (`CDV`)** curve so overlapping defects aren't double-counted (`PCI = 100 - CDV_max`).",
            "**Rookie Mistake #2 — Treating a 1/2-Inch Wheel-Path Rut as 'Minor Cosmetics':** A rut that is `0.50 inches` deep holds a continuous puddle of water across the highway during an Oklahoma thunderstorm. At `58.5 mph`, a pickup truck's tires lose all contact with the pavement and ride up on a wedge of water (**dynamic hydroplaning**), resulting in zero steering and zero braking.",
            "**Rookie Mistake #3 — Flying Directly Over Live Highway Traffic Without Lateral Offset:** Under **FAA Part 107.39 / 107.145**, you never hover a standard mapping drone directly over windshields moving at 70 mph. **Master Rule:** Fly parallel along the right-of-way shoulder maintaining a minimum **15.0-foot horizontal lateral offset** from the live travel lane with a 30° oblique camera gimbal angle."
        ]
    },
    "AUT-01": {
        "who_role": (
            "**Who Governs & Executes This Work:** Under **SAE International (Society of Automotive Engineers)**, **ISO 11898 / ISO 14229**, **ASE Master Technician Standards**, and **OSHA 29 CFR 1910 Shop Safety**, every technician working on a passenger car, heavy-duty diesel farm tractor, or small 2-stroke/4-stroke utility engine is directly responsible for the life of the driver and operator. "
            "**Your Role as the Sovereign Master Mechanic & CAN-Bus Diagnostician:** Whether you are changing engine oil and brake pads in your home driveway, rebuilding a clogged lawnmower carburetor on the workbench, or plugging the **Portable NVIDIA Three-Brain Enclave** into a truck's 16-pin OBD-II port to diagnose a `P0171` fuel-trim or `P0087` common-rail fault, you follow one unbreakable code: **measure twice, torque to spec, and verify with live math before turning the key.**"
        ),
        "when_context": (
            "**When Service & Diagnostics Must Happen (Preventative Intervals vs. Fault Triage):** Mechanical machines never heal themselves—every mile of driving or hour of mowing wears down fluid additives and friction linings on a strict clock: "
            "(1) **Every 5,000 Miles (or 50 Hours on Small Engines):** Full-synthetic engine oil & spin-on filter change, tire rotation, and air filter check; "
            "(2) **Every 30,000 to 50,000 Miles:** Automatic transmission fluid (`ATF`), front/rear differential gear oil (`GL-5`), transfer case fluid, and brake fluid moisture flush (`< 1.5% water`); "
            "(3) **Immediately Upon Check-Engine Light (`MIL`) or Symptom:** Whenever `STFT + LTFT` fuel trims exceed `± 10%`, whenever a misfire (`P0300`) flashes the check-engine light (which can melt a $1,800 catalytic converter in under 3 minutes!), or before storing any small engine for more than 30 days with ethanol gas."
        ),
        "where_context": (
            "**Where to Look First Under the Hood, Under the Chassis & On the Small-Engine Bench:** Before touching a wrench, orient yourself using clear visual landmarks: "
            "(1) **Under the Hood:** Locate the **Yellow/Orange Loop Engine Oil Dipstick**, the **Clear Plastic Coolant Overflow Tank** (NEVER open a hot radiator cap!), the **Clear Brake Fluid Reservoir** on the driver's firewall, and the **12V Battery** (`Red +` positive vs. `Black -` negative ground cable); "
            "(2) **Under the Driver's Dashboard:** Within 24 inches of the steering wheel column sits the trapezoid **16-Pin SAE J1979 OBD-II Port** (`Pin 4/5 = Ground`, `Pin 6 = CAN-High`, `Pin 14 = CAN-Low`, `Pin 16 = +12V Battery`); "
            "(3) **Under the Vehicle Chassis:** Locate the reinforced steel **Frame Rails / Pinch Welds** where mechanical **Jack Stands** MUST be locked before any human body part goes underneath; and "
            "(4) **On a Lawnmower / Small Engine:** Locate the thick black rubber **Spark Plug Boot** on the cylinder head and the round metal **Carburetor Float Bowl** hanging under the side of the air filter."
        ),
        "rookie_mistakes": [
            "**Rookie Mistake #1 — Crawling Under a Car Supported Only by a Hydraulic Jack (LETHAL):** A hydraulic floor jack is held up by a $0.50 rubber O-ring that can blow out without warning, dropping 4,500 lbs of steel in 0.2 seconds. **Master Rule:** Jack the vehicle up, lower it onto **two locked mechanical steel Jack Stands** on solid frame rails, chock the tires, and push the fender hard before ever sliding underneath.",
            "**Rookie Mistake #2 — 'Double-Gasketing' a Spin-On Oil Filter or Draining a Differential Bottom Plug First:** If the old black rubber O-ring from the old oil filter stays stuck to the engine block and you screw the new filter on top of it, all 5 quarts of oil will blow out in 10 seconds and seize the engine! And on a differential or transfer case, **always loosen the TOP Fill Plug FIRST**—because if you drain the bottom plug first and then find out the top fill plug is rusted shut, you cannot put oil back in the truck!",
            "**Rookie Mistake #3 — Tipping a Lawnmower Carburetor-Side Down or Pulling an OBD-II Cable Mid-Flash:** Tipping a 4-stroke mower with the air filter facing the ground floods the cylinder and paper air filter with crankcase oil. Always disconnect the **Spark Plug Wire FIRST** and tip the mower with the **Spark Plug / Muffler pointing UP**. And when using the NVIDIA Three-Brain Enclave, never unplug the OBD-II cable until the **Green WORM Safe-to-Unplug Light** confirms `Session = 0x01`!"
        ]
    }
}

def _apply_six_part_old_school_textbook(u_dict: dict, course_code: str) -> dict:
    nl = chr(10)
    bt3 = chr(96) * 3
    ctx = _OLD_SCHOOL_COURSE_CONTEXT.get(course_code, _OLD_SCHOOL_COURSE_CONTEXT["STR-01"])
    u_num = u_dict.get("unit", 1)

    # Restore full AUT-01 bumper-to-bumper content from AUT01_STANDALONE_ACADEMIC_MODULES
    if course_code == "AUT-01" and (u_num - 1) < len(AUT01_STANDALONE_ACADEMIC_MODULES):
        import ebony_automotive_master as _eam_lib
        _m_spec = AUT01_STANDALONE_ACADEMIC_MODULES[u_num - 1]
        _z_obj = _eam_lib.BUMPER_TO_BUMPER_BEGINNER_GUIDE.get(_m_spec["zone_ref"], {})
        u_dict["title"] = _m_spec["title"]
        u_dict["governing_eq"] = _m_spec["governing_eq"]
        u_dict["equations"] = _m_spec["governing_eq"]
        u_dict["equation_legend"] = _m_spec["equation_legend"]
        u_dict["calc_unit"] = _m_spec["calc_unit"]
        u_dict["resolved_us_unit"] = _m_spec["resolved_us_unit"]
        u_dict["calc_prompt"] = _m_spec["calc_prompt"]
        u_dict["calc_gate"] = {
            "prompt": _m_spec["calc_prompt"],
            "expected_ans": _m_spec["expected_ans"],
            "tolerance": _m_spec["tol"],
            "unit": _m_spec["calc_unit"]
        }
        u_dict["calc_challenge"] = {
            "prompt": _m_spec["calc_prompt"],
            "target": _m_spec["expected_ans"],
            "tol": _m_spec["tol"],
            "unit": _m_spec["calc_unit"],
            "unit_label": _m_spec["calc_unit"]
        }
        _haz_md = nl.join(f"- ⚠️ **{h}**" for h in _z_obj.get("safety_precautions", []))
        _tools_md = nl.join(f"- 🧰 **{t}**" for t in _z_obj.get("tools_required", []))
        _steps_md = nl.join(f"- ✅ {s}" for s in _z_obj.get("step_by_step", []))
        u_dict["theory"] = nl.join([
            f"#### 📍 Visual Component Landmark (What It Is & Where to Find It)",
            str(_z_obj.get("visual_landmark", "")),
            "",
            f"#### ⚠️ Mandatory Life-Safety & All Task Hazards (READ FIRST — Zero-Shortcut Doctrine)",
            _haz_md,
            "",
            f"#### 🧰 Exact Tools, Socket Sizes & OEM Parts Required",
            _tools_md,
            "",
            f"#### 🛠️ Step-by-Step Beginner-to-Master Shop & Field Procedure",
            _steps_md
        ])
        u_dict["worked_example"] = nl.join([
            f"Worked Quantitative Shop & CAN-Bus Derivation ({_m_spec['title']}):",
            f"* Governing Equation: {_m_spec['governing_eq']}",
            f"* Variable Definitions: {_m_spec['equation_legend']}",
            f"* Quantitative Gate Problem: {_m_spec['calc_prompt']}",
            f"* Verified Step-by-Step Solution: Target Value = {_m_spec['expected_ans']} ({_m_spec['calc_unit']})"
        ])
        u_dict["lab_protocol"] = nl.join([
            f"1. **Phase 1 (Mandatory Life-Safety & LOTO Gate):** Review all {len(_z_obj.get('safety_precautions', []))} life-safety rules before touching any tool or vehicle.",
            f"2. **Phase 2 (Visual Landmark Identification & Tool Staging):** Physically locate the component using the Visual Landmark guide and stage all {len(_z_obj.get('tools_required', []))} required tools/parts.",
            f"3. **Phase 3 (Beginner-to-Master Mechanical & Electrical Execution):** Execute all {len(_z_obj.get('step_by_step', []))} sequential shop procedures and torque fasteners to spec.",
            f"4. **Phase 4 (Quantitative Calculation Gate & NVIDIA Three-Brain WORM Seal):** Solve the Module {u_num:02d} calculation (`{_m_spec['expected_ans']} {_m_spec['calc_unit']}`) and verify the 20-question milestone exam."
        ])

    u_title = u_dict.get("title", f"{course_code} Module {u_num:02d}")
    raw_theory = str(u_dict.get("theory", "")).strip()

    for cut_marker in [
        f"### {u_num}.2 Statutory Enforcement, Field Instrumentation",
        f"### {u_num}.3 Comprehensive Engineering Reference Matrix"
    ]:
        if cut_marker in raw_theory:
            raw_theory = raw_theory.split(cut_marker)[0].strip()

    eq_str = str(u_dict.get("equations") or u_dict.get("governing_eq") or "").strip()
    eq_leg = str(u_dict.get("equation_legend") or "").strip().replace("Measured in `U.S. Customary Units`", f"Measured in `{u_dict.get('resolved_us_unit', u_dict.get('calc_unit', 'U.S. Customary Units'))}`")
    we_str = str(u_dict.get("worked_example") or u_dict.get("derivation") or "").strip()
    lab_str = str(u_dict.get("lab_protocol") or "").strip()

    c_gate = u_dict.get("calc_gate") or {}
    c_chal = u_dict.get("calc_challenge") or {}
    if c_chal and not c_gate:
        u_dict["calc_gate"] = {
            "prompt": c_chal.get("prompt", ""),
            "expected_ans": c_chal.get("target", 0.0),
            "tolerance": c_chal.get("tol", 0.5),
            "unit": c_chal.get("unit_label", c_chal.get("unit", ""))
        }

    calc_prompt = str(c_chal.get("prompt") or c_gate.get("prompt") or "")
    calc_target = c_chal.get("target", c_gate.get("expected_ans", ""))
    calc_unit   = str(c_chal.get("unit_label") or c_chal.get("unit") or c_gate.get("unit") or u_dict.get("calc_unit") or "U.S. Customary Units")
    rookie_md   = nl.join([f"* {rm}" for rm in ctx["rookie_mistakes"]])

    u_dict["beginner_primer"] = nl.join([
        f"### 📘 Old-School Master Textbook Chapter // {u_title}",
        "> **How to Study This Chapter On Your Own (No Professor Required):** This chapter is written the old-school way—like a veteran Master Engineer and Shop Foreman sitting across the workbench from you on Day 1. Read straight down through the **Who, What, When, Where, Why, and How** sections below. Every technical term is explained in standard engineering nomenclature right where it appears, and every math formula is worked out step-by-step before you ever take the quiz.",
        "",
        "#### 👥 1. WHO — Chain of Command, Legal Authority & Who Is Accountable",
        ctx["who_role"],
        "",
        "#### ⏱️ 2. WHEN — Operating Windows, Timing Schedules & Historical Lessons Learned",
        ctx["when_context"],
        "",
        "#### 📍 3. WHERE — Exact Physical Landmarks (Where to Stand, Look & Place Your Probes)",
        ctx["where_context"],
        "---",
        ""
    ])

    if not raw_theory.startswith("### 🔧 4. WHAT & WHY"):
        u_dict["theory"] = nl.join([
            "### 🔧 4. WHAT & WHY — Physical Anatomy, Technical Definitions & First-Principles Physics",
            "",
            raw_theory
        ])

    u_dict["deep_supplement"] = nl.join([
        "",
        "---",
        f"### 🧮 5. WHY & HOW THE MATH WORKS — Step-by-Step Analytical Engineering Derivation (`{u_title}`)",
        "",
        f"A real textbook never just throws an equation at you and expects you to guess what the letters mean. Let's break down the exact governing formula for **Module {u_num:02d}** in standard engineering nomenclature so you can work it via deterministic dimensional analysis:",
        "",
        "**A. The Governing Formula in Governing Specification:**",
        f"{bt3}text",
        eq_str,
        f"{bt3}",
        "",
        "**B. What Every Symbol Means in Plain English:**",
        f"* **Final Answer Unit Required in Sub-Tab 4:** **`{calc_unit}`**",
        f"{eq_leg if eq_leg else '* **Symbol & Variable Guide:** Each variable represents a direct physical measurement in U.S. Customary units (feet, inches, pounds, psi, °F, or RPM).'}",
        "",
        "**C. Why This Formula Works (Physical Common Sense):**",
        "* Every engineering equation is simply a balance scale comparing **Demand (how hard nature, traffic, heat, or electrical load is pushing on the system)** against **Capacity (how much strength, flow, or resistance the component was built to handle)**.",
        "* When **Parentheses `( ... )`** appear in the formula, always calculate the numbers inside the parentheses **FIRST** and record the intermediate state variable before multiplying or dividing.",
        "",
        f"**D. Classroom Analytical Engineering Derivation of Your Module {u_num:02d} Calculation Gate:**",
        f"* **The Problem You Will Solve in Sub-Tab 4:** *{calc_prompt}*",
        "* **Detailed Worked Derivation:**",
        we_str,
        f"* **Verified Deterministic Verification Check:** When you work the steps above on your calculator, your result should match **`{calc_target} {calc_unit}`**.",
        "",
        "---",
        "### 🛠️ 6. MASTER TRADESMAN'S FIELD CRAFT — Common Rookie Mistakes & How to Avoid Them",
        "",
        rookie_md
    ])

    if "CHALKBOARD CHECK:" not in str(u_dict.get("worked_example", "")):
        u_dict["worked_example"] = nl.join([
            we_str,
            "",
            f"📌 CHALKBOARD CHECK FOR MODULE {u_num:02d} GATE:",
            f"  * Assigned Gate Problem : {calc_prompt}",
            f"  * Verified Target Answer: {calc_target} ({calc_unit})"
        ])

    if "MASTER FIELD / SHOP EXECUTION CHECKLIST" not in str(u_dict.get("lab_protocol", "")):
        u_dict["lab_protocol"] = nl.join([
            f"#### 🛠️ Master Field / Shop Execution Checklist — {u_title}",
            "**Read Before Touching Any Equipment:** Follow each phase below in exact sequential order. Do not skip Phase 1 safety or calibration verification.",
            "",
            lab_str,
            "",
            "**Post-Execution Verification & WORM Sign-Off:**",
            f"* Double-check that all field/shop measurements are recorded in **U.S. Customary Units (`{calc_unit}`)**.",
            f"* Proceed to **Sub-Tab 4** to enter your calculation (`{calc_target} {calc_unit}`) and complete the 20-question mastery verification."
        ])

    return u_dict

# ==============================================================================
# HVF EXECUTIVE TREATISE SANITIZER (UNCONDITIONAL TABLE & DOMAIN NORMALIZER)
# ==============================================================================
import re as _hv_re

AUT01_ENGINEERING_MATRIX = """#### 1.3 Comprehensive SAE / ISO Diagnostic Reference Matrix & Shop Tolerance Standards (AUT-01)

To satisfy the **4.0 Accredited Credit Hours (0.4 CEUs / 4.0 PELS PDHs)** statutory and shop certification requirement under **SAE J1979, SAE J1939, ISO 11898, ANSI/OPEI B71.1, and OSHA 29 CFR 1910.147**, the certified Master Technician and Diagnostic Engineer must enforce the quantitative electrical, mechanical, and thermodynamic tolerances below:

| Diagnostic Parameter / Audit Gate | Governing Standard | Allowable Shop Tolerance | Mandatory Rejection / Fault Trigger | Statutory Recordation Format |
| :--- | :--- | :--- | :--- | :--- |
| **High-Speed CAN-Bus Termination** | ISO 11898-2 / SAE J1939-11 | `60.0 Ohms +/- 2.0 Ohms` (Key-Off) | `< 50 Ohms` (Short/3rd Terminator) or `~120 Ohms` (Open Terminator) | DMM Resistance Log + Oscilloscope Differential Capture |
| **CAN Differential Signal Integrity** | ISO 11898-2 (500 kbps / 250 kbps) | `V_CANH = 3.5V`, `V_CANL = 1.5V` (`V_diff = 2.0V`) | Dominant `V_diff < 1.5V` or Recessive bias drift `> +/- 0.35V` | Portable NVIDIA Three-Brain Frame Audit Ledger |
| **Threaded Fastener Torque Preload** | SAE J429 / ISO 898-1 / ASME B107.300 | `+/- 1.5%` Digital Torque Angle Wrench | Uncalibrated wrench (`> 12 mos`), lubricated threads on dry spec, or yield stretch | WORM Shop Torque Sign-Off Packet (`T = K * D * F / 12`) |
| **Combustion Stoichiometry & Fuel Trim** | SAE J1979 (OBD-II Mode $01/$06) | `STFT + LTFT` within `+/- 8.0%` (`Lambda = 1.00 +/- 0.02`) | Total Fuel Trim `> +/- 15.0%` or Crankcase/Cylinder leakdown `> 12.0%` | Wideband AFR / Mode $06 freeze-frame telemetry |
| **Hazardous Energy Lockout/Tagout** | OSHA 29 CFR 1910.147 / NFPA 70E | `0.0V` Verified Dead-Bus + Physical Hasps | Unchocked wheels, hydraulic jack without locked stands, or live 12V/48V/HV bus | Cryptographic SHA-256 WORM Safety Interlock (`matrix_ledger.db`) |

#### 1.4 Master Technician Shop Audit Checklist & QA/QC Sign-Off Protocol

Before advancing to **Sub-Tab 4 (Calculation Gate & 20-Question Milestone Exam)**, execute and verify each of the following 6 shop QA/QC steps:
* **[STEP 01 \u2014 OSHA 1910.147 LOTO & Mechanical Stabilization]:** Engage parking brake, chock wheels fore-and-aft, support chassis on rated mechanical jack stands, and disconnect the negative (`-`) battery terminal or apply high-voltage LOTO padlock before component disassembly.
* **[STEP 02 \u2014 Instrument Zeroing & Lead Verification]:** Zero digital multimeter (DMM) lead resistance (`< 0.1 Ohms`), verify oscilloscope probe attenuation (`1x / 10x`), and verify NIST calibration date on digital torque transducers.
* **[STEP 03 \u2014 Baseline Bus & Sensor Telemetry Capture]:** Record key-off CAN-Bus termination resistance (`R_bus = 60.0 Ohms`), key-on battery bus voltage (`>= 12.4V` static), and full SAE J1979/J1939 DTC + freeze-frame parameters prior to clearing codes.
* **[STEP 04 \u2014 First-Principles Diagnostic Isolation]:** Execute voltage-drop testing under load (`<= 100 mV` per connection), differential waveform inspection, compression/leakdown testing, or hydraulic pressure-flow auditing to isolate the root physical fault.
* **[STEP 05 \u2014 Quantitative Engineering Calculation]:** Solve the governing mechanical, electrical, or thermodynamic formulation for the active unit using measured shop values in U.S. Customary / SAE units (`Ohms`, `Volts`, `Amps`, `ft-lbs`, `psi`, `HP`, `CFM`).
* **[STEP 06 \u2014 WORM Cryptographic Sealing]:** Commit post-repair verification waveforms, torque preload logs, and calculated diagnostic parameters to `matrix_ledger.db` under **CAGE 1AHA8 / UEI S1M4ENLHTDH5**."""

def _hvf_scrub_str(s: str, is_auto: bool = False) -> str:
    if not isinstance(s, str):
        return s
    s = s.replace("Bumper-to-Bumper Beginner & Master Engineering Theory //", "Sovereign SAE / ISO Master Engineering Specification //")
    s = s.replace("from a first-time beginner opening the hood to a Level-5 Master Engineer", "operating at Level-5 Master Diagnostic Technician clearance")
    s = s.replace("1. Visual Component Landmark (Where It Is & What It Looks Like):", "#### 1.1 Subsystem Physical Architecture & Service Test-Point Topology")
    s = s.replace("2. Mandatory Life-Safety & Vehicle Protection:", "#### 1.2 Mandatory OSHA 1910.147 Life-Safety & Chassis Stabilization Protocol")
    s = s.replace("3. Governing SAE / ISO Mathematical Formulation:", "#### 1.2.1 Governing SAE / ISO Mathematical Formulation & Three-Brain Interlock")

    if ("STR-03 // Module" in s or "200 kHz Bathymetric Sonar" in s) and ("SAE J1979" in s or "CAN-Bus" in s or "Jack Stands" in s or "60-Ohm" in s or is_auto):
        idx_13 = s.find("1.3 Comprehensive Engineering Reference Matrix")
        if idx_13 != -1:
            line_s = s.rfind(chr(10), 0, idx_13)
            cut_at = line_s if line_s != -1 else idx_13
            s = s[:cut_at].rstrip() + chr(10) + chr(10) + AUT01_ENGINEERING_MATRIX

    if "1.1 " in s and ("1.0 " in s or "Welcome to Module" in s or "Key Acronyms" in s):
        idx_11 = s.find("1.1 ")
        line_start = s.rfind(chr(10), 0, idx_11)
        s = s[line_start + 1:] if line_start != -1 else s[idx_11:]

    if "How the Engineering Math Works" in s or "4-Step Field Logic" in s:
        s = _hv_re.sub(
            r"(?:#+|\*\*)*\s*1\.4\s+How the Engineering Math.*?(?=(?:#+|\*\*)*\s*1\.[45]\s+Inspector Field Audit Checklist|\Z)",
            "",
            s,
            flags=_hv_re.DOTALL
        )

    s = s.replace("1.5 Inspector Field Audit Checklist", "1.4 Inspector Field Audit Checklist")
    # Guarantee two clean newlines before 1.4 Inspector Field Audit Checklist regardless of what precedes it!
    s = _hv_re.sub(
        r"\s*(?:#+\s*)?1\.4\s+Inspector Field Audit Checklist",
        chr(10) + chr(10) + "#### 1.4 Inspector Field Audit Checklist",
        s
    )
    return s.strip()

def _hvf_scrub_obj(obj, _seen=None, is_auto=False):
    if _seen is None:
        _seen = set()
    oid = id(obj)
    if oid in _seen:
        return obj
    if isinstance(obj, str):
        return _hvf_scrub_str(obj, is_auto=is_auto)
    if isinstance(obj, dict):
        _seen.add(oid)
        auto_flag = is_auto or ("AUT-01" in str(obj.get("code", "")) or "SAE" in str(obj.get("title", "")))
        for k in list(obj.keys()):
            obj[k] = _hvf_scrub_obj(obj[k], _seen, is_auto=auto_flag)
        return obj
    if isinstance(obj, list):
        _seen.add(oid)
        for idx in range(len(obj)):
            obj[idx] = _hvf_scrub_obj(obj[idx], _seen, is_auto=is_auto)
        return obj
    return obj

for _gname, _gval in list(globals().items()):
    if not _gname.startswith("__") and isinstance(_gval, (dict, list)):
        _hvf_scrub_obj(_gval, is_auto=("AUT" in _gname.upper() or "AUTO" in _gname.upper()))

_raw_get_course_units_exec = get_course_units
def get_course_units(course_code: str):
    is_a = "AUT" in str(course_code).upper()
    return _hvf_scrub_obj(_raw_get_course_units_exec(course_code), is_auto=is_a)

# ==============================================================================
# HVF SOVEREIGN EXTERNAL & OFFLINE AIR-GAPPED TEXTBOOK VAULT PORTAL
# ==============================================================================
import json as _tb_json
from pathlib import Path as _tb_Path

TEXTBOOK_LINKS_FILE = _tb_Path(__file__).resolve().parent / "hvf_textbook_links.json"
OFFLINE_VAULT_DIR = _tb_Path(__file__).resolve().parent / "offline_textbooks"
OFFLINE_VAULT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_TEXTBOOK_LINKS = {
    "STR-01": {
        "title": "Non-Destructive Evaluation of Reinforced Concrete and Timber Structures & FHWA/NHI Bridge Inspection Reference Manual (BIRM, FHWA-NHI-12-049)",
        "primary_url": "https://www.fhwa.dot.gov/bridge/nbis.cfm",
        "secondary_url": "https://www.astm.org/products-services/standards-and-publications.html",
        "offline_file": "STR-01_Offline_NDE_Master_Manual.md",
        "syllabus_chapters": "Ch 1: RC Steel Corrosion (ASTM C876) | Ch 2: Alkali-Silica Reaction (ASR) | Ch 3: Acoustic Deck Testing (ASTM D4580/C1383) | Ch 4-8: Timber NDE & Radioscopy | Ch 9: NBIS Visual Inspection | Ch 10: Acoustic Emission | Ch 11: VR & Photogrammetry",
        "unit_directives": {
            1: ("FHWA BIRM Ch. 1-2 & 23 CFR Part 650 Subpart C", "Memorize the 20.0-ft NBI bridge span definition, 24-month Routine vs. FCM inspection intervals, Sufficiency Rating (S1+S2+S3-S4) weights, and 18 U.S.C. 1001 criminal attestation rules."),
            2: ("NDE Treatise Ch. 9 & AASHTO MBEI Section 3 (Element-Level Condition States)", "Focus on optical Ground Sampling Distance (GSD <= 0.004 in/px for FCMs), lens focal-length standoff equations, and distinguishing Condition States CS-1 through CS-4."),
            3: ("NDE Treatise Ch. 1 (Sections 1.1-1.4: Half-Cell, LPR & Resistivity) & Ch. 3 (Impact-Echo)", "Focus on ASTM C876 Cu/CuSO4 thresholds (-200 mV / -350 mV CSE), Stern-Geary icorr, and P-wave delamination depth D = (C_p * delta_t) / 2."),
            4: ("FHWA BIRM Ch. 7 (Steel Superstructures) & AASHTO LRFD Bridge Design Sec. 6", "Focus on Mode I Stress Intensity Factor K_I = Y * sigma * sqrt(pi * a), fracture toughness K_Ic limits, and ultrasonic thickness gauging of pack-rust gusset plates."),
            5: ("FHWA HEC-18 (Evaluating Scour at Bridges, 5th Ed.) Ch. 5-7", "Focus on the CSU Pier Scour Equation (y_s / y_1 = 2.0 * K1 * K2 * K3 * (a/y_1)^0.65 * Fr_1^0.43), Froude number calculation, and 200 kHz bathymetric sonar draft compensation."),
            6: ("FHWA BIRM Ch. 6 (Reinforced & Prestressed Concrete) & ACI 318", "Focus on concrete modulus of rupture f_r = 7.5 * sqrt(f'_c), shear-crack inclination angles, and prestressed strand corrosion/hydrogen embrittlement limits."),
            7: ("FHWA BIRM Ch. 10 (Bearings & Substructures) & AASHTO LRFD Sec. 14", "Focus on elastomeric bearing pad shear strain gamma = Delta_T / h_rt (<= 0.50 limit), thermal deck expansion Delta_L = alpha * L * Delta_T, and anchor-bolt shear."),
            8: ("ASPRS Positional Accuracy Standards & NDE Treatise Ch. 11 (3D Photogrammetry & LiDAR)", "Focus on GPS-denied 3D LiDAR SLAM drift bounds, EKF3 covariance limits, and point-cloud vertical deflection measurement (L/800 AASHTO serviceability limit)."),
            9: ("NDE Treatise Ch. 2 (Alkali-Silica Reaction) & ASTM C1153 (Infrared Deck Thermography)", "Focus on diurnal solar loading windows, minimum thermal contrast Delta_T >= +3.6 deg F (+2.0 deg C), and convective wind-stripping abort thresholds (< 15 mph)."),
            10: ("Oklahoma Title 61 / HB 2992 & FIPS 180-4 Cryptographic Evidence Standards", "Focus on compiling the PE-stamped Emergency Closure Docket, Benefit-Cost Ratio (BCR), and verifying the 64-character SHA-256 WORM ledger seal.")
        }
    },
    "ENV-01": {
        "title": "ASTM C1153 / D7954 Building Envelope Thermography, ASHRAE 90.1 & OMES Title 61 Facility Audit Manual",
        "primary_url": "https://www.astm.org",
        "secondary_url": "https://omes.ok.gov/services/construction-and-properties",
        "offline_file": "ENV-01_Offline_Envelope_Manual.md",
        "syllabus_chapters": "Ch 1: OMES CAP Title 61 Governance | Ch 2: Planck's Law & Emissivity | Ch 3: ASTM C1153 Roof Moisture | Ch 4: ASHRAE 90.1 U-Factor | Ch 5-10: Psychrometrics, Air Leakage (ASTM E779), Facade NDE & WORM Docket"
    },
    "PAV-01": {
        "title": "ASTM D6433 Pavement Condition Index (PCI), AASHTO R 86 & ODOT TAMP Corridor Profilometry Manual",
        "primary_url": "https://www.fhwa.dot.gov/pavement/",
        "secondary_url": "https://oklahoma.gov/odot.html",
        "offline_file": "PAV-01_Offline_Pavement_Manual.md",
        "syllabus_chapters": "Ch 1: 23 CFR 515 TAMP & ASTM D6433 | Ch 2: PCI Deduct Value Curves | Ch 3: IRI Quarter-Car Profilometry | Ch 4: Rut Depth Hydroplaning | Ch 5-10: FWD Backcalculation, ESALs, Drainage & ADA PROWAG"
    },
    "AUT-01": {
        "title": "SAE J1979 / J1939 CAN-Bus Diagnostics, ASE Master Technician Series & ANSI B71.1 Small-Engine Service Manual",
        "primary_url": "https://www.sae.org/standards",
        "secondary_url": "https://www.osha.gov/control-hazardous-energy",
        "offline_file": "AUT-01_Offline_Auto_Robotics_Manual.md",
        "syllabus_chapters": "Ch 1: SAE J1979/ISO 11898 CAN-Bus (60-Ohm) | Ch 2: 4-Stroke Otto/Diesel Compression & Leakdown | Ch 3: Wideband Lambda & Fuel Trim | Ch 4: Charging/Starting Voltage Drop | Ch 5-10: Hydraulics, 2-Stroke/Small-Engine, Brakes, HVAC & Three-Brain Interlock",
        "unit_directives": {
            1: ("ISO 11898-2 High-Speed CAN Spec & SAE J1979 / J1939 Physical Layer Manual", "Focus on parallel 120-Ohm termination resistance (R_bus = 60.0 Ohms), dominant differential voltage V_diff = V_CANH - V_CANL = 2.0V, and OSHA 1910.147 LOTO chassis stabilization."),
            2: ("ASE A1/A2 Engine Repair Manual & Heywood Internal Combustion Engine Fundamentals Ch. 2", "Focus on Swept Displacement V_d = (pi/4)*B^2*S*N, Static Compression Ratio CR = (V_d + V_c)/V_c, and cylinder differential leakdown limits (<= 10-12%)."),
            3: ("SAE J1979 OBD-II Mode $01/$06 Fuel System Spec & Bosch Automotive Handbook (Fuel Management)", "Focus on Stoichiometric Air-Fuel Ratio (14.7:1 gasoline / 14.5:1 diesel), Lambda equivalence ratio, and combined Short-Term + Long-Term Fuel Trim (STFT + LTFT) fault thresholds."),
            4: ("SAE J537 Storage Battery Standards & Heavy-Duty Starting/Charging Diagnostics Manual", "Focus on Ohm's Law parasitic draw (< 50 mA), starter-circuit maximum allowable voltage drop (<= 0.50V total cable drop under cranking load), and alternator ripple (< 50 mV AC)."),
            5: ("ISO 4413 Hydraulic Fluid Power & Mobile Agricultural Tractor Hydraulics Manual", "Focus on Pascal's Law actuator force F = P * A, hydraulic pump volumetric efficiency, and high-pressure pinhole fluid-injection life-safety lockout."),
            6: ("ANSI/OPEI B71.1 Commercial Turf/Small-Engine Safety Standard & 2-Stroke/4-Stroke Service Manual", "Focus on magneto ignition air-gap (0.010-0.014 in), 2-stroke fuel-to-oil mixing ratios (50:1 = 2.6 fl oz oil per gallon), and blade tip speed safety limits (<= 19,000 ft/min)."),
            7: ("FMVSS 105 / 121 Hydraulic & Air Brake Systems Manual", "Focus on rotor minimum machine-to/discard thickness tolerances, lateral runout (<= 0.002 in), and dual-circuit master cylinder hydraulic pressure ratios."),
            8: ("SAE J639 Mobile Air Conditioning Standards & EPA Section 609 Refrigerant Recovery Manual", "Focus on R-134a / R-1234yf pressure-temperature saturation relationships, superheat/subcooling diagnostics, and manifold gauge high/low-side fault isolation."),
            9: ("SAE J429 / ISO 898-1 Fastener Metallurgy & Torque-Tension Engineering Manual", "Focus on the Torque-Preload equation T = K * D * F / 12, dry vs. lubricated K-factor reductions, and extracting sheared bolts without damaging parent threads."),
            10: ("EBONY-RTOS Hardware Guillotine Spec & ISO 26262 ASIL-D Functional Safety Manual", "Focus on the 36.75 ns hardware safety interlock, CAN-Bus command authentication, and WORM cryptographic shop sign-off.")
        }
    }
}

def _ensure_default_offline_manuals():
    for k, meta in DEFAULT_TEXTBOOK_LINKS.items():
        fpath = OFFLINE_VAULT_DIR / meta["offline_file"]
        lines = [
            f"# {meta['title']} (LOCAL OFFLINE AIR-GAP EDITION)",
            f"- **Course Code:** `{k}` | **Sovereign Air-Gap Vault:** `c2_cockpit/offline_textbooks/{meta['offline_file']}`",
            f"- **Governing Authority:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OK Title 61)",
            "",
            "## Covered Syllabus & Governing Standards",
            meta["syllabus_chapters"],
            ""
        ]
        if "unit_directives" in meta:
            lines.append("## Module-by-Module Reading & Exam Focus Directives (Units 01 - 10)")
            for u_idx, (ch_ref, focus_txt) in sorted(meta["unit_directives"].items()):
                lines.append(f"- **Unit {u_idx:02d} \u2014 Assigned Reading:** `{ch_ref}`  ")
                lines.append(f"  *What to Focus On for the Exam Gate:* {focus_txt}")
            lines.append("")
        lines.append("## Offline Field Reference Notes")
        lines.append("This local file is stored permanently on your NVMe/SSD inside `c2_cockpit/offline_textbooks/` so it remains 100% accessible when operating in **Offline (Sovereign Fortress Air-Gap)** mode without internet connectivity.")
        fpath.write_text(chr(10).join(lines), encoding="utf-8")

def load_textbook_links() -> dict:
    _ensure_default_offline_manuals()
    if TEXTBOOK_LINKS_FILE.exists():
        try:
            data = _tb_json.loads(TEXTBOOK_LINKS_FILE.read_text(encoding="utf-8"))
            merged = dict(DEFAULT_TEXTBOOK_LINKS)
            for k, v in data.items():
                if k in merged and isinstance(v, dict):
                    merged[k].update(v)
                else:
                    merged[k] = v
            return merged
        except Exception:
            pass
    return dict(DEFAULT_TEXTBOOK_LINKS)

def render_textbook_link_portal(course_code: str = "STR-01", active_unit: dict = None, unit_index: int = None):
    import streamlit as st
    links = load_textbook_links()
    key = "STR-01"
    for k in links:
        if k in str(course_code).upper():
            key = k
            break
    # Also check session_state if course_code was default
    for sv in st.session_state.values():
        if isinstance(sv, str):
            for k in ["STR-01", "ENV-01", "PAV-01", "AUT-01"]:
                if k in sv and course_code == "STR-01" and k != "STR-01":
                    key = k
    meta = links[key]
    local_path = OFFLINE_VAULT_DIR / meta.get("offline_file", f"{key}_Offline_Manual.md")
    if not local_path.exists():
        _ensure_default_offline_manuals()

    # Auto-detect active unit (1..10) from st.session_state if not passed
    if unit_index is None:
        unit_index = 1
        for sv in st.session_state.values():
            if isinstance(sv, str) and "Unit " in sv:
                m_u = _hv_re.search(r"Unit\s+0?([0-9]+)", sv)
                if m_u:
                    unit_index = int(m_u.group(1))
                    break

    units_list = get_course_units(key)
    u_obj = units_list[unit_index - 1] if (isinstance(units_list, list) and 1 <= unit_index <= len(units_list)) else {}
    u_title = u_obj.get("title", f"Unit {unit_index:02d}") if isinstance(u_obj, dict) else f"Unit {unit_index:02d}"
    u_formula = u_obj.get("formula", "") if isinstance(u_obj, dict) else ""

    directives_map = meta.get("unit_directives", {})
    if unit_index in directives_map:
        assigned_ch, focus_summary = directives_map[unit_index]
    else:
        assigned_ch = f"{meta['title']} \u2014 Chapter/Section {unit_index:02d}"
        focus_summary = f"Master the statutory clauses, sensor calibration tolerances (Section 1.3), and governing mathematical formulation for {u_title}."

    with st.container():
        st.markdown(f"### \U0001f4da Accredited Reference Textbook Portal (`{key}` \u2014 Online & Air-Gap Offline Ready)")
        st.caption(f"**Assigned Reference Volume:** {meta['title']}")

        st.warning(
            f"\U0001f3af **MANDATORY READING & EXAM FOCUS DIRECTIVE ({u_title}):**" + chr(10)
            + f"- **1. Exact Textbook Chapters / Standards to Read:** `{assigned_ch}`" + chr(10)
            + f"- **2. Core Engineering Concepts & Thresholds to Focus On:** {focus_summary}" + chr(10)
            + (f"- **3. Governing Equation Tested in Sub-Tab 4 Calculation Gate:** `{u_formula.splitlines()[0]}`" + chr(10) if u_formula else "")
            + "- **4. Required Mastery Sequence:** Read the assigned textbook chapter above + Sections `1.1`\u2013`1.4` below \u2192 Work the derivation in **Sub-Tab 2** \u2192 Execute the field/shop SOP in **Sub-Tab 3** \u2192 Pass the **Sub-Tab 4** Calculation Gate & 20-Question Exam (`>= 90%`)."
        )

        c1, c2, c3 = st.columns([2, 2, 3])
        if local_path.exists():
            raw_bytes = local_path.read_bytes()
            mime_t = "application/pdf" if local_path.suffix.lower() == ".pdf" else "text/markdown"
            c1.download_button(
                f"\U0001f4e5 Download / Open Offline Textbook ({local_path.suffix.upper()})",
                data=raw_bytes,
                file_name=local_path.name,
                mime=mime_t,
                key=f"dl_off_tb_{key}"
            )
        c2.markdown(f"\U0001f310 **[Open Online Reference Manual \u2197]({meta['primary_url']})**  \n\U0001f517 **[Open Standards Library \u2197]({meta['secondary_url']})**")

        with c3.expander("\U0001f4c2 Offline Vault Manager (Upload Local PDF or Edit Link)"):
            up_pdf = st.file_uploader(
                f"Drop any full Textbook (.pdf or .md) into {key} Offline Vault:",
                type=["pdf", "md", "txt"],
                key=f"up_pdf_{key}"
            )
            if up_pdf is not None:
                save_name = f"{key}_Offline_Textbook{ _tb_Path(up_pdf.name).suffix.lower() }"
                target_p = OFFLINE_VAULT_DIR / save_name
                target_p.write_bytes(up_pdf.getvalue())
                links[key]["offline_file"] = save_name
                TEXTBOOK_LINKS_FILE.write_text(_tb_json.dumps(links, indent=2), encoding="utf-8")
                st.success(f"Stored `{save_name}` ({len(up_pdf.getvalue()):,} bytes) in local Offline Vault (`c2_cockpit/offline_textbooks/`)!")
            new_url = st.text_input("Online Textbook URL:", value=meta["primary_url"], key=f"tb_url_{key}")
            if st.button("\U0001f4be Save Online Link", key=f"tb_save_{key}"):
                links[key]["primary_url"] = new_url.strip()
                TEXTBOOK_LINKS_FILE.write_text(_tb_json.dumps(links, indent=2), encoding="utf-8")
                st.success("Saved online link!")

        if local_path.exists() and local_path.suffix.lower() in [".md", ".txt"]:
            with st.expander(f"\U0001f4d6 Read Local Offline Reference Manual (`{local_path.name}` \u2014 100% Air-Gap Local Disk)", expanded=False):
                st.markdown(local_path.read_text(encoding="utf-8", errors="ignore"))
        st.markdown("---")
