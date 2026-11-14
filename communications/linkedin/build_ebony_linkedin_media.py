import asyncio
import os
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"C:\hvf_c2\Archive\LinkedIn_EBONY_Sovereign_AI_2026")
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350

SLIDES = [
    {
        "num": "01 / 06",
        "tag": "CRITICAL INFRASTRUCTURE BRIEF // CAGE: 1AHA8",
        "title": "ONE LINE OF CLOUD CODE\nSHOULDN'T STOP THE WORLD.",
        "bullets": [
            "Centralized cloud failures ground commercial aircraft.",
            "Unverified upstream pushes stall freight corridors.",
            "Enterprise platforms go dark across entire continents.",
            "Why Sovereign Edge AI is now an operational mandate."
        ],
        "accent": (245, 158, 11),
        "narration": (
            "One line of cloud code should not be able to ground commercial aircraft, "
            "halt freight corridors, and darken enterprise platforms like Microsoft 365 at the exact same time. "
            "Yet that is the exact single-point-of-failure architecture most organizations still run today."
        ),
    },
    {
        "num": "02 / 06",
        "tag": "THE PROBLEM // CENTRALIZED FRAGILITY",
        "title": "THE HIDDEN FLAW IN\nCLOUD-DEPENDENT SYSTEMS",
        "bullets": [
            "Zero Local Autonomy: Edge nodes freeze without cloud auth.",
            "Unverified Update Cascades: One bad push bricks endpoints.",
            "Opaque Audit Trails: Teams wait on vendor status pages.",
            "Mission-critical fleets cannot wait for cloud recovery."
        ],
        "accent": (239, 68, 68),
        "narration": (
            "Modern aviation, logistics, and defense systems share a dangerous structural flaw: "
            "tightly coupled dependence on remote cloud control planes. "
            "When external links sever or an unverified update cascades, high-value assets turn into stationary steel."
        ),
    },
    {
        "num": "03 / 06",
        "tag": "THE SHIFT // SOVEREIGN EDGE ARCHITECTURE",
        "title": "RESILIENCE CANNOT BE\nAN AFTERTHOUGHT",
        "bullets": [
            "Think Locally: Zero external cloud round-trips required.",
            "Isolate Physically: Hardware-enforced optical air-gaps.",
            "Verify Deterministically: Cryptographic SHA-256 sealing.",
            "Built to operate uninterrupted when networks go dark."
        ],
        "accent": (16, 185, 129),
        "narration": (
            "True operational resilience requires a fundamental architectural shift. "
            "Systems must execute locally without external round-trips, isolate critical control buses physically, "
            "and verify every byte cryptographically before execution."
        ),
    },
    {
        "num": "04 / 06",
        "tag": "THE SOLUTION // E.B.O.N.Y. & HVF MCC",
        "title": "ENGINEERED FOR ZERO\nSINGLE-POINT-OF-FAILURE",
        "bullets": [
            "100% Sovereign Local AI: NVIDIA Jetson AGX Orin & MIL-SPEC.",
            "Hardware Optical Air-Gap: Unidirectional CC EAL 4+ Diode.",
            "Zero-Trust Access: PIV/CAC smartcard + biometric lock.",
            "Built by Humphrey Virtual Farm (CAGE: 1AHA8)."
        ],
        "accent": (16, 185, 129),
        "narration": (
            "At Humphrey Virtual Farm, CAGE 1-A-H-A-8, we built E.B.O.N.Y. and the HVF Mobile Command Center "
            "to eliminate centralized cloud fragility permanently—combining sovereign local edge AI, "
            "a hardware-enforced optical air-gap, and zero-trust biometric access."
        ),
    },
    {
        "num": "05 / 06",
        "tag": "VERIFIED BENCHMARKS // 72/72 MILESTONES SEALED",
        "title": "PROVEN DETERMINISTIC\nPERFORMANCE",
        "bullets": [
            "< 16 ms Solid-State Microgrid Islanding (500 kWh LFP).",
            "150 kW Multi-Fuel Turbine APU Off-Grid Endurance.",
            "0% Reverse-Path Leakage Across Optical Data Diode.",
            "100% NDAA Section 889 & DFARS 252.204-7012 Compliant."
        ],
        "accent": (56, 189, 248),
        "narration": (
            "Across seventy-two sealed program milestones, the HVF Mobile Command Center delivers "
            "sub-sixteen-millisecond solid-state microgrid islanding, five hundred kilowatt-hours of energy storage, "
            "zero reverse-path optical leakage, and one hundred percent NDAA Section 889 compliance."
        ),
    },
    {
        "num": "06 / 06",
        "tag": "EXECUTIVE CALL TO ACTION // CAGE: 1AHA8",
        "title": "WHEN THE CLOUD GOES SILENT,\nTHE MISSION CONTINUES.",
        "bullets": [
            "Read the full executive breakdown in the linked article.",
            "Deploy sovereign, Merkle-verified edge resilience.",
            "Jeffery Humphrey, Chief Executive Officer",
            "Humphrey Virtual Farm | CAGE: 1AHA8"
        ],
        "accent": (245, 158, 11),
        "narration": (
            "When the grid flickers and the cloud goes silent, the mission never stops. "
            "Read the full executive breakdown in my article, and connect with me, Jeffery Humphrey, "
            "CEO of Humphrey Virtual Farm, to bring sovereign edge resilience to your operations."
        ),
    },
]

