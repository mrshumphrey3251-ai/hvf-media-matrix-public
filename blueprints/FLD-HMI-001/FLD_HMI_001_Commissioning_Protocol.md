# FLD-HMI-001 - 7-Display C2 Command Wall & Zero-Trust Session Lock Commissioning Directive
## HMI-WALL-001 Matrix Switching (<= 100 ms) & SEC-AUTH-HW PIV/CAC + Biometric Lock (FLD-HMI-14)
**Program:** HVF Mobile Command Center (MCC) - Phase 3 | **CAGE:** 1AHA8  
**Author:** E.B.O.N.Y. (Core AI) - Authorized by Jeffery Humphrey, CEO | **Revision:** 1.0 - 2026-11-12

### 1. Display Matrix & Touch-Calibration Verification (`HMI-WALL-001`)
- **Display Array:** `1x 55-in` primary tactical center display + `6x 27-in` flanking interactive touchscreens (`VLAN 10` isolated video matrix)
- **Matrix Switching Latency:** Cross-panel source routing and KVM cursor handoff verified `<= 100 ms` via high-speed photodiode/oscilloscope capture
- **Touch-Calibration Accuracy:** Multi-point capacitive touch coordinate error `<= 1.5 mm` across all 7 panels (`ISO 9241-210` ergonomic compliance)

### 2. Zero-Trust Hardware Authentication & WORM Audit (`SEC-AUTH-HW`)
- **Dual-Factor Authentication Timeout:** Simultaneous PIV/CAC smartcard cryptographic challenge + biometric fingerprint match completed within `<= 500 ms`
- **Automatic Screen-Blank Session Lock:** Physical smartcard withdrawal triggers hardware screen-blanking and session lock across all 7 panels within `<= 250 ms`
- **WORM Audit Logging:** All authentication events, card-removal lock timestamps, and matrix switch logs sealed in `matrix_ledger.db` with CEO-level HMAC-SHA256