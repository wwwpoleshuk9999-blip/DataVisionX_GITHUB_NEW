#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_intelligence_metrics_report.json"
)


def build_metrics(events):

    total = len(events)

    blocked = sum(
        1 for e in events
        if e.get("status") == "BLOCKED"
    )

    ready = sum(
        1 for e in events
        if e.get("status") == "READY_FOR_ORCHESTRATOR"
    )

    recover = sum(
        1 for e in events
        if e.get("decision") == "RECOVER"
    )

    escalate = sum(
        1 for e in events
        if e.get("decision") == "ESCALATE"
    )

    confidences = [
        e["confidence"]
        for e in events
        if isinstance(e.get("confidence"), (int, float))
    ]

    average_confidence = (
        round(
            sum(confidences) / len(confidences),
            3
        )
        if confidences
        else 0
    )

    return {
        "total_events": total,
        "blocked_events": blocked,
        "ready_events": ready,
        "blocked_ratio": (
            round(blocked / total, 3)
            if total else 0
        ),
        "ready_ratio": (
            round(ready / total, 3)
            if total else 0
        ),
        "recovery_count": recover,
        "escalation_count": escalate,
        "average_confidence": average_confidence,
    }


def main():

    events = [
        {
            "decision": "RECOVER",
            "confidence": 0.9,
            "status": "BLOCKED",
        },
        {
            "decision": "ESCALATE",
            "confidence": 0.95,
            "status": "BLOCKED",
        },
    ]

    metrics = build_metrics(events)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-023.3",
        "mode": "METRICS_ONLY",
        "metrics": metrics,
        "status": "READY",
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
