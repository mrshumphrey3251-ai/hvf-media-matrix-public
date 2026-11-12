# Executive Engineering Directive - UI-STACK-001
## Operator Console Software Stack - 7-Display C2 Command Wall (UI-STACK-001)
**Prepared by:** E.B.O.N.Y. - Project Management Interface  
**Version:** 1.0 | **Date:** 2026-11-12 | **Status:** APPROVED (MFA Token: 515757)

### 1. Scope & Air-Gapped Container Architecture
- Governing Standards: CIS RHEL 9 Benchmark Level 2, NIST SP 800-53 Rev 5 (AC-3, AU-9, SC-7)
- Host Environment: Hardened RHEL 9 with SELinux enforcing, KVM isolation, and dedicated physical 10 GbE NICs mapped to VLAN 10 (SCADA Control Plane), VLAN 20 (E.B.O.N.Y. AI Inference UI), and VLAN 30 (Telemetry Dashboard)
- Container Hardening: Read-only rootfs, default-deny seccomp/AppArmor profiles, cosign RSA-4096 image signature verification, and outbound host firewall drop policy (`iptables -A OUTPUT -j DROP`)

### 2. Deterministic 60 FPS Multi-Display Rendering Pipeline
- Center Theater Display (55-in 4K UHD): WebGL 2.0 rendering engine locked to 60 Hz (<= 16.6 ms 99th-percentile frame budget)
- Flanking Touchscreens (6x 27-in QHD): PyQt5 + OpenGL-ES 3.0 hardware-accelerated touch interface (<= 30 ms tap-to-response latency)
- Real-Time Scheduling: Dedicated CPU core pinning (`isolcpus`), `SCHED_FIFO` priority 99 rendering threads, and forced V-Sync (`glXSwapIntervalEXT(1)`)

### 3. Zero-Trust RBAC & Session Management
- Authentication & Authorization: Mutual-TLS OpenLDAP + Kerberos authentication with Open Policy Agent (OPA) JWS-signed policies evaluated per request by Envoy mTLS sidecars
- Token Lifecycle: 5-minute short-lived JWTs signed by HSM-protected RSA-4096 key with granular per-display and per-service role enforcement

### 4. Local WORM Telemetry Store & Cryptographic Audit
- Storage Engine: Append-only Apache Iceberg tables over ClickHouse backed by 4 TB T10-PIE hardware-enforced Write-Once-Read-Many (WORM) NVMe storage
- Integrity & Retention: 5-year immutable retention; every ingested telemetry batch hashed (SHA-256) and anchored to `MERKLE_AUDIT_LEDGER.json`