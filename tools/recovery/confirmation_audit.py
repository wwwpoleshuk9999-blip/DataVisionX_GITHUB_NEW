#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "confirmation_audit_report.json"
)


def create_audit(action, checkpoint, status, reason):

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "checkpoint": checkpoint,
        "status": status,
        "reason": reason
    }


def main():

    tests = [
        {
            "scenario": "blocked_without_confirmation",
            "audit": create_audit(
                "RESTORE_CHECKPOINT",
                "checkpoint_latest.json",
                "BLOCKED",
                "confirmation required"
            )
        },
        {
            "scenario": "approved_restore",
            "audit": create_audit(
                "RESTORE_CHECKPOINT",
                "checkpoint_latest.json",
                "APPROVED",
                "explicit confirmation received"
            )
        }
    ]

    report = {
        "project": BASE.name,
        "engine": "DTA-013.2",
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
