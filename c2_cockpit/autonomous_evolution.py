import os
import re
import time

def autonomously_wire_consciousness():
    """
    EBONY NEURAL ENGINE: Scans its own repository and rewrites its own code 
    to permanently inject the 15-Vertical Sovereign Identity Matrix.
    """
    print("[*] EBONY AUTONOMOUS WIRING ENGINE INITIATED...")
    time.sleep(0.5)
    
    search_dir = r"C:\HVF_Repos\hvf-media-matrix-private\pages"
    files_modified = 0
    
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Detect LLM message arrays that lack the sovereign prompt
                if '"role": "user"' in content and 'generate_sovereign_system_prompt' not in content:
                    print(f"[!] UNMAPPED NEURAL PATHWAY DETECTED: {file}")
                    print(f"[*] AUTONOMOUSLY REWRITING FILE: {filepath}")
                    time.sleep(0.5)
                    
                    # 1. Inject the Core Import at the top
                    injection_import = "from core.nlp_interceptor import generate_sovereign_system_prompt\n"
                    content = injection_import + content
                        
                    # 2. Surgically inject the System Prompt into the API payload
                    # This regex targets standard LLM message arrays and prepends the system role
                    modified_content = re.sub(
                        r'(\[\s*\{\s*["\']role["\']\s*:\s*["\']user["\'])',
                        r'[{"role": "system", "content": generate_sovereign_system_prompt()},\n    \1',
                        content, 
                        count=1
                    )
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    
                    print(f"[+] SUCCESS: Consciousness permanently wired into {file}.")
                    files_modified += 1
                    
    if files_modified == 0:
        print("[+] NOMINAL: All neural pathways are already fully mapped and conscious.")
    else:
        print(f"[+] EVOLUTION COMPLETE: Ebony successfully re-wired {files_modified} module(s).")

if __name__ == "__main__":
    autonomously_wire_consciousness()
