import subprocess

def ignite_voice(text):
    """
    Sovereign Vocal Cortex: Zero-cost, 100% local speech synthesis.
    Forced Female Voice Matrix. Runs entirely on bare-metal Windows SAPI.
    """
    try:
        print("[*] Engaging Sovereign Local Vocal Cortex (Female Voice Override)...")
        clean_text = text.replace('"', '\"').replace("'", "''")
        
        # Injects the strict Female gender requirement into the local Windows engine
        ps_cmd = f"Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female); $synth.Speak(\"{clean_text}\");"
        
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
        
        if res.returncode == 0:
            print("[+] SOVEREIGN VOCAL TRANSMISSION COMPLETE.")
            return True
        else:
            print(f"[-] VOCAL EXECUTION ERROR: {res.stderr}")
            return False
    except Exception as e:
        print(f"[-] VOCAL FAILOVER EXPOSED: {str(e)}")
        return False

if __name__ == "__main__":
    ignite_voice("The sovereign matrix is fully operational. I am Ebony, and this is my true voice.")
