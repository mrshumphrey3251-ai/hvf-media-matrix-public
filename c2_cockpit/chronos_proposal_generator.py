# -*- coding: utf-8 -*-
"""
EBONY CHRONOS: SOVEREIGN DEFENSE FUNDING PROPOSAL GENERATOR & SBIR COMPILER
Classification: PUBLIC RELEASE // REVISION v8.0 // CAGE: 1AHA8
Contracting Entity: HVF Omni-Industrial Matrix (CAGE: 1AHA8)
System Designation: Ebony Chronos (Operational Brevity: Chronos)
Statutory Standards: NIST SP 800-82 Rev 2 | MIL-STD-810H | HL7 FHIR | HIPAA / SaMD | DFARS 252.227-7018
Target Vehicles: DoD SBIR Direct to Phase II | Tradewinds Solutions Marketplace | OCAST
"""

import os
import json
from typing import Dict, Any, Optional

class ChronosProposalGenerator:
    """
    Public Funding Proposal Generator Interface for Ebony Chronos.
    [Proprietary WBS cost breakdowns and internal ledger telemetry REDACTED]
    """

    def __init__(
        self,
        node_id: str = "CHRONOS_SOVEREIGN_NODE_01",
        operator_callsign: str = "CEO Jeffery Humphrey",
        cage_code: str = "1AHA8",
        db_path: Optional[str] = None
    ):
        self.node_id = node_id
        self.operator_callsign = operator_callsign
        self.cage_code = cage_code
        self.db_path = db_path

    def generate_sbir_direct_phase_two_proposal(
        self,
        solicitation_topic: str = "AAL-D2P2-WARIGHTER-SENTINEL",
        requested_amount_usd: float = 1800000.0,
        period_of_performance_months: int = 18
    ) -> Dict[str, Any]:
        return {
            "proposal_title": "Ebony Chronos: Sovereign Multi-Modal Edge Sentinel (Public Contract)",
            "solicitation_topic": solicitation_topic,
            "contractor": "HVF Omni-Industrial Matrix",
            "cage_code": self.cage_code,
            "status": "PUBLIC_PROPOSAL_INTERFACE_ACTIVE",
            "data_rights": "DFARS 252.227-7018 (GPR)",
            "proposal_integrity_token": "PUBLIC_PROPOSAL_INTEGRITY_TOKEN_SHA256"
        }

    def export_proposal(self, filepath: Optional[str] = None) -> str:
        data = self.generate_sbir_direct_phase_two_proposal()
        out = filepath or os.path.join(".", "funding_engine", "CHRONOS_SBIR_PHASE_TWO_PROPOSAL.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return out


def _export_pdf_ChronosProposalGenerator(self, output_path=None) -> bytes:
    import json as _json
    from pathlib import Path as _Path
    import hvf_pdf_engine as _hpe
    payload = self.generate_sbir_direct_phase_two_proposal()
    title_str = payload.get("title") or payload.get("proposal_title") or "ChronosProposalGenerator Executive Deliverable"
    body_str = _json.dumps(payload, indent=2)
    art = _hpe.HVFSovereignPDFEngine().compile_sovereign_pdf(
        title=str(title_str),
        body_text=body_str,
        document_id="HVF-SBIR-PHASE2-1AHA8",
    )
    if output_path:
        _p = _Path(output_path)
        _p.parent.mkdir(parents=True, exist_ok=True)
        _p.write_bytes(art.pdf_bytes)
    return art.pdf_bytes

ChronosProposalGenerator.export_pdf = _export_pdf_ChronosProposalGenerator
