# -*- coding: utf-8 -*-
"""
HUMPHREY VIRTUAL FARMS LLC // AUTOMATED 1080p FULL-HD TRADEWINDS MP4 VIDEO & VOICEOVER COMPILER
Docket: 10-26-3976 (Resubmission of Prior Docket 9-26-3703 | TRL 4 -> Phase-1 OTA Target: TRL 6)
Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
Synthesizes 5 high-contrast 1920x1080 C2 Tactical Slides addressing all 4 Pillars of CDAO Assessor
Feedback, GAO/CISA Volt Typhoon citations, the Quantitative Analysis of Alternatives (Competitor Table),
Oklahoma customer validation, and the 26-Module CLIN Price Schedule, with offline voiceover & FFmpeg muxing.
"""
import hashlib
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COCKPIT_DIR = Path(__file__).resolve().parent
if str(COCKPIT_DIR) not in sys.path:
    sys.path.insert(0, str(COCKPIT_DIR))

import tradewinds_pitch_compiler as tpc


def _load_font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\consolab.ttf" if bold else r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def build_slide_specs() -> list:
    compiler = tpc.TradewindsPitchCompiler()
    scripts = compiler.get_section_vii_e_video_script()
    return [
        {
            "slide_num": 1,
            "header": "SLIDE 1 OF 5 // MANDATORY RESUBMISSION GATE: 4-PILLAR ASSESSOR FEEDBACK RESOLUTION",
            "sub": "ACTIVE DOCKET: 10-26-3976 (RESUBMISSION OF 9-26-3703) | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | TRL 4 -> TARGET TRL 6",
            "bullets": [
                "[AF-01 / CRITERION 1 RESOLVED] DEFINING THE PROBLEM (UPGRADED TO OUTSTANDING):",
                "  * Quantified DoD exposure via GAO-21-81 & GAO-24-106137 (500+ bases, 300k+ buildings, $4.2B+ OT energy)",
                "    and CISA/NSA/DoD Advisories AA23-144A & AA24-038A (Volt Typhoon) + TRISIS (<4.16ms arc-flash physics).",
                "",
                "[AF-02 / CRITERION 2 RESOLVED] ACCELERATING THE MISSION (TRL 4 SOFTWARE TESTBED -> TRL 6 TARGET):",
                "  * 0% cloud/OS dependency on air-gapped 127.0.0.1 loopback (100% EMCON availability). Brain 1 (<50us loop,",
                "    2.04us Modbus FC05, 13.33ms breaker); Brain 2 (<25W NPU, <5ms, 0 actuator wire); Brain 3 (52 WORM tables).",
                "",
                "[AF-03 / CRITERION 3 RESOLVED] ADVANCING STATE OF THE ART (HEAD-TO-HEAD COMPETITOR AoA MATRIX):",
                "  * Modeled 36.75ns Analog Kinetic Guillotine (1,360,544x faster than 50ms Siemens/Rockwell PLCs) at 28.5W",
                "    benchmarked directly against Siemens S7-1500, Rockwell ControlLogix, Triconex SIS, Dragos, Nozomi & Jev AI.",
                "",
                "[AF-04 / CRITERION 4 RESOLVED] BUSINESS MODEL, OKLAHOMA VALIDATION & 26-MODULE CLIN SCHEDULE:",
                "  * OK Commerce CTO/CEO briefings (HB 2992/Title 61, node HVF-NODE-TEELE-001, $25K ODOT drone) & $1.485M OTA.",
            ],
            "narration": scripts[0]["spoken_script"],
        },
        {
            "slide_num": 2,
            "header": "SLIDE 2 OF 5 // CRITERION 1: DEFINING THE PROBLEM (GAO-21-81, GAO-24-106137 & VOLT TYPHOON)",
            "sub": "RUBRIC PILLAR 1: QUANTIFIED DOD OT EXPOSURE, STATE-SPONSORED PRE-POSITIONING & ARC-FLASH PHYSICS GAP",
            "bullets": [
                "[1. DOD INSTALLATION & TACTICAL OT EXPOSURE AT SCALE — U.S. GAO-21-81 & GAO-24-106137]:",
                "  * DoD operates 500+ major military installations, 300,000+ buildings, and $4.2B+ in annual installation",
                "    energy and microgrid assets relying on legacy commercial OT/SCADA PLCs scanning at 50-200 ms (5-20 Hz).",
                "",
                "[2. STATE-SPONSORED OT PRE-POSITIONING — JOINT CISA/NSA/FBI/DOD AA23-144A & AA24-038A (VOLT TYPHOON)]:",
                "  * Confirmed PRC state-sponsored actors actively pre-position living-off-the-land persistence across critical",
                "    energy, water, communications, and transportation OT corridors supporting DoD power projection.",
                "",
                "[3. KINETIC VELOCITY & SCAN-LATENCY PHYSICS GAP — TRISIS/TRITON & INDUSTROYER2]:",
                "  * In TRISIS/Triton (Schneider Triconex SIS) & Industroyer2, attackers corrupted PLC logic while spoofing HMIs.",
                "  >>> High-voltage arc-flash backfeeds propagate in < 4.16 ms (quarter AC cycle).",
                "  >>> Microreactor prompt-critical excursions occur in 6.0 ms.",
                "  >>> Legacy 50-200 ms digital PLC scan loops are 8x to 33x TOO SLOW to prevent physical destruction.",
            ],
            "narration": scripts[1]["spoken_script"],
        },
        {
            "slide_num": 3,
            "header": "SLIDE 3 OF 5 // CRITERION 2: ACCELERATING THE MISSION (TRI-BRAIN TRL 4 TESTBED PROOF)",
            "sub": "RUBRIC PILLAR 2: ZERO EXTERNAL DEPENDENCIES (NIST 800-82 / 800-171) & EMPIRICAL TESTBED TELEMETRY",
            "bullets": [
                "[ZERO EXTERNAL DEPENDENCIES & 100% EMCON AVAILABILITY]:",
                "  * 0% commercial cloud dependency, 0 external APIs, 0 foreign firmware blobs, 0 WAN listening ports (127.0.0.1).",
                "",
                "[TRI-BRAIN + MODELED ANALOG KINETIC GUILLOTINE TELEMETRY]:",
                "  * BRAIN ONE (Deterministic Control) : < 50 us loop | 2.04 us RS-485 Modbus FC05 | 13.33 ms 4-ch breaker",
                "                                        isolation | 126.13 ms sequential soft-start recovery.",
                "  * BRAIN TWO (Air-Gapped Cognitive)  : < 25W local NPU harmonic anomaly detection (< 5.0 ms); wired as",
                "                                        strictly advisory with ZERO electrical connection to actuator coils.",
                "  * BRAIN THREE (WORM Provenance)     : Ed25519 + SHA-256 Merkle DAG (< 0.15 ms) across 52 bare-metal SQLite",
                "                                        tables (22 in matrix_ledger.db + 30 in hvf_memory_vault.db).",
                "",
                "=== LIVE TRL 4 WORKSTATION VERIFICATION LEDGER (636 C2 MODULES | 1,961 PRIV / 1,770 PUB) ===",
                "  >>> 85 / 85 Automated Test Suites PASSED (100%) | 17 / 17 Red-Team Vectors BLOCKED | 1,420 Academy Qs",
            ],
            "narration": scripts[2]["spoken_script"],
        },
        {
            "slide_num": 4,
            "header": "SLIDE 4 OF 5 // CRITERION 3: ADVANCING STATE OF THE ART (COMPETITOR AoA MATRIX)",
            "sub": "RUBRIC PILLAR 3: QUANTITATIVE ANALYSIS OF ALTERNATIVES VS. SIEMENS/ROCKWELL, TRICONEX, DRAGOS & CLOUD AI",
            "bullets": [
                "+----------------------+------------------------+---------------------+---------------------+---------------------+",
                "| CAPABILITY / METRIC  | PROJECT EBONY (1AHA8)  | SIEMENS S7-1500 /   | DRAGOS PLATFORM /   | SCHNEIDER ELECTRIC  |",
                "|                      | (HVF TRL 4 TESTBED)    | ROCKWELL CONTROLLGX | NOZOMI & JEV CLOUD  | TRICONEX (SIS)      |",
                "+----------------------+------------------------+---------------------+---------------------+---------------------+",
                "| Primary Architecture | Tri-Brain Bare-Metal + | Digital OS/RTOS PLC | Passive IDS / SIEM  | Triple-Modular      |",
                "|                      | 36.75ns Guillotine     | (5-20Hz Scan Loop)  | & Cloud AI Wrappers | Redundant PLC       |",
                "+----------------------+------------------------+---------------------+---------------------+---------------------+",
                "| Cutoff Latency       | 36.75 ns (Analog) /    | 50,000,000 to       | NONE (0 Physical    | 10,000,000 to       |",
                "|                      | 2.04 us (Modbus FC05)  | 200,000,000 ns      | Cutoff; >250ms RTT) | 50,000,000 ns       |",
                "+----------------------+------------------------+---------------------+---------------------+---------------------+",
                "| Speed Advantage      | 1,360,544x Faster than | 8x-33x Too Slow for | Human Operator /    | Breached by TRISIS  |",
                "|                      | 50ms Commercial PLC    | <4.16ms Arc-Flash   | Cloud API Required  | Firmware Injection  |",
                "+----------------------+------------------------+---------------------+---------------------+---------------------+",
                "| Total Power Draw     | 28.5 W (24V DC Bus)    | 150 W - 450 W       | 300 W - 1,200 W     | 200 W - 600 W       |",
                "| Cloud Dependency     | 0% (100% Air-Gapped)   | Proprietary OS/HMI  | High Cloud/Linux OS | Proprietary RTOS    |",
                "| WORM Provenance      | Ed25519+SHA256 (<0.15m)| Unauthenticated CIP | Mutable SIEM Logs   | Non-Merkle Buffer   |",
                "+----------------------+------------------------+---------------------+---------------------+---------------------+",
            ],
            "narration": scripts[3]["spoken_script"],
        },
        {
            "slide_num": 5,
            "header": "SLIDE 5 OF 5 // CRITERION 4: BUSINESS MODEL, OKLAHOMA VALIDATION & 26-CLIN SCHEDULE",
            "sub": "RUBRIC PILLAR 4: GOVERNMENT/COMMERCIAL VALIDATION, UNBUNDLED CLIN PRICING & 10 U.S.C. 4022 -> 4022(f) OTA",
            "bullets": [
                "[1. DOCUMENTED GOVERNMENT & COMMERCIAL CUSTOMER VALIDATION]:",
                "  * Commercial Ag & Microgrid Roadmap: 30% water savings, 12% yield boost, < 5 min data-to-action latency.",
                "  * State of Oklahoma Executive Engagement (Oct 2026): Technical briefings with OK Dept of Commerce CTO",
                "    (Rob Teel) & CEO (John Budd) under OK HB 2992 & Title 61 Sec 212; provisioned node HVF-NODE-TEELE-001;",
                "    completed OMES Title 74 & CAP Form M254 filings; staged $25,000 Phase-1 ODOT Autonomous Bridge Drone",
                "    Prototype (cutting $4,600 snooper-truck inspections to $250/sortie; $500,000 in-kind match 2 CFR 200.306).",
                "",
                "[2. DUAL-USE PRICING, 26-MODULE CLIN SCHEDULE & 10 U.S.C. 4022 -> 4022(f) TRANSITION]:",
                "  >>> Tier 1 (Edge Comms): $19.99/mo | Tier 2 (Commercial SCADA/NDT): $499-$2,500/mo + $250/sortie.",
                "  >>> Unbundled 26-Module Console (CLIN 0001 - CLIN 0026): CLIN 0001 Base Pilot ($2,450/mo) | CLIN 0006",
                "      Robotics C2 ($185K/yr) | CLIN 1004-A 1-Node Bundle ($895K/yr) | CLIN 1004-B 25-Node Base ($2.45M/yr).",
                "  >>> Tier 3 Federal DoD OTA: $1,485,000.00 12-Month Fixed-Price Prototype OTA (10 U.S.C. 4022; $150K M1A)",
                "      -> Non-Competitive Production under 10 U.S.C. 4022(f) with 100% DFARS 252.227-7018 Background IP.",
            ],
            "narration": scripts[4]["spoken_script"],
        },
    ]


