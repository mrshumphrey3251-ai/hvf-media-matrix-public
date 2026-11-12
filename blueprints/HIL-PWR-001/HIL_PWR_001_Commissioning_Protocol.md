# Executive Commissioning Directive - HIL-PWR-001
## NI PXIe Hardware-in-the-Loop Power-Chain Validation Protocol (HIL-PWR-01)
**Prepared by:** E.B.O.N.Y. - Sovereign AI Platform  
**Version:** 1.0 | **Date:** 2026-11-12 | **Status:** APPROVED (MFA Token: 515757)

### 1. Purpose & Closed-Loop Hardware Architecture
- **HIL Chassis:** NI PXIe-1082 (8-slot) + PXIe-8881 Xeon 8-core RT Controller + PXIe-7868 Kintex-7 FPGA (`<= 100 ns` jitter) + PXIe-8510 dual-port CAN/CAN-FD & Modbus-TCP
- **Powertrain Under Test:** Victron 480V 3-phase inverter (`150 kVA` continuous / `300 kVA` surge) and redundant `1200V -> 48V -> 24V` Wolfspeed SiC MOSFET DC-DC conversion chain (`BUS-24V-001`, `<= 2.33%` drop)
- **Instrumentation:** Keysight Infiniium (`1 GHz` BW, `10 GSa/s`, `<= 350 ps` rise time), `250 kW / 125 kVAR` programmable 3-phase load bank (`LOAD-TEST-01`), and IEC 61000-4-30 Class-A power analyzer (`10.0.0.20`)

### 2. Deterministic FPGA Stimulus Profile (`S-00` to `S-11`)
- `S-00` (`2 s`): System idle, outputs zeroed, GFD safety interlocks armed
- `S-01` (`500 ms`): Linear DC-bus ramp-up to `480 V`
- `S-02` to `S-07` (`5 s` each): Stepped load progression `0% -> 20% -> 40% -> 60% -> 80% -> 100%` (`0` to `250 kW` / `125 kVAR`)
- `S-08` (`3 s`): Overload stress at `110%` (`275 kW` / `137.5 kVAR`); verify `ALARM-VOLT-SAG` protection if `V < 440 V > 2 s`
- `S-09` (`2 s`): Grid-to-island transition via CAN-FD grid-present flag drop (`<= 20 ms` transfer, bus `>= 440 V`)
- `S-10` (`1 ms` pulse): `85 A` short-circuit fault injection on `1200V` SiC MOSFET bus; verify `36.75 ns +/- 0.5 ns` interlock propagation delay
- `S-11` (`500 ms`): Controlled DC-bus ramp-down to `0 V` and safety lockout

### 3. Transient Acceptance Thresholds & Oscilloscope Triggers
- **Transient Limits:** Voltage sag `<= 2%` at 20% load, `<= 3%` at 40%, `<= 4%` at 60%, `<= 5%` (`>= 456 V`) at 80–100% load; frequency deviation `<= 0.20 Hz`; Phase-A AC `THD <= 5%`
- **Keysight Capture Channels:** CH-1 Inverter L-L Phase-A (`1 GHz`, `10 GSa/s`), CH-2 `480V` DC-Bus (`480 V +/- 5 V` trigger), CH-3 SiC Gate-Driver (`500 MHz`, `100 ns/div`), CH-4 Inverter Output Current (`2 Mpts` record length, SHA-256 `.wfm` WORM sealing)