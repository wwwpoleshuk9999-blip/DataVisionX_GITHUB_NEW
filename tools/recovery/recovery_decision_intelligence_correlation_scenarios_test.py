#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_intelligence_correlation import (
    correlate,
)


SCENARIOS = [
    {
        "scenario": "unknown_signals",
        "intelligence": {},
        "trend": {},
        "history": {},
        "expected": {
            "correlation_state": "UNKNOWN",
            "correlation_strength": 0,
            "pattern": None,
            "recommendation": "NO_DATA",
        },
    },
    {
        "scenario": "no_alignment",
        "intelligence": {
            "intelligence_state": "STABLE",
        },
        "trend": {
            "trend_direction": "STABLE",
        },
        "history": {
            "history_state": "MIXED",
        },
        "expected": {
            "correlation_state": "NO_ALIGNMENT",
            "correlation_strength": 0,
            "pattern": "STABLE_PATTERN",
            "recommendation": "CONTINUE_MONITORING",
        },
    },
    {
        "scenario": "partial_alignment",
        "intelligence": {
            "intelligence_state": "DEGRADED",
        },
        "trend": {
            "trend_direction": "STABLE",
        },
        "history": {
            "history_state": "MIXED",
        },
        "expected": {
            "correlation_state": "PARTIAL_ALIGNMENT",
            "correlation_strength": 0.333,
            "pattern": "HIGH_RISK_STATE",
            "recommendation": "MONITOR",
        },
    },
    {
        "scenario": "strong_alignment",
        "intelligence": {
            "intelligence_state": "DEGRADED",
        },
        "trend": {
            "trend_direction": "WORSENING",
        },
        "history": {
            "history_state": "MIXED",
        },
        "expected": {
            "correlation_state": "STRONG_ALIGNMENT",
            "correlation_strength": 0.667,
            "pattern": "HIGH_RISK_STATE+WORSENING_TREND",
            "recommendation": "REVIEW_REQUIRED",
        },
    },
    {
        "scenario": "critical_alignment",
        "intelligence": {
            "intelligence_state": "CRITICAL",
        },
        "trend": {
            "trend_direction": "WORSENING",
        },
        "history": {
            "history_state": "DOMINANT",
        },
        "expected": {
            "correlation_state": "CRITICAL_ALIGNMENT",
            "correlation_strength": 1.0,
            "pattern": (
                "HIGH_RISK_STATE+WORSENING_TREND"
                "+DOMINANT_HISTORY"
            ),
            "recommendation": "IMMEDIATE_REVIEW",
        },
    },
    {
        "scenario": "stable_high_risk",
        "intelligence": {
            "intelligence_state": "DEGRADED",
        },
        "trend": {
            "trend_direction": "STABLE",
        },
        "history": {
            "history_state": "DOMINANT",
        },
        "expected": {
            "correlation_state": "STRONG_ALIGNMENT",
            "correlation_strength": 0.667,
            "pattern": (
                "HIGH_RISK_STATE+DOMINANT_HISTORY"
            ),
            "recommendation": "REVIEW_REQUIRED",
        },
    },
    {
        "scenario": "worsening_dominant_history",
        "intelligence": {
            "intelligence_state": "STABLE",
        },
        "trend": {
            "trend_direction": "WORSENING",
        },
        "history": {
            "history_state": "DOMINANT",
        },
        "expected": {
            "correlation_state": "STRONG_ALIGNMENT",
            "correlation_strength": 0.667,
            "pattern": (
                "WORSENING_TREND+DOMINANT_HISTORY"
            ),
            "recommendation": "REVIEW_REQUIRED",
        },
    },
]


def main():
    results = []

    for scenario in SCENARIOS:
        result = correlate(
            scenario["intelligence"],
            scenario["trend"],
            scenario["history"],
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
        "engine": "DTA-026.2",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_intelligence_correlation_scenarios_report.json"
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
