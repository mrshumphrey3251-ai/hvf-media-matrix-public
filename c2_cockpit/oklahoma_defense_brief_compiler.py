# -*- coding: utf-8 -*-
"""
EBONY CHRONOS: OKLAHOMA STATE DEFENSE & AEROSPACE TRANSITION COMPILER
Classification: PUBLIC RELEASE // REVISION v8.0 // CAGE: 1AHA8
Contracting Entity: HVF Omni-Industrial Matrix (CAGE: 1AHA8)
System Designation: Ebony Chronos Sovereign Sentinel Platform
Target Entities: Oklahoma Aerospace & Defense Stakeholders
"""

import os
import json
from typing import Dict, Any, Optional

class OklahomaDefenseBriefCompiler:
    """
    Public Interface for Oklahoma State Defense Brief Compiler.
    [Proprietary economic formulas, grant budgets, and regional facility layouts REDACTED]
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

    def compile_oklahoma_package(self) -> Dict[str, Any]:
        return {
            "state_initiative": "Oklahoma Defense & Aerospace Economic Transition (Public Interface)",
            "contractor": "HVF Omni-Industrial Matrix",
            "cage_code": self.cage_code,
            "status": "PUBLIC_OKLAHOMA_INTERFACE_ACTIVE",
            "target_state": "Oklahoma",
            "data_rights": "DFARS 252.227-7018 (GPR)",
            "oklahoma_brief_integrity_token": "PUBLIC_OKLAHOMA_BRIEF_TOKEN_SHA256"
        }

    def export_package(self, filepath: Optional[str] = None) -> str:
        data = self.compile_oklahoma_package()
        out = filepath or os.path.join(".", "funding_engine", "OKLAHOMA_DEFENSE_TRANSITION_PACKAGE.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return out


def _export_pdf_OklahomaDefenseBriefCompiler(self, output_path=None) -> bytes:
    import json as _json
    from pathlib import Path as _Path
    import hvf_pdf_engine as _hpe
    payload = self.compile_oklahoma_package()
    title_str = payload.get("title") or payload.get("proposal_title") or "OklahomaDefenseBriefCompiler Executive Deliverable"
    body_str = _json.dumps(payload, indent=2)
    art = _hpe.HVFSovereignPDFEngine().compile_sovereign_pdf(
        title=str(title_str),
        body_text=body_str,
        document_id="HVF-OKLAHOMA-HB2992-1AHA8",
    )
    if output_path:
        _p = _Path(output_path)
        _p.parent.mkdir(parents=True, exist_ok=True)
        _p.write_bytes(art.pdf_bytes)
    return art.pdf_bytes

OklahomaDefenseBriefCompiler.export_pdf = _export_pdf_OklahomaDefenseBriefCompiler
