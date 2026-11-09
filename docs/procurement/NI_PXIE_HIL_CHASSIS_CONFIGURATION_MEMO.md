# HIL BENCHTOP COMPONENT SELECTION: NI PXIe CHASSIS
**Contractor Entity:** Humphrey Virtual Farms LLC (CAGE: 1AHA8)
**System Sub-Assembly:** Project E.B.O.N.Y. Hardware-in-the-Loop (HIL) Simulation Core
**Sourcing Target:** National Instruments (NI) PXIe-1082 Chassis with Real-Time Controller

---

## 1. TECHNICAL JUSTIFICATION FOR PHASE I HIL TESTING
To safely validate the Wolfspeed Silicon Carbide (SiC) MOSFET circuit protection without risking catastrophic failure on a live 480V/150kW Class-8 powertrain, Humphrey Virtual Farms LLC requires a deterministic Hardware-in-the-Loop (HIL) simulator. 

A standard commercial operating system cannot provide the nanosecond-level deterministic timing required to trigger the SiC gate drivers during a simulated arc-fault. The NI PXIe system utilizes a Real-Time Operating System (RTOS) and Field-Programmable Gate Arrays (FPGAs) to achieve strict timing closures.

## 2. PROCUREMENT SPECIFICATIONS
* **Core Chassis:** NI PXIe-1082 (8-Slot, High-Bandwidth Backplane).
* **System Controller:** NI PXIe-8840 Quad-Core Real-Time Controller.
* **Digital I/O (Gate Drive Control):** NI PXIe-7820R (Kintex-7 FPGA for <10ns pulse-width modulation generation).
* **Analog Input (Voltage/Current Sensing):** NI PXIe-6363 (Simultaneous sampling for phase current/voltage monitoring).
* **Communication Interface:** NI PXIe-8510 (High-Speed Controller Area Network [CAN] interface for simulated J1939 vehicle telemetry).

## 3. NEXT ACTIONS
1. Submit the configuration to the National Instruments regional sales engineering team for a formal quote.
2. Allocate $38,500.00 from the Phase I Volume 3 Cost Budget for chassis, modules, and LabVIEW Real-Time software licensing.