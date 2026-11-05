# Phase 11b -- 18kW Mobile Command Convoy SCADA Bridge (HAL)

- **Entity Legal Name:** HUMPHREY VIRTUAL FARMS LLC (`UEI: S1M4ENLHTDH5` | `CAGE: 1AHA8`)
- **Classification:** Public Redacted Hardware Blueprint
- **Private Module Path:** `c2_cockpit/hardware_bridges/convoy_modbus_scada_bridge.py`

## Architecture Overview
This module acts as the physical translation layer between the sovereign E.B.O.N.Y. C2 software matrix and the physical 18kW Solar / 500kWh Series-Electric microgrid.
- Utilizes `Modbus TCP` (Port 502) to poll industrial holding registers from standard Victron/SMA inverters and high-voltage Battery Management Systems (BMS).
- Aggregates physical telemetry (DC Bus Voltage, Amperage, and State of Charge) and securely bridges it into the air-gapped E.B.O.N.Y. JSON logging architecture for instant visualization by the Command Executive.
