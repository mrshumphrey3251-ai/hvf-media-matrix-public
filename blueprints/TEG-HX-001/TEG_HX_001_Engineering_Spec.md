# Executive Engineering Directive - TEG-HX-001
## Heat-Recovery Exchangers Integrated with Waste-Heat TEG Modules (TEG-HX-INT)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** Rev A | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Thermal Interface & Gradient Modeling
- Waste-Heat Source: 12 kW Sensible Heat from 5-ton MIL-SPEC ECU Exhaust (150°C peak, 120°C steady-state)
- Target Hot-Side (Th): 120°C +/- 5°C
- Target Cold-Side (Tc): 30°C nominal (<= 35°C full-load limit)
- Design Thermal Gradient (Delta-T): 90°C baseline (up to 99°C nominal peak)

### 2. Thermoelectric Array Architecture
- Chemistry: Bismuth-Telluride (Bi2Te3) optimized for 25°C - 200°C range (peak ZT ~ 1.1)
- Total Array Size: 200 Modules (127mm x 127mm x 4mm each)
- Electrical Topology: 20 parallel strings of 10 series-connected modules
- Harvested Output: ~600 W electric power at 5% thermal-to-electric conversion efficiency

### 3. Closed-Loop Liquid Cooling Interface
- Coolant: 40% Propylene Glycol / 60% De-ionized Water (freeze protection to -20°C)
- Flow Rate: 2 L/min continuous closed loop via 24V DC brushless pump
- Heat Exchanger: Machined copper cold plates with 8 serpentine channels (1mm hydraulic diameter)

### 4. Electrical Bus & MPPT Integration
- Converter: 800W Synchronous Buck-Boost with Perturb-and-Observe MPPT (>= 95% efficiency)
- Output Bus: Selectable 24V / 48V DC Bus injection tied to Victron distribution side-car
- Telemetry: Modbus-TCP telemetry over Owl Cyber Defense Data Diode to SCADA