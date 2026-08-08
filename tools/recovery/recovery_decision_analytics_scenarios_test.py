#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_analytics import analyze_events


def main():

    scenarios = [

        {
            "scenario": "empty_analysis",
            "events": [],
            "expected": {
                "health_state": "UNKNOWN",
                "risk_level": "LOW",
            },
        },

        {
            "scenario": "stable_state",
            "events": [
                {
                    "decision": "OBSERVE",
                    "confidence": 0.5,
                    "status": "READY_FOR_ORCHESTRATOR",
                }
            ],
            "expected": {
                "health_state": "STABLE",
                "risk_level": "LOW",
            },
        },

        {
            "scenario": "warning_state",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                    "status": "BLOCKED",
                },
                {
                    "decision": "OBSERVE",
                    "confidence": 0.5,
                    "status": "READY_FOR_ORCHESTRATOR",
                },
            ],
            "expected": {
                "health_state": "WARNING",
                "risk_level": "MEDIUM",
            },
        },

        {
            "scenario": "degraded_high_risk",
            "events": [
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
            ],
            "expected": {
                "health_state": "DEGRADED",
                "risk_level": "HIGH",
            },
        },

        {
            "scenario": "dominant_decision",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.9,
                    "status": "BLOCKED",
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                    "status": "BLOCKED",
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 0.95,
                    "status": "BLOCKED",
                },
            ],
            "expected": {
                "dominant_decision": "RECOVER",
            },
        },

    ]

    results = []

    for item in scenarios:

        result = analyze_events(
            item["events"]
        )

        passed = all(
            result.get(k) == v
            for k, v in item["expected"].items()
        )

        results.append(
            {
                "scenario": item["scenario"],
                "result": result,
                "passed": passed,
            }
        )


    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-024.2",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": (
            "READY"
            if all(x["passed"] for x in results)
            else "FAILED"
        ),
    }


    path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_analytics_scenarios_report.json"
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", path)


if __name__ == "__main__":
    main()
