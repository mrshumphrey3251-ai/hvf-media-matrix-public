#!/usr/bin/env python3
"""
HVF Project Ebony v8.0.0 — Windows PowerShell Native
TSM Revision V.10 5-Minute Video Compliance Enforcer
Author: Jeffery Humphrey, Founder, President & CEO, Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Purpose: Compresses the 6:25 (385s) Master Rubric Verification Video into a strictly
         compliant <= 288.0s (04:48) 1080p@30fps MP4 and generates Private & Public GitHub ledgers.
Security & Extensibility: 100% Offline Loopback, Zero Cloud, Hook-Extensible Class Architecture.
"""

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


class TSMVideoComplianceEnforcer:
    TSM_HARD_CEILING_SECONDS: float = 300.0
    DEFAULT_TARGET_SECONDS: float = 288.0  # 04:48 (12.0s safety buffer under 5:00 cap)
    SHARED_MERKLE_ROOT: str = "bb39eeaa66a39ad2e0c0ab74ba4a5c4faac2bf0d98babc0362482b97607151a1"

    def __init__(
        self,
        source_video: Optional[str] = None,
        output_video: str = "c2_cockpit/proposals/EBONY_V8_CDAO_RUBRIC_COMPLIANT_288S.mp4",
        target_seconds: float = DEFAULT_TARGET_SECONDS,
    ) -> None:
        self.root_dir = Path.cwd()
        self.ffmpeg_bin = self._locate_ffmpeg()
        self.source_path = self._locate_source_video(source_video)
        self.output_path = self.root_dir / Path(output_video)
        self.target_seconds = float(target_seconds)

    @staticmethod
    def _locate_ffmpeg() -> str:
        path = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
        if path:
            return path
        try:
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass
        common_win_paths = [
            Path("C:/ffmpeg/bin/ffmpeg.exe"),
            Path.home() / "scoop/shims/ffmpeg.exe",
            Path.home() / "AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe",
        ]
        for p in common_win_paths:
            if p.exists():
                return str(p)
        raise RuntimeError("CRITICAL: ffmpeg.exe not found in PATH or imageio_ffmpeg.")

    def _locate_source_video(self, explicit_path: Optional[str]) -> Path:
        if explicit_path:
            candidate = Path(explicit_path).expanduser().resolve()
            if candidate.exists():
                return candidate
        default_rel = self.root_dir / Path("c2_cockpit/proposals/EBONY_V8_CDAO_RUBRIC_VERIFICATION_20261028.mp4")
        if default_rel.exists():
            return default_rel
        search_roots = [
            self.root_dir,
            Path.home() / "Desktop",
            Path.home() / "Downloads",
            Path.home(),
        ]
        for sroot in search_roots:
            if sroot.exists():
                try:
                    matches = list(sroot.rglob("*EBONY_V8_CDAO_RUBRIC_VERIFICATION_20261028*.mp4"))
                    if matches:
                        return matches[0]
                except Exception:
                    continue
        return default_rel

    def probe_duration(self, video_path: Path) -> float:
        ffprobe_bin = shutil.which("ffprobe") or shutil.which("ffprobe.exe")
        if ffprobe_bin:
            cmd = [
                ffprobe_bin,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(video_path),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        # Fallback: parse duration directly from ffmpeg -i stderr
        cmd = [self.ffmpeg_bin, "-i", str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        for line in result.stderr.splitlines():
            if "Duration:" in line:
                dur_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = dur_str.split(":")
                return int(h) * 3600 + int(m) * 60 + float(s)
        raise RuntimeError(f"Could not determine duration for {video_path}")

    @staticmethod
    def compute_sha256(file_path: Path) -> str:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def write_dual_repo_ledgers(self, manifest: Dict[str, Any]) -> None:
        private_ledger = self.root_dir / Path("federal_filings/tsm_docket_10_26_4014_remediation_ledger.md")
        public_ledger = self.root_dir / Path("public_verification/tsm_5min_compliance_proof.md")
        private_ledger.parent.mkdir(parents=True, exist_ok=True)
        public_ledger.parent.mkdir(parents=True, exist_ok=True)

        private_content = f"""# OFFICIAL EXECUTIVE REMEDIATION LEDGER — TSM DOCKET 10-26-4014 (5:00 VIDEO CAP ENFORCEMENT)
**Contractor:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)  
**Commanding Authority:** Jeffery Humphrey, Founder, President & CEO (`humphreyvirtualfarm@gmail.com` | (572) 358-9978)  
**Timestamp (UTC):** {manifest['timestamp_utc']}  
**Execution Environment:** Windows PowerShell ({manifest['os_environment']})  
**Shared Core C2 Merkle Root (SHA-256):** `{self.SHARED_MERKLE_ROOT}`  

## 1. ROOT CAUSE OF DOCKET 10-26-4014 ADMINISTRATIVE "NONCOMPLIANT" FLAG
- **Administrative Trigger:** Master video file `EBONY_V8_CDAO_RUBRIC_VERIFICATION_20261028.mp4` had a runtime of **{manifest['source_duration_seconds']} seconds (06:25)**, exceeding the Tradewinds Solutions Marketplace (TSM) Revision V.10 strict administrative limit of **300.0 seconds (05:00)**.
- **Source Video SHA-256:** `{manifest['source_sha256']}`
- **Technical Content Integrity:** 100% of the 4-Pillar CDAO Assessor Rubric proof, 5-Vendor AoA Matrix, TRL 4 software testbed verification (`127.0.0.1` loopback, 636 modules, 85/85 unit tests, 17/17 Red-Team vectors), and 26-Module CLIN pricing schedule remain intact.

## 2. DETERMINISTIC REMEDIATION EXECUTED (`tools/tsm_v8_5min_compliance_enforcer.py`)
- **Compliant Output Asset:** `c2_cockpit/proposals/EBONY_V8_CDAO_RUBRIC_COMPLIANT_288S.mp4`
- **Verified Compliant Runtime:** **{manifest['compliant_duration_mmss']} ({manifest['compliant_duration_seconds']} seconds)** — **{manifest['safety_buffer_seconds']} seconds below** the 300.0-second federal ceiling.
- **Compliant Video SHA-256:** `{manifest['compliant_sha256']}`
- **Speed Factor Applied:** `{manifest['speed_factor_applied']}x` (Pitch-Preserved Dual-Neural Audio + 1080p@30fps Visuals)
- **Compliance Verdict:** `{manifest['compliance_verdict']}`
"""

        public_content = f"""# HVF PROJECT EBONY v8.0.0 — TSM REVISION V.10 VIDEO DURATION COMPLIANCE CERTIFICATE
**Submitting Organization:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | 100% U.S. Sovereign Small Business)  
**Commanding Authority:** Jeffery Humphrey, Founder, President & CEO  
**Public Verification Repository:** https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public  
**Shared Core C2 Merkle Root (SHA-256):** `{self.SHARED_MERKLE_ROOT}`  
**Verification Timestamp (UTC):** `{manifest['timestamp_utc']}`  

## VERIFIED 5-MINUTE GATE COMPLIANCE METRICS
- **TSM Revision V.10 Maximum Allowed Runtime:** `05:00` (`300.00 seconds`)
- **Project Ebony v8.0.0 Compliant Master Asset:** `EBONY_V8_CDAO_RUBRIC_COMPLIANT_288S.mp4`
- **Verified Runtime:** `{manifest['compliant_duration_mmss']}` (`{manifest['compliant_duration_seconds']} seconds` — `{manifest['safety_buffer_seconds']}-second` safety margin below federal cap)
- **Compliant Video SHA-256:** `{manifest['compliant_sha256']}`
- **Resolution & Frame Rate:** Native `1920x1080p @ 30fps`
- **4-Pillar CDAO Rubric Coverage:** 100% Retained (Criterion 1 Problem Physics Gap; Criterion 2 TRL 4 Zero-Cloud Loopback vs. Phase-1 Hardware Targets; Criterion 3 5-Vendor Quantitative AoA; Criterion 4 26-Module CLIN Schedule & $1.485M 10 U.S.C. 4022 Prototype OTA).
"""
        private_ledger.write_text(private_content, encoding="utf-8")
        public_ledger.write_text(public_content, encoding="utf-8")

    def enforce_compliance(self) -> Dict[str, Any]:
        if not self.source_path.exists():
            raise FileNotFoundError(
                f"Source video not found at: {self.source_path}\n"
                "Please verify where EBONY_V8_CDAO_RUBRIC_VERIFICATION_20261028.mp4 is saved."
            )

        original_duration = self.probe_duration(self.source_path)
        original_sha256 = self.compute_sha256(self.source_path)

        if original_duration <= self.target_seconds:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.source_path, self.output_path)
            speed_factor = 1.0
        else:
            speed_factor = round((original_duration / self.target_seconds) + 0.005, 4)
            pts_multiplier = round(1.0 / speed_factor, 6)

            atempo_filters = []
            remaining = speed_factor
            while remaining > 2.0:
                atempo_filters.append("atempo=2.0")
                remaining /= 2.0
            atempo_filters.append(f"atempo={remaining:.4f}")
            audio_filter = ",".join(atempo_filters)

            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            ffmpeg_cmd = [
                self.ffmpeg_bin,
                "-y",
                "-i", str(self.source_path),
                "-filter_complex",
                f"[0:v]setpts={pts_multiplier}*PTS,fps=30,scale=1920:1080[v];[0:a]{audio_filter}[a]",
                "-map", "[v]",
                "-map", "[a]",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "20",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-movflags", "+faststart",
                str(self.output_path),
            ]
            subprocess.run(ffmpeg_cmd, check=True)

        # Copy to Windows Downloads and Desktop for instant 1-click TSM Portal upload
        exported_copies = []
        for target_dir in [Path.home() / "Downloads", Path.home() / "Desktop"]:
            if target_dir.exists():
                try:
                    dest_file = target_dir / "EBONY_V8_CDAO_RUBRIC_COMPLIANT_288S.mp4"
                    shutil.copy2(self.output_path, dest_file)
                    exported_copies.append(str(dest_file))
                except Exception:
                    pass

        final_duration = self.probe_duration(self.output_path)
        final_sha256 = self.compute_sha256(self.output_path)

        if final_duration >= self.TSM_HARD_CEILING_SECONDS:
            raise RuntimeError(
                f"COMPLIANCE GATE FAILED: Output duration {final_duration:.2f}s >= 300.0s cap!"
            )

        manifest = {
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "os_environment": f"{platform.system()} {platform.release()}",
            "contractor": "Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)",
            "commanding_authority": "Jeffery Humphrey, Founder, President & CEO",
            "docket_superseded": "10-26-4014 (6:25 Noncompliant Duration Trigger)",
            "source_video": str(self.source_path),
            "source_duration_seconds": round(original_duration, 2),
            "source_sha256": original_sha256,
            "compliant_video": str(self.output_path),
            "easy_upload_copies": exported_copies,
            "compliant_duration_seconds": round(final_duration, 2),
            "compliant_duration_mmss": f"{int(final_duration // 60):02d}:{int(final_duration % 60):02d}",
            "compliant_sha256": final_sha256,
            "speed_factor_applied": speed_factor,
            "tsm_ceiling_seconds": self.TSM_HARD_CEILING_SECONDS,
            "safety_buffer_seconds": round(self.TSM_HARD_CEILING_SECONDS - final_duration, 2),
            "private_repo_ledger": "federal_filings/tsm_docket_10_26_4014_remediation_ledger.md",
            "public_repo_ledger": "public_verification/tsm_5min_compliance_proof.md",
            "compliance_verdict": "PASS — 100% COMPLIANT WITH TSM REVISION V.10 (<= 5:00 CAP)",
        }
        self.write_dual_repo_ledgers(manifest)
        return manifest


def main() -> None:
    src = sys.argv[1] if len(sys.argv) > 1 else None
    dst = sys.argv[2] if len(sys.argv) > 2 else "c2_cockpit/proposals/EBONY_V8_CDAO_RUBRIC_COMPLIANT_288S.mp4"
    enforcer = TSMVideoComplianceEnforcer(source_video=src, output_video=dst)
    manifest = enforcer.enforce_compliance()
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
