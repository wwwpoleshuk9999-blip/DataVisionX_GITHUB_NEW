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
    / "recovery_pattern_analyzer_report.json"
)


def analyze_pattern(events):
    event_names = [
        event.get("event", "unknown")
        for event in events
    ]

    results = [
        event.get("result", "UNKNOWN")
        for event in events
    ]

    frequencies = Counter(event_names)

    runtime_failures = frequencies.get("runtime_failed", 0)
    restore_errors = frequencies.get("restore_error", 0)

    triggered = results.count("TRIGGERED")
    failed = results.count("FAILED")

    patterns = []

    if runtime_failures >= 2:
        patterns.append("REPEATED_RUNTIME_FAILURE")

    if runtime_failures > 0 and "runtime_restored" in event_names:
        patterns.append("FAILURE_THEN_RESTORE")

    if restore_errors > 0:
        patterns.append("RECOVERY_FAILURE")

    if not patterns:
        patterns.append("NO_RECOVERY_PATTERN")

    if restore_errors > 0:
        recommendation = "ESCALATE"
    elif runtime_failures >= 2:
        recommendation = "RECOVER"
    elif triggered > 0:
        recommendation = "RECOVER"
    else:
        recommendation = "OBSERVE"

    if restore_errors > 0:
        confidence = 0.95
    elif runtime_failures >= 2:
        confidence = 0.90
    elif triggered > 0:
        confidence = 0.75
    else:
        confidence = 0.50

    return {
        "patterns": patterns,
        "event_frequency": dict(frequencies),
        "runtime_failures": runtime_failures,
        "restore_errors": restore_errors,
        "triggered_events": triggered,
        "failed_events": failed,
        "recommendation": recommendation,
        "confidence": confidence,
    }


def main():

    scenarios = [
        {
            "scenario": "healthy_runtime",
            "events": [
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
            "scenario": "failure_then_restore",
            "events": [
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
            "scenario": "repeated_failure",
            "events": [
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
            "scenario": "recovery_failure",
            "events": [
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
    ]

    tests = []

    for scenario in scenarios:
        analysis = analyze_pattern(scenario["events"])

        tests.append(
            {
                "scenario": scenario["scenario"],
                "analysis": analysis,
            }
        )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-020.3",
        "mode": "ANALYSIS_ONLY",
        "tests": tests,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
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
