#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
TEST_TARGET = Path.home() / "DataVisionX_dta007_test"
REPORT = BASE / "runtime" / "recovery" / "disaster_test_report.json"


def run(cmd):
    return subprocess.run(
        cmd,
        cwd=BASE,
        text=True,
        capture_output=True
    )


def main():
    print("=== DataVisionX DTA-007 Disaster Simulation ===")

    if TEST_TARGET.exists():
        shutil.rmtree(TEST_TARGET)

    print("[1/4] Creating restore test copy")

    restore = run([
        sys.executable,
        str(BASE / "tools/recovery/cli.py"),
        "restore",
        "latest",
        "--target",
        str(TEST_TARGET)
    ])

    if restore.returncode != 0:
        raise RuntimeError(restore.stderr)

    print("[2/4] Simulating failure")

    state = TEST_TARGET / "runtime" / "state.json"

    if state.exists():
        state.write_text(
            json.dumps({"corrupted": True}, indent=4),
            encoding="utf-8"
        )

    print("[3/4] Running validation")

    audit = run([
        sys.executable,
        str(TEST_TARGET / "devtools/auditor/auditor.py")
    ])

    result = {
        "project": TEST_TARGET.name,
        "restore": True,
        "failure_simulation": True,
        "auditor_after_failure": audit.returncode == 0
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)

    REPORT.write_text(
        json.dumps(result, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(result, indent=4))
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
