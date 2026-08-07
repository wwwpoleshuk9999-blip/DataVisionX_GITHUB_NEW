#!/usr/bin/env python3

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_intelligence_report.json"
)


def analyze_history(events):
    total = len(events)

    successful = sum(
        1 for event in events
        if event.get("result") == "SUCCESS"
    )

    failed = sum(
        1 for event in events
        if event.get("result") == "FAILED"
    )

    triggered = sum(
        1 for event in events
        if event.get("result") == "TRIGGERED"
    )

    event_types = Counter(
        event.get("event", "unknown")
        for event in events
    )

    if failed > 0:
        recommendation = "ESCALATE"
    elif triggered > 0:
        recommendation = "RECOVER"
    else:
        recommendation = "OBSERVE"

    return {
        "total_events": total,
        "successful_events": successful,
        "failed_events": failed,
        "triggered_events": triggered,
        "event_frequency": dict(event_types),
        "recommendation": recommendation,
    }


def main():

    history = [
        {
            "event": "runtime_started",
            "result": "SUCCESS",
        },
        {
            "event": "runtime_failed",
            "result": "TRIGGERED",
        },
        {
            "event": "runtime_failed",
            "result": "TRIGGERED",
        },
        {
            "event": "runtime_restored",
            "result": "SUCCESS",
        },
    ]

    analysis = analyze_history(history)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-020.1",
        "mode": "ANALYSIS_ONLY",
        "history": history,
        "analysis": analysis,
        "execution": {
            "automatic_recovery": False,
            "action": "NO_EXECUTION",
        },
        "status": "READY",
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)

    REPORT.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
