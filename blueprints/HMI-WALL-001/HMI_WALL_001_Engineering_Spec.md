# Executive Engineering Directive - HMI-WALL-001
## 7-Display C2 Tactical Command Wall & Seamless Multi-Viewer Matrix (HMI-WALL-001)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Display Wall Topology
- Governing Standards: MIL-STD-810H, MIL-STD-3009 (NVIS), UL 508A, IEC 60364-5-52, CISPR 22 Class B
- Center Theater Display: 1x 55-inch 4K UHD (3840x2160, 60 Hz, IP65) ruggedized primary canvas
- Flanking Touchscreens: 6x 27-inch industrial 10-point capacitive touchscreens (3 stacked left, 3 stacked right) on Aluminum 6061-T6 structural bulkhead frame
- Control Interface: 12-inch Ethernet-IP industrial HMI console running PyQt5 C2 routing matrix UI

### 2. Zero-Latency Multi-Viewer Matrix Switching
- Switcher Core: 8x8 Zero-Latency HDMI 2.0 / DisplayPort 1.4 Multi-Viewer Matrix (< 1 ms switching latency)
- One-Touch "Throw-to-Main": Single-button Modbus-TCP register write (`FC 0x10`, Register `0x0010 = 0x0001`) instantly routes any flanking feed to the 55-inch center screen
- 2x2 Quad-Split Tiling: Register `0x0011 = 0x0001` divides the 55-inch display into four independent 25% quadrants mapped to operator-selected feeds

### 3. Unidirectional Optical Video Isolation
- External Feed Air-Gap: External live news and NOAA weather radar feeds enter via an HDMI-to-LC-SFP optical video data diode (`< -70 dBm` reverse optical sensitivity) upstream of the matrix switcher
- Back-Channel Elimination: Zero USB/HID or Ethernet return paths permitted between external video sources and internal compute (`VLAN 10`)

### 4. Shock-Mounting, NVIS Bonding & Isolated 24V DC Power
- Shock & Vibration Isolation: 7x wire-rope shock-mount brackets (`FASTEN-W-Rope-001`, +/- 15g shock, 2 Hz - 2 kHz damping) with PT100 thermal telemetry tied to the 5-ton ECU
- Optical Bonding: MIL-STD-3009 NVIS UV-cured optical bonding (0.5 mm glass, <= 2% internal reflection)
- Power & UPS: Galvanically isolated 24V DC distribution bus (1 kV SiC MOSFET isolation, 5A dedicated UL 508A breaker per display) backed by a 500 Wh LiFePO4 24V UPS (>= 30 min runtime)