#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "intelligence_orchestrator_bridge_scenarios_report.json"
)


TARGETS = {
    "OBSERVE": ("MONITOR", "MONITOR"),
    "RECOVER": ("REQUEST_RECOVERY", "RECOVERY_REQUIRED"),
    "ESCALATE": ("REQUEST_ESCALATION", "ESCALATION_REQUIRED"),
}


def bridge(decision, confidence):

    if decision not in TARGETS:
        return {
            "decision": decision,
            "status": "BLOCKED",
            "orchestrator_action": "NONE",
            "target_state": "FAILED",
            "confidence": confidence,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "unknown decision",
        }

    if not isinstance(confidence, (int, float)):
        return {
            "decision": decision,
            "status": "BLOCKED",
            "orchestrator_action": "NONE",
            "target_state": "FAILED",
            "confidence": confidence,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "invalid confidence",
        }

    if confidence < 0.0 or confidence > 1.0:
        return {
            "decision": decision,
            "status": "BLOCKED",
            "orchestrator_action": "NONE",
            "target_state": "FAILED",
            "confidence": confidence,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "confidence outside valid range",
        }

    orchestrator_action, target_state = TARGETS[decision]

    return {
        "decision": decision,
        "status": "ACCEPTED",
        "orchestrator_action": orchestrator_action,
        "target_state": target_state,
        "confidence": confidence,
        "execution_allowed": False,
        "action": "NO_EXECUTION",
    }


def main():

    scenarios = [
        {
            "scenario": "observe",
            "decision": "OBSERVE",
            "confidence": 0.50,
            "expected_status": "ACCEPTED",
            "expected_action": "MONITOR",
            "expected_state": "MONITOR",
        },
        {
            "scenario": "recover",
            "decision": "RECOVER",
            "confidence": 0.90,
            "expected_status": "ACCEPTED",
            "expected_action": "REQUEST_RECOVERY",
            "expected_state": "RECOVERY_REQUIRED",
        },
        {
            "scenario": "escalate",
            "decision": "ESCALATE",
            "confidence": 0.95,
            "expected_status": "ACCEPTED",
            "expected_action": "REQUEST_ESCALATION",
            "expected_state": "ESCALATION_REQUIRED",
        },
        {
            "scenario": "unknown_decision",
            "decision": "UNKNOWN",
            "confidence": 0.80,
            "expected_status": "BLOCKED",
            "expected_action": "NONE",
            "expected_state": "FAILED",
        },
        {
            "scenario": "negative_confidence",
            "decision": "RECOVER",
            "confidence": -0.10,
            "expected_status": "BLOCKED",
            "expected_action": "NONE",
            "expected_state": "FAILED",
        },
        {
            "scenario": "overconfidence",
            "decision": "RECOVER",
            "confidence": 1.10,
            "expected_status": "BLOCKED",
            "expected_action": "NONE",
            "expected_state": "FAILED",
        },
        {
            "scenario": "invalid_confidence_type",
            "decision": "RECOVER",
            "confidence": "HIGH",
            "expected_status": "BLOCKED",
            "expected_action": "NONE",
            "expected_state": "FAILED",
        },
    ]

    tests = []

    for scenario in scenarios:

        result = bridge(
            scenario["decision"],
            scenario["confidence"],
        )

        passed = (
            result["status"] == scenario["expected_status"]
            and result["orchestrator_action"] == scenario["expected_action"]
            and result["target_state"] == scenario["expected_state"]
            and result["execution_allowed"] is False
            and result["action"] == "NO_EXECUTION"
        )

        tests.append(
            {
                "scenario": scenario["scenario"],
                "result": result,
                "passed": passed,
            }
        )

    status = (
        "READY"
        if all(test["passed"] for test in tests)
        else "FAILED"
    )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-021.2",
        "mode": "SCENARIO_TEST",
        "tests": tests,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "execution_gate_required": True,
        },
        "status": status,
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
