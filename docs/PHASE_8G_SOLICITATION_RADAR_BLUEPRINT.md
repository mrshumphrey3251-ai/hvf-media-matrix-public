# Phase 8g — Plug-and-Play Federal Solicitation Radar & SHA-256 WORM Hook Blueprint

- **Entity Legal Name:** HUMPHREY VIRTUAL FARMS LLC (`UEI: S1M4ENLHTDH5` | `CAGE: 1AHA8`)
- **Classification:** Public Redacted Architectural Blueprint (`ZERO_SECRETS_EXPOSED`)
- **Private Module Path:** `c2_cockpit/sam_solicitation_radar.py` (Subscribes to `c2_cockpit/sam_opportunity_monitor.py`)

## 1. Non-Destructive Plug-and-Play Extension (`register_hook`)
- `SamSolicitationRadarHook` attaches directly to `SamGovSovereignMonitor.register_hook()` without modifying a single line of the existing Phase 8f `sam_opportunity_monitor.py` codebase.
- Queries GSA's production Opportunities v2 API (`https://api.sam.gov/opportunities/v2/search`) across rolling 30-day windows while verifying the `api.sam.gov:443` TLS 1.3 leaf certificate expiration (`Nov 14 23:59:59 2026 GMT` ahead of the `Nov 10, 2026` GSA renewal).

## 2. Deterministic SHA-256 WORM Audit Chain
- Every radar execution hashes the prior entry's `worm_chain_sha256` with the current UTC timestamp, `UEI: S1M4ENLHTDH5`, TLS certificate `notAfter` timestamp, and active solicitation count into an untracked local JSONL WORM ledger (`c2_cockpit/logs/sam_radar_worm_ledger.jsonl`).
