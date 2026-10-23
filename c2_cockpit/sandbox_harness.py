import sys
import importlib.util
from pathlib import Path

def test_module(module_file):
    sandbox_dir = Path(__file__).resolve().parent
    mod_path = sandbox_dir / module_file
    
    if not mod_path.exists():
        print(f"FATAL: Candidate {module_file} does not exist.")
        sys.exit(1)
        
    try:
        spec = importlib.util.spec_from_file_location("candidate", str(mod_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        if not hasattr(mod, "render"):
            print(f"FATAL: Module is hollow or improperly formatted. Missing 'def render():'.")
            sys.exit(1)
            
        print("SUCCESS: Module compiled and render() function verified.")
        sys.exit(0)
    except Exception as e:
        print(f"SYNTAX/RUNTIME ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_module(sys.argv[1])
    else:
        print("FATAL: No module specified for testing.")
        sys.exit(1)
