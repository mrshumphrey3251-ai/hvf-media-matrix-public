# Executive Engineering Directive - SEC-AUTH-HW-001
## Hardware Multi-Factor Operator Authentication Terminal (SEC-AUTH-HW)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-12 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Cryptographic Compliance
- Governing Standards: FIPS-201, FIPS-140-2 Level 2, NIST SP 800-63-3, ISO/IEC 19794-2, ISO/IEC 30107-3, MIL-STD-810H, MIL-STD-461G
- Hardware Architecture: ARM Cortex-M33 TrustZone MCU with TPM 2.0, FIPS-201 PIV/CAC contact smart-card reader (ISO 7816-3), and 500 dpi capacitive biometric fingerprint scanner
- Authentication SLA: Dual-factor presentation and enclave validation completed within <= 3.0 seconds

### 2. Encrypted OSDP v2 Enclave Communication
- Physical & Link Layer: Galvanically isolated (2 kV) RS-485 bus operating OSDP v2.2 up to 115.2 kbps
- Session Encryption: AES-128-CBC with per-session keys derived via HMAC-SHA256 KDF from TPM-anchored master key; automatic key rotation every 24 hours
- Session Auto-Lockout: Smart-card removal (`Card-Detect` transition) enforces workstation session lock and volatile key purge within <= 250 ms

### 3. Biometric Liveness & Anti-Spoofing Thresholds
- Accuracy Bounds: False Acceptance Rate (FAR) <= 0.0001%; False Rejection Rate (FRR) <= 0.5%
- Liveness Engine: Real-time capacitive waveform and pulse-width modulation liveness scoring (threshold >= 0.92) defending against 2D/3D silicone and latent spoofs
- Brute-Force Lockout: 5 consecutive failed attempts trigger a 30-minute hardware cool-down requiring CEO MFA override

### 4. Tamper-Evident Potted Enclosure & Power
- Physical Security: IP66 / NEMA-4X rack enclosure potted with color-change security epoxy (`EPO-TIT-X`) and dual magnetic/pressure tamper switches (<= 10 ms interrupt lockout)
- Isolated Power: 24V DC (+/- 10%) trailer bus input with polyfuse and MIL-STD-461G TVS surge suppression