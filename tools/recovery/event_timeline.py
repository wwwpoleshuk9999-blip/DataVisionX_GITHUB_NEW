#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "event_timeline_report.json"
)


def create_event(
    state_from,
    state_to,
    trigger,
    result
):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "state_from": state_from,
        "state_to": state_to,
        "trigger": trigger,
        "result": result
    }


def main():

    events = [
        create_event(
            "HEALTHY",
            "MONITORING",
            "startup",
            "SUCCESS"
        ),
        create_event(
            "MONITORING",
            "RECOVERY_REQUIRED",
            "health_failure",
            "SUCCESS"
        ),
        create_event(
            "WAIT_CONFIRMATION",
            "RESTORING",
            "user_approval",
            "SUCCESS"
        ),
        create_event(
            "RECOVERY_REQUIRED",
            "RESTORING",
            "skip_confirmation",
            "BLOCKED"
        )
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-017.1",
        "events": events,
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
