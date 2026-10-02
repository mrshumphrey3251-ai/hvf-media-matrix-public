# SOVEREIGN SPECIFICATION: RING 0 / LEVEL 5 PARTITION & GOVERNANCE
# CLASSIFICATION: TOP SECRET // COMMERCIAL DEFENSE STANDARD // COMMERCIAL LEASE MODEL
# REVISION: 1.0.0-GOLD

## 1. ARCHITECTURAL BOUNDARIES
- **Ring 0 (Sovereign Core - Read-Only):**
  - Path: /ebony_core/
  - Permissions: POSIX 0444 (Read-Only) locked to TPM 2.0 PCR-7.
  - Scope: Foundational LLM orchestration, cryptographic Merkle audit logger, chassis tamper zeroization monitors, and the CEO Authorization Gate.
  - Invariant: Zero write or modify permissions granted to any autonomous agent.

- **Level 5 (Autonomous Expansion Shell - Dynamic):**
  - Path: /sandbox_staging/ and /level5_extensions/
  - Permissions: Read/Write within isolated container jail.
  - Scope: Custom scrapers, SCADA modules, CRM workflows, code synthesis.
  - Isolation: No direct system calls to host OS. Communication strictly via typed RPC.

## 2. GOVERNANCE & NON-REPUDIABLE OPERATOR LIABILITY
- Ebony has full autonomy to generate, test, and debug code strictly within /sandbox_staging/.
- Deployment to /level5_extensions/ requires an explicit, cryptographic CEO Signature.
- All actions append to an immutable SHA-256 Merkle Ledger.
- The human operator assumes 100% legal and operational responsibility for approved executions.
