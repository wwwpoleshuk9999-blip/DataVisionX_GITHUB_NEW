#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

STORAGE = (
    BASE
    / "runtime"
    / "recovery"
    / "audit_history.json"
)


def load_events():

    if not STORAGE.exists():
        return []

    return json.loads(
        STORAGE.read_text(
            encoding="utf-8"
        )
    )


def build_report(events):

    decisions = {}
    statuses = {}

    for event in events:

        decision = event.get("decision", "UNKNOWN")
        status = event.get("status", "UNKNOWN")

        decisions[decision] = (
            decisions.get(decision, 0) + 1
        )

        statuses[status] = (
            statuses.get(status, 0) + 1
        )

    return {
        "total_events": len(events),
        "decisions": decisions,
        "statuses": statuses,
        "blocked_events": len(
            [
                x for x in events
                if x.get("status") == "BLOCKED"
            ]
        ),
        "ready_events": len(
            [
                x for x in events
                if x.get("status") == "READY_FOR_ORCHESTRATOR"
            ]
        ),
    }


def main():

    events = load_events()

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-023.1",
        "mode": "REPORT_ONLY",

        "summary": build_report(events),

        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
        },

        "status": "READY",
    }


    output = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_intelligence_report.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", output)


if __name__ == "__main__":
    main()
