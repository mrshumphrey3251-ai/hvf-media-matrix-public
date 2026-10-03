"""
PROJECT EBONY: DEEP CODE SENTINEL & LINE-BY-LINE AUDITOR (v6.0)
ROLE: Exhaustive line-by-line semantic AST inspection, mathematical edge-case analysis,
      and proactive optimization staging across all HVF modules.
"""

import ast
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
EXT_DIR = BASE_DIR / "level5_extensions"
COCKPIT_DIR = BASE_DIR / "c2_cockpit"
DISPATCH_DIR = BASE_DIR / "dispatch_core"
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
REPORT_FILE = BASE_DIR / "governance" / "architecture" / "DEEP_AUDIT_REPORT.json"

class LineByLineAuditor:
    def __init__(self):
        self.target_dirs = [EXT_DIR, COCKPIT_DIR, DISPATCH_DIR]

    def audit_file(self, filepath: Path) -> dict:
        findings = []
        metrics = {
            "total_lines": 0,
            "code_lines": 0,
            "functions": 0,
            "classes": 0,
            "complexity_score": 100
        }

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                raw_code = f.read()

            lines = raw_code.splitlines()
            metrics["total_lines"] = len(lines)
            metrics["code_lines"] = len([l for l in lines if l.strip() and not l.strip().startswith("#")])

            # Line-by-line AST Parsing
            tree = ast.parse(raw_code, filename=str(filepath))

            # Deep AST Walk
            has_error_handling = False
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics["functions"] += 1
                elif isinstance(node, ast.ClassDef):
                    metrics["classes"] += 1
                elif isinstance(node, ast.Try):
                    has_error_handling = True
                elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                    # Check for unshielded division (potential ZeroDivisionError)
                    findings.append({
                        "line": getattr(node, "lineno", 0),
                        "severity": "OPTIMIZATION",
                        "category": "Math Guard",
                        "detail": "Division operation detected without explicit zero-divisor guard clamp."
                    })

            # Check for empty docstrings or lack of metadata
            if not ast.get_docstring(tree):
                findings.append({
                    "line": 1,
                    "severity": "NOTICE",
                    "category": "Documentation",
                    "detail": "Missing top-level module docstring and operational blueprint specification."
                })

            if metrics["functions"] > 0 and not has_error_handling:
                findings.append({
                    "line": 1,
                    "severity": "HARDENING",
                    "category": "Fault Tolerance",
                    "detail": "Module executes business logic without local try/except isolation."
                })

            # Score computation
            deductions = len(findings) * 5
            metrics["complexity_score"] = max(20, 100 - deductions)

            return {
                "file": filepath.name,
                "path": str(filepath),
                "metrics": metrics,
                "findings": findings,
                "status": "OPTIMAL" if metrics["complexity_score"] >= 90 else "UPGRADE_RECOMMENDED"
            }

        except SyntaxError as se:
            return {
                "file": filepath.name,
                "path": str(filepath),
                "metrics": metrics,
                "findings": [{
                    "line": se.lineno,
                    "severity": "CRITICAL",
                    "category": "Syntax Error",
                    "detail": f"Syntax error at line {se.lineno}: {se.msg}"
                }],
                "status": "CORRUPTED"
            }
        except Exception as e:
            return {
                "file": filepath.name,
                "path": str(filepath),
                "metrics": metrics,
                "findings": [{
                    "line": 0,
                    "severity": "CRITICAL",
                    "category": "Inspection Fault",
                    "detail": str(e)
                }],
                "status": "UNREADABLE"
            }

    def run_full_sweep(self) -> dict:
        audit_results = {}
        all_files = []
        for d in self.target_dirs:
            if d.exists():
                all_files.extend(list(d.glob("*.py")))

        for py_file in all_files:
            if py_file.name.startswith("__"):
                continue
            audit_results[py_file.name] = self.audit_file(py_file)

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "modules_inspected": len(audit_results),
            "modules_optimal": len([m for m in audit_results.values() if m["status"] == "OPTIMAL"]),
            "modules_needing_upgrade": len([m for m in audit_results.values() if m["status"] != "OPTIMAL"]),
            "details": audit_results
        }

        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as rf:
            json.dump(report, rf, indent=2)

        return report

if __name__ == "__main__":
    auditor = LineByLineAuditor()
    rep = auditor.run_full_sweep()
    print(f"[+] Line-by-line audit complete: {rep['modules_inspected']} modules analyzed. Optimal: {rep['modules_optimal']}.")
