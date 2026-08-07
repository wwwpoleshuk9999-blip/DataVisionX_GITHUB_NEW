#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "intelligence_orchestrator_bridge_report.json"
)


DECISION_TARGETS = {
    "OBSERVE": "MONITOR",
    "RECOVER": "RECOVERY_REQUIRED",
    "ESCALATE": "ESCALATION_REQUIRED",
}


def bridge_to_orchestrator(decision, confidence):

    if decision not in DECISION_TARGETS:
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

    if decision == "OBSERVE":
        orchestrator_action = "MONITOR"

    elif decision == "RECOVER":
        orchestrator_action = "REQUEST_RECOVERY"

    elif decision == "ESCALATE":
        orchestrator_action = "REQUEST_ESCALATION"

    return {
        "decision": decision,
        "status": "ACCEPTED",
        "orchestrator_action": orchestrator_action,
        "target_state": DECISION_TARGETS[decision],
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
        },
        {
            "scenario": "recover",
            "decision": "RECOVER",
            "confidence": 0.90,
        },
        {
            "scenario": "escalate",
            "decision": "ESCALATE",
            "confidence": 0.95,
        },
    ]

    results = []

    for scenario in scenarios:

        result = bridge_to_orchestrator(
            scenario["decision"],
            scenario["confidence"],
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
        "engine": "DTA-021.1",
        "mode": "FOUNDATION_ONLY",
        "tests": results,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
            "execution_gate_required": True,
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
