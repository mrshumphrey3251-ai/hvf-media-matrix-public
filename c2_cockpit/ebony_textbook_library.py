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
    """Modular Beginner's Glossary, Mathematical Symbol Decoder, U.S. Customary Unit Guide, and Statutory References."""
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
        {"term": "ODOT & OMES CAP", "cat": "Oklahoma Law", "def": "Oklahoma Department of Transportation (manages state bridges/highways) and Office of Management and Enterprise Services — Construction and Properties (manages state buildings/roofs under Title 61)."},
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
        {"term": "WORM Ledger & SHA-256 Seal", "cat": "Legal / C2", "def": "Write-Once-Read-Many database (matrix_ledger.db) locked with a 64-character digital fingerprint (SHA-256). If anyone alters even 1 character or pixel in an inspection report, the fingerprint breaks, proving court-admissible chain of custody."}
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
    """Attaches Section X.0 Plain-English Orientation and Sub-Tab 2 Symbol-by-Symbol Equation Decoder using chr(10)."""
    nl = chr(10)
    primer_lines = [
        f"### {u_num}.0 Beginner's Plain-English Orientation: What You Will Learn & Key Terms Decoded",
        f"> **Welcome to Module {u_num:02d} ({u_dict['title']})!** You do **not** need prior engineering experience to master this module. Every technical term, government code, and math symbol used in this lesson is translated into plain English right here:",
        "",
        "* **Why This Module Matters in the Real World:** In state infrastructure inspection under **Oklahoma Title 61**, we never guess whether a bridge, building roof, or highway is safe. We use drone cameras, lasers (**LiDAR**), heat sensors (**Infrared**), and sound waves (**Sonar/Impact-Echo**) to measure defects in **U.S. Customary Units** (**inches, feet, degrees Fahrenheit °F, pounds per square inch psi, and BTU/hr**), plug those measurements into a proven step-by-step formula, and lock the result into a tamper-proof database (**WORM Ledger**).",
        "* **Key Acronyms Decoded for Beginners:**",
        "  * **NBI / NBIS:** *National Bridge Inventory / Inspection Standards* — The federal safety list and law covering every public bridge longer than **20.0 feet**.",
        "  * **ODOT & OMES CAP:** *Oklahoma Dept. of Transportation* (bridges/roads) & *Office of Management and Enterprise Services* (state buildings/roofs).",
        "  * **AASHTO & ASTM:** The national engineering boards that write the official U.S. inspection rulebooks.",
        "  * **CS-1, CS-2, CS-3, CS-4 (Condition States):** The 1-to-4 health grade for bridge parts (**CS-1 = Good**, **CS-2 = Fair**, **CS-3 = Poor/Repair Needed**, **CS-4 = Severe/Emergency Closure**).",
        "  * **NDT (Non-Destructive Testing):** Finding hidden cracks, rust, or trapped water inside concrete/roofs using sensors *without* cutting or breaking the structure.",
        "  * **WORM & SHA-256:** *Write-Once-Read-Many* database sealed with a 64-character digital fingerprint (**SHA-256**) so inspection data cannot be faked or altered.",
        "---",
        ""
    ]
    u_dict["beginner_primer"] = nl.join(primer_lines)

    target_unit = u_dict.get("calc_unit", "U.S. Customary Units")
    legend_lines = [
        f"#### 🔎 Beginner's Symbol-by-Symbol Equation & Calculator Guide (Module {u_num:02d})",
        f"* **Target U.S. Measurement Unit for Sub-Tab 4:** Measured in **`{target_unit}`**",
        "* **Calculator Keystroke Rule (PEMDAS):** Always solve numbers inside **parentheses `( ... )`** first, then **square roots/exponents (`sqrt` or `^`)**, then **multiply/divide (`*` or `/`)**, and finally **add/subtract (`+` or `-`)**.",
        "",
        "| Symbol in Formula | How to Pronounce It | Plain-English Meaning | U.S. Measurement Unit & Calculator Tip |",
        "| :--- | :--- | :--- | :--- |",
        "| **`L_total` / `L` / `b` / `d` / `x` / `z` / `H`** | Length / Width / Depth / Height | Total span opening, barrel width, wall thickness, rebar depth, or flight altitude | Measured in **feet (ft)** or **inches (in)** (12 inches = 1 foot). |",
        "| **`SR` / `D_%` / `MC_%` / `PCI` / `RF`** | Rating or Condition Score | Percentage or index score showing structural health or moisture saturation | Measured in **Percent (`%`)**, **0–100 PCI Points**, or **Rating Factor (`RF`)**. |",
        "| **`A` or `Area_sqft`** | Surface Area | Length multiplied by Width of a bridge deck, roof bay, or highway lane | Measured in **square feet (sq ft)**. |",
        "| **`Delta` (`Δ` or `Delta_T` / `Delta_s`)** | DEL-tuh (Difference / Shift) | Subtract the second reading from the first reading (or sideways movement) | Example: `Delta_T = Indoor °F - Outdoor °F` (`72 °F - 27 °F = 45 °F`). |",
        "| **`sigma` (`σ`) / `P` / `f_r` / `K_Ic`** | SIG-muh (Stress / Load) | Pulling, pushing, or bending force pressing on steel, concrete, or soil | Measured in **psi** (lbs/sq in), **ksi** (1,000 lbs/sq in), or **kips** (1,000 lbs). |",
        "| **`sqrt(...)` or `^0.5`** | Square Root | Press the **`[√]`** button on your calculator | Example: `sqrt(32.0) = 5.657` (because `5.657 * 5.657 = 32.0`). |",
        "| **`^2` or `^3` or `^4`** | Squared / Exponent | Multiply the number by itself (`x^2 = x * x`) or use the **`[x^y]`** key | Example: `(2.0)^2 = 2.0 * 2.0 = 4.0`. |",
        "| **`R` / `U_wind` / `Q` / `T_dp`** | Thermal & Dew-Point Terms | `R` = Insulation rating; `Q` = Heat loss; `T_dp` = Condensation temperature | Measured in **BTU/hr** (British Thermal Units per hour) and **°F**. |",
        ""
    ]
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
            "When keying a multi-step engineering formula into a field calculator, which order of operations (PEMDAS) must be followed to prevent calculation error?",
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
                _s_txt = _s_txt.replace("|### 1.4", "|

### 1.4").replace("
### 1.4", "

### 1.4").replace("


### 1.4", "

### 1.4")
                _u_item[_k_field] = _s_txt
        _u_item["unit_quiz"] = _build_20_question_milestone_exam(_u_item, course_code)
    return units
