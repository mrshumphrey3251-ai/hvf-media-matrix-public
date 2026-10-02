"""
/// PRIVATE KINETIC ASSET FORGE (V17: UNIFIED SAPPHIRE FOUNDATION) ///
Sector: branding_assets
Purpose: Injects the Abyssal Sapphire color profile into the foundation base plate to perfectly frame the Platinum crest.
"""
import os
import sys
import logging
import webbrowser

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hvf_compliance_guard import simulation_firewall

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def generate_kinetic_sculpture():
    logging.info("/// FORGING UNIFIED SAPPHIRE FOUNDATION CREST ///")
    
    def build_cube(cube_class, x, y):
        return f"""
                <div class="cube {cube_class}" style="left: {x}px; top: {y}px;">
                    <div class="face front"></div><div class="face back"></div>
                    <div class="face right"></div><div class="face left"></div>
                    <div class="face top"></div><div class="face bottom"></div>
                </div>"""

    h_structure = f"""
                <!-- Left Pillar -->
                {build_cube("l-block5", 0, 160)}
                {build_cube("l-block4", 0, 120)}
                {build_cube("l-block3", 0, 80)}
                {build_cube("l-block2", 0, 40)}
                {build_cube("l-block1", 0, 0)}
                
                <!-- Right Pillar -->
                {build_cube("r-block5", 120, 160)}
                {build_cube("r-block4", 120, 120)}
                {build_cube("r-block3", 120, 80)}
                {build_cube("r-block2", 120, 40)}
                {build_cube("r-block1", 120, 0)}
                
                <!-- Crossbeam Fragments -->
                {build_cube("f1", 40, 80)}
                {build_cube("f2", 80, 80)}
    """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Humphrey Dynamics - Unified Sapphire Sovereign Crest</title>
    <style>
        :root {{
            /* Primary Layer (Sovereign Platinum) */
            --brand-primary: #F8F9FA;    
            --brand-glow: rgba(255, 255, 255, 0.7);
            
            /* Shadow Layer (Abyssal Sapphire) */
            --shadow-primary: #0033A0;
            --shadow-glow: rgba(0, 51, 160, 0.8);
            
            /* Security Lock (Aegis Gold) */
            --lock-color: #FFDF00;
            --lock-glow: rgba(255, 223, 0, 0.9);
            
            /* Environment */
            --bg-center: #050a11;        
            --bg-edge: #000000;          
            --text-color: #ffffff;       
        }}

        body {{ 
            background: radial-gradient(circle at center, var(--bg-center) 0%, var(--bg-edge) 100%); 
            overflow: hidden; display: flex; justify-content: center; align-items: center; 
            height: 100vh; margin: 0; perspective: 1200px;
        }}
        
        .scene-tilt {{ transform: rotateX(15deg); transform-style: preserve-3d; }}

        .matrix-world {{ 
            position: relative; transform-style: preserve-3d; 
            animation: worldSpinUp 15s cubic-bezier(0.4, 0.0, 0.2, 1) infinite; 
        }}
        
        .h-core {{ position: absolute; width: 160px; height: 200px; transform-style: preserve-3d; top: -100px; left: -80px; }}
        
        /* MICRO-TOLERANCE FUSION: 4px gap */
        .shadow-layer {{ transform: translate3d(4px, 4px, -4px); }}
        .primary-layer {{ transform: translate3d(0, 0, 0); }}
        
        .cube {{ position: absolute; width: 40px; height: 40px; transform-style: preserve-3d; opacity: 0; }}
        .face {{ position: absolute; width: 40px; height: 40px; backface-visibility: visible; }}
        
        .primary-layer .face {{ background: rgba(248, 249, 250, 0.2); border: 2px solid var(--brand-primary); box-shadow: inset 0 0 15px var(--brand-glow); }}
        .primary-layer .face.back, .primary-layer .face.bottom, .primary-layer .face.left {{ background: rgba(150, 150, 160, 0.5); }}

        .shadow-layer .face {{ background: rgba(0, 51, 160, 0.2); border: 2px solid var(--shadow-primary); box-shadow: inset 0 0 15px var(--shadow-glow); }}
        .shadow-layer .face.back, .shadow-layer .face.bottom, .shadow-layer .face.left {{ background: rgba(0, 20, 80, 0.5); }}

        .front  {{ transform: translateZ(20px); }}
        .back   {{ transform: rotateY(180deg) translateZ(20px); }}
        .right  {{ transform: rotateY(90deg) translateZ(20px); }}
        .left   {{ transform: rotateY(-90deg) translateZ(20px); }}
        .top    {{ transform: rotateX(90deg) translateZ(20px); }}
        .bottom {{ transform: rotateX(-90deg) translateZ(20px); }}

        /* THE UNHACKABLE LOCK */
        .security-lock {{
            position: absolute; top: 75px; left: 60px;
            width: 40px; height: 50px;
            transform-style: preserve-3d;
            animation: lockSlam 15s infinite;
        }}
        .lock-shackle {{
            position: absolute; top: -15px; left: 8px;
            width: 16px; height: 25px;
            border: 4px solid var(--lock-color);
            border-bottom: none;
            border-radius: 12px 12px 0 0;
            box-shadow: 0 0 10px var(--lock-glow), inset 0 0 5px var(--lock-glow);
        }}
        .lock-body {{
            position: absolute; top: 10px; left: 0;
            width: 40px; height: 35px;
            background: var(--lock-color);
            border-radius: 4px;
            box-shadow: 0 0 25px var(--lock-glow);
            display: flex; justify-content: center; align-items: center;
        }}
        .keyhole {{
            width: 6px; height: 6px;
            background: var(--bg-center);
            border-radius: 50%;
            position: relative;
        }}
        .keyhole::after {{
            content: ''; position: absolute; top: 4px; left: 1px;
            width: 4px; height: 6px;
            background: var(--bg-center);
            clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
        }}

        /* NARRATIVE KEYFRAMES */
        @keyframes worldSpinUp {{ 
            0% {{ transform: rotateY(0deg) rotateX(15deg); }} 
            30% {{ transform: rotateY(180deg) rotateX(15deg); }} 
            60% {{ transform: rotateY(1440deg) rotateX(5deg); }} 
            85%, 100% {{ transform: rotateY(1800deg) rotateX(15deg); }} 
        }}

        .l-block5, .r-block5 {{ animation: forgeSlam5 15s infinite; }}
        .l-block4, .r-block4 {{ animation: forgeSlam4 15s infinite; }}
        .l-block3, .r-block3 {{ animation: forgeSlam3 15s infinite; }}
        .l-block2, .r-block2 {{ animation: forgeSlam2 15s infinite; }}
        .l-block1, .r-block1 {{ animation: forgeSlam1 15s infinite; }}
        .f1, .f2 {{ animation: forgeCrossbeam 15s infinite; }}

        @keyframes forgeSlam5 {{ 0%, 25% {{ transform: translate3d(-300px, 400px, -300px) scale(0); opacity: 0; }} 55%, 90% {{ transform: translate3d(0, 0, 0) scale(1); opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}
        @keyframes forgeSlam4 {{ 0%, 30% {{ transform: translate3d(300px, 300px, 300px) scale(0); opacity: 0; }} 56%, 90% {{ transform: translate3d(0, 0, 0) scale(1); opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}
        @keyframes forgeSlam3 {{ 0%, 35% {{ transform: translate3d(-300px, -300px, 200px) scale(0); opacity: 0; }} 57%, 90% {{ transform: translate3d(0, 0, 0) scale(1); opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}
        @keyframes forgeSlam2 {{ 0%, 40% {{ transform: translate3d(200px, -400px, -300px) scale(0); opacity: 0; }} 58%, 90% {{ transform: translate3d(0, 0, 0) scale(1); opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}
        @keyframes forgeSlam1 {{ 0%, 45% {{ transform: translate3d(-400px, 0, -400px) scale(0); opacity: 0; }} 59%, 90% {{ transform: translate3d(0, 0, 0) scale(1); opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}
        @keyframes forgeCrossbeam {{ 0%, 48% {{ transform: translate3d(0, -500px, 500px) rotateX(180deg) scale(0); opacity: 0; }} 60%, 90% {{ transform: translate3d(0, 0, 0) rotateX(0deg) scale(1); opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}

        @keyframes lockSlam {{
            0%, 59% {{ transform: translateZ(600px) scale(3); opacity: 0; }}
            60% {{ transform: translateZ(22px) scale(1); opacity: 1; filter: drop-shadow(0 0 50px var(--lock-color)); }}
            62%, 90% {{ transform: translateZ(22px) scale(1); opacity: 1; filter: drop-shadow(0 0 10px var(--lock-color)); }}
            95%, 100% {{ opacity: 0; }}
        }}

        /* Anchor Plate - Unified Sapphire Background */
        .h-text-container {{ position: absolute; bottom: -200px; left: 0; width: 100%; display: flex; justify-content: center; transform-style: preserve-3d; }}
        .h-text {{
            transform: translateZ(22px);
            font-family: "Old English Text MT", "UnifrakturMaguntia", "Blackletter", serif; 
            font-size: 32px; letter-spacing: 4px; color: var(--brand-primary);
            text-shadow: 0 0 10px var(--brand-primary), 0 0 20px var(--brand-primary);
            /* INJECTED SAPPHIRE BACKGROUND */
            background: rgba(0, 51, 160, 0.85); 
            padding: 12px 25px 12px 25px;
            border-top: 2px solid var(--brand-primary); border-bottom: 2px solid var(--brand-primary);
            white-space: nowrap; 
            /* SAPPHIRE GLOW */
            box-shadow: 0 0 40px var(--shadow-glow), inset 0 0 15px rgba(0,0,0,0.5);
            animation: igniteBase 15s infinite;
        }}
        @keyframes igniteBase {{
            0%, 59% {{ opacity: 0; transform: translateZ(22px) scale(0.8); }}
            60%, 90% {{ opacity: 1; transform: translateZ(22px) scale(1); }}
            95%, 100% {{ opacity: 0; }}
        }}
    </style>
</head>
<body>
    <div class="scene-tilt">
        <div class="matrix-world">
            <div class="h-core shadow-layer">
                {h_structure}
            </div>
            <div class="h-core primary-layer">
                {h_structure}
                
                <div class="security-lock">
                    <div class="lock-shackle"></div>
                    <div class="lock-body">
                        <div class="keyhole"></div>
                    </div>
                </div>
            </div>
            <div class="h-text-container">
                <div class="h-text">Humphrey Dynamics</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kinetic_sculpture_sapphire_base.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    logging.info(f"[ASSET SECURED]: Unified Sapphire Base HTML sculpture forged at -> {filepath}")
    webbrowser.open('file://' + os.path.realpath(filepath))
    logging.info("[VISUALIZATION]: Launched unified sapphire sequence in default browser.")

if __name__ == "__main__":
    simulation_firewall(authorized_user="Ebony")
    generate_kinetic_sculpture()
