# Phase 8h — Project Ebony NAICS 541715 Precision Filter Hook Blueprint

- **Entity Legal Name:** HUMPHREY VIRTUAL FARMS LLC (`UEI: S1M4ENLHTDH5` | `CAGE: 1AHA8`)
- **Classification:** Public Redacted Architectural Blueprint (`ZERO_SECRETS_EXPOSED`)
- **Private Module Path:** `c2_cockpit/sam_ebony_filter_hook.py`

## 1. Multi-Hook Chaining Architecture (8f -> 8g -> 8h)
- `SamEbonyFilterHook` registers as the second subscriber on `SamGovSovereignMonitor.register_hook()` immediately behind `SamSolicitationRadarHook` (Phase 8g).
- Neither `sam_opportunity_monitor.py` (Phase 8f) nor `sam_solicitation_radar.py` (Phase 8g) is modified—demonstrating strict O(1) plug-and-play extensibility.

## 2. NAICS `541715` R&D & Sovereign Patent-Claim Scoring
- Filters live `api.sam.gov/opportunities/v2/search` queries by `ncode=541715` (R&D in the Physical, Engineering, and Life Sciences) and ranks solicitations against Project Ebony's core hardware and cyber-physical domains.
