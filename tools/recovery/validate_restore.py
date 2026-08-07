#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
AUDITOR = BASE / "devtools" / "auditor" / "auditor.py"
REPORT = BASE / "runtime" / "recovery" / "validation_report.json"


def run_auditor():
    result = subprocess.run(
        [sys.executable, str(AUDITOR)],
        cwd=BASE,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


def validate():
    print("=== DataVisionX DTA-006 Recovery Validation ===")

    checks = {
        "auditor": False,
        "runtime": False,
        "recovery": False
    }

    report = {
        "project": BASE.name,
        "status": "FAILED",
        "checks": {}
    }

    audit = run_auditor()

    checks["auditor"] = audit.get("status") in ("HEALTHY", "WARNING")
    checks["runtime"] = audit.get("runtime", {}).get("present", False)
    checks["recovery"] = audit.get("checks", {}).get("recovery", False)

    report["checks"] = checks
    report["auditor_status"] = audit.get("status")

    if all(checks.values()):
        report["status"] = "READY"

    REPORT.parent.mkdir(parents=True, exist_ok=True)

    REPORT.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)

    if report["status"] == "READY":
        print("=== DTA-006 STATUS: READY ===")
    else:
        print("=== DTA-006 STATUS: FAILED ===")


if __name__ == "__main__":
    validate()
