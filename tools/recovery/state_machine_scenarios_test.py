#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "state_machine_scenarios_report.json"
)


TRANSITIONS = {
    "HEALTHY": ["MONITORING"],
    "MONITORING": ["RECOVERY_REQUIRED", "HEALTHY"],
    "RECOVERY_REQUIRED": ["WAIT_CONFIRMATION", "FAILED"],
    "WAIT_CONFIRMATION": ["RESTORING", "FAILED"],
    "RESTORING": ["RECOVERY_COMPLETE", "FAILED"],
    "RECOVERY_COMPLETE": ["HEALTHY"],
    "FAILED": ["RECOVERY_REQUIRED"]
}


def move(current, target):
    return {
        "from": current,
        "to": target,
        "allowed": target in TRANSITIONS.get(current, [])
    }


def main():

    tests = [
        {
            "scenario": "normal_recovery_cycle",
            "steps": [
                move("HEALTHY", "MONITORING"),
                move("MONITORING", "RECOVERY_REQUIRED"),
                move("RECOVERY_REQUIRED", "WAIT_CONFIRMATION"),
                move("WAIT_CONFIRMATION", "RESTORING"),
                move("RESTORING", "RECOVERY_COMPLETE"),
                move("RECOVERY_COMPLETE", "HEALTHY")
            ]
        },
        {
            "scenario": "failed_recovery_cycle",
            "steps": [
                move("RECOVERY_REQUIRED", "FAILED"),
                move("FAILED", "RECOVERY_REQUIRED")
            ]
        },
        {
            "scenario": "blocked_direct_restore",
            "steps": [
                move("RECOVERY_REQUIRED", "RESTORING")
            ]
        }
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-016.2",
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
