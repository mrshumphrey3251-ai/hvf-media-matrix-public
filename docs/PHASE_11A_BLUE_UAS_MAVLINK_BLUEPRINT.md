# Phase 11a -- Blue UAS MAVLink Hardware Abstraction Layer (HAL)

- **Entity Legal Name:** HUMPHREY VIRTUAL FARMS LLC (`UEI: S1M4ENLHTDH5` | `CAGE: 1AHA8`)
- **Classification:** Public Redacted Hardware Blueprint
- **Private Module Path:** `c2_cockpit/hardware_bridges/blue_uas_mavlink_bridge.py`

## Architecture Overview
This module acts as the physical translation layer between the sovereign E.B.O.N.Y. C2 software matrix and standardized DoD Blue UAS assets running PX4/ArduPilot. 
- Ingests the JSON ML GLI Confidence state at a polling rate of `1 Hz`.
- If confidence drops below the strict `0.85` threshold, the script generates a deterministic `MAV_CMD_NAV_RETURN_TO_LAUNCH` packet over radio serial telemetry, executing the 36.75ns Kinetic Guillotine parameter in physical airspace.
