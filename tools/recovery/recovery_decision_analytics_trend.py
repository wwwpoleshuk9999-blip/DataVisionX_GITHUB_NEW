#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_analytics_trend_report.json"
)


def analyze_trend(events):
    total = len(events)

    if total == 0:
        return {
            "trend_direction": "UNKNOWN",
            "trend_strength": 0,
            "dominant_pattern": None,
            "confidence_trend": "UNKNOWN",
        }

    recovery_count = sum(
        1 for event in events
        if event.get("decision") == "RECOVER"
    )

    escalation_count = sum(
        1 for event in events
        if event.get("decision") == "ESCALATE"
    )

    confidence_values = [
        event.get("confidence")
        for event in events
        if isinstance(event.get("confidence"), (int, float))
    ]

    if recovery_count > escalation_count:
        dominant_pattern = "RECOVER"
    elif escalation_count > recovery_count:
        dominant_pattern = "ESCALATE"
    else:
        dominant_pattern = "BALANCED"

    if total < 2:
        trend_direction = "STABLE"
        trend_strength = 0
    else:
        midpoint = total // 2

        first_half = events[:midpoint]
        second_half = events[midpoint:]

        first_recover = sum(
            1 for event in first_half
            if event.get("decision") == "RECOVER"
        )

        second_recover = sum(
            1 for event in second_half
            if event.get("decision") == "RECOVER"
        )

        first_escalate = sum(
            1 for event in first_half
            if event.get("decision") == "ESCALATE"
        )

        second_escalate = sum(
            1 for event in second_half
            if event.get("decision") == "ESCALATE"
        )

        first_pressure = (
            first_recover + 2 * first_escalate
        )

        second_pressure = (
            second_recover + 2 * second_escalate
        )

        if second_pressure > first_pressure:
            trend_direction = "WORSENING"
        elif second_pressure < first_pressure:
            trend_direction = "IMPROVING"
        else:
            trend_direction = "STABLE"

        difference = abs(
            second_pressure - first_pressure
        )

        trend_strength = round(
            difference / max(total, 1),
            3,
        )

    if len(confidence_values) < 2:
        confidence_trend = "STABLE"
    else:
        midpoint = len(confidence_values) // 2

        first_values = confidence_values[:midpoint]
        second_values = confidence_values[midpoint:]

        first_confidence = (
            sum(first_values) / len(first_values)
        )

        second_confidence = (
            sum(second_values) / len(second_values)
        )

        if second_confidence > first_confidence:
            confidence_trend = "INCREASING"
        elif second_confidence < first_confidence:
            confidence_trend = "DECREASING"
        else:
            confidence_trend = "STABLE"

    return {
        "trend_direction": trend_direction,
        "trend_strength": trend_strength,
        "dominant_pattern": dominant_pattern,
        "confidence_trend": confidence_trend,
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

    trend = analyze_trend(events)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-024.3",
        "mode": "ANALYTICS_ONLY",
        "trend": trend,
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
