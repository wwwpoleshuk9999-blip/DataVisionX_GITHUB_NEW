#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_intelligence_synthesis import (
    synthesize,
)


SCENARIOS = [
    {
        "scenario": "unknown_inputs",
        "intelligence": {},
        "trend": {},
        "history": {},
        "correlation": {},
        "expected": {
            "synthesis_state": "UNKNOWN",
            "synthesis_strength": 0,
            "dominant_signal": None,
            "recommendation": "NO_DATA",
            "review_required": False,
        },
    },
    {
        "scenario": "stable_synthesis",
        "intelligence": {
            "intelligence_state": "STABLE",
        },
        "trend": {
            "trend_direction": "STABLE",
        },
        "history": {
            "history_state": "MIXED",
        },
        "correlation": {
            "correlation_state": "NO_ALIGNMENT",
        },
        "expected": {
            "synthesis_state": "STABLE",
            "synthesis_strength": 0.25,
            "dominant_signal": "STABLE_PATTERN",
            "recommendation": "CONTINUE_MONITORING",
            "review_required": False,
        },
    },
    {
        "scenario": "partial_risk",
        "intelligence": {
            "intelligence_state": "DEGRADED",
        },
        "trend": {
            "trend_direction": "STABLE",
        },
        "history": {
            "history_state": "MIXED",
        },
        "correlation": {
            "correlation_state": "PARTIAL_ALIGNMENT",
        },
        "expected": {
            "synthesis_state": "WARNING",
            "synthesis_strength": 0.5,
            "dominant_signal": "PARTIAL_RISK",
            "recommendation": "MONITOR",
            "review_required": False,
        },
    },
    {
        "scenario": "strong_risk",
        "intelligence": {
            "intelligence_state": "DEGRADED",
        },
        "trend": {
            "trend_direction": "WORSENING",
        },
        "history": {
            "history_state": "MIXED",
        },
        "correlation": {
            "correlation_state": "STRONG_ALIGNMENT",
        },
        "expected": {
            "synthesis_state": "DEGRADED",
            "synthesis_strength": 0.8,
            "dominant_signal": "MULTI_LAYER_RISK",
            "recommendation": "REVIEW_REQUIRED",
            "review_required": True,
        },
    },
    {
        "scenario": "critical_synthesis",
        "intelligence": {
            "intelligence_state": "CRITICAL",
        },
        "trend": {
            "trend_direction": "WORSENING",
        },
        "history": {
            "history_state": "DOMINANT",
        },
        "correlation": {
            "correlation_state": "CRITICAL_ALIGNMENT",
        },
        "expected": {
            "synthesis_state": "CRITICAL",
            "synthesis_strength": 1.0,
            "dominant_signal": "MULTI_LAYER_CRITICAL",
            "recommendation": "IMMEDIATE_REVIEW",
            "review_required": True,
        },
    },
    {
        "scenario": "improving_high_risk",
        "intelligence": {
            "intelligence_state": "DEGRADED",
        },
        "trend": {
            "trend_direction": "IMPROVING",
        },
        "history": {
            "history_state": "DOMINANT",
        },
        "correlation": {
            "correlation_state": "STRONG_ALIGNMENT",
        },
        "expected": {
            "synthesis_state": "STABLE",
            "synthesis_strength": 0.25,
            "dominant_signal": "STABLE_PATTERN",
            "recommendation": "CONTINUE_MONITORING",
            "review_required": False,
        },
    },
    {
        "scenario": "mixed_signals",
        "intelligence": {
            "intelligence_state": "WARNING",
        },
        "trend": {
            "trend_direction": "WORSENING",
        },
        "history": {
            "history_state": "MIXED",
        },
        "correlation": {
            "correlation_state": "PARTIAL_ALIGNMENT",
        },
        "expected": {
            "synthesis_state": "WARNING",
            "synthesis_strength": 0.5,
            "dominant_signal": "PARTIAL_RISK",
            "recommendation": "MONITOR",
            "review_required": False,
        },
    },
]


def main():
    results = []

    for scenario in SCENARIOS:
        result = synthesize(
            scenario["intelligence"],
            scenario["trend"],
            scenario["history"],
            scenario["correlation"],
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
        "engine": "DTA-027.2",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_intelligence_synthesis_scenarios_report.json"
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
