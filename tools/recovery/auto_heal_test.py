#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
TARGET = Path.home() / "DataVisionX_dta007_autoheal_test"
REPORT = BASE / "runtime" / "recovery" / "auto_heal_report.json"


def run(cmd):
    return subprocess.run(
        cmd,
        cwd=BASE,
        text=True,
        capture_output=True
    )


def main():
    print("=== DataVisionX DTA-007.1 Auto-Heal Test ===")

    if TARGET.exists():
        shutil.rmtree(TARGET)

    print("[1/5] Initial restore")

    restore = run([
        sys.executable,
        str(BASE / "tools/recovery/cli.py"),
        "restore",
        "latest",
        "--target",
        str(TARGET)
    ])

    if restore.returncode != 0:
        raise RuntimeError(restore.stderr)

    print("[2/5] Injecting failure")

    state = TARGET / "runtime" / "state.json"
    state.write_text(
        json.dumps({"broken": True}, indent=4),
        encoding="utf-8"
    )

    print("[3/5] Auto restore")

    shutil.rmtree(TARGET)

    restore_again = run([
        sys.executable,
        str(BASE / "tools/recovery/cli.py"),
        "restore",
        "latest",
        "--target",
        str(TARGET)
    ])

    if restore_again.returncode != 0:
        raise RuntimeError(restore_again.stderr)

    print("[4/5] Validation")

    audit = run([
        sys.executable,
        str(TARGET / "devtools/auditor/auditor.py")
    ])

    result = {
        "failure_detected": True,
        "auto_restore": restore_again.returncode == 0,
        "final_status": "HEALTHY" if audit.returncode == 0 else "FAILED"
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(result, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(result, indent=4))
    print("Report:", REPORT)
    print("=== DTA-007.1 STATUS:", result["final_status"], "===")


if __name__ == "__main__":
    main()
