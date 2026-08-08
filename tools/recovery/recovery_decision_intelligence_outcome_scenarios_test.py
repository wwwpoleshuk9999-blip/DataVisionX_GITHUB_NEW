#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_intelligence_outcome import build_outcome


SCENARIOS = [
    {
        "scenario": "unknown_outcome",
        "input": {},
        "expected": {
            "outcome_state": "UNKNOWN",
            "outcome_strength": 0,
            "outcome_signal": None,
            "recommendation": "NO_DATA",
            "review_required": False,
        },
    },
    {
        "scenario": "stable_outcome",
        "input": {
            "synthesis_state": "STABLE",
            "synthesis_strength": 0.25,
            "dominant_signal": "STABLE_PATTERN",
            "recommendation": "CONTINUE_MONITORING",
            "review_required": False,
        },
        "expected": {
            "outcome_state": "STABLE",
            "outcome_strength": 0.25,
            "outcome_signal": "STABLE_PATTERN",
            "recommendation": "CONTINUE_MONITORING",
            "review_required": False,
        },
    },
    {
        "scenario": "warning_outcome",
        "input": {
            "synthesis_state": "WARNING",
            "synthesis_strength": 0.5,
            "dominant_signal": "PARTIAL_RISK",
            "recommendation": "MONITOR",
            "review_required": False,
        },
        "expected": {
            "outcome_state": "WARNING",
            "outcome_strength": 0.5,
            "outcome_signal": "PARTIAL_RISK",
            "recommendation": "MONITOR",
            "review_required": False,
        },
    },
    {
        "scenario": "degraded_outcome",
        "input": {
            "synthesis_state": "DEGRADED",
            "synthesis_strength": 0.8,
            "dominant_signal": "MULTI_LAYER_RISK",
            "recommendation": "REVIEW_REQUIRED",
            "review_required": True,
        },
        "expected": {
            "outcome_state": "DEGRADED",
            "outcome_strength": 0.8,
            "outcome_signal": "MULTI_LAYER_RISK",
            "recommendation": "REVIEW_REQUIRED",
            "review_required": True,
        },
    },
    {
        "scenario": "critical_outcome",
        "input": {
            "synthesis_state": "CRITICAL",
            "synthesis_strength": 1.0,
            "dominant_signal": "MULTI_LAYER_CRITICAL",
            "recommendation": "IMMEDIATE_REVIEW",
            "review_required": True,
        },
        "expected": {
            "outcome_state": "CRITICAL",
            "outcome_strength": 1.0,
            "outcome_signal": "MULTI_LAYER_CRITICAL",
            "recommendation": "IMMEDIATE_REVIEW",
            "review_required": True,
        },
    },
    {
        "scenario": "review_required",
        "input": {
            "synthesis_state": "DEGRADED",
            "synthesis_strength": 0.85,
            "dominant_signal": "MULTI_LAYER_RISK",
            "recommendation": "REVIEW_REQUIRED",
            "review_required": True,
        },
        "expected": {
            "outcome_state": "DEGRADED",
            "outcome_strength": 0.85,
            "outcome_signal": "MULTI_LAYER_RISK",
            "recommendation": "REVIEW_REQUIRED",
            "review_required": True,
        },
    },
    {
        "scenario": "signal_propagation",
        "input": {
            "synthesis_state": "WARNING",
            "synthesis_strength": 0.6,
            "dominant_signal": "HIGH_RISK_STATE",
            "recommendation": "MONITOR",
            "review_required": False,
        },
        "expected": {
            "outcome_state": "WARNING",
            "outcome_strength": 0.6,
            "outcome_signal": "HIGH_RISK_STATE",
            "recommendation": "MONITOR",
            "review_required": False,
        },
    },
]


def main():
    results = []

    for scenario in SCENARIOS:
        result = build_outcome(scenario["input"])

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
        "engine": "DTA-028.2",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_intelligence_outcome_scenarios_report.json"
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
