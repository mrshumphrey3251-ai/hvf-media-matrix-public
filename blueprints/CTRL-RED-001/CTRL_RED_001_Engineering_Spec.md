# Executive Engineering Directive - CTRL-RED-001
## Dual-Redundant Hall-Effect 3-Axis Joystick & IP68 Trackball Controls (CTRL-RED-01)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-12 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Environmental Envelope
- Governing Standards: MIL-STD-810H, MIL-STD-461F (Category 2), ISO-11898-1 (CAN-FD), SAE J1939, IEC 60364-4-41
- Ingress & Mechanical Tolerance: IP68 sealed aluminum chassis (1m immersion / 30 min), 30g 10ms shock, 0.5g RMS vibration (10-2000 Hz), -40°C to +85°C operational range
- Primary Role: Deterministic drive-by-wire vehicle actuation and multi-agent drone swarm C2

### 2. Dual-Die Hall-Effect & Trackball Sensing
- 3-Axis Joystick: Non-contact dual-die Hall-effect sensor stacks (TI TLE493D-W2B6), <= 0.2% full-scale non-linearity
- FPGA Sensor Fusion: Xilinx Artix-7 12-bit oversampling (2 kS/s) with 100 us cross-die fault detection and automatic channel masking (> 5% divergence triggers J1939 PGN 65260 fault flag)
- Ruggedized Trackball: 30 mm IP68 optical encoder (500 cpr, >= 0.01 mm resolution at 200 dpi) with sealed ceramic bearings

### 3. Dual-Channel CAN-FD Bus Redundancy & Latency
- Bus Architecture: Redundant dual-channel CAN-FD (NXP TJA1463 transceivers, 500 kbps arbitration / 2 Mbps data phase) carrying mirrored SAE J1939 PGN 65260 frames
- Failover & Isolation: < 1 ms automatic channel switchover on bus-off detection; 1 kV galvanic isolation between power and CAN domains
- End-to-End Loop Latency: <= 4.8 ms (99th percentile; 4.3 ms worst-case measured sensor-to-actuator PWM output)

### 4. Dead-Man Interlocks & Hardware E-Stop Integration
- Operator Presence: Capacitive dead-man plate (auto safe-stop if signal lost > 50 ms) paired with a 30N mechanical spring-loaded override switch
- Physical E-Stop: Hard-wired normally closed (NC) 24V DC stainless-steel lever and secondary IP68 panic button tied directly to Master Safety PLC (<= 2 ms trip latency) with power-on BIST continuity verification
- Redundant Power: Dual-input 24V DC primary bus with automatic 12V-to-24V boost failover (< 150 ms)