#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_intelligence import (
    analyze_intelligence,
)


SCENARIOS = [
    {
        "scenario": "unknown_state",
        "args": {
            "health_state": "UNKNOWN",
            "risk_level": "LOW",
            "dominant_decision": None,
            "confidence": 0,
            "trend_direction": "UNKNOWN",
            "trend_strength": 0,
        },
        "expected": {
            "intelligence_state": "UNKNOWN",
            "priority": "LOW",
            "recommendation": "NO_DATA",
            "review_required": False,
        },
    },
    {
        "scenario": "stable_low_risk",
        "args": {
            "health_state": "STABLE",
            "risk_level": "LOW",
            "dominant_decision": "OBSERVE",
            "confidence": 0.5,
            "trend_direction": "STABLE",
            "trend_strength": 0,
        },
        "expected": {
            "intelligence_state": "STABLE",
            "priority": "LOW",
            "recommendation": "MONITOR",
            "review_required": False,
        },
    },
    {
        "scenario": "medium_risk",
        "args": {
            "health_state": "WARNING",
            "risk_level": "MEDIUM",
            "dominant_decision": "RECOVER",
            "confidence": 0.65,
            "trend_direction": "STABLE",
            "trend_strength": 0,
        },
        "expected": {
            "intelligence_state": "WARNING",
            "priority": "HIGH",
            "recommendation": "MONITOR",
            "review_required": False,
        },
    },
    {
        "scenario": "high_risk",
        "args": {
            "health_state": "DEGRADED",
            "risk_level": "HIGH",
            "dominant_decision": "RECOVER",
            "confidence": 0.8,
            "trend_direction": "STABLE",
            "trend_strength": 0,
        },
        "expected": {
            "intelligence_state": "DEGRADED",
            "priority": "CRITICAL",
            "recommendation": "REVIEW_REQUIRED",
            "review_required": True,
        },
    },
    {
        "scenario": "worsening_high_risk",
        "args": {
            "health_state": "DEGRADED",
            "risk_level": "HIGH",
            "dominant_decision": "RECOVER",
            "confidence": 0.85,
            "trend_direction": "WORSENING",
            "trend_strength": 0.5,
        },
        "expected": {
            "intelligence_state": "DEGRADED",
            "priority": "CRITICAL",
            "recommendation": "IMMEDIATE_REVIEW",
            "review_required": True,
        },
    },
    {
        "scenario": "improving_high_risk",
        "args": {
            "health_state": "DEGRADED",
            "risk_level": "HIGH",
            "dominant_decision": "RECOVER",
            "confidence": 0.85,
            "trend_direction": "IMPROVING",
            "trend_strength": 0.5,
        },
        "expected": {
            "intelligence_state": "DEGRADED",
            "priority": "CRITICAL",
            "recommendation": "CONTINUE_MONITORING",
            "review_required": False,
        },
    },
    {
        "scenario": "critical_confidence",
        "args": {
            "health_state": "DEGRADED",
            "risk_level": "HIGH",
            "dominant_decision": "RECOVER",
            "confidence": 0.95,
            "trend_direction": "WORSENING",
            "trend_strength": 0.75,
        },
        "expected": {
            "intelligence_state": "CRITICAL",
            "priority": "CRITICAL",
            "recommendation": "IMMEDIATE_REVIEW",
            "review_required": True,
        },
    },
    {
        "scenario": "review_required",
        "args": {
            "health_state": "WARNING",
            "risk_level": "HIGH",
            "dominant_decision": "ESCALATE",
            "confidence": 0.9,
            "trend_direction": "STABLE",
            "trend_strength": 0,
        },
        "expected": {
            "intelligence_state": "DEGRADED",
            "priority": "CRITICAL",
            "recommendation": "REVIEW_REQUIRED",
            "review_required": True,
        },
    },
]


def main():
    results = []

    for scenario in SCENARIOS:
        result = analyze_intelligence(
            **scenario["args"]
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
        "engine": "DTA-025.2",
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
        / "recovery_decision_intelligence_scenarios_report.json"
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
