#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "orchestrator_control_report.json"
)


def orchestrate(
    health,
    decision,
    plan,
    confirmation,
    audit,
    gate
):

    if health != "HEALTHY":
        return {
            "status": "BLOCKED",
            "reason": "system health failure"
        }

    if decision == "KEEP_RUNNING":
        return {
            "status": "KEEP_RUNNING",
            "reason": "system healthy"
        }

    if (
        decision == "RESTORE_CHECKPOINT"
        and plan == "PREPARE_RESTORE"
        and confirmation == "APPROVED"
        and audit == "APPROVED"
        and gate == "OPEN"
    ):
        return {
            "status": "READY_TO_RESTORE",
            "reason": "all recovery controls passed"
        }

    return {
        "status": "BLOCKED",
        "reason": "recovery controls failed"
    }


def main():

    tests = [
        {
            "scenario": "healthy_system",
            "result": orchestrate(
                "HEALTHY",
                "KEEP_RUNNING",
                None,
                None,
                None,
                None
            )
        },
        {
            "scenario": "approved_restore",
            "result": orchestrate(
                "HEALTHY",
                "RESTORE_CHECKPOINT",
                "PREPARE_RESTORE",
                "APPROVED",
                "APPROVED",
                "OPEN"
            )
        },
        {
            "scenario": "blocked_restore",
            "result": orchestrate(
                "HEALTHY",
                "RESTORE_CHECKPOINT",
                "PREPARE_RESTORE",
                "BLOCKED",
                "BLOCKED",
                "CLOSED"
            )
        }
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-015.1",
        "tests": tests,
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
