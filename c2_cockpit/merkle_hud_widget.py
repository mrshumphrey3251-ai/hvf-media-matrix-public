"""
HVF Sovereign C2 Cockpit Live WORM Merkle HUD Widget (CAGE: 1AHA8)
Modular telemetry component that reads live SHA-256 Merkle chain height,
latest block hash, and WORM integrity status from matrix_ledger.db (or Port 3000)
for real-time operator situational awareness.
"""
from pathlib import Path
import sys
import streamlit as st

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT / "scada_engine") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scada_engine"))

from merkle_ingest_bridge import SovereignMerkleLedger


def render_merkle_chain_badge(db_path: Path | None = None) -> dict:
    """Render live WORM SHA-256 Merkle ledger status badge in the C2 sidebar/cockpit."""
    ledger = SovereignMerkleLedger(db_path)
    audit = ledger.audit_chain()
    status_label = "VERIFIED INTACT (WORM)" if audit.get("valid") else "INTEGRITY ALERT"
    head_short = str(audit.get("merkle_head", ""))[:16]
    height = int(audit.get("chain_height", 0))

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"**🔐 WORM Merkle Ledger:** `{status_label}`  \n"
        f"**Blocks Sealed:** `{height}` | **Head:** `{head_short}...`"
    )
    return audit