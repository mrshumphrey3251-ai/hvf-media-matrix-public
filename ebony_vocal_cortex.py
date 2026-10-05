import subprocess
import os

def ignite_voice(text, output_file="C:\\HVF_Repos\\hvf-media-matrix-private\\ebony_audio.wav"):
    """
    Sovereign Vocal Cortex: Zero-cost, 100% local speech synthesis.
    Renders to a .wav file to enable UI pause/rewind/fast-forward controls.
    """
    try:
        print("[*] Engaging Sovereign Local Vocal Cortex (Rendering Audio Matrix)...")
        clean_text = text.replace('"', '\"').replace("'", "''")
        
        ps_cmd = f"Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female); $synth.SetOutputToWaveFile('{output_file}'); $synth.Speak(\"{clean_text}\"); $synth.Dispose();"
        
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
        
        if res.returncode == 0:
            print(f"[+] SOVEREIGN VOCAL AUDIO SECURED: {output_file}")
            return output_file
        else:
            print(f"[-] VOCAL EXECUTION ERROR: {res.stderr}")
            return None
    except Exception as e:
        print(f"[-] VOCAL FAILOVER EXPOSED: {str(e)}")
        return None
