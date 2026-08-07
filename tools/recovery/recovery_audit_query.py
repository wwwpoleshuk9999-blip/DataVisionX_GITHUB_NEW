#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


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


def query_events(
    decision=None,
    status=None,
    target_state=None,
    min_confidence=None,
):

    events = load_events()

    result = []

    for event in events:

        if decision and event.get("decision") != decision:
            continue

        if status and event.get("status") != status:
            continue

        if target_state and event.get("target_state") != target_state:
            continue

        if (
            min_confidence is not None
            and event.get("confidence", 0) < min_confidence
        ):
            continue

        result.append(event)

    return result


def summary(events):

    return {
        "total": len(events),
        "blocked": len(
            [
                x for x in events
                if x.get("status") == "BLOCKED"
            ]
        ),
        "ready": len(
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
        "engine": "DTA-022.3",
        "mode": "QUERY_FOUNDATION",

        "queries": {
            "all_events": summary(events),

            "recover_blocked": summary(
                query_events(
                    decision="RECOVER",
                    status="BLOCKED",
                )
            ),

            "high_confidence": summary(
                query_events(
                    min_confidence=0.9
                )
            ),
        },

        "status": "READY",
    }


    print(
        json.dumps(
            report,
            indent=4
        )
    )


if __name__ == "__main__":
    main()
