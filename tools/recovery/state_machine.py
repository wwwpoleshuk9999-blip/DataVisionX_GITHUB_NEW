#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "state_machine_report.json"
)


TRANSITIONS = {
    "HEALTHY": [
        "MONITORING"
    ],
    "MONITORING": [
        "RECOVERY_REQUIRED",
        "HEALTHY"
    ],
    "RECOVERY_REQUIRED": [
        "WAIT_CONFIRMATION",
        "FAILED"
    ],
    "WAIT_CONFIRMATION": [
        "RESTORING",
        "FAILED"
    ],
    "RESTORING": [
        "RECOVERY_COMPLETE",
        "FAILED"
    ],
    "RECOVERY_COMPLETE": [
        "HEALTHY"
    ],
    "FAILED": [
        "RECOVERY_REQUIRED"
    ]
}


def transition(current, target):

    if target in TRANSITIONS.get(current, []):
        return {
            "allowed": True,
            "from": current,
            "to": target
        }

    return {
        "allowed": False,
        "from": current,
        "to": target
    }


def main():

    tests = [
        {
            "scenario": "normal_monitoring",
            "result": transition(
                "HEALTHY",
                "MONITORING"
            )
        },
        {
            "scenario": "start_recovery",
            "result": transition(
                "MONITORING",
                "RECOVERY_REQUIRED"
            )
        },
        {
            "scenario": "invalid_skip_confirmation",
            "result": transition(
                "RECOVERY_REQUIRED",
                "RESTORING"
            )
        }
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-016.1",
        "states": list(TRANSITIONS.keys()),
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
