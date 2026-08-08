#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_intelligence_history import (
    aggregate_history,
)


SCENARIOS = [
    {
        "scenario": "empty_history",
        "events": [],
        "expected": {
            "total_events": 0,
            "recover_count": 0,
            "escalate_count": 0,
            "recover_ratio": 0,
            "escalate_ratio": 0,
            "average_confidence": 0,
            "dominant_decision": None,
            "history_state": "EMPTY",
        },
    },
    {
        "scenario": "single_recover",
        "events": [
            {
                "decision": "RECOVER",
                "confidence": 0.9,
            },
        ],
        "expected": {
            "total_events": 1,
            "recover_count": 1,
            "escalate_count": 0,
            "recover_ratio": 1.0,
            "escalate_ratio": 0.0,
            "average_confidence": 0.9,
            "dominant_decision": "RECOVER",
            "history_state": "INITIAL",
        },
    },
    {
        "scenario": "single_escalate",
        "events": [
            {
                "decision": "ESCALATE",
                "confidence": 0.95,
            },
        ],
        "expected": {
            "total_events": 1,
            "recover_count": 0,
            "escalate_count": 1,
            "recover_ratio": 0.0,
            "escalate_ratio": 1.0,
            "average_confidence": 0.95,
            "dominant_decision": "ESCALATE",
            "history_state": "INITIAL",
        },
    },
    {
        "scenario": "balanced_history",
        "events": [
            {
                "decision": "RECOVER",
                "confidence": 0.85,
            },
            {
                "decision": "ESCALATE",
                "confidence": 0.95,
            },
        ],
        "expected": {
            "total_events": 2,
            "recover_count": 1,
            "escalate_count": 1,
            "recover_ratio": 0.5,
            "escalate_ratio": 0.5,
            "average_confidence": 0.9,
            "dominant_decision": "BALANCED",
            "history_state": "MIXED",
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
                "decision": "RECOVER",
                "confidence": 0.9,
            },
            {
                "decision": "ESCALATE",
                "confidence": 0.95,
            },
        ],
        "expected": {
            "total_events": 4,
            "recover_count": 3,
            "escalate_count": 1,
            "recover_ratio": 0.75,
            "escalate_ratio": 0.25,
            "average_confidence": 0.875,
            "dominant_decision": "RECOVER",
            "history_state": "DOMINANT",
        },
    },
    {
        "scenario": "escalate_dominant",
        "events": [
            {
                "decision": "ESCALATE",
                "confidence": 0.8,
            },
            {
                "decision": "ESCALATE",
                "confidence": 0.85,
            },
            {
                "decision": "ESCALATE",
                "confidence": 0.9,
            },
            {
                "decision": "RECOVER",
                "confidence": 0.95,
            },
        ],
        "expected": {
            "total_events": 4,
            "recover_count": 1,
            "escalate_count": 3,
            "recover_ratio": 0.25,
            "escalate_ratio": 0.75,
            "average_confidence": 0.875,
            "dominant_decision": "ESCALATE",
            "history_state": "DOMINANT",
        },
    },
    {
        "scenario": "confidence_average",
        "events": [
            {
                "decision": "RECOVER",
                "confidence": 0.8,
            },
            {
                "decision": "ESCALATE",
                "confidence": 0.9,
            },
            {
                "decision": "RECOVER",
                "confidence": 0.95,
            },
        ],
        "expected": {
            "total_events": 3,
            "recover_count": 2,
            "escalate_count": 1,
            "recover_ratio": 0.667,
            "escalate_ratio": 0.333,
            "average_confidence": 0.883,
            "dominant_decision": "RECOVER",
            "history_state": "MIXED",
        },
    },
    {
        "scenario": "history_state_transition",
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
                "decision": "RECOVER",
                "confidence": 0.9,
            },
            {
                "decision": "RECOVER",
                "confidence": 0.95,
            },
        ],
        "expected": {
            "total_events": 4,
            "recover_count": 4,
            "escalate_count": 0,
            "recover_ratio": 1.0,
            "escalate_ratio": 0.0,
            "average_confidence": 0.875,
            "dominant_decision": "RECOVER",
            "history_state": "DOMINANT",
        },
    },
]


def main():
    results = []

    for scenario in SCENARIOS:
        result = aggregate_history(
            scenario["events"]
        )

        passed = all(
            result.get(key) == value
            for key, value in scenario["expected"].items()
        )

        results.append(
            {
                "scenario": scenario["scenario"],
                "result": result,
                "expected": scenario["expected"],
                "passed": passed,
            }
        )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-025.4",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": (
            "READY"
            if all(item["passed"] for item in results)
            else "FAILED"
        ),
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_intelligence_history_scenarios_report.json"
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
