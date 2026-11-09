# COMPONENT SELECTION: AUTONOMOUS SENSOR & EDGE COMPUTE SUITE
**Contractor Entity:** Humphrey Virtual Farms LLC (CAGE: 1AHA8)
**System Sub-Assembly:** Project E.B.O.N.Y. Level-4/5 Autonomous Driving Core
**Sourcing Target:** Solid-State LiDAR, Imaging Radar, and Edge GPU Inference Server

---

## 1. TECHNICAL JUSTIFICATION FOR TACTICAL AUTONOMY
Per CEO directive, the E.B.O.N.Y. platform must function as an unmanned, autonomous logistical operator. In tactical environments, Global Positioning System (GPS) signals are routinely jammed or spoofed, and high-bandwidth cellular networks are non-existent.

To achieve Level-4/Level-5 autonomy in GPS-denied, off-road environments, the platform requires an air-gapped sensor suite capable of simultaneous localization and mapping (SLAM). The sensor data must be processed locally on the truck via a ruggedized Edge GPU, which then executes pathfinding algorithms and issues Controller Area Network (CAN) commands to the vehicle's Drive-by-Wire (DbW) interface.

## 2. PROCUREMENT SPECIFICATIONS
* **Edge Compute Core:** NVIDIA Jetson AGX Orin Industrial Module (Ruggedized, 248 TOPS AI performance, extreme shock/vibration tolerance).
* **Primary Spatial Sensor:** Ouster OS1 (or equivalent) Solid-State 3D LiDAR (120-meter range, high-resolution point cloud generation in dust/smoke).
* **Secondary Penetration Sensor:** Continental ARS540 (or equivalent) 4D Imaging Radar (For object detection through heavy precipitation and fog).
* **Network Interconnect:** Automotive Ethernet (1000BASE-T1) for ultra-low latency sensor fusion data transfer to the GPU.

## 3. NEXT ACTIONS
1. Issue formal Request for Quote (RFQ) to NVIDIA and Ouster authorized distributors for engineering samples.
2. Index the resulting $18,000 to $25,000 capital expenditure requirement for integration into the future SBIR Phase II prototype budget.