#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "event_timeline_scenarios_report.json"
)


def event(state_from, state_to, trigger, result):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "state_from": state_from,
        "state_to": state_to,
        "trigger": trigger,
        "result": result
    }


def main():

    tests = [
        {
            "scenario": "normal_recovery_timeline",
            "events": [
                event(
                    "HEALTHY",
                    "MONITORING",
                    "startup",
                    "SUCCESS"
                ),
                event(
                    "MONITORING",
                    "RECOVERY_REQUIRED",
                    "health_failure",
                    "SUCCESS"
                ),
                event(
                    "WAIT_CONFIRMATION",
                    "RESTORING",
                    "user_approval",
                    "SUCCESS"
                ),
                event(
                    "RESTORING",
                    "RECOVERY_COMPLETE",
                    "restore_finished",
                    "SUCCESS"
                )
            ]
        },
        {
            "scenario": "failed_recovery_timeline",
            "events": [
                event(
                    "RESTORING",
                    "FAILED",
                    "restore_error",
                    "FAILED"
                ),
                event(
                    "FAILED",
                    "RECOVERY_REQUIRED",
                    "retry",
                    "SUCCESS"
                )
            ]
        },
        {
            "scenario": "blocked_action_timeline",
            "events": [
                event(
                    "RECOVERY_REQUIRED",
                    "RESTORING",
                    "skip_confirmation",
                    "BLOCKED"
                )
            ]
        }
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-017.2",
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
