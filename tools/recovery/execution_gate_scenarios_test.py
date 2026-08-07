#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "execution_gate_scenarios_report.json"
)


def execution_gate(
    decision,
    confidence,
    target_state,
    confirmation=False,
    execution_allowed=False,
    automatic_recovery=False,
):

    valid = {
        "OBSERVE": "MONITOR",
        "RECOVER": "RECOVERY_REQUIRED",
        "ESCALATE": "ESCALATION_REQUIRED",
    }

    if decision not in valid:
        return blocked("unknown decision")

    if not isinstance(confidence, (int, float)):
        return blocked("invalid confidence")

    if confidence < 0 or confidence > 1:
        return blocked("confidence outside valid range")

    if target_state != valid[decision]:
        return blocked("target state mismatch")

    if automatic_recovery:
        return blocked("automatic recovery disabled")

    if not execution_allowed:
        return blocked("execution disabled by safety gate")

    if decision != "OBSERVE" and not confirmation:
        return blocked("confirmation required")

    return {
        "status": "READY_FOR_ORCHESTRATOR",
        "decision": decision,
        "target_state": target_state,
        "confidence": confidence,
        "execution_allowed": True,
        "action": "ORCHESTRATOR_REQUEST",
    }


def blocked(reason):

    return {
        "status": "BLOCKED",
        "target_state": "FAILED",
        "execution_allowed": False,
        "action": "NO_EXECUTION",
        "reason": reason,
    }


def main():

    scenarios = [

        {
            "scenario": "observe_safe",
            "input": (
                "OBSERVE",
                0.5,
                "MONITOR",
                False,
                False,
                False,
            ),
            "expected": "BLOCKED",
        },

        {
            "scenario": "recover_without_confirmation",
            "input": (
                "RECOVER",
                0.9,
                "RECOVERY_REQUIRED",
                False,
                True,
                False,
            ),
            "expected": "BLOCKED",
        },

        {
            "scenario": "recover_confirmed_gate",
            "input": (
                "RECOVER",
                0.9,
                "RECOVERY_REQUIRED",
                True,
                True,
                False,
            ),
            "expected": "READY_FOR_ORCHESTRATOR",
        },

        {
            "scenario": "automatic_recovery_violation",
            "input": (
                "RECOVER",
                0.9,
                "RECOVERY_REQUIRED",
                True,
                True,
                True,
            ),
            "expected": "BLOCKED",
        },

        {
            "scenario": "wrong_state",
            "input": (
                "RECOVER",
                0.9,
                "MONITOR",
                True,
                True,
                False,
            ),
            "expected": "BLOCKED",
        },

        {
            "scenario": "bad_confidence",
            "input": (
                "RECOVER",
                1.5,
                "RECOVERY_REQUIRED",
                True,
                True,
                False,
            ),
            "expected": "BLOCKED",
        },
    ]


    results = []

    for item in scenarios:

        result = execution_gate(*item["input"])

        passed = result["status"] == item["expected"]

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
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-021.4",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
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
