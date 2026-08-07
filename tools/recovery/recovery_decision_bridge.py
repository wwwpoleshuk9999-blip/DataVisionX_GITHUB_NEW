#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_bridge_report.json"
)


ALLOWED_DECISIONS = {
    "OBSERVE": "MONITOR",
    "RECOVER": "RECOVERY_REQUIRED",
    "ESCALATE": "ESCALATION_REQUIRED",
}


def bridge_decision(recommendation, confidence):

    if recommendation not in ALLOWED_DECISIONS:
        return {
            "decision": recommendation,
            "status": "BLOCKED",
            "target_state": "FAILED",
            "confidence": confidence,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "unknown recovery recommendation",
        }

    if not isinstance(confidence, (int, float)):
        return {
            "decision": recommendation,
            "status": "BLOCKED",
            "target_state": "FAILED",
            "confidence": confidence,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "invalid confidence value",
        }

    if confidence < 0.0 or confidence > 1.0:
        return {
            "decision": recommendation,
            "status": "BLOCKED",
            "target_state": "FAILED",
            "confidence": confidence,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "confidence outside valid range",
        }

    return {
        "decision": recommendation,
        "status": "ACCEPTED",
        "target_state": ALLOWED_DECISIONS[recommendation],
        "confidence": confidence,
        "execution_allowed": False,
        "action": "NO_EXECUTION",
    }


def main():

    scenarios = [
        {
            "scenario": "observe",
            "recommendation": "OBSERVE",
            "confidence": 0.50,
        },
        {
            "scenario": "recover",
            "recommendation": "RECOVER",
            "confidence": 0.90,
        },
        {
            "scenario": "escalate",
            "recommendation": "ESCALATE",
            "confidence": 0.95,
        },
        {
            "scenario": "unknown_decision",
            "recommendation": "UNKNOWN",
            "confidence": 0.80,
        },
        {
            "scenario": "invalid_confidence",
            "recommendation": "RECOVER",
            "confidence": 1.50,
        },
    ]

    tests = []

    for scenario in scenarios:

        result = bridge_decision(
            scenario["recommendation"],
            scenario["confidence"],
        )

        tests.append(
            {
                "scenario": scenario["scenario"],
                "input": {
                    "recommendation": scenario["recommendation"],
                    "confidence": scenario["confidence"],
                },
                "result": result,
            }
        )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-020.5",
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
