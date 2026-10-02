import time
import sys
import subprocess
import os
from datetime import datetime

def schedule_strike(delay_seconds, target_script="ebony_launch.py"):
    # Ensure we are looking in the right directory for the payload engine
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(base_dir, target_script)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [AUTO COMMANDER]: Countdown initiated. Strike in {delay_seconds} seconds.")
    time.sleep(delay_seconds)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [AUTO COMMANDER]: Zero hour reached. Executing {target_script}.")
    try:
        subprocess.Popen([sys.executable, script_path])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [AUTO COMMANDER]: Payload deployed. Returning to the shadows.")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [AUTO COMMANDER]: Misfire. Error: {e}")

if __name__ == "__main__":
    # If run directly from terminal, it expects a delay in seconds
    delay = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    script = sys.argv[2] if len(sys.argv) > 2 else "ebony_launch.py"
    schedule_strike(delay, script)