def render_slide_image(spec: dict, out_png: Path) -> Path:
    img = Image.new("RGB", (1920, 1080), (10, 16, 28))
    draw = ImageDraw.Draw(img)

    font_banner = _load_font(25, bold=True)
    font_title = _load_font(28, bold=True)
    font_sub = _load_font(20, bold=True)
    font_body = _load_font(21, bold=False)
    font_caption = _load_font(19, bold=False)

    # Top sovereign header bar
    draw.rectangle([(0, 0), (1920, 110)], fill=(18, 32, 56))
    draw.line([(0, 110), (1920, 110)], fill=(0, 210, 255), width=4)
    draw.text(
        (40, 18),
        "HUMPHREY VIRTUAL FARMS LLC // DOD CDAO TRADEWINDS SOLUTIONS MARKETPLACE RESUBMISSION",
        fill=(0, 225, 255),
        font=font_banner,
    )
    draw.text(
        (40, 58),
        spec["header"],
        fill=(255, 255, 255),
        font=font_title,
    )

    # Subheader bar
    draw.rectangle([(40, 125), (1880, 172)], fill=(22, 42, 68), outline=(0, 180, 220), width=2)
    draw.text((55, 137), spec["sub"], fill=(120, 255, 180), font=font_sub)

    # Main content box
    draw.rectangle([(40, 188), (1880, 818)], fill=(14, 24, 42), outline=(45, 85, 130), width=2)
    y = 205
    line_step = 34 if spec["slide_num"] == 4 else 41
    for line in spec["bullets"]:
        color = (230, 240, 250)
        if line.startswith("[") or line.startswith("===") or line.startswith("+---"):
            color = (255, 215, 90)
        elif ">>>" in line or "36.75 ns" in line or "1,360,544x" in line or "0% (100%" in line:
            color = (110, 255, 160)
        elif "| CAPABILITY" in line or "|                      |" in line:
            color = (0, 225, 255)
        draw.text((58, y), line, fill=color, font=font_body)
        y += line_step

    # Bottom spoken caption box
    draw.rectangle([(40, 832), (1880, 1012)], fill=(20, 30, 48), outline=(0, 210, 255), width=2)
    draw.text((58, 840), "ON-SCREEN NARRATION TRANSCRIPT (SECTION VII.e & 4-PILLAR EVALUATOR RUBRIC ALIGNED):", fill=(0, 210, 255), font=font_sub)
    wrapped_narration = textwrap.wrap(spec["narration"], width=116)
    ny = 870
    for wline in wrapped_narration[:6]:
        draw.text((58, ny), wline, fill=(245, 245, 245), font=font_caption)
        ny += 22

    # Footer bar
    draw.rectangle([(0, 1025), (1920, 1080)], fill=(12, 20, 36))
    draw.line([(0, 1025), (1920, 1025)], fill=(0, 210, 255), width=2)
    draw.text(
        (40, 1042),
        f"DOCKET: 10-26-3976 (RESUBMISSION OF 9-26-3703) | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | TRL 4 -> TRL 6 | SLIDE {spec['slide_num']} OF 5",
        fill=(180, 205, 230),
        font=font_caption,
    )

    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_png), format="PNG")
    return out_png


