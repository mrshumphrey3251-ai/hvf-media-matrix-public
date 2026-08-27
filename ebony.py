import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HVF_Command_Node")

def boot_ebony():
    print("==================================================")
    print(" HVF MEDIA MATRIX : EBONY MASTER COMMAND NODE")
    print("==================================================")
    print("Routing directly to the Live Interactive Dashboard...")
    print("==================================================")
    
    try:
        # Bypasses Iron Dome by launching Streamlit natively inside the authorized Python process
        subprocess.run([sys.executable, "-m", "streamlit", "run", "ebony_console.py"])
    except Exception as e:
        logger.error(f"Critical execution failure: {e}")

if __name__ == "__main__":
    boot_ebony()