# Executive Engineering Directive - CABLE-001
## Shielded Power Cable Routing & Grounding Architecture (CABLE-SHIELD-001)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Voltage Domain Architecture
- Standard: IEC 60364-4-41, MIL-STD-461F, NEMA-4X
- Power Domains:
  - HV-DC: 1200V DC / 15A max (4x 25 mm^2 tinned copper, XLPE 150°C)
  - HV-AC: 480V 3-Phase AC / 200A max (3x 95 mm^2 + 1x 25 mm^2 neutral, XLPE 90°C)
  - LV-DC-48: 48V DC / 200A max (4x 35 mm^2 tinned copper, PVC 75°C)
  - LV-DC-24: 24V DC / 250A max (4x 25 mm^2 tinned copper, PVC 75°C)
  - Data-Air-Gap: 2x 0.5 mm^2 shielded twisted-pair (AWG 24, FEP 150°C, 1 Gbps+)

### 2. Shielding & Grounding Protocols
- Braided Shield Coverage: >= 85% optical coverage tinned-copper braid with 0.05mm aluminum foil backing
- Shield Impedance: <= 0.1 Ohm/m measured at 1 kHz (IEC 61000-5-2)
- Chassis Grounding Straps: Continuous >= 2 mm^2 tinned-copper braid clamped every 1.0 m to chassis (M8 studs, 12 Nm)
- Ground Loop Resistance: <= 0.05 Ohm total per strap verified by 4-wire Kelvin measurement
- Tray Bonding: 10 mm^2 copper lugs clamped to tray sections, linked via 0.5 mm^2 braided strap (<= 0.02 Ohm per joint)

### 3. Physical Tray Segregation & EMI Clearances
- HV-DC (1200V) to LV-DC (48V/24V): >= 300 mm center-to-center
- HV-AC (480V) to LV-DC (48V/24V): >= 250 mm center-to-center
- Power Trays to Air-Gapped Data: >= 500 mm physical clearance via isolated non-metallic roof conduit (> 80 dB attenuation)
- LV-48 to LV-24 Separation: >= 150 mm

### 4. Dynamic Bend-Radius Constraints (Mobile Transport)
- HV-DC (1200V): Minimum 10x OD (~250 mm); recommended <= 12x OD
- HV-AC (480V): Minimum 8x OD (~200 mm); recommended <= 10x OD
- LV-48 / LV-24: Minimum 6x OD (~130-150 mm); recommended <= 8x OD
- Air-Gap Data: Minimum 4x OD (~80 mm); recommended <= 6x OD