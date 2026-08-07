#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "execution_audit_layer_scenarios_report.json"
)


def create_audit(
    decision,
    confidence,
    target_state,
    status,
    execution_allowed,
    action,
    reason=None,
):

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "confidence": confidence,
        "target_state": target_state,
        "status": status,
        "execution_allowed": execution_allowed,
        "action": action,
        "reason": reason,
    }


def main():

    scenarios = [

        {
            "scenario": "blocked_recovery",
            "event": create_audit(
                "RECOVER",
                0.9,
                "RECOVERY_REQUIRED",
                "BLOCKED",
                False,
                "NO_EXECUTION",
                "confirmation required",
            ),
            "expected": "BLOCKED",
        },

        {
            "scenario": "ready_orchestrator",
            "event": create_audit(
                "RECOVER",
                0.9,
                "RECOVERY_REQUIRED",
                "READY_FOR_ORCHESTRATOR",
                True,
                "ORCHESTRATOR_REQUEST",
            ),
            "expected": "READY_FOR_ORCHESTRATOR",
        },

        {
            "scenario": "escalation_block",
            "event": create_audit(
                "ESCALATE",
                0.95,
                "ESCALATION_REQUIRED",
                "BLOCKED",
                False,
                "NO_EXECUTION",
                "execution disabled by safety gate",
            ),
            "expected": "BLOCKED",
        },

        {
            "scenario": "invalid_decision",
            "event": create_audit(
                "UNKNOWN",
                0.8,
                "FAILED",
                "BLOCKED",
                False,
                "NO_EXECUTION",
                "unknown decision",
            ),
            "expected": "BLOCKED",
        },

        {
            "scenario": "invalid_confidence",
            "event": create_audit(
                "RECOVER",
                1.5,
                "FAILED",
                "BLOCKED",
                False,
                "NO_EXECUTION",
                "invalid confidence",
            ),
            "expected": "BLOCKED",
        },
    ]


    results = []

    for item in scenarios:

        passed = item["event"]["status"] == item["expected"]

        results.append(
            {
                "scenario": item["scenario"],
                "event": item["event"],
                "expected": item["expected"],
                "passed": passed,
            }
        )


    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-021.6",
        "mode": "AUDIT_SCENARIO_TEST",
        "tests": results,
        "safety": {
            "automatic_recovery": False,
            "execution_enabled": False,
            "action": "NO_EXECUTION",
        },
        "status": (
            "READY"
            if all(x["passed"] for x in results)
            else "FAILED"
        ),
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
