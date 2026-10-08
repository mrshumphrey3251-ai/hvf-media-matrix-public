"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: FIX CONSOLE IMPORTS
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sys

    import py_compile



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    TARGET_FILES = [

        os.path.join(BASE_DIR, "ebony_console.py"),

        os.path.join(BASE_DIR, "ebony_console_GREEN.py")

    ]



    IMPORT_BLOCK = """import sys

    import os

    sys.path.insert(0, r"C:\\HVF_Repos\\hvf-media-matrix-private")

    import email_triage_core

    """



    print("=" * 80)

    print("INJECTING CORE ENGINE IMPORTS INTO TOP-LEVEL HEADERS")

    print("=" * 80)



    for fpath in TARGET_FILES:

        if not os.path.exists(fpath):

            continue



        print(f"\nProcessing target: {os.path.basename(fpath)}")

        with open(fpath, "r", encoding="utf-8") as f:

            content = f.read()



        # If import already present at top level, skip

        if "import email_triage_core" in content[:1500]:

            print(f"  * [INFO] 'import email_triage_core' already present in header.")

        else:

            # Prepend to file right after initial docstring or at line 0

            if content.startswith('"""'):

                end_doc = content.find('"""', 3)

                if end_doc != -1:

                    content = content[:end_doc+3] + "\n" + IMPORT_BLOCK + content[end_doc+3:]

                else:

                    content = IMPORT_BLOCK + content

            elif content.startswith("import streamlit"):

                content = content.replace("import streamlit as st", "import streamlit as st\n" + IMPORT_BLOCK, 1)

            else:

                content = IMPORT_BLOCK + content



            with open(fpath, "w", encoding="utf-8") as f:

                f.write(content)

            print(f"  * [SUCCESS] Injected global import into {os.path.basename(fpath)}.")



        py_compile.compile(fpath, doraise=True)

        print(f"  * [SUCCESS] Clean compile verified for: {os.path.basename(fpath)}")



    print("\n" + "=" * 80)

    print("GLOBAL NAMESPACE RESTORATION COMPLETE")

    print("=" * 80)


if __name__ == "__main__":
    render()
