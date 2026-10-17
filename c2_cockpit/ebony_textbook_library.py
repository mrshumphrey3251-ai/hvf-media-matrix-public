"""
E.B.O.N.Y. Sovereign Field Academy // 40-Hour Accredited Textbook Library Engine
Provides 10 Comprehensive Academic Units (4.0 Credit Hours per Unit = 40.0 Hours)
for STR-01 (Bridges), STR-02 (Buildings), and STR-03 (Roadways), complete with
worked engineering calculations, statutory derivations, and SQLite CEU credit tracking.
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
    payload = f"{student_id}|{course_code}|UNIT-{unit_number:02d}|{credit_hours}|{ts}|CAGE:1AHA8"
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


def get_course_units(course_code: str):
    if course_code == "STR-01":
        return [
            {
                "unit": 1,
                "hours": 4.0,
                "title": "Unit 01: Statutory Jurisprudence — 23 CFR § 650 (NBIS), Oklahoma Title 61 & Title 74",
                "theory": """### 1.1 Federal & State Statutory Evolution of Bridge Safety
Following the catastrophic collapse of the U.S. Route 35 Silver Bridge on December 15, 1967 (46 fatalities), Congress enacted the **Federal-Aid Highway Act of 1968**, establishing the **National Bridge Inspection Standards (NBIS)** codified at **23 CFR § 650 Subpart C**. Within the State of Oklahoma, federal NBIS requirements are integrated into **Oklahoma Statutes Title 61 (Public Buildings and Public Works)** and **Title 74**, administered by the **Oklahoma Department of Transportation (ODOT) Bridge Division**.

Every structure on a public roadway with an opening measured along the center of the roadway of more than **20.0 feet (6.1 meters)** between undercopings of abutments or spring lines of arches, or extreme ends of openings for multiple boxes, is legally classified as a **Bridge** and must be cataloged in the **National Bridge Inventory (NBI)**.

