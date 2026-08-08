#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_analytics_trend import analyze_trend


def main():

    scenarios = [

        {
            "scenario": "empty_history",
            "events": [],
            "expected": {
                "trend_direction": "UNKNOWN",
                "trend_strength": 0,
                "dominant_pattern": None,
                "confidence_trend": "UNKNOWN",
            },
        },

        {
            "scenario": "stable_trend",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                },
            ],
            "expected": {
                "trend_direction": "STABLE",
                "trend_strength": 0,
                "dominant_pattern": "RECOVER",
                "confidence_trend": "STABLE",
            },
        },

        {
            "scenario": "improving_trend",
            "events": [
                {
                    "decision": "ESCALATE",
                    "confidence": 0.9,
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 0.9,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                },
            ],
            "expected": {
                "trend_direction": "IMPROVING",
                "dominant_pattern": "BALANCED",
            },
        },

        {
            "scenario": "worsening_trend",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 0.9,
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 0.9,
                },
            ],
            "expected": {
                "trend_direction": "WORSENING",
                "dominant_pattern": "BALANCED",
            },
        },

        {
            "scenario": "recover_dominant",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.85,
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 0.9,
                },
            ],
            "expected": {
                "dominant_pattern": "RECOVER",
            },
        },

        {
            "scenario": "escalate_dominant",
            "events": [
                {
                    "decision": "ESCALATE",
                    "confidence": 0.9,
                },
                {
                    "decision": "ESCALATE",
                    "confidence": 0.95,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.8,
            },
            ],
            "expected": {
                "dominant_pattern": "ESCALATE",
            },
        },

        {
            "scenario": "confidence_increasing",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.6,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.7,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.9,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.95,
                },
            ],
            "expected": {
                "confidence_trend": "INCREASING",
            },
        },

        {
            "scenario": "confidence_decreasing",
            "events": [
                {
                    "decision": "RECOVER",
                    "confidence": 0.95,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.9,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.7,
                },
                {
                    "decision": "RECOVER",
                    "confidence": 0.6,
                },
            ],
            "expected": {
                "confidence_trend": "DECREASING",
            },
        },
    ]

    results = []

    for item in scenarios:

        result = analyze_trend(
            item["events"]
        )

        passed = all(
            result.get(key) == value
            for key, value in item["expected"].items()
        )

        results.append(
            {
                "scenario": item["scenario"],
                "result": result,
                "expected": item["expected"],
                "passed": passed,
            }
        )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-024.4",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": (
            "READY"
            if all(
                item["passed"]
                for item in results
            )
            else "FAILED"
        ),
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_analytics_trend_scenarios_report.json"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=4,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            report,
            indent=4,
        )
    )

    print()
    print("Report:", report_path)


if __name__ == "__main__":
    main()
