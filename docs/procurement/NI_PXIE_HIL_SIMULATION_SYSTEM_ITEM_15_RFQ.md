# HVF Procurement: National Instruments PXIe HIL Simulation System (Item 15) RFQ
**Issuing Entity:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)  
**Budget Allocation:** $48,000.00 (CapEx, Contractor-Acquired Property)  
**Target Vendors:** National Instruments (Emerson Test & Measurement) / OPAL-RT / Speedgoat  

## Technical Requirements
- **Chassis & Controller:** PXIe-1082 or PXIe-1092 8-slot high-bandwidth chassis with PXIe-8881 Intel Xeon 8-Core Embedded Real-Time Controller.
- **FPGA Reconfigurable I/O:** PXIe-7868 or PXIe-7858 Kintex-7 FPGA module for deterministic sub-microsecond electrical transient and arc-flash emulation.
- **Multifunction I/O:** 16-channel analog input (minimum 1 MSa/s, 16-bit resolution) and 8-channel analog output with isolated high-voltage breakout terminal blocks.
- **Communication Bus Modules:** PXIe-8510 dual-port isolated CAN / CAN-FD and Modbus TCP interfaces for real-time turbine/BMS/inverter telemetry closed-loop simulation.
- **Operating Environment:** Runs NI Linux Real-Time locally with 100% offline license deployment; zero reliance on continuous external cloud or subscription licensing.
- **HIL Capability:** Hard-real-time closed-loop loopback testing to verify the 36.75ns SiC kinetic gate trip without hazardous live 480V/750V arc-flash energy exposure.
