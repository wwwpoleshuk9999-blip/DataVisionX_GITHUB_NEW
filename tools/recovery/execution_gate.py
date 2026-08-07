#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "execution_gate_report.json"
)


VALID_DECISIONS = {
    "OBSERVE": "MONITOR",
    "RECOVER": "RECOVERY_REQUIRED",
    "ESCALATE": "ESCALATION_REQUIRED",
}


def evaluate_execution(
    decision,
    confidence,
    target_state,
    confirmation=False,
    execution_allowed=False,
    automatic_recovery=False,
):

    if decision not in VALID_DECISIONS:
        return {
            "status": "BLOCKED",
            "decision": decision,
            "target_state": "FAILED",
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "unknown decision",
        }

    if not isinstance(confidence, (int, float)):
        return {
            "status": "BLOCKED",
            "decision": decision,
            "target_state": "FAILED",
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "invalid confidence",
        }

    if confidence < 0.0 or confidence > 1.0:
        return {
            "status": "BLOCKED",
            "decision": decision,
            "target_state": "FAILED",
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "confidence outside valid range",
        }

    expected_state = VALID_DECISIONS[decision]

    if target_state != expected_state:
        return {
            "status": "BLOCKED",
            "decision": decision,
            "target_state": "FAILED",
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "reason": "target state mismatch",
        }

    # Current Phoenix 012 safety mode:
    # real execution is deliberately disabled.
    if not execution_allowed:
        return {
            "status": "BLOCKED",
            "decision": decision,
            "target_state": target_state,
            "confidence": confidence,
            "confirmation": confirmation,
            "execution_allowed": False,
            "automatic_recovery": automatic_recovery,
            "action": "NO_EXECUTION",
            "reason": "execution disabled by safety gate",
        }

    if automatic_recovery:
        return {
            "status": "BLOCKED",
            "decision": decision,
            "target_state": target_state,
            "confidence": confidence,
            "confirmation": confirmation,
            "execution_allowed": False,
            "automatic_recovery": automatic_recovery,
            "action": "NO_EXECUTION",
            "reason": "automatic recovery disabled by safety policy",
        }

    if decision == "OBSERVE":
        return {
            "status": "ACCEPTED",
            "decision": decision,
            "target_state": target_state,
            "confidence": confidence,
            "confirmation": confirmation,
            "execution_allowed": False,
            "automatic_recovery": automatic_recovery,
            "action": "NO_EXECUTION",
            "reason": "observe requires no execution",
        }

    if not confirmation:
        return {
            "status": "BLOCKED",
            "decision": decision,
            "target_state": target_state,
            "confidence": confidence,
            "confirmation": False,
            "execution_allowed": False,
            "automatic_recovery": automatic_recovery,
            "action": "NO_EXECUTION",
            "reason": "user confirmation required",
        }

    return {
        "status": "READY_FOR_ORCHESTRATOR",
        "decision": decision,
        "target_state": target_state,
        "confidence": confidence,
        "confirmation": confirmation,
        "execution_allowed": True,
        "automatic_recovery": False,
        "action": "ORCHESTRATOR_REQUEST",
    }


def main():

    scenarios = [
        {
            "scenario": "observe",
            "decision": "OBSERVE",
            "confidence": 0.50,
            "target_state": "MONITOR",
        },
        {
            "scenario": "recover_blocked",
            "decision": "RECOVER",
            "confidence": 0.90,
            "target_state": "RECOVERY_REQUIRED",
        },
        {
            "scenario": "escalate_blocked",
            "decision": "ESCALATE",
            "confidence": 0.95,
            "target_state": "ESCALATION_REQUIRED",
        },
    ]

    results = []

    for scenario in scenarios:

        result = evaluate_execution(
            decision=scenario["decision"],
            confidence=scenario["confidence"],
            target_state=scenario["target_state"],
            confirmation=False,
            execution_allowed=False,
            automatic_recovery=False,
        )

        results.append(
            {
                "scenario": scenario["scenario"],
                "result": result,
            }
        )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-021.3",
        "mode": "FOUNDATION_ONLY",
        "tests": results,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "confirmation_required": True,
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
