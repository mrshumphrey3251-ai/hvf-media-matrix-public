# Phase 8f/8g — Modular SAM.gov TLS Certificate & Opportunity Monitor Blueprint

- **Entity Legal Name:** HUMPHREY VIRTUAL FARMS LLC (`UEI: S1M4ENLHTDH5` | `CAGE: 1AHA8`)
- **Module Classification:** Public Redacted Architectural Specification (`ZERO_SECRETS_EXPOSED`)
- **Private Implementation Path:** `c2_cockpit/sam_opportunity_monitor.py` (Air-gapped inside `hvf-media-matrix-private`)

## 1. Architectural Purpose & Forward Compatibility
1. **Zero-Rewrite Hook Pattern (`register_hook`):** Future Phase 8g+ ingestion pipelines, SQLite WORM loggers, and SCADA telemetry triggers can subscribe directly to `SamGovSovereignMonitor` outputs without altering core authentication or socket logic.
2. **Air-Gapped Credential Resolution (`_load_local_env`):** Strictly reads `SAM_API_KEY` / `SAM_GOV_API_KEY` from untracked local `.env` vaults (`C:\hvf_c2\hvf-media-matrix-private\.env`). Zero credentials or tokens exist in source code.
3. **November 10, 2026 GSA TLS Certificate Renewal Readiness (`verify_tls_certificate`):** Inspects the live `api.sam.gov:443` X.509 certificate chain (`notAfter`, TLS protocol version, and cipher suite) prior to every automated API handshake.