def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines

def render_slide(idx, slide):
    img = Image.new("RGB", (W, H), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    accent = slide["accent"]

    # Subtle architectural grid lines
    for gx in range(0, W, 90):
        draw.line([(gx, 0), (gx, H)], fill=(19, 26, 42), width=1)
    for gy in range(0, H, 90):
        draw.line([(0, gy), (W, gy)], fill=(19, 26, 42), width=1)

    # Outer tactical frame & top accent bar
    draw.rectangle([36, 36, W - 36, H - 36], outline=(38, 49, 74), width=2)
    draw.rectangle([36, 36, W - 36, 50], fill=accent)

    f_tag = load_font(24, bold=True)
    f_num = load_font(26, bold=True)
    f_title = load_font(56, bold=True)
    f_body = load_font(34, bold=False)
    f_foot = load_font(23, bold=True)

    # Header tag + slide counter
    draw.text((76, 86), slide["tag"], font=f_tag, fill=accent)
    num_w = draw.textbbox((0, 0), slide["num"], font=f_num)[2]
    draw.text((W - 76 - num_w, 84), slide["num"], font=f_num, fill=(148, 163, 184))

    # Headline
    y = 165
    for raw_line in slide["title"].split("\n"):
        for line in wrap_text(draw, raw_line, f_title, W - 152):
            draw.text((76, y), line, font=f_title, fill=(248, 250, 252))
            y += 72

    # Divider bar
    y += 22
    draw.rectangle([76, y, 280, y + 6], fill=accent)
    y += 56

    # Bullet cards
    for b in slide["bullets"]:
        wrapped = wrap_text(draw, b, f_body, W - 220)
        card_h = max(84, len(wrapped) * 46 + 34)
        draw.rounded_rectangle([76, y, W - 76, y + card_h], radius=14, fill=(18, 25, 41), outline=(38, 49, 74), width=2)
        draw.rectangle([76, y + 14, 86, y + card_h - 14], fill=accent)
        ty = y + 18
        for wl in wrapped:
            draw.text((112, ty), wl, font=f_body, fill=(226, 232, 240))
            ty += 46
        y += card_h + 24

    # Footer bar
    draw.line([(76, H - 115), (W - 76, H - 115)], fill=(38, 49, 74), width=2)
    draw.text((76, H - 90), "HVF OMNI-INDUSTRIAL MATRIX // E.B.O.N.Y. SOVEREIGN AI", font=f_foot, fill=(148, 163, 184))
    cage_txt = "CAGE: 1AHA8"
    cw = draw.textbbox((0, 0), cage_txt, font=f_foot)[2]
    draw.text((W - 76 - cw, H - 90), cage_txt, font=f_foot, fill=accent)

    out_png = OUT_DIR / f"Slide_{idx:02d}.png"
    img.save(out_png, "PNG")
    return out_png

async def synth_voice(idx, text):
    out_mp3 = OUT_DIR / f"Voice_{idx:02d}.mp3"
    try:
        import edge_tts
        comm = edge_tts.Communicate(text, voice="en-US-AndrewMultilingualNeural", rate="-3%")
        await comm.save(str(out_mp3))
        return out_mp3
    except Exception:
        # Offline Windows SAPI fallback if air-gapped
        out_wav = OUT_DIR / f"Voice_{idx:02d}.wav"
        ps_cmd = (
            "Add-Type -AssemblyName System.Speech; "
            "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$s.SetOutputToWaveFile('{out_wav}'); "
            f"$s.Speak('{text.replace(chr(39), '')}'); "
            "$s.Dispose()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
        return out_wav

async def main():
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    segments = []

    for idx, slide in enumerate(SLIDES, start=1):
        png_path = render_slide(idx, slide)
        aud_path = await synth_voice(idx, slide["narration"])
        seg_mp4 = OUT_DIR / f"Segment_{idx:02d}.mp4"
        subprocess.run([
            ffmpeg, "-y",
            "-loop", "1", "-i", str(png_path),
            "-i", str(aud_path),
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
            str(seg_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segments.append(seg_mp4)
        print(f"[+] Rendered Slide {idx:02d}/06 + Voiceover Segment")

    concat_list = OUT_DIR / "concat.txt"
    concat_list.write_text("\n".join([f"file '{s.as_posix()}'" for s in segments]), encoding="utf-8")

    final_mp4 = OUT_DIR / "HVF_EBONY_Sovereign_AI_LinkedIn_2026.mp4"
    subprocess.run([
        ffmpeg, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(final_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n[SUCCESS] 6 Carousel PNGs + Final Narrated MP4 Ready at:\n  -> {final_mp4}")

if __name__ == "__main__":
    asyncio.run(main())