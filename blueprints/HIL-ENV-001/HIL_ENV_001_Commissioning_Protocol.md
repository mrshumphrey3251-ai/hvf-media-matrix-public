# Executive Commissioning Directive - HIL-ENV-001
## NI PXIe-8510 Synthetic CAN-FD & Modbus-TCP Fault-Injection Protocol (HIL-ENV-03)
**Prepared by:** E.B.O.N.Y. - Sovereign AI Platform  
**Version:** 1.0 | **Date:** 2026-11-12 | **Status:** APPROVED (MFA Token: 515757)

### 1. Hardware & Bus Architecture
- **HIL Stack:** NI PXIe-1082 chassis, PXIe-8881 Xeon RTOS controller, PXIe-7868 Kintex-7 FPGA (`<= 2 us` jitter), PXIe-8510 dual-port CAN/CAN-FD & Modbus-TCP module, PXIe-6341 16-bit analog I/O, Keysight Infiniium (`1 GHz`, `10 GSa/s`), Crystal Group RS-Series WORM SQLite host
- **Target Under Test:** `ENV-PANEL-01` environmental sensor rack & `HMI-WALL-001` 7-display C2 Command Wall

### 2. Deterministic Fault-Injection Sequence (`S-00` to `S-08`)
- `S-00` (`0-200 ms`): CAN-FD ID sweep (`0x180`-`0x1FF`, `64-byte` DLC, `0xAA` pattern) with `CRC-16-CCITT (0x1021)` bit-23 flip every 16th frame
- `S-01` (`200-400 ms`): CAN-FD `CRC-32 (0x04C11DB7)` final-byte inversion every 8th frame (`0x55` pattern)
- `S-02` (`400-600 ms`): Modbus-TCP (`Port 502`) baseline `FC 0x03` Read Holding Registers (`Txn ID 0x0001`)
- `S-03` (`600-800 ms`): Modbus-TCP MBAP header corruption (`Txn ID 0xFFFF`, length `-2 bytes`) -> protocol reject verification
- `S-04` (`800-1000 ms`): Modbus-TCP `CRC-16 (0xA001)` bit-10 flip injection
- `S-05` (`1000-1200 ms`): `PT1000` Open-Circuit (`> 10 kOhm`, high-Z) -> `PT1000_OPEN` flag
- `S-06` (`1200-1400 ms`): `PT1000` Short-Circuit (`~0 Ohm`) -> `PT1000_SHORT` flag
- `S-07` (`1400-1500 ms`): Dual-channel `IEPE` accelerometer saturation (`+/- 10 V` square wave, `100 ms`) -> `IEPE_SAT` flag
- `S-08` (`1500-1600 ms`): Controlled return to nominal (`PT1000 = 100 Ohm`, `IEPE = 0 V`)

### 3. Escalation Latency & WORM SQLite Sealing
- **Latency Bounds:** FPGA injection to MCC Safety PLC alarm flag `<= 50 ms`; PLC alarm to `HMI-WALL-001` 7-display update `<= 50 ms`; end-to-end round-trip into WORM SQLite `<= 100 ms`
- **WORM Database:** `env_fault_log.db` (`PRAGMA journal_mode=WAL`) storing `utc_ts`, `src_module`, `frame_id`, `error_type`, `payload_hex`, sealed with SHA-256 Merkle root cross-checked against `matrix_ledger.db`