#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_analytics_report.json"
)


def analyze_events(events):

    total = len(events)

    if total == 0:
        return {
            "health_state": "UNKNOWN",
            "risk_level": "LOW",
            "dominant_decision": None,
            "confidence": 0,
            "recommendation": "NO_DATA",
        }

    decisions = {}

    for event in events:
        decision = event.get("decision")

        if decision:
            decisions[decision] = (
                decisions.get(decision, 0) + 1
            )

    dominant = max(
        decisions,
        key=decisions.get
    )

    blocked = sum(
        1
        for e in events
        if e.get("status") == "BLOCKED"
    )

    blocked_ratio = blocked / total

    confidence_values = [
        e.get("confidence")
        for e in events
        if isinstance(
            e.get("confidence"),
            (int, float)
        )
    ]

    confidence = (
        round(
            sum(confidence_values)
            / len(confidence_values),
            3
        )
        if confidence_values
        else 0
    )

    if blocked_ratio >= 0.8:
        health = "DEGRADED"
        risk = "HIGH"
        recommendation = "REVIEW_REQUIRED"

    elif blocked_ratio >= 0.5:
        health = "WARNING"
        risk = "MEDIUM"
        recommendation = "MONITOR"

    else:
        health = "STABLE"
        risk = "LOW"
        recommendation = "CONTINUE_MONITORING"


    return {
        "health_state": health,
        "risk_level": risk,
        "dominant_decision": dominant,
        "confidence": confidence,
        "recommendation": recommendation,
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

    analysis = analyze_events(events)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-024.1",
        "mode": "ANALYTICS_ONLY",
        "analysis": analysis,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
        },
        "status": "READY",
    }


    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT.write_text(
        json.dumps(
            report,
            indent=4
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            report,
            indent=4
        )
    )

    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
