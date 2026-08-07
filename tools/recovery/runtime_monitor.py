#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "runtime_monitor_report.json"
)


def health_check(runtime_status):
    if runtime_status == "RUNNING":
        return {
            "status": "HEALTHY",
            "reason": "runtime active"
        }

    return {
        "status": "RECOVERY_REQUIRED",
        "reason": "runtime unavailable"
    }


def main():

    tests = [
        {
            "scenario": "runtime_alive",
            "result": health_check("RUNNING")
        },
        {
            "scenario": "runtime_missing",
            "result": health_check("STOPPED")
        }
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-018.1",
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
