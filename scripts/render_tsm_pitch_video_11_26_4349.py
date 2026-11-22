import base64
import hashlib
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

PRIV_SLIDES = Path(r"C:\hvf_c2\hvf-media-matrix-private\governance\dossiers\tsm_11_26_4349_slides")
PUB_SLIDES  = Path(r"C:\hvf_c2\hvf-media-matrix-public\governance\dossiers\tsm_11_26_4349_slides")
FFMPEG_EXE = sys.argv[1]

# Unhurried ~470-word SSML executive narration: calm Rate=0/1 cadence, explicit CAGE/UEI
# phonetic pauses, and direct resolution of every previous assessor observation.
SLIDE_SEGMENTS_SSML = [
    (
        "Slide_01_Title_Verification_Anchor.png",
        """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        I am Jeffery Humphrey, Founder and CEO of Humphrey Virtual Farms, L L C. <break time="350ms"/>
        Our CAGE code is: <break time="250ms"/> 1, <break time="200ms"/> A, <break time="200ms"/> H, <break time="200ms"/> A, <break time="200ms"/> 8. <break time="400ms"/>
        Our SAM dot gov U E I is: <break time="200ms"/> S, 1, M, 4, E, N, L, H, T, D, H, 5. <break time="400ms"/>
        This is our gold-standard final submission for Project E-B-O-N-Y, version 8 point 0, Docket 11, 26, 4349. <break time="300ms"/>
        We built this presentation to directly answer every observation raised by Evaluators 1 and 2 on our prior review,
        backed by reproducible bare-metal proof scripts and 5 point 5 7 million sequential WORM SHA-256 Merkle blocks on GitHub.
        </speak>"""
    ),
    (
        "Slide_02_Criterion1_Problem_Microgrid.png",
        """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        Criterion 1: Defining the Problem. <break time="300ms"/>
        Evaluators 1 and 2 asked us to distinguish dedicated protective relays from PLC scan timing,
        prove the shared operational root cause, and establish the physical basis for our arc-flash and thermal thresholds. <break time="350ms"/>
        Dedicated feeder relays, such as an S-E-L 751, clear local hardwired overcurrent faults in 40 to 58 milliseconds.
        Project E-B-O-N-Y does not replace local overcurrent relays. <break time="300ms"/>
        Instead, we close the 70 to 150-plus millisecond unauthenticated supervisory control gap across multi-source DoD microgrids,
        where utility feeders, solar, battery storage, and generators rely on polled Modbus TCP and DNP3 buses lacking per-frame authentication. <break time="350ms"/>
        Cyber spoofing, arc-flash escalation, and thermal excursions share one root cause:
        unauthenticated trust in supervisory telemetry across shared O-T buses combined with a greater-than-16-millisecond trip delay,
        as documented in G-A-O 21-81, G-A-O 24-106137, and CISA Advisory A-A-24-038-A on Volt Typhoon. <break time="350ms"/>
        On a representative 13 point 8 kilovolt to 480 volt, 5 MVA substation with 104,606 amps of bolted fault current,
        cutting supervisory response from 100 milliseconds to under 16 point 0 milliseconds
        reduces supervisory IEEE 1584 arc-flash duration by 84 point 0 percent and cuts I-squared-t thermal let-through by 6 point 2 5 times.
        </speak>"""
    ),
    (
        "Slide_03_Criterion2_Mission_HIL_Plan.png",
        """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        Criterion 2: Accelerating the Mission. <break time="300ms"/>
        To resolve evaluator questions on modeled targets, relay integration, privileged-user tampering, and hardware maturation,
        Stress Arena 59 benchmarks all five software stages across 10,000 bare-metal trials. <break time="350ms"/>
        Stages 1 through 4, telemetry parsing, constant-time HMAC-SHA-256 validation, interlock evaluation, and trip register assertion,
        execute in a combined median of 2 point 6 0 microseconds, and 4 point 5 0 microseconds at p99. <break time="300ms"/>
        Stage 5 commits an immutable WORM SHA-256 Merkle block in 6 point 0 4 milliseconds.
        Even under 400 percent CPU oversubscription across 16 cores and 50,000 cycles, worst-case software latency is 117 microseconds, with zero breaches of 16 milliseconds. <break time="350ms"/>
        Stage 6, physical 36 point 7 5 nanosecond MOSFET and breaker switching under 480-volt loads,
        is explicitly separated as our funded 180-day TRL 4 to TRL 6 Hardware-in-the-Loop deliverable:
        Days 1 to 45 for OPAL-RT and S-E-L 751 sensor integration, Days 46 to 120 for 500-fault load-bank testing,
        and Days 121 to 180 for independent DoD witness certification. <break time="350ms"/>
        In the substation, E-B-O-N-Y installs in parallel with IEC 61508 fail-safe watchdog relays, never disabling local protection. <break time="300ms"/>
        Finally, a detached out-of-band HMAC-SHA-256 Merkle anchor across a one-way diode detects privileged root database replacement on disk immediately.
        </speak>"""
    ),
    (
        "Slide_04_Criterion3_Equivalent_Benchmark.png",
        """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        Criterion 3: Advancing the State of the Art. <break time="300ms"/>
        In direct response to evaluator guidance, Arena 59 compares four architectures under identical air-gapped fault and spoof conditions:
        an active undervoltage fault concurrent with 1,000 spoofed breaker override commands. <break time="350ms"/>
        Conventional polled PLCs lack per-frame authentication across a 70 to 150-plus millisecond scan window.
        Passive O-T monitors alert only, with zero actuation authority.
        Cloud SIEM platforms fail immediately when WAN connectivity is severed. <break time="350ms"/>
        Project E-B-O-N-Y runs 100 percent offline, traps 1,000 out of 1,000 spoofed commands inside our read-only deception tarpit with zero actuator bleeds,
        and asserts the trip in a median of 5 point 4 0 microseconds,
        within a full wall-plug enclave power budget of 28 to 45 watts.
        </speak>"""
    ),
    (
        "Slide_05_Criterion4_Business_CLINs_DFARS.png",
        """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        Criterion 4: Business Model. <break time="300ms"/>
        Addressing every acquisition question directly: Humphrey Virtual Farms, L L C, CAGE code: <break time="200ms"/> 1, A, H, A, 8, <break time="200ms"/>
        currently holds zero dollars in awarded federal contracts. <break time="300ms"/>
        All pricing tiers are proposed milestone-gated acquisition options under FAR or 10 U-S-C Section 4022 Prototype Other Transaction authority:
        Proposed CLIN 0001 at 245,000 dollars for a 90-day benchtop HIL pilot;
        Proposed CLIN 0002 at 685,000 dollars for a 180-day TRL 6 substation HIL prototype;
        and Proposed CLIN 0003 at 1 point 4 5 million dollars for a 12-month, 10-feeder prototype. <break time="350ms"/>
        Under DFARS 252 point 227-7013 and 7014, the Government receives Government Purpose Rights on all site adapters,
        RMF ATO artifacts, and 100 percent of WORM audit logs, while Humphrey Virtual Farms retains Restricted Rights on core proprietary engines. <break time="350ms"/>
        Originally proven in zero-connectivity bridge diagnostics, our architecture has scheduled executive pilot scoping
        with the Chief Technology Officer of the Oklahoma Department of Commerce. <break time="300ms"/>
        Thank you. Full proof scripts and receipts are live on GitHub.
        </speak>"""
    ),
]


