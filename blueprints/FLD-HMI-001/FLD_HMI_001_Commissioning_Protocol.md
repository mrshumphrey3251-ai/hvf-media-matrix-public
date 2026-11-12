# HVF Omni-Industrial Matrix - Executive Commissioning Directive (FLD-HMI-001)
## 7-Display C2 Command Wall (HMI-WALL-001) & SEC-AUTH-HW Zero-Trust Session Lock (FLD-HMI-14)
**Program:** HVF Mobile Command Center (MCC) - Phase 3 Field Commissioning | **CAGE:** 1AHA8  
**Prepared By:** E.B.O.N.Y. - Sovereign AI Core | **Authorized By:** Jeffery Humphrey, CEO | **Date:** 2026-11-12

### 1. Quantitative Acceptance Matrix (Concurrent Integrated Run)
1. **Matrix Switching Latency (`HMI-WALL-001`):** `<= 100 ms` (99th-percentile across `30x` random source-to-display pairs; oscilloscope trigger to first-pixel change across `55-in` center + `6x 27-in` flanking displays)
2. **PIV/CAC Smartcard Authentication (`SEC-AUTH-HW`):** `<= 500 ms` card insertion to OS-level certificate-validated session (`20x` user certificates)
3. **Biometric Fingerprint Verification (`SEC-AUTH-HW`):** `<= 500 ms` capture-to-match confirmation (`20x` enrolled prints)
4. **Automatic Screen-Blank Session Lock:** `<= 250 ms` from physical smartcard removal to all 7 displays entering blank-lock with input disabled (`15x` pull cycles)
5. **Touch-Calibration Accuracy:** `<= 2.0 mm` RMS positional deviation across `10 mm` automated test grid (`touch_calibrate.py`) on each of the 7 touchscreens
6. **WORM Audit Logging (`audit_worm_mode = true`):** `100%` of session auth and matrix switch events sealed in `matrix_ledger.db` with SHA-256 hash continuity and active tamper rejection

### 2. Controlled Artifacts & Merkle Sealing
- Baseline config `hmi_wall_config_master.json` (firmware `v3.2.7-SEC-HMI-001`), raw oscilloscope traces, calibration plots, and `audit_worm_root.sha256` sealed under CEO-level HMAC-SHA256 (`SBIR-CEO-20`)