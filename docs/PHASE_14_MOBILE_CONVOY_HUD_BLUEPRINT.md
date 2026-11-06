# Phase 14 -- Unified Mobile Command Convoy Tactical HUD

- **Entity Legal Name:** HUMPHREY VIRTUAL FARMS LLC (`UEI: S1M4ENLHTDH5` | `CAGE: 1AHA8`)
- **Classification:** Public Redacted C2 Blueprint
- **Private Module Path:** `c2_cockpit/pages/18_mobile_convoy_hud.py`

## Architecture Overview
Phase 14 projects the Phase 11 and Phase 13 Hardware Abstraction Layers (HAL) onto the tactical glass. The Unified Mobile Convoy HUD ingests multi-protocol edge telemetry (J1939 CAN-bus, Modbus TCP, MAVLink) and visualizes it inside a single, air-gapped Streamlit interface. 
This provides the Level-5 Command Executive with immediate, mathematically verified situational awareness of the physical Prime Mover, the 18kW Microgrid, and the Blue UAS Airspace, alongside the live arming status of the 36.75ns SiC MOSFET Kinetic Guillotine.
