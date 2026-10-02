import subprocess
import datetime
import sys

# HVF Media Matrix - Diagnostic Logger
# Engineered for secure, scalable error extraction across all modules.

def execute_diagnostic():
    print("==================================================")
    print("HVF Media Matrix: Diagnostic System Engaged.")
    print("==================================================")
    
    # Prompts for the exact command to ensure no hardcoded vulnerabilities
    command = input("Enter the exact command you use to run Ebony (e.g., python ebony.py): ")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"ebony_diagnostic_{timestamp}.log"

    print(f"\nExecuting '{command}' and isolating telemetry...")
    
    try:
        # Executes the command and forces standard output and errors into memory
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Writes the captured data securely to a localized log file
        with open(log_file, "w", encoding="utf-8") as file:
            file.write("--- HVF MEDIA MATRIX DIAGNOSTIC LOG ---\n")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Command: {command}\n\n")
            file.write("--- SYSTEM ERROR (BREAK POINT) ---\n")
            file.write(result.stderr + "\n\n")
            file.write("--- SYSTEM OUTPUT ---\n")
            file.write(result.stdout + "\n")

        print(f"\n[SUCCESS] Diagnostic complete.")
        print(f"The exact failure point has been captured in: {log_file}")
        print("Please open this file, copy the contents, and transmit them for architectural analysis.")

    except Exception as e:
        print(f"\n[CRITICAL FAILURE] The diagnostic tool encountered an anomaly: {e}")

if __name__ == "__main__":
    execute_diagnostic()