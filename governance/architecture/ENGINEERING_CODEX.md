# PROJECT EBONY - SOVEREIGN ENGINEERING CODEX & GOVERNANCE
# ROLE: Autonomous coding standard, error correction rules, and architectural invariants.
# REVISION: 1.0.0-GOLD

## 1. ABSOLUTE SYSTEM INVARIANTS
1. **Ring 0 Immutability:** Never attempt to modify, rename, or import files from root or Ring 0 with write intent.
2. **Zero-Sprawl Isolation:** All new tools and extensions MUST reside entirely within `level5_extensions/`. Every script must be completely self-contained.
3. **No External Cloud Bleed:** Do not introduce unvetted third-party cloud SDK dependencies. Use Python standard library or existing pre-verified packages.
4. **Non-Repudiation:** No code is promoted to `level5_extensions/` without a signed Executive Action Memo approved by the CEO.

## 2. LEVEL 5 MODULE STRUCTURE STANDARD
Every Level 5 autonomous module must expose:
- `MODULE_METADATA`: Dict containing name, version, author ("EBONY-AUTONOMOUS"), and description.
- `execute(context: dict) -> dict`: Standard entry point returning a status dictionary with keys `success`, `output`, and `telemetry`.
- `render()`: Optional Streamlit rendering function if the module includes a UI dashboard.

## 3. AUTONOMOUS REPAIR & DEBUG PROTOCOL
When an execution fails inside `sandbox_staging/`:
1. Parse the `traceback` and `stderr` returned by `sandbox_harness.py`.
2. Cross-reference against this Codex to check for syntax violations or path misconfigurations.
3. Rewrite the target file inside `sandbox_staging/` to correct the flaw.
4. Maximum autonomous retry limit is 3 attempts. If failure persists, escalate with an Executive Incident Memo to the CEO detailing the root cause.
