#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_intelligence_metrics import build_metrics


def main():

    scenarios = [

        {
            "scenario": "empty_metrics",
            "events": [],
            "checks": {
                "total_events": 0,
                "blocked_events": 0,
                "ready_events": 0,
            },
        },

        {
            "scenario": "blocked_only_metrics",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.9,
                    "status": "BLOCKED",
                }
            ],
            "checks": {
                "blocked_events": 1,
                "ready_events": 0,
            },
        },

        {
            "scenario": "ready_only_metrics",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.9,
                    "status": "READY_FOR_ORCHESTRATOR",
                }
            ],
            "checks": {
                "ready_events": 1,
                "blocked_events": 0,
            },
        },

        {
            "scenario": "mixed_metrics",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.9,
                    "status": "BLOCKED",
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 0.95,
                    "status": "READY_FOR_ORCHESTRATOR",
                },
            ],
            "checks": {
                "total_events": 2,
                "recovery_count": 1,
                "escalation_count": 1,
            },
        },

        {
            "scenario": "confidence_average",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                    "status": "BLOCKED",
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 1.0,
                    "status": "BLOCKED",
                },
            ],
            "checks": {
                "average_confidence": 0.9,
            },
        },

    ]

    results = []

    for item in scenarios:

        result = build_metrics(
            item["events"]
        )

        passed = all(
            result.get(key) == value
            for key, value in item["checks"].items()
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
        "engine": "DTA-023.4",
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
        / "recovery_intelligence_metrics_scenarios_report.json"
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", path)


if __name__ == "__main__":
    main()
