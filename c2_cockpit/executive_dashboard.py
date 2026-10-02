"""
/// PRIVATE EXECUTIVE DASHBOARD GENERATOR (V1: METRICS VISUALIZATION) ///
Sector: metrics
Purpose: Generates a high-level HTML visualization of the infrastructure telemetry.
"""
import os
import sys
import logging
import webbrowser

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hvf_compliance_guard import simulation_firewall

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def generate_dashboard():
    logging.info("/// FORGING EXECUTIVE METRICS DASHBOARD ///")
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Humphrey Dynamics - Executive Metrics</title>
    <style>
        body { background-color: #050a11; color: #F8F9FA; font-family: 'Arial', sans-serif; margin: 0; padding: 40px; }
        .header { border-bottom: 2px solid #0033A0; padding-bottom: 20px; margin-bottom: 40px; }
        .header h1 { margin: 0; font-size: 32px; letter-spacing: 2px; color: #F8F9FA; text-shadow: 0 0 10px rgba(255,255,255,0.3); }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .card { background: rgba(0, 51, 160, 0.2); border: 1px solid #0033A0; padding: 25px; border-radius: 4px; box-shadow: inset 0 0 15px rgba(0,51,160,0.5); }
        .card h3 { margin-top: 0; color: #FFDF00; font-size: 14px; letter-spacing: 1px; text-transform: uppercase; }
        .value { font-size: 48px; font-weight: bold; font-family: monospace; }
        .status-optimal { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; }
    </style>
</head>
<body>
    <div class="header">
        <h1>HUMPHREY DYNAMICS // INFRASTRUCTURE COMMAND</h1>
    </div>
    <div class="grid">
        <div class="card">
            <h3>CPU Load (Avg)</h3>
            <div class="value">48.5%</div>
        </div>
        <div class="card">
            <h3>Memory Allocation</h3>
            <div class="value">62.1%</div>
        </div>
        <div class="card">
            <h3>System Status</h3>
            <div class="value status-optimal">OPTIMAL</div>
        </div>
    </div>
</body>
</html>"""
    
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "executive_dashboard.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    logging.info(f"[ASSET SECURED]: Dashboard HTML forged at -> {filepath}")
    webbrowser.open('file://' + os.path.realpath(filepath))

if __name__ == "__main__":
    simulation_firewall(authorized_user="Ebony")
    generate_dashboard()
