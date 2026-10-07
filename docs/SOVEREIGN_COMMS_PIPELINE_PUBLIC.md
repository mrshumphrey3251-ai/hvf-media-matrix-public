# HVFNEXUS SOVEREIGN COMMUNICATIONS PIPELINE SPECIFICATION
## STATUTORY FRAMEWORK COMPLIANT (OK TITLE 61 / OK HB 2992)

### 1. Cryptographic Key Architecture
- Master Key Management: Sovereign on-premise symmetric key isolation.
- Credential Storage: Encrypted dynamic database vault (`[REDACTED_DATABASE]`).
- Protection: Non-persisted transient decryption strictly scoped to active runtime execution.

### 2. Transport Protocol Specification
- Inbound Ingestion: Authenticated zero-trust IMAP (TLS 993) with inbound heuristic sender triage.
- Outbound Dispatch: Authenticated TLS SMTP (Port 465) with immutable ledger dispatch receipts.
- Integrity: Non-repudiation logging with hardware provenance tracking.

### 3. Sovereign Mesh Routing
- External Dispatch: Validated domain gateways for administrative compliance.
- Sovereign Node Mode: Air-gapped point-to-point packet routing (`node://<id>`).
### Dual-Mode Air-Gap Enforcement Update
- **Online Mode:** Authenticated TLS 1.3 socket transmission via external gateway.
- **Offline Sovereign Mode:** Strict local ledger queuing (`QUEUED_SOVEREIGN_LOCAL`) with zero-trust socket suppression and SHA-256 dispatch tracking.
