"""
c2_cockpit/modules/c2_briefing_audio_narrator.py
Project E.B.O.N.Y. v8.0.0 - USACE ERDC / DIU Executive Briefing Synchronized Narrator
Classification: HVF Proprietary // 10 U.S.C. § 4022 Prototype OTA
Authority: 100% Offline Architecture (Zero Cloud, Native Windows SAPI)
"""

import sys
import os
import subprocess

NARRATION_SCRIPTS = {
    1: "Slide one. Statutory authority and executive positioning. Humphrey Virtual Farms LLC, CAGE code 1AHA8, presents Project Ebony Version 8.0.0. This sovereign microgrid and logistics convoy is under active assessment with CDAO Tradewinds under Docket 10-26-4046, ready for direct award under 10 U.S.C. Section 4022.",
    2: "Slide two. The status quo problem. Per GAO reports 21-81 and 24-106137, over 500 defense installations and 4.2 billion dollars in operational energy rely on legacy digital PLCs. CISA Advisories on Volt Typhoon confirm adversaries are pre-positioned to corrupt control logic while spoofing valid telemetry to operators.",
    3: "Slide three. The timing physics gap. High-voltage arc-flash faults propagate in less than 4.16 milliseconds. Legacy PLCs scan at 50 to 200 milliseconds, arriving up to 33 times too late to prevent physical destruction. Project Ebony eliminates this physics failure window.",
    4: "Slide four. The hardware air-gap. Our analog Silicon Carbide MOSFET kinetic interlock executes physical gate severance in a modeled 36.75 nanoseconds. That is 1.36 million times faster than digital PLCs, drawing just 28.5 watts with zero cloud dependencies.",
    5: "Slide five. 7,500-mile expeditionary mobility. Carrying 950 gallons of multi-fuel, a 150-kilowatt micro-turbine, an active powered eAxle, and thermoelectric heat recovery, Project Ebony provides 110 continuous hours of rolling highway operation without refueling or grid charging.",
    6: "Slide six. Sovereign expeditionary microgrid. On site, the trailer decouples into an islanded 480-volt 3-phase substation. It deploys an 18-kilowatt non-specular matte ETFE tactical solar canopy engineered for ULCANS camouflage compatibility, sustaining forward operations for over 30 days off-grid.",
    7: "Slide seven. Commercial title and DFARS protection. Humphrey Virtual Farms LLC retains 100 percent commercial title to all prototype assets under Contractor-Acquired Property provisions, with complete retention of DFARS Background intellectual property.",
    8: "Slide eight. 12-month prototype milestones. Structured under a fixed-price 1.485 million dollar budget with a 150,000 dollar day-15 mobilization, advancing through hardware-in-the-loop validation to a live military field demonstration.",
    9: "Slide nine. TRL 4 verification audit. Project Ebony operates 100 percent offline on loopback with 85 of 85 unit tests passing and 17 of 17 red-team exploits blocked. We invite USACE ERDC and DIU to execute this prototype award immediately."
}

def speak_slide_ps(slide_num: int, export_wav_path: str = None) -> None:
    text = NARRATION_SCRIPTS.get(slide_num, "")
    if not text:
        return
    safe_text = text.replace('"', '`"')
    if export_wav_path:
        ps_cmd = f"""
        Add-Type -AssemblyName System.Speech;
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
        $synth.Rate = 0;
        $synth.SetOutputToWaveFile('{export_wav_path}');
        $synth.Speak('{safe_text}');
        $synth.Dispose();
        """
    else:
        ps_cmd = f"""
        Add-Type -AssemblyName System.Speech;
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
        $synth.Rate = 0;
        $synth.Speak('{safe_text}');
        $synth.Dispose();
        """
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)

def export_all_slide_audio(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Exporting 9 executive narration audio tracks to {output_dir}...")
    for slide_num in range(1, 10):
        wav_path = os.path.join(output_dir, f"slide_{slide_num:02d}_narration.wav")
        print(f"  [+] Synthesizing Slide {slide_num}/9 -> {wav_path}")
        speak_slide_ps(slide_num, export_wav_path=wav_path)
    print("[+] All 9 narration audio tracks exported successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        target_dir = sys.argv[2] if len(sys.argv) > 2 else "c2_cockpit/presentations/audio"
        export_all_slide_audio(target_dir)
    elif len(sys.argv) > 1 and sys.argv[1].isdigit():
        slide_to_speak = int(sys.argv[1])
        print(f"[*] Narrating Slide {slide_to_speak}/9 aloud...")
        speak_slide_ps(slide_to_speak)
    else:
        print("Usage: python c2_briefing_audio_narrator.py [1-9] (narrate aloud) OR --export [output_folder]")
