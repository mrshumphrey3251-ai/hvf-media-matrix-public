# STR-01: Bridge Deck, Pier & Fracture-Critical Member Inspection
**Official Master Technical Textbook // Sovereign Field Academy**
**Course Duration:** 40 Hours | **Statutory Framework:** Oklahoma Title 61 & ODOT NBI

## MODULE 1: ODOT NBI & AASHTO ELEMENT-LEVEL DEFECT CLASSIFICATION
### 1.1 The AASHTO Condition State (CS) Framework
To standardize bridge safety, the National Bridge Inventory (NBI) requires elements to be graded on a 4-tier Condition State (CS) scale:
* **Condition State 1 (Good):** The structural member operates at its original design capacity. Only minor weathering or cosmetic anomalies exist.
* **Condition State 2 (Fair):** Minor surface degradation. For concrete, this means minor spalling or hairline cracking (<0.04 inches) without section loss. For steel, minor surface rust without pitting.
* **Condition State 3 (Poor):** Advanced section loss or structural distress. For concrete, this includes severe delamination and spalling with exposed reinforcing steel. **CS-3 mandates priority maintenance docketing.**
* **Condition State 4 (Severe):** Critical structural defects affecting the load-carrying capacity of the element. **CS-4 requires immediate emergency closure or load restriction protocols.**

### 1.2 Mathematical Defect Calculation & Title 61 Mandates
When assessing concrete bridge decks, inspectors must calculate the Concrete Deck Delamination Percentage (D_%). Delamination occurs when subsurface rebar oxidizes and expands, separating the upper concrete layer.

**Formula:**
D_% = (Area_delam / Area_total) * 100

**Statutory Mandate:** If D_% >= 10.0%, the deck is structurally compromised. Oklahoma Title 61 capital rehabilitation programs mandate immediate hydrodemolition (high-pressure water jet removal of decayed concrete) followed by a latex-modified concrete overlay.

## MODULE 2: GPS-DENIED UNDER-DECK FLIGHT OPERATIONS
### 2.1 Overcoming Faraday Shielding & Magnetic Declination
Flying a UAS directly beneath a reinforced concrete deck or steel truss induces severe signal degradation:
* **Faraday Shielding:** The steel rebar grid blocks satellite GNSS signals, causing the drone to drop below the minimum required 4 satellites for position hold.
* **Magnetic Declination Anomalies:** Structural steel girders distort the earth's magnetic field, causing the flight compass to drift uncontrollably. 
* **The Solution:** The primary flight controller must disengage satellite hold and fuse internal gyros with downward LiDAR rangefinding and optical flow.

### 2.2 Optical Flow Navigation Physics
The HereFlow optical flow sensor acts as a downward-facing camera, tracking the physical displacement of pixels on the ground to calculate velocity (Delta x / Delta t).
* **Illumination Constraint:** Optical flow requires contrast. You must maintain a **minimum of 15 lux** of surface illumination using on-board LED luminaire bars when inspecting dark, shaded girders.
* **Flight Protocol:** Approach the abutment at a maximum ingress speed of **1.5 m/s**. Maintain a 15-minute GPS-denied hover within +/- 0.2 meters lateral tolerance while keeping a 360-degree LiDAR obstacle avoidance bubble active.

## MODULE 3: PIER SCOUR & FRACTURE-CRITICAL NDT
### 3.1 Hydrologic Pier Scour Bathymetry (ODOT Item 113)
Scour is the erosive removal of riverbed sediment around bridge substructures caused by swift hydrologic flow. 
* **Deployment:** Deploy a down-looking acoustic single-beam sonar (200 kHz) suspended 1.0 meter above the water line.
* **Scour Depth Formulation:**
d_s = y_0 - y_bed
*(Where y_0 is the historical baseline riverbed elevation, and y_bed is the current sonar depth return).*
* **Emergency Trigger:** If the calculated scour depth (d_s) exceeds the foundation footing depth, the bridge is declared scour critical and an emergency structural stabilization docket is issued.

### 3.2 Fracture-Critical Member (FCM) Inspection
A Fracture-Critical Member is a steel component in tension whose failure would result in the partial or total collapse of the bridge.
* Inspectors deploy 48MP optical zoom photogrammetry to detect and size fatigue-induced micro-cracks in tension flanges down to **0.1mm** in width.
* Ultrasonic testing is deployed to measure shear-wave acoustic velocity, identifying concealed micro-fissures in welded details.