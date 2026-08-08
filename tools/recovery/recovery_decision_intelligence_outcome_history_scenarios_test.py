#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_intelligence_outcome_history import (
    append_outcome,
    summarize_history,
)


SCENARIOS = [
    {
        "scenario": "empty_history",
        "events": [],
        "expected": {
            "total_events": 0,
            "current_state": "UNKNOWN",
            "average_strength": 0,
            "review_required_count": 0,
            "history_state": "EMPTY",
        },
    },
    {
        "scenario": "single_stable",
        "events": [
            {
                "outcome_state": "STABLE",
                "outcome_strength": 0.25,
                "review_required": False,
            }
        ],
        "expected": {
            "total_events": 1,
            "current_state": "STABLE",
            "average_strength": 0.25,
            "review_required_count": 0,
            "history_state": "INITIAL",
        },
    },
    {
        "scenario": "single_warning",
        "events": [
            {
                "outcome_state": "WARNING",
                "outcome_strength": 0.5,
                "review_required": False,
            }
        ],
        "expected": {
            "total_events": 1,
            "current_state": "WARNING",
            "average_strength": 0.5,
            "review_required_count": 0,
            "history_state": "INITIAL",
        },
    },
    {
        "scenario": "single_degraded",
        "events": [
            {
                "outcome_state": "DEGRADED",
                "outcome_strength": 0.8,
                "review_required": True,
            }
        ],
        "expected": {
            "total_events": 1,
            "current_state": "DEGRADED",
            "average_strength": 0.8,
            "review_required_count": 1,
            "history_state": "DEGRADED",
        },
    },
    {
        "scenario": "single_critical",
        "events": [
            {
                "outcome_state": "CRITICAL",
                "outcome_strength": 1.0,
                "review_required": True,
            }
        ],
        "expected": {
            "total_events": 1,
            "current_state": "CRITICAL",
            "average_strength": 1.0,
            "review_required_count": 1,
            "history_state": "CRITICAL",
        },
    },
    {
        "scenario": "multiple_outcomes",
        "events": [
            {
                "outcome_state": "STABLE",
                "outcome_strength": 0.2,
                "review_required": False,
            },
            {
                "outcome_state": "WARNING",
                "outcome_strength": 0.5,
                "review_required": False,
            },
            {
                "outcome_state": "CRITICAL",
                "outcome_strength": 1.0,
                "review_required": True,
            },
        ],
        "expected": {
            "total_events": 3,
            "current_state": "CRITICAL",
            "average_strength": 0.567,
            "review_required_count": 1,
            "history_state": "CRITICAL",
        },
    },
    {
        "scenario": "review_required_count",
        "events": [
            {
                "outcome_state": "DEGRADED",
                "outcome_strength": 0.8,
                "review_required": True,
            },
            {
                "outcome_state": "WARNING",
                "outcome_strength": 0.5,
                "review_required": False,
            },
            {
                "outcome_state": "CRITICAL",
                "outcome_strength": 1.0,
                "review_required": True,
            },
        ],
        "expected": {
            "total_events": 3,
            "current_state": "CRITICAL",
            "average_strength": 0.767,
            "review_required_count": 2,
            "history_state": "CRITICAL",
        },
    },
    {
        "scenario": "average_strength",
        "events": [
            {
                "outcome_state": "STABLE",
                "outcome_strength": 0.2,
                "review_required": False,
            },
            {
                "outcome_state": "WARNING",
                "outcome_strength": 0.6,
                "review_required": False,
            },
            {
                "outcome_state": "DEGRADED",
                "outcome_strength": 0.9,
                "review_required": True,
            },
        ],
        "expected": {
            "total_events": 3,
            "current_state": "DEGRADED",
            "average_strength": 0.567,
            "review_required_count": 1,
            "history_state": "DEGRADED",
        },
    },
]


def main():
    results = []

    for scenario in SCENARIOS:
        history = []

        for event in scenario["events"]:
            append_outcome(history, event)

        result = summarize_history(history)

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

    status = (
        "READY"
        if all(item["passed"] for item in results)
        else "FAILED"
    )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-029.2",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_intelligence_outcome_history_scenarios_report.json"
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
