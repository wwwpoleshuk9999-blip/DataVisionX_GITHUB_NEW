#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "runtime_event_bridge_report.json"
)


def create_event(runtime_state):

    timestamp = datetime.now(timezone.utc).isoformat()

    if runtime_state == "RUNNING":
        return {
            "timestamp": timestamp,
            "event": "runtime_started",
            "state": "HEALTHY",
            "result": "SUCCESS"
        }

    if runtime_state == "STOPPED":
        return {
            "timestamp": timestamp,
            "event": "runtime_failed",
            "state": "RECOVERY_REQUIRED",
            "result": "TRIGGERED"
        }

    if runtime_state == "RESTORED":
        return {
            "timestamp": timestamp,
            "event": "runtime_restored",
            "state": "HEALTHY",
            "result": "SUCCESS"
        }


def main():

    events = [
        create_event("RUNNING"),
        create_event("STOPPED"),
        create_event("RESTORED")
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-019.1",
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
