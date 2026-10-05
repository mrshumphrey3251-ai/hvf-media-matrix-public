import os
import sys
from pathlib import Path

priv_root = Path(r"C:\HVF_Repos\hvf-media-matrix-private")
pub_root  = Path(r"C:\HVF_Repos\hvf-media-matrix-public")

print(f"[*] Private Repo Exists: {priv_root.exists()} | Path: {priv_root}")
print(f"[*] Public Repo Exists:  {pub_root.exists()}  | Path: {pub_root}")

# Check action_desk.py in both
priv_action = priv_root / "level5_extensions" / "action_desk.py"
pub_action  = pub_root / "level5_extensions" / "action_desk.py"

print(f"[>] Private action_desk.py: {priv_action.exists()} (Size: {priv_action.stat().st_size if priv_action.exists() else 0} bytes)")
print(f"[>] Public action_desk.py:  {pub_action.exists()}  (Size: {pub_action.stat().st_size if pub_action.exists() else 0} bytes)")

# Check SIDEBAR_MODULES.json in both
priv_sb = priv_root / "governance" / "architecture" / "SIDEBAR_MODULES.json"
pub_sb  = pub_root / "governance" / "architecture" / "SIDEBAR_MODULES.json"

print(f"[>] Private SIDEBAR_MODULES: {priv_sb.exists()}")
print(f"[>] Public SIDEBAR_MODULES:  {pub_sb.exists()}")
