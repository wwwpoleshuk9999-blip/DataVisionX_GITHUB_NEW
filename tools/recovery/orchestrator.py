#!/usr/bin/env python3

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
RECOVERY_DIR = BASE / "runtime" / "recovery"
REPORT = RECOVERY_DIR / "recovery_health_report.json"


def run(cmd):
    result = subprocess.run(
        cmd,
        cwd=BASE,
        capture_output=True,
        text=True
    )

    return {
        "command": " ".join(cmd),
        "returncode": result.returncode,
        "stdout": result.stdout[-1000:],
        "stderr": result.stderr[-1000:]
    }


def save_report(data):
    RECOVERY_DIR.mkdir(parents=True, exist_ok=True)

    REPORT.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )


def check():
    result = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {}
    }

    audit = run([
        "python",
        "devtools/auditor/auditor.py"
    ])

    result["checks"]["auditor"] = audit["returncode"] == 0

    result["status"] = (
        "HEALTHY"
        if all(result["checks"].values())
        else "WARNING"
    )

    save_report(result)

    print(json.dumps(result, indent=4))
    print()
    print("Report:", REPORT)


def full_test():
    result = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests": {}
    }

    validation = run([
        "python",
        "tools/recovery/validate_restore.py"
    ])

    disaster = run([
        "python",
        "tools/recovery/disaster_test.py"
    ])

    auto_heal = run([
        "python",
        "tools/recovery/auto_heal_test.py"
    ])

    result["tests"]["validation"] = validation["returncode"] == 0
    result["tests"]["disaster"] = disaster["returncode"] == 0
    result["tests"]["auto_heal"] = auto_heal["returncode"] == 0

    result["status"] = (
        "HEALTHY"
        if all(result["tests"].values())
        else "FAILED"
    )

    save_report(result)

    print(json.dumps(result, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: orchestrator.py [check|full-test]")
        raise SystemExit(1)

    if sys.argv[1] == "check":
        check()

    elif sys.argv[1] == "full-test":
        full_test()

    else:
        print("Unknown command")
        raise SystemExit(1)