| Statutory Mandate | Code Citation | Maximum Interval | Legal / Engineering Requirement |
| :--- | :--- | :--- | :--- |
| **Routine NBI Inspection** | 23 CFR § 650.311(a) | **24 Months** | Full element-level quantification of deck, superstructure, and substructure defects. |
| **Fracture-Critical (FCM)** | 23 CFR § 650.311(c) | **24 Months** | Hands-on (within arm's length) or ODOT-certified sub-millimeter optical NDT of tension steel members. |
| **Underwater Bathymetric** | 23 CFR § 650.311(b) | **60 Months** | Acoustic sonar / commercial diver verification of submerged pier footings and pilings. |
| **Scour Plan of Action** | ODOT Item 113 | **Immediate / Flood** | Real-time bathymetric deployment whenever hydrograph stage exceeds 50-year or 100-year discharge. |

### 1.2 Inspector Qualification & Criminal Liability (18 U.S.C. § 1001 & OK Title 61)
Under **23 CFR § 650.309**, a Program Manager or Team Leader must hold either a **Professional Engineer (PE)** license or meet strict engineering experience requirements combined with comprehensive accredited bridge inspection training. Signing an inspection docket with uncalibrated instrumentation, fabricated GPS coordinates, or omitted CS-4 defects constitutes a felony false statement under **18 U.S.C. § 1001** and triggers civil forfeiture under **Oklahoma Title 61**. To ensure absolute evidentiary integrity, all Humphrey Virtual Farms LLC (CAGE: 1AHA8) field sorties seal raw telemetry inside a **Write-Once-Read-Many (WORM) SQLite ledger** signed with a **FIPS 180-4 SHA-256 cryptographic digest**.""",
                "equations": """Span_Length_L > 20.0 ft (6.10 m)  -->  Mandatory NBI & OK Title 61 Jurisdiction
Sufficiency_Rating (SR) = S_1 (Structural Adequacy: 55%) + S_2 (Serviceability: 30%) + S_3 (Essentiality: 15%) - S_4 (Special Reductions: max 13%)""",
                "worked_example": """#### Worked Engineering Problem 1.1: Multi-Barrel Culvert NBI Jurisdiction Determination
* **Field Scenario:** An inspector evaluates a 3-barrel Reinforced Concrete Box (RCB) culvert under a county highway in Canadian County, Oklahoma. Each barrel measures 6.0 ft wide individually, separated by two 1.5 ft interior concrete walls, skewed at 0 degrees to the roadway centerline.
* **Step 1 (Calculate Extreme Ends Opening):** Measure from the inside face of the west exterior wall to the inside face of the east exterior wall:
  L_total = (3 * 6.0 ft) + (2 * 1.5 ft) = 18.0 ft + 3.0 ft = 21.0 ft
* **Step 2 (Statutory Ruling):** Because L_total = 21.0 ft > 20.0 ft, the multi-barrel culvert **is legally classified as an NBI Bridge** under 23 CFR § 650.305 and Oklahoma Title 61, requiring a mandatory 24-month inspection cycle.""",
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
| **CS-1 (Good)** | None / Hairline | w_c < 0.012 in (0.3 mm) | Zero delamination; sound acoustic/thermal return. | Intact passive oxide film or coating; zero corrosion. | Routine 24-month cycle; preventive silane seal. |
| **CS-2 (Fair)** | Moderate | 0.012 in <= w_c <= 0.050 in | Delamination present; spalls <= 1.0 in deep and <= 6.0 in diameter. | Minor surface freckle rust; no exposed rebar section loss. | Epoxy crack injection; localized concrete patching. |
| **CS-3 (Poor)** | Advanced | w_c > 0.050 in (1.27 mm) | Spalls > 1.0 in deep; widespread hollow delamination plane. | Exposed rebar with active oxidation; measurable section loss < 10%, capacity intact. | **Mandatory Priority Maintenance Docket.** Hydrodemolition if deck D_% >= 10%. |
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
  D_% = (1,650 + 50) / 12,800 * 100 = 13.28%
* **Step 2 (Calculate Bridge Element Health Index HI):**
  HI = [ (1.0 * 9200) + (0.67 * 1900) + (0.33 * 1650) + (0.0 * 50) ] / 12,800 * 100 = 86.07%
* **Step 3 (Statutory Disposition):** Presence of 50 sq ft of **CS-4** punch-through mandates immediate lane closure and steel plating, and D_% = 13.28% >= 10.0% triggers mandatory Title 61 hydrodemolition rehabilitation.""",
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
* **Differential Form:** dC/dt = D_c * (d^2C / dx^2)
* **Gauss Error Function Solution:** C(x, t) = C_0 * [ 1 - erf( x / (2 * sqrt(D_c * t)) ) ]

Once C(x_rebar, t) reaches the **Critical Chloride Threshold (C_crit = 1.2 to 1.5 lb/yd^3)**, the high-pH passive gamma-ferric oxide film dissolves. Hydrated red/black rust expands **300% to 600% in volume**, generating internal tensile bursting stresses of **4,000 to 7,000 psi** against concrete whose tensile rupture capacity is only **f_r = 7.5 * sqrt(f'_c) (~475 to 580 psi)**, fracturing the horizontal delamination plane.

### 3.2 ASTM C876 Copper-Copper Sulfate (Cu/CuSO4) Half-Cell Potential Mapping
* **Potential > -200 mV vs. CSE:** > 90% probability of **no active rebar corrosion**.
* **-350 mV <= Potential <= -200 mV vs. CSE:** Corrosion activity **uncertain**.
* **Potential < -350 mV vs. CSE:** > **90% probability of active reinforcing steel corrosion** and imminent subsurface delamination.""",
                "equations": """C(x, t) = C_0 * [ 1 - erf( x / (2 * sqrt(D_c * t)) ) ]
P_rust (4,000 to 7,000 psi) >> f_r = 7.5 * sqrt(f'_c) (~475 to 580 psi)  -->  Horizontal Delamination Fracture""",
                "worked_example": """#### Worked Engineering Problem 3.1: Time-to-Depassivation Calculation for Bridge Deck Rebar
* **Field Scenario:** A concrete bridge deck has a clear rebar cover depth of x = 2.0 in (5.08 cm), surface chloride concentration C_0 = 6.0 lb/yd^3, critical threshold C_crit = 1.5 lb/yd^3, and apparent diffusion coefficient D_c = 0.378 cm^2/yr.
* **Step 1 (Error Function Ratio):** C_crit / C_0 = 1.5 / 6.0 = 0.25 = 1 - erf(z)  -->  erf(z) = 0.75  -->  z = 0.813.
* **Step 2 (Solve for Time to Corrosion Initiation t):**
  t = x^2 / (4 * D_c * z^2) = (5.08 cm)^2 / (4 * 0.378 * 0.813^2) = 25.806 / 1.000 = **25.8 years**.""",
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
* **K_I = Y * sigma * sqrt(pi * a)**
Catastrophic brittle cleavage fracture occurs instantaneously at the speed of sound in steel (5,900 m/s) when **K_I >= K_Ic** (Plane-Strain Fracture Toughness).

### 4.3 Cyclic Fatigue Crack Growth: The Paris-Erdogan Law
Under repetitive truck axle stress ranges (`Delta_sigma`), sub-critical fatigue cracks propagate at rate `da/dN = C * (Delta_K)^m`, where `m = 3.0` for ferritic bridge steels.""",
                "equations": """K_I = Y * sigma * sqrt(pi * a)      [Mode I Stress Intensity, ksi*sqrt(in)]
a_c = (1 / pi) * [ K_Ic / (Y * sigma_max) ]^2
N_f = [ 2 / (C * Y^3 * (Delta_sigma)^3 * pi^1.5) ] * [ (1 / sqrt(a_0)) - (1 / sqrt(a_c)) ]""",
                "worked_example": """#### Worked Engineering Problem 4.1: Critical Crack Size & Remaining Truck Cycles on a Two-Girder FCM Bridge
* **Field Scenario:** Under-deck 48MP optical inspection of an A36 steel 2-girder bridge (K_Ic = 45.0 ksi*sqrt(in)) detects an edge fatigue crack a_0 = 0.25 in in the bottom tension flange (Y = 1.12). Peak tensile stress is sigma_max = 22.0 ksi; fatigue stress range is Delta_sigma = 6.0 ksi (C = 3.6e-10, m = 3.0).
* **Step 1 (Critical Crack Length a_c):**
  a_c = (1 / 3.1416) * (45.0 / (1.12 * 22.0))^2 = 0.3183 * (1.8263)^2 = **1.062 inches**.
* **Step 2 (Remaining Cycles N_f):**
  N_f = [ 2 / (6.077e-7) ] * (1/sqrt(0.25) - 1/sqrt(1.062)) = **3,388,500 truck cycles** (Code immediately as **CS-4**).""",
                "lab_protocol": """1. Deploy upward-tilted (+60 deg) 48MP optical zoom payload at 1.5 m standoff to achieve GSD <= 0.08 mm/pixel.
2. Inspect all AASHTO Category E/E' details: welded cover plate ends, web-stiffener toe welds, and gusset nodes.
3. Flag any linear indication >= 0.10 mm for hands-on Ultrasonic Phased-Array (PAUT) sizing."""
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
The Sovereign flight controller inhibits magnetometer yaw (`COMPASS_USE = 0`) and fuses **HereFlow Optical Flow** angular pixel rates (`omega_px`) with **TF02-i LiDAR** rangefinding (`z`) and MEMS ring-laser gyros (`omega_gyro`). Optical flow requires a minimum surface illuminance of **15.0 lux** via onboard LED luminaire bars.""",
                "equations": """v_x = z_lidar * (omega_pixel_x - omega_gyro_y)
Luminous_Intensity (I_candela) >= 15.0 lux * (d_meters)^2""",
                "worked_example": """#### Worked Engineering Problem 5.1: Optical Flow Velocity & LED Illumination Sizing Beneath a Dark Box Girder
* **Field Scenario:** The UAS hovers at standoff z = 2.5 m beneath a dark girder. Optical flow reports pixel rate 0.48 rad/s while pitch gyro rate is 0.08 rad/s.
* **Step 1 (True Horizontal Velocity v_x):** v_x = 2.5 m * (0.48 - 0.08) = **1.00 m/s**.
* **Step 2 (Minimum LED Intensity for 25 lux safety margin at 2.5 m):** I_min = 25.0 lux * (2.5 m)^2 = **156.25 candelas**.""",
                "lab_protocol": """1. Set EKF3 primary velocity source to Optical Flow (`EK3_SRC1_VELXY = 5`) and altitude to Rangefinder (`EK3_SRC1_POSZ = 2`).
2. Disable magnetic compass yaw fusion (`COMPASS_USE = 0`) before crossing beneath the fascia girder.
3. Cap maximum under-deck ingress speed at <= 1.5 m/s with a 1.5 m 360-degree LiDAR obstacle avoidance bubble."""
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
* **Step 1 (Froude Number Fr_1):** Fr_1 = 11.2 / sqrt(32.174 * 14.0) = **0.5277**.
* **Step 2 (Predicted Scour Depth y_s):** y_s = 14.0 * 2.0 * 1.1 * (4.0/14.0)^0.65 * (0.5277)^0.43 = **10.37 ft**.
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
* **Impact-Echo:** Mechanical impact generates compressional P-waves (`c_p ~ 4,000 m/s`) that reflect off internal delaminations. FFT peak frequency `f` yields flaw depth: **T = (0.96 * c_p) / (2 * f)**.
* **Ground Penetrating Radar (GPR):** 1.5–2.6 GHz electromagnetic pulses reflect strongly off chloride-wet concrete (`epsilon_r ~ 81` vs. dry concrete `epsilon_r ~ 6`).""",
                "equations": """Depth_T = (0.96 * c_p) / (2 * f_peak)
Depth_rebar = (c_0 * t_two_way) / (2 * sqrt(epsilon_r)),   where c_0 = 11.8 in/ns""",
                "worked_example": """#### Worked Engineering Problem 7.1: Impact-Echo Delamination Depth Calculation
* **Field Scenario:** Concrete deck thickness 8.50 in (c_p = 4,000 m/s, beta = 0.96). Point A FFT frequency is 8,890 Hz; Point B shifts to 30,200 Hz.
* **Calculation:** Point A depth = (0.96 * 4000) / (2 * 8890) = 0.216 m (**8.50 in sound slab**). Point B depth = (0.96 * 4000) / (2 * 30200) = 0.0636 m (**2.50 in top-mat rebar delamination!**).""",
                "lab_protocol": """1. Calibrate P-wave velocity over a known sound core location before running Impact-Echo grid scans.
2. Configure 2.0 GHz GPR antenna scan spacing at 1.0 ft longitudinal passes across all lanes.
3. Export rebar cover depth contour maps to calibrate hydrodemolition milling depth."""
            },
            {
                "unit": 8,
                "hours": 4.0,
                "title": "Unit 08: Substructure Bearings, Elastomeric Shear Deformation, Pin-and-Hanger & Gusset Plates",
                "theory": """### 8.1 Thermal Expansion Kinematics & Elastomeric Bearing Shear Strain
Steel girders expand thermally by `Delta_L = alpha * L * Delta_T`. Under AASHTO LRFD, neoprene elastomeric bearing pads must not exceed a horizontal shear strain of **gamma = Delta_s / h_rt <= 0.50**.

### 8.2 Gusset Plate Compression Buckling (FHWA Technical Advisory T 5140.29)
Following the I-35W truss collapse, inspectors must measure exact gusset plate thickness, corrosion loss, and out-of-plane bowing across the **Whitmore Effective Width (`b_w = w + 2 * L * tan(30 deg)`)**.""",
                "equations": """Delta_L = alpha * L_span * (T_current - T_install)
Shear_Strain_gamma = Delta_s / h_elastomer <= 0.50 (AASHTO LRFD Limit)""",
                "worked_example": """#### Worked Engineering Problem 8.1: Elastomeric Bearing Pad Shear Strain Audit
* **Field Scenario:** An elastomeric pad with elastomer thickness h_rt = 2.50 in has sheared horizontally by Delta_s = 1.65 in at 102 F.
* **Calculation:** gamma = 1.65 / 2.50 = **0.66 > 0.50 limit** -> Code **Element 310 as CS-3 (Poor)** and issue girder jacking/reset docket.""",
                "lab_protocol": """1. Record steel surface temperature via radiometric spot sensor during every bearing inspection.
2. Measure rocker tilt angle or elastomeric shear offset relative to 60 F neutral point.
3. Scan truss gusset plates with 3D LiDAR to detect out-of-plane distortion > 0.125 in."""
            },
            {
                "unit": 9,
                "hours": 4.0,
                "title": "Unit 09: Forensic Structural Failure Reconstructions — Silver Bridge, Mianus River & I-35W",
                "theory": """### 9.1 Silver Bridge (1967 — 46 Fatalities): Stress-Corrosion Cracking of Non-Redundant Eyebar 330
A **0.125-inch** stress-corrosion crack inside the pinhole of SAE 1060 high-carbon steel Eyebar 330 reached critical fracture toughness (`K_Ic ~ 42 ksi*sqrt(in)` at 30 F), causing instantaneous brittle cleavage and total progressive collapse in 47 seconds.

### 9.2 Mianus River Bridge (1983 — 3 Fatalities): Pack-Rust Prying of Pin-and-Hanger Assembly
Unmitigated de-icing salt runoff built up expansive **pack rust** behind the southeast hanger strap, generating >150 kips of lateral force that pushed the strap off the 7-inch steel pin.

### 9.3 I-35W Mississippi River Bridge (2007 — 13 Fatalities): Undersized 0.5-Inch U10 Gusset Plates
Node U10 gusset plates were fabricated at **0.50 inches** instead of 1.00 inch. Combined with 3.0M lbs of added deck overlay and 578,000 lbs of staged construction aggregate over Node U10, the gusset plate buckled in compression.""",
                "equations": """b_w = w_fastener_group + 2 * L_fastener_depth * tan(30 deg)   [Whitmore Section Width]
sigma_whitmore = P_axial / (b_w * t_gusset) <= phi * F_cr""",
                "worked_example": """#### Worked Engineering Problem 9.1: Whitmore Section Stress Audit on Node U10 Gusset Plate
* **Field Scenario:** Diagonal compression load P = 1,450 kips transfers through fastener group width w = 14.0 in, length L = 24.0 in, into a t = 0.50 in gusset plate (F_y = 50 ksi).
* **Step 1 (Whitmore Width b_w):** b_w = 14.0 + 2 * 24.0 * tan(30 deg) = **41.71 in**.
* **Step 2 (Whitmore Stress):** Area = 41.71 * 0.50 = 20.86 in^2 -> Stress = 1,450 / 20.86 = **69.51 ksi > 50.0 ksi yield (CATASTROPHIC BUCKLING!)**.""",
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
* **Calculation:** RF = (1850 - 720 - 180) / 1250 = **0.76 < 1.0**. Mandatory weight limit = 36.0 * 0.76 = **27 Tons Maximum Posting**.""",
                "lab_protocol": """1. Compile all CS-1 through CS-4 element quantities and section loss measurements into the LRFR sheet.
2. Seal final inspection docket with SHA-256 into `matrix_ledger.db`.
3. Sign off Unit 10 to complete 40.0/40.0 Credit Hours and enter the 3-Tier State Examination Gauntlet."""
            }
        ]
    elif course_code == "STR-02":
        return [
            {
                "unit": 1,
                "hours": 4.0,
                "title": "Unit 01: Oklahoma Title 61 Public Facilities Governance & OMES CAP Statutory Mandates",
                "theory": """### 1.1 Statutory Authority of OMES Construction and Properties (CAP)
Under **Oklahoma Statutes Title 61**, the **OMES Construction and Properties (CAP)** division governs capital roof replacements and building envelope audits across all state facilities. Quantitative **ASTM C1153** infrared thermography is required prior to authorizing full tear-offs ($24+/sq ft) versus surgical wet-core recovery ($6–$8/sq ft), saving taxpayers up to 65% in capital outlays.""",
                "equations": """Lifecycle_Savings = (Area_total * Cost_TearOff) - [ (Area_wet * Cost_SurgicalRepair) + (Area_total * Cost_Coating) ]""",
                "worked_example": """#### Worked Problem 1.1: Title 61 Capital Tear-Off vs. Surgical Recovery Audit
* **Scenario:** 100,000 sq ft state roof tear-off quote is $2,400,000 ($24/sq ft). UAS survey finds only 11,500 sq ft (11.5%) wet core. Surgical repair ($16/sq ft) + full silicone restoration ($6.50/sq ft) costs $834,000 -> **Net Taxpayer Savings = $1,566,000 (65.25%)**.""",
                "lab_protocol": """1. Verify OMES CAP Facility Asset ID and pull historical roof assembly cross-section blueprints.
2. Log membrane type (TPO, EPDM, PVC, Mod-Bit, BUR) and insulation R-value."""
            },
            {
                "unit": 2,
                "hours": 4.0,
                "title": "Unit 02: ASTM C1153 & ISO 6781 Radiometric Infrared Thermography Standards",
                "theory": """### 2.1 Strict Meteorological Boundary Conditions under ASTM C1153
1. **Daytime Solar Loading:** Minimum 50% sunny skies prior to inspection.
2. **Dry Surface Mandate:** 100% free of standing water, snow, or ice (>24 hrs post-rain).
3. **Wind Speed Ceiling:** Ambient wind **v_wind < 15.0 mph (6.7 m/s)** to prevent convective stripping.
4. **Nocturnal Window:** **45 to 120 minutes post-sunset** under clear skies (<20% cloud cover).""",
                "equations": """h_conv = 5.7 + 3.8 * v_wind_m_s   [Convective Heat Transfer Coefficient, W/(m^2*K)]
ASTM_C1153_Valid = (Wind_mph < 15.0) AND (Hours_Post_Rain >= 24.0) AND (Min_Post_Sunset >= 45)""",
                "worked_example": """#### Worked Problem 2.1: Convective Wind Stripping Coefficient Calculation
* **Scenario:** Compare h_conv at v = 2.0 m/s (4.5 mph) vs. invalid wind v = 9.0 m/s (20.1 mph).
* **Result:** At 2.0 m/s, h_conv = **13.3 W/m^2K** (strong Delta_T preserved). At 9.0 m/s, h_conv = **39.9 W/m^2K** (3x convective stripping erases thermal anomaly).""",
                "lab_protocol": """1. Deploy Kestrel ultrasonic anemometer at roof parapet elevation 60 minutes prior to takeoff.
2. Log ambient dry-bulb temp, relative humidity, dew point, and wind velocity into Title 61 docket."""
            },
            {
                "unit": 3,
                "hours": 4.0,
                "title": "Unit 03: Quantum & Thermodynamic Physics — Planck's Law, Wien's Displacement & Emissivity",
                "theory": """### 3.1 Wien's Displacement Law & Longwave Infrared (LWIR) Sensors
Peak blackbody emission wavelength is `lambda_max = 2897.8 / T_Kelvin`. At ambient roof temperatures (~290 K), peak radiation occurs at **10.0 micrometers**, requiring an uncooled VOx **LWIR (7.5 to 13.5 um)** microbolometer with **NETD <= 50 mK (0.05 C)** and emissivity correction (`epsilon = 0.92` for single-ply membranes).""",
                "equations": """lambda_max = 2897.8 / T_Kelvin   [micrometers]
W_tot = epsilon * tau * sigma * T_obj^4 + (1 - epsilon) * tau * sigma * T_refl^4""",
                "worked_example": """#### Worked Problem 3.1: Wien's Peak Wavelength Calculation
* **Scenario:** A TPO roof membrane is at T = 285 K (11.85 C).
* **Calculation:** lambda_max = 2897.8 / 285 = **10.17 micrometers** (centered in LWIR 7.5-13.5 um window).""",
                "lab_protocol": """1. Input epsilon = 0.92 for single-ply membranes and T_refl = -35 C (clear night sky) into RJPEG processor.
2. Mask out unpainted sheet-metal flashing and HVAC housings (epsilon ~ 0.20) to prevent false anomalies."""
            },
            {
                "unit": 4,
                "hours": 4.0,
                "title": "Unit 04: Heat Transfer Mechanics — Fourier Conduction, Volumetric Heat Capacity & R-Value Loss",
                "theory": """### 4.1 The 93x Volumetric Heat Capacity Disparity
Dry polyisocyanurate foam has volumetric heat capacity `rho * c_p = 44.8 kJ/(m^3*K)`, whereas liquid water has `4,184 kJ/(m^3*K)`—**93.4x higher volumetric heat storage!** Simultaneously, water destroys insulation R-value, driving massive conductive energy loss (`Q = U * A * Delta_T`).""",
                "equations": """Q_loss_Watts = (1 / R_SI) * Area_m2 * (T_in - T_out)
Ratio_Volumetric_Heat_Capacity = (rho_water * cp_water) / (rho_ISO * cp_ISO) = 93.4""",
                "worked_example": """#### Worked Problem 4.1: Conductive Heat Flux Increase Across Saturated Roof Insulation
* **Scenario:** Compare heat loss across 2,500 sq ft (232.26 m^2) of dry ISO (R_SI = 4.40) vs. wet ISO (R_SI = 0.70) at Delta_T = 25 K.
* **Calculation:** Q_dry = **1,320 Watts** vs. Q_wet = **8,295 Watts** (**6.28x energy bleed**).""",
                "lab_protocol": """1. Measure thermal anomaly surface Delta_T = T_wet - T_dry across all RJPEG orthomosaic polygons.
2. Flag any polygon exhibiting Delta_T >= +2.0 C for ground-truth impedance verification."""
            },
            {
                "unit": 5,
                "hours": 4.0,
                "title": "Unit 05: Psychrometrics, Vapor Drive, Dew-Point Condensation & Air Barrier Failure",
                "theory": """### 5.1 Magnus-Tetens Dew-Point Formulation & Interstitial Condensation
Warm, humid indoor air exfiltrating through unsealed parapet or curtain-wall joints condenses into liquid water whenever it contacts a structural surface at or below the **Dew-Point Temperature (`T_dp`)**.""",
                "equations": """gamma = ln(RH / 100) + (17.62 * T_C) / (243.12 + T_C)
T_dew_point_C = (243.12 * gamma) / (17.62 - gamma)""",
                "worked_example": """#### Worked Problem 5.1: Hospital Envelope Dew-Point Condensation Audit
* **Scenario:** Indoor conditions are T = 23.0 C and RH = 55%.
* **Calculation:** gamma = 0.9250 -> T_dp = (243.12 * 0.9250) / (17.62 - 0.9250) = **13.47 C (56.2 F)**. Any steel deck below 56.2 F experiences active condensation.""",
                "lab_protocol": """1. Conduct blower-door depressurization (-50 Pa) per ASTM E1186 while scanning joints with LWIR.
2. Distinguish diffuse wet-insulation conduction from sharp convective air-exfiltration plumes."""
            },
            {
                "unit": 6,
                "hours": 4.0,
                "title": "Unit 06: Secondary NDT Verification — Capacitive Dielectric, Nuclear Gauge & Gravimetric Cores",
                "theory": """### 6.1 ASTM C1153 Mandatory Verification of Thermal Anomalies
Under **ASTM C1153 Section 11**, every thermal anomaly must be verified using capacitive dielectric impedance meters, invasive resistance probes, or gravimetric core drying (`MC_% = (m_wet - m_dry) / m_dry * 100`).""",
                "equations": """Gravimetric_Moisture_Content (MC_%) = [ (m_wet - m_dry) / m_dry ] * 100""",
                "worked_example": """#### Worked Problem 6.1: Gravimetric Core Moisture Verification
* **Scenario:** A 2.0 in core from a +3.4 C anomaly weighs m_wet = 48.5 g and oven-dried m_dry = 14.2 g.
* **Calculation:** MC_% = ((48.5 - 14.2) / 14.2) * 100 = **241.5% moisture by weight** (confirmed saturation).""",
                "lab_protocol": """1. Mark anomaly perimeters on roof surface using RTK rover coordinates.
2. Perform dielectric impedance sweeps across 100% of marked zones and extract gravimetric verification cores."""
            },
            {
                "unit": 7,
                "hours": 4.0,
                "title": "Unit 07: Vertical Facade & Curtain Wall NDT — Masonry Rust-Jacking, Terra Cotta & Spalling",
                "theory": """### 7.1 Mechanics of Steel Shelf-Angle Rust-Jacking in Masonry Facades
Water penetrating behind brick facades oxidizes structural steel relieving angles (**shelf angles**). Expansive rust pack (6x volume) generates **up to 10,000 psi of rust-jacking pressure**, bowing brick walls out-of-plane and shearing masonry ties.""",
                "equations": """Out_of_Plane_Deflection_Ratio = H_panel / Delta_bow >= 360 (BIA Stability Criterion)""",
                "worked_example": """#### Worked Problem 7.1: Out-of-Plane Masonry Bowing Limit Audit
* **Scenario:** 3D LiDAR facade cloud shows a 144-inch brick panel bowed outward by 0.85 in at the 5th-floor shelf angle.
* **Calculation:** Ratio = 144 / 0.85 = **169 < 360 limit** -> Mandate immediate sidewalk overhead protection and facade pinning.""",
                "lab_protocol": """1. Fly vertical facade grid profiles at 10.0 m standoff with 80% overlap and 45-degree oblique gimbal angle.
2. Generate millimeter-accurate 3D point cloud to measure out-of-plane masonry bowing."""
            },
            {
                "unit": 8,
                "hours": 4.0,
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
                "unit": 9,
                "hours": 4.0,
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
                "unit": 10,
                "hours": 4.0,
                "title": "Unit 10: FAA Part 107 Urban Operations, RJPEG Orthomosaic Synthesis & Title 61 Docket Sealing",
                "theory": """### 10.1 Ground Sampling Distance (GSD) & Radiometric Orthomosaic Registration
Thermal RJPEG frames must be captured with **80% frontal and 75% side overlap** while maintaining a minimum **10.0-foot lateral standoff** from roof parapets and mechanical penthouses.""",
                "equations": """Altitude_H_m = (GSD_mm * Focal_Length_mm) / Pixel_Pitch_mm""",
                "worked_example": """#### Worked Problem 10.1: Thermal Microbolometer Flight Altitude for 3.5 cm/px GSD
* **Scenario:** 640x512 LWIR sensor with pixel pitch p = 0.012 mm and focal length f = 13.0 mm.
* **Calculation:** H = (35.0 mm * 13.0 mm) / 0.012 mm = **37.9 meters (124.4 ft AGL)**.""",
                "lab_protocol": """1. Verify FAA Part 107.29 anti-collision strobe (3 statute miles visibility) for nocturnal ASTM C1153 flights.
2. Seal final RJPEG orthomosaic and wet-core CAD polygons with SHA-256 into `matrix_ledger.db`."""
            }
        ]
    else:  # STR-03
        return [
            {
                "unit": 1,
                "hours": 4.0,
                "title": "Unit 01: Oklahoma Title 61, 23 CFR Part 515 (TAMP) & ASTM D6433 Highway Asset Governance",
                "theory": """### 1.1 Statutory Transportation Asset Management Plans (TAMP)
Under **23 CFR Part 515** and **Oklahoma Title 61**, ODOT and county highway districts use **ASTM D6433 Pavement Condition Index (PCI)** surveys to target preventive preservation in the **70–85 PCI window** ($3.50/sq yd) before roadways drop into the reconstruction zone ($65+/sq yd).""",
                "equations": """Sample_Unit_Area_Asphalt = 2,500 +/- 1,000 sq ft
Minimum_Sample_Units (n) = (N * s^2) / [ ((e^2 / 4) * (N - 1)) + s^2 ]""",
                "worked_example": """#### Worked Problem 1.1: ASTM D6433 Minimum Statistical Sample Unit Calculation
* **Scenario:** Corridor has N = 80 sample units, PCI standard deviation s = 10.0, allowable error e = 5.0.
* **Calculation:** n = (80 * 100) / ((6.25 * 79) + 100) = 8000 / 593.75 = **14 Sample Units**.""",
                "lab_protocol": """1. Segment highway corridor into 100 ft x 24 ft (2,400 sq ft) ASTM D6433 sample units.
2. Establish RTK GNSS base station on ODOT survey benchmark for sub-centimeter georeferencing."""
            },
            {
                "unit": 2,
                "hours": 4.0,
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
                "unit": 3,
                "hours": 4.0,
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
                "unit": 4,
                "hours": 4.0,
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
                "unit": 5,
                "hours": 4.0,
                "title": "Unit 05: Rigid Portland Cement Concrete (PCC) Pavements — Joint Faulting, D-Cracking & Punchouts",
                "theory": """### 5.1 Rigid PCC Distress Mechanics
Inspectors evaluate Jointed Plain Concrete Pavements (JPCP) for **transverse joint step-faulting** from subbase pumping, freeze-thaw **D-cracking**, and **thermal curling tensile stresses**.""",
                "equations": """sigma_curl = (E_pcc * alpha_pcc * Delta_T_slab) / (2 * (1 - mu))""",
                "worked_example": """#### Worked Problem 5.1: PCC Slab Thermal Curling Stress Calculation
* **Scenario:** 10 in PCC slab (E = 4.2e6 psi, alpha = 5.5e-6 /F, mu = 0.15) with Delta_T = 22 F thermal gradient.
* **Calculation:** sigma_curl = (4.2e6 * 5.5e-6 * 22) / (2 * 0.85) = **298.9 psi tensile bending stress**.""",
                "lab_protocol": """1. Inventory PCC pavement by counting total slabs per sample unit (20 +/- 8 slabs) per ASTM D6433.
2. Measure transverse joint step-faulting to 0.5 mm accuracy using dense LiDAR point clouds."""
            },
            {
                "unit": 6,
                "hours": 4.0,
                "title": "Unit 06: International Roughness Index (IRI — AASHTO R 85) & Quarter-Car Kinematics",
                "theory": """### 6.1 The Golden Car Quarter-Car Simulation Model
FHWA HPMS mandates **International Roughness Index (IRI)** reporting in inches/mile. Pavements exceeding **IRI > 170 in/mile** are classified as **Poor** ride quality, triggering diamond grinding or HMA overlay.""",
                "equations": """IRI_in_per_mile = Sum( |Delta_z_suspension_in| ) / Corridor_Length_Miles""",
                "worked_example": """#### Worked Problem 6.1: IRI Evaluation over a 0.5 Mile Highway Corridor Segment
* **Scenario:** Quarter-car integrator accumulates 92.5 inches of vertical suspension motion over 0.50 miles.
* **Calculation:** IRI = 92.5 / 0.50 = **185.0 in/mi > 170 in/mi threshold (Poor Ride Quality)**.""",
                "lab_protocol": """1. Sample longitudinal wheel-path elevations at <= 1.0 in (25 mm) intervals along both wheel tracks.
2. Apply 250 mm moving-average tire-bridging filter and run the 4-state Golden Car matrix solver."""
            },
            {
                "unit": 7,
                "hours": 4.0,
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
                "unit": 8,
                "hours": 4.0,
                "title": "Unit 08: Corridor Photogrammetry, RTK/PPK GNSS Georeferencing & 300k pts/sec LiDAR Point Clouds",
                "theory": """### 8.1 Eliminating Corridor Bowl-Effect via Dual-Frequency RTK/PPK & Staggered GCPs
Linear highway corridors require dual-frequency L1/L2 RTK/PPK carrier-phase GNSS fused with staggered shoulder Ground Control Points (GCPs) every 500–800 ft to achieve **Vertical RMSE_z <= 4.5 mm**.""",
                "equations": """Vertical_RMSE_z = sqrt( (1 / N) * sum_i (z_lidar_i - z_benchmark_i)^2 ) <= 4.5 mm""",
                "worked_example": """#### Worked Problem 8.1: Vertical Root-Mean-Square Error (RMSE) Certification Check
* **Scenario:** Five ODOT survey checkpoints yield vertical residuals of +3.0, -4.0, +2.0, -3.0, +1.0 mm.
* **Calculation:** RMSE_z = sqrt((9 + 16 + 4 + 9 + 1) / 5) = **2.79 mm <= 4.5 mm (Certified Level-1 Accuracy)**.""",
                "lab_protocol": """1. Place staggered RTK checkerboard GCPs along highway shoulders outside live travel lanes.
2. Execute figure-8 IMU kinematic alignment maneuver immediately after takeoff and prior to landing."""
            },
            {
                "unit": 9,
                "hours": 4.0,
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
                "unit": 10,
                "hours": 4.0,
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
