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
    / "recovery_intelligence_scenarios_report.json"
)


def analyze_history(events):
    failed = sum(
        1 for event in events
        if event.get("result") == "FAILED"
    )

    triggered = sum(
        1 for event in events
        if event.get("result") == "TRIGGERED"
    )

    frequencies = Counter(
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
        "total_events": len(events),
        "failed_events": failed,
        "triggered_events": triggered,
        "event_frequency": dict(frequencies),
        "recommendation": recommendation,
        "automatic_recovery": False,
        "action": "NO_EXECUTION",
    }


def main():

    scenarios = [
        {
            "scenario": "healthy_history",
            "history": [
                {
                    "event": "runtime_started",
                    "result": "SUCCESS",
                },
                {
                    "event": "runtime_restored",
                    "result": "SUCCESS",
                },
            ],
        },
        {
            "scenario": "single_runtime_failure",
            "history": [
                {
                    "event": "runtime_failed",
                    "result": "TRIGGERED",
                },
                {
                    "event": "runtime_restored",
                    "result": "SUCCESS",
                },
            ],
        },
        {
            "scenario": "repeated_runtime_failure",
            "history": [
                {
                    "event": "runtime_failed",
                    "result": "TRIGGERED",
                },
                {
                    "event": "runtime_failed",
                    "result": "TRIGGERED",
                },
                {
                    "event": "runtime_failed",
                    "result": "TRIGGERED",
                },
            ],
        },
        {
            "scenario": "failed_recovery",
            "history": [
                {
                    "event": "runtime_failed",
                    "result": "TRIGGERED",
                },
                {
                    "event": "restore_error",
                    "result": "FAILED",
                },
            ],
        },
        {
            "scenario": "unknown_event",
            "history": [
                {
                    "event": "unknown_runtime_event",
                    "result": "UNKNOWN",
                },
            ],
        },
    ]

    tests = []

    for scenario in scenarios:
        analysis = analyze_history(scenario["history"])

        tests.append(
            {
                "scenario": scenario["scenario"],
                "analysis": analysis,
            }
        )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-020.2",
        "mode": "ANALYSIS_ONLY",
        "tests": tests,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
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
