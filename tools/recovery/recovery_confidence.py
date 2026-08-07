#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_confidence_report.json"
)


def evaluate_confidence(confidence, recommendation):

    if confidence >= 0.80:
        risk_level = "HIGH"
        priority = "CRITICAL"
    elif confidence >= 0.50:
        risk_level = "MEDIUM"
        priority = "NORMAL"
    else:
        risk_level = "LOW"
        priority = "LOW"

    if recommendation == "ESCALATE":
        priority = "CRITICAL"
        risk_level = "HIGH"

    return {
        "confidence": confidence,
        "risk_level": risk_level,
        "priority": priority,
        "recommendation": recommendation,
    }


def main():

    scenarios = [
        {
            "scenario": "healthy_runtime",
            "confidence": 0.50,
            "recommendation": "OBSERVE",
        },
        {
            "scenario": "single_failure",
            "confidence": 0.75,
            "recommendation": "RECOVER",
        },
        {
            "scenario": "repeated_failure",
            "confidence": 0.90,
            "recommendation": "RECOVER",
        },
        {
            "scenario": "recovery_failure",
            "confidence": 0.95,
            "recommendation": "ESCALATE",
        },
    ]

    tests = []

    for scenario in scenarios:

        evaluation = evaluate_confidence(
            scenario["confidence"],
            scenario["recommendation"],
        )

        tests.append(
            {
                "scenario": scenario["scenario"],
                "evaluation": evaluation,
            }
        )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-020.4",
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
