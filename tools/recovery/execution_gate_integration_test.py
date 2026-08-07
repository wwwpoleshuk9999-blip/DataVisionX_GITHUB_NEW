#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "execution_gate_integration_report.json"
)


def execution_gate(decision, plan, confirmation, audit):

    if (
        decision == "RESTORE_CHECKPOINT"
        and plan == "PREPARE_RESTORE"
        and confirmation == "APPROVED"
        and audit == "APPROVED"
    ):
        return {
            "gate": "OPEN",
            "action": "ALLOW_EXECUTION"
        }

    return {
        "gate": "CLOSED",
        "action": "BLOCK_EXECUTION"
    }


def main():

    scenarios = [
        {
            "scenario": "full_approved_recovery",
            "result": execution_gate(
                "RESTORE_CHECKPOINT",
                "PREPARE_RESTORE",
                "APPROVED",
                "APPROVED"
            )
        },
        {
            "scenario": "blocked_confirmation",
            "result": execution_gate(
                "RESTORE_CHECKPOINT",
                "PREPARE_RESTORE",
                "BLOCKED",
                "BLOCKED"
            )
        }
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-014.2",
        "tests": scenarios,
        "status": "READY"
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
