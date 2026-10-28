# -*- coding: utf-8 -*-
"""
HUMPHREY VIRTUAL FARMS LLC // TRADEWINDS DOCKET 10-26-3976 ON-SCREEN VIDEO TELEPROMPTER
Displays the Mandatory Assessor Feedback Resolution Matrix & Section VII.e Rubric Segments
on screen for video capture while executing live TRL 4 software verification.
"""
from pathlib import Path
import sys

COCKPIT_DIR = Path(__file__).resolve().parent
if str(COCKPIT_DIR) not in sys.path:
    sys.path.insert(0, str(COCKPIT_DIR))

import tradewinds_pitch_compiler as tpc


class BriefingTeleprompterConsole:
    def __init__(self, cage_code: str = "1AHA8", **kw) -> None:
        self.cage_code = cage_code
        self.compiler = tpc.TradewindsPitchCompiler(cage_code=cage_code)

    def get_full_presentation_manifest(self) -> dict:
        return {
            "cage_code": self.cage_code,
            "uei": "S1M4ENLHTDH5",
            "active_docket": "10-26-3976",
            "prior_docket": "9-26-3703",
            "readiness_level": "TRL 4",
            "status": "PUBLIC_TELEPROMPTER_INTERFACE_ACTIVE",
            "data_rights": "DFARS 252.227-7018 (GPR)",
            "assessor_feedback_resolutions": self.compiler.get_assessor_feedback_resolutions(),
            "segments": self.compiler.get_section_vii_e_video_script(),
        }

    def render_slide_card(self, slide_number: int = 1) -> dict:
        segs = self.compiler.get_section_vii_e_video_script()
        idx = max(0, min(slide_number - 1, len(segs) - 1))
        return {
            "slide_number": slide_number,
            "status": "PUBLIC_SLIDE_FRAMEWORK_ACTIVE",
            "segment": segs[idx],
        }

    def print_on_screen_briefing(self) -> None:
        manifest = self.get_full_presentation_manifest()
        print("=" * 96)
        print("  DOD CDAO TRADEWINDS SOLUTIONS MARKETPLACE // OFFICIAL VIDEO RESUBMISSION BRIEFING")
        print("  DOCKET: 10-26-3976 (RESUBMISSION OF 9-26-3703) | ENTITY: HUMPHREY VIRTUAL FARMS LLC")
        print("  CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | BASELINE: TRL 4 SOFTWARE EMULATION TESTBED (127.0.0.1)")
        print("=" * 96)
        print("\n--- ON-SCREEN MATRIX 1: PRIOR DOCKET 9-26-3703 ASSESSOR FEEDBACK RESOLUTION ---")
        for r in manifest["assessor_feedback_resolutions"]:
            print(f"\n  [{r['id']}] PRIOR CRITIQUE : {r['prior_assessor_critique']}")
            print(f"          RESOLUTION     : {r['resubmission_resolution']}")
        print("\n" + "=" * 96)
        print("--- ON-SCREEN MATRIX 2: SECTION VII.e RUBRIC TELEPROMPTER SCRIPT (5 SEGMENTS) ---")
        print("=" * 96)
        for seg in manifest["segments"]:
            print(f"\n>>> {seg['segment']}")
            print(f"    [RUBRIC ALIGNMENT]: {seg['rubric_criterion']}")
            print(f"    [READ ON CAMERA]  : \"{seg['spoken_script']}\"")
        print("\n" + "=" * 96)


if __name__ == "__main__":
    BriefingTeleprompterConsole().print_on_screen_briefing()
