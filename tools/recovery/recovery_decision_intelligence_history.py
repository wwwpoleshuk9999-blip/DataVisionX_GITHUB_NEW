#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_intelligence_history_report.json"
)


def aggregate_history(events):
    total = len(events)

    if total == 0:
        return {
            "total_events": 0,
            "recover_count": 0,
            "escalate_count": 0,
            "recover_ratio": 0,
            "escalate_ratio": 0,
            "average_confidence": 0,
            "dominant_decision": None,
            "history_state": "EMPTY",
        }

    recover_count = sum(
        1
        for event in events
        if event.get("decision") == "RECOVER"
    )

    escalate_count = sum(
        1
        for event in events
        if event.get("decision") == "ESCALATE"
    )

    confidence_values = [
        event.get("confidence")
        for event in events
        if isinstance(
            event.get("confidence"),
            (int, float),
        )
    ]

    average_confidence = round(
        sum(confidence_values)
        / len(confidence_values),
        3,
    ) if confidence_values else 0

    if recover_count > escalate_count:
        dominant_decision = "RECOVER"
    elif escalate_count > recover_count:
        dominant_decision = "ESCALATE"
    else:
        dominant_decision = "BALANCED"

    if total >= 4 and (
        recover_count / total >= 0.75
        or escalate_count / total >= 0.75
    ):
        history_state = "DOMINANT"
    elif total >= 2:
        history_state = "MIXED"
    else:
        history_state = "INITIAL"

    return {
        "total_events": total,
        "recover_count": recover_count,
        "escalate_count": escalate_count,
        "recover_ratio": round(
            recover_count / total,
            3,
        ),
        "escalate_ratio": round(
            escalate_count / total,
            3,
        ),
        "average_confidence": average_confidence,
        "dominant_decision": dominant_decision,
        "history_state": history_state,
    }


def main():
    events = [
        {
            "decision": "RECOVER",
            "confidence": 0.85,
        },
        {
            "decision": "RECOVER",
            "confidence": 0.90,
        },
        {
            "decision": "ESCALATE",
            "confidence": 0.95,
        },
        {
            "decision": "ESCALATE",
            "confidence": 0.98,
        },
    ]

    aggregation = aggregate_history(events)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-025.3",
        "mode": "REPORT_ONLY",
        "aggregation": aggregation,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
        },
        "status": "READY",
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            report,
            indent=4,
        ),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
