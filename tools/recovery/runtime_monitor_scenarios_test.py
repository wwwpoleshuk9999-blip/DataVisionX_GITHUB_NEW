#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "runtime_monitor_scenarios_report.json"
)


def check_runtime(status):

    if status == "RUNNING":
        return {
            "status": "HEALTHY",
            "next_state": "MONITORING",
            "reason": "runtime active"
        }

    if status == "STOPPED":
        return {
            "status": "RECOVERY_REQUIRED",
            "next_state": "RECOVERY_REQUIRED",
            "reason": "runtime unavailable"
        }

    if status == "RESTORED":
        return {
            "status": "HEALTHY",
            "next_state": "HEALTHY",
            "reason": "runtime recovered"
        }


def main():

    tests = [
        {
            "scenario": "runtime_online",
            "result": check_runtime("RUNNING")
        },
        {
            "scenario": "runtime_failure",
            "result": check_runtime("STOPPED")
        },
        {
            "scenario": "runtime_after_restore",
            "result": check_runtime("RESTORED")
        }
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-018.2",
        "tests": tests,
        "status": "READY"
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
