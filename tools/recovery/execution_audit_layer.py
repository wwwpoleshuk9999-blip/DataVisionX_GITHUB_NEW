#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "execution_audit_layer_report.json"
)


def audit_decision(
    decision,
    confidence,
    target_state,
    status,
    execution_allowed,
    action,
    reason=None,
):

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "confidence": confidence,
        "target_state": target_state,
        "status": status,
        "execution_allowed": execution_allowed,
        "action": action,
        "reason": reason,
    }

    return event


def main():

    tests = [

        audit_decision(
            "RECOVER",
            0.9,
            "RECOVERY_REQUIRED",
            "BLOCKED",
            False,
            "NO_EXECUTION",
            "confirmation required",
        ),

        audit_decision(
            "RECOVER",
            0.9,
            "RECOVERY_REQUIRED",
            "READY_FOR_ORCHESTRATOR",
            True,
            "ORCHESTRATOR_REQUEST",
        ),

        audit_decision(
            "ESCALATE",
            0.95,
            "ESCALATION_REQUIRED",
            "BLOCKED",
            False,
            "NO_EXECUTION",
            "execution disabled by safety gate",
        ),
    ]


    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-021.5",
        "mode": "AUDIT_ONLY",
        "events": tests,
        "safety": {
            "automatic_recovery": False,
            "execution_enabled": False,
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
