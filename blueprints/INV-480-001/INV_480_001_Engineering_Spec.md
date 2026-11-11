# Executive Engineering Directive - INV-480-001
## Victron 480V 3-Phase Inverter Integration with Modbus-TCP Telemetry (INV-480-MOD-001)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-11 | **Status:** APPROVED (MFA Token: 515757)

### 1. Power Envelope & Isolation Transformer Architecture
- Continuous Rating: 120 kW / 120 kVA (PF = 0.95 - 1.00)
- Peak Overload: 150 kW / 150 kVA (10s - 15s rating, 30% margin)
- Transformer Topology: Delta-Wye (480V L-L Delta Primary / 400V L-L, 230V L-N Wye Secondary with neutral chassis bond)
- Transformer Specs: Model TP-480-DW-120 (KORE Power, NDAA-compliant), Class H (180°C), Impedance Z <= 5%, forced air NEMA-4X
- Harmonics & Efficiency: Total Harmonic Distortion (THD) <= 3% (IEEE 519), Overall Efficiency >= 96%

### 2. Frequency Stabilization & Control Loop
- Nominal Frequency: 60 Hz +/- 0.1 Hz active digital PLL stabilization
- Reference Oscillator: Oven-Controlled Crystal Oscillator (OCXO) with redundant GPS-disciplined 10 MHz reference
- Lock Time & Droop: Lock time <= 200 ms; droop control at 0.5%/Hz for islanded parallel operations

### 3. DC Bus Tie-in & Energy Storage
- Source: KORE Power 500 kWh LFP Battery Bank (96% DoD, 1C discharge)
- Nominal DC Bus: 48V DC, 1,500A max; Custom DC-DC stage feeding inverter core

### 4. Modbus-TCP Telemetry Map (Port 502 / Default IP: 10.0.0.12)
- Reg 0x0000: Status Word (Bitfield: On/Off/Fault/Overload/Freq-Lock/Temp-Alarm)
- Reg 0x0002 / 0x0004 / 0x0006: Active (kW), Reactive (kVAR), Apparent (kVA) Power
- Reg 0x0008 - 0x000C: Line-to-Line Voltages (V_AB, V_BC, V_CA)
- Reg 0x000E - 0x0012: Phase Currents (I_A, I_B, I_C)
- Reg 0x0014: Output Frequency (Scale: 0.01 Hz, 6000 = 60.00 Hz)
- Reg 0x0016 / 0x0018 / 0x001A: DC Input Voltage, Current, and Battery SOC (%)
- Reg 0x0100: Control Word (Write-only: Start, Stop, Reset, Enable-Freq-Ctrl, Enable-PF-Ctrl)
- SCADA Ingest Rate: Polled at 500 ms interval via Owl Cyber Defense Data Diode