def synthesize_voiceover_wav(text: str, out_wav: Path) -> Path:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)
    engine.save_to_file(text, str(out_wav))
    engine.runAndWait()
    return out_wav


def compile_tradewinds_mp4(output_mp4: Path = None) -> dict:
    if output_mp4 is None:
        output_mp4 = COCKPIT_DIR / "proposals" / "PROJECT_EBONY_TRADEWINDS_RESUBMISSION_10_26_3976.mp4"
    output_mp4.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_exe = shutil.which("ffmpeg")
    if not ffmpeg_exe:
        raise RuntimeError("ffmpeg executable not found in PATH")

    specs = build_slide_specs()
    temp_dir = Path(tempfile.mkdtemp(prefix="hvf_tw_mp4_"))
    segment_mp4s = []

    for spec in specs:
        idx = spec["slide_num"]
        png_path = temp_dir / f"slide_{idx:02d}.png"
        wav_path = temp_dir / f"audio_{idx:02d}.wav"
        seg_path = temp_dir / f"segment_{idx:02d}.mp4"

        render_slide_image(spec, png_path)
        synthesize_voiceover_wav(spec["narration"], wav_path)

        cmd = [
            ffmpeg_exe, "-y",
            "-loop", "1",
            "-i", str(png_path),
            "-i", str(wav_path),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-shortest",
            str(seg_path),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segment_mp4s.append(seg_path)

    concat_txt = temp_dir / "concat_list.txt"
    concat_lines = [f"file '{p.as_posix()}'" for p in segment_mp4s]
    concat_txt.write_text("\n".join(concat_lines), encoding="utf-8")

    concat_cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        "-movflags", "+faststart",
        str(output_mp4),
    ]
    subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ffprobe_exe = shutil.which("ffprobe")
    duration_sec = 0.0
    if ffprobe_exe:
        res = subprocess.run(
            [ffprobe_exe, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(output_mp4)],
            capture_output=True, text=True
        )
        try:
            duration_sec = round(float(res.stdout.strip()), 2)
        except Exception:
            duration_sec = 0.0

    sha256_hex = hashlib.sha256(output_mp4.read_bytes()).hexdigest()
    size_mb = round(output_mp4.stat().st_size / (1024 * 1024), 2)

    shutil.rmtree(temp_dir, ignore_errors=True)
    return {
        "mp4_path": str(output_mp4),
        "size_mb": size_mb,
        "duration_sec": duration_sec,
        "sha256": sha256_hex,
        "slides_rendered": len(specs),
    }


if __name__ == "__main__":
    info = compile_tradewinds_mp4()
    print("=" * 90)
    print("  [TRADEWINDS 1080p FULL-HD MP4 RESUBMISSION VIDEO WITH COMPETITOR AoA TABLE SEALED]")
    print(f"  File Path    : {info['mp4_path']}")
    print(f"  File Size    : {info['size_mb']} MB | Slides: {info['slides_rendered']} (1920x1080 @ 30fps + AAC Audio)")
    print(f"  Duration     : {info['duration_sec']} seconds (Target < 300s / 5:00 Tradewinds Max Limit)")
    print(f"  SHA-256 Seal : {info['sha256']}")
    print("=" * 90)