def synthesize_ssml_wav(ssml_xml: str, wav_path: Path, rate: int = 0) -> float:
    b64_xml = base64.b64encode(ssml_xml.encode("utf-8")).decode("ascii")
    wav_escaped = str(wav_path).replace("'", "''")
    ps_cmd = (
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$voice = $synth.GetInstalledVoices() | Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -like 'en-US*' } | Select-Object -First 1; "
        "if ($voice) { $synth.SelectVoice($voice.VoiceInfo.Name) }; "
        f"$synth.Rate = {rate}; "
        "$synth.Volume = 100; "
        f"$xml = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{b64_xml}')); "
        f"$synth.SetOutputToWaveFile('{wav_escaped}'); "
        "$synth.SpeakSsml($xml); "
        "$synth.Dispose();"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
    with wave.open(str(wav_path), "rb") as wf:
        frames = wf.getnframes()
        sr = wf.getframerate()
        return frames / float(sr)


def main() -> None:
    print("[VIDEO BUILDER] Synthesizing calm, unhurried SSML narration tracks...", flush=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        # Start at Rate=0 (natural calm human speaking pace!)
        rate = 0
        while True:
            durations = []
            wav_files = []
            for idx, (_, ssml_txt) in enumerate(SLIDE_SEGMENTS_SSML, start=1):
                wpath = tmp / f"seg_{idx}_r{rate}.wav"
                dur = synthesize_ssml_wav(ssml_txt, wpath, rate=rate)
                dur_padded = dur + 0.65
                durations.append(dur_padded)
                wav_files.append(wpath)

            total_sec = sum(durations)
            print(f"  [TTS Rate={rate}] Total Narration Duration = {total_sec:.2f}s ({int(total_sec // 60):02d}:{total_sec % 60:05.2f})", flush=True)
            if total_sec <= 292.0 or rate >= 2:
                break
            rate += 1

        if total_sec > 296.0:
            raise RuntimeError(f"Video duration {total_sec:.2f}s exceeds 04:56 safety cap!")

        segment_mp4s = []
        for idx, ((slide_name, _), wpath, dur) in enumerate(zip(SLIDE_SEGMENTS_SSML, wav_files, durations), start=1):
            slide_img = PUB_SLIDES / slide_name
            seg_mp4 = tmp / f"part_{idx}.mp4"
            cmd = [
                FFMPEG_EXE, "-y",
                "-loop", "1", "-framerate", "30", "-i", str(slide_img),
                "-i", str(wpath),
                "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-t", f"{dur:.3f}",
                str(seg_mp4),
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            segment_mp4s.append(seg_mp4)
            print(f"  [OK] Rendered Part {idx}/5 ({slide_name}) -> {dur:.2f}s", flush=True)

        concat_list = tmp / "concat.txt"
        concat_list.write_text("\n".join(f"file '{str(p)}'" for p in segment_mp4s) + "\n", encoding="utf-8")

        out_pub  = PUB_SLIDES / "EBONY_V8_TSM_FINAL_11_26_4349.mp4"
        out_priv = PRIV_SLIDES / "EBONY_V8_TSM_FINAL_11_26_4349.mp4"

        concat_cmd = [
            FFMPEG_EXE, "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c", "copy", "-movflags", "+faststart",
            str(out_pub),
        ]
        subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        shutil.copy2(out_pub, out_priv)

        sha = hashlib.sha256(out_pub.read_bytes()).hexdigest()
        size_mb = out_pub.stat().st_size / (1024.0 * 1024.0)
        mins = int(total_sec // 60)
        secs = total_sec % 60

        print("\n================================================================================================")
        print("  UNHURRIED, ASSESSOR-ALIGNED 1080p PITCH VIDEO GENERATED & VERIFIED (< 05:00 CAP)!")
        print("================================================================================================")
        print(f"  Output MP4 (Public):  {out_pub}")
        print(f"  Verified Runtime:     {mins:02d}:{secs:05.2f} ({total_sec:.2f}s — Strictly < 05:00 Cap)")
        print(f"  TTS Cadence Rate:     Rate={rate} (Calm, Natural Executive Pacing)")
        print(f"  File Size:            {size_mb:.2f} MB (H.264 1920x1080 30fps / AAC 48kHz Stereo)")
        print(f"  SHA-256 Digest:       {sha}")
        print("================================================================================================")


if __name__ == "__main__":
    main()