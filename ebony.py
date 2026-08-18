import sys
import subprocess
import logging

# HVF Media Matrix - Ebony Master Command Node
# Engineered for unified, secure routing of all Ebony subsystems.

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HVF_Command_Node")

def boot_ebony():
    print("==================================================")
    print(" HVF MEDIA MATRIX : EBONY MASTER COMMAND NODE")
    print("==================================================")
    print("Select Operational Vector:")
    print("1. Execute Autonomous LinkedIn Strike (ebony_launch.py)")
    print("2. Enter Interactive Web Console (ebony_console.py)")
    print("3. Run Diagnostic Logger (hvf_error_logger.py)")
    print("==================================================")
    
    choice = input("Enter command designation (1, 2, or 3): ")
    
    try:
        if choice == '1':
            logger.info("Routing execution to Ebony Launch Sequence...")
            subprocess.run([sys.executable, "ebony_launch.py"])
        elif choice == '2':
            logger.info("Routing execution to Ebony Web Console...")
            # Bypassing Iron Dome: Launching Streamlit natively inside the authorized Python process
            subprocess.run([sys.executable, "-m", "streamlit", "run", "ebony_console.py"])
        elif choice == '3':
            logger.info("Routing execution to Diagnostic Logger...")
            subprocess.run([sys.executable, "hvf_error_logger.py"])
        else:
            logger.error("Invalid designation. Security protocol mandates termination.")
    except Exception as e:
        logger.error(f"Critical execution failure: {e}")

if __name__ == "__main__":
    boot_ebony()