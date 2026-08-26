import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

# ==========================================
# HUMPHREY VIRTUAL FARMS - PROJECT EBONY
# STAGE-1 EVALUATION NODE (REDACTED)
# ==========================================

# Access Key Configuration
AUTHORIZED_KEY = "HVF-SIGNAL-16WJ1"

def authenticate():
    print("\n=======================================================")
    print("   PROJECT EBONY - SOVEREIGN COMMAND DECK (EVAL NODE)  ")
    print("=======================================================\n")
    print("WARNING: PROPRIETARY ARCHITECTURE.")
    print("AI ALGORITHMS, GLI MATH, AND NEURAL MODELS REDACTED.\n")
    
    attempts = 3
    while attempts > 0:
        key = input("ENTER STAGE-1 ACCESS KEY: ")
        if key == AUTHORIZED_KEY:
            print("\n[+] KEY ACCEPTED. DECRYPTING UI ARCHITECTURE...")
            time.sleep(1)
            print("[+] LAUNCHING SOVEREIGN EDGE ENVIRONMENT...")
            return True
        else:
            attempts -= 1
            print(f"[-] ACCESS DENIED. {attempts} ATTEMPTS REMAINING.")
    
    print("\n[!] SECURITY LOCKOUT TRIGGERED. TERMINATING.")
    sys.exit()

class EbonyEvalDeck(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Ebony - Stage 1 Eval (REDACTED)")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #0d0d0d; color: #00ff00; font-family: Courier;")

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Header
        header = QLabel("EBONY EDGE-COMPUTE NODE | STATUS: ACTIVE | AI: REDACTED")
        header.setStyleSheet("font-size: 18px; font-weight: bold; border-bottom: 1px solid #00ff00;")
        layout.addWidget(header)

        # Body
        body_text = (
            "\n[SYSTEM READY]\n\n"
            "> UI ARCHITECTURE: NOMINAL\n"
            "> TELEMETRY INGESTION: NOMINAL\n"
            "> EDGE-AI MODELS: [REMOVED FOR PUBLIC EVALUATION]\n"
            "> K-FOR-CRYPTO ANCHOR: [AWAITING SIGNALLINK INTEGRATION]\n\n"
            "This is the physical UI layer. In the live environment, this node processes "
            "un-spoofable GLI data and biometrics locally without cloud dependencies."
        )
        body = QLabel(body_text)
        body.setStyleSheet("font-size: 14px;")
        layout.addWidget(body)

        central_widget.setLayout(layout)

if __name__ == '__main__':
    if authenticate():
        app = QApplication(sys.argv)
        window = EbonyEvalDeck()
        window.show()
        sys.exit(app.exec_())