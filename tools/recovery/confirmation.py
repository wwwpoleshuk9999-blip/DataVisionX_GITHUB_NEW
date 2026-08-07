#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "confirmation_report.json"
)


def check_confirmation(plan, confirmed=False):

    if plan.get("mode") != "PREPARE_RESTORE":
        return {
            "status": "SKIPPED",
            "reason": "no restore requested"
        }

    if confirmed:
        return {
            "status": "APPROVED",
            "reason": "explicit confirmation received"
        }

    return {
        "status": "BLOCKED",
        "reason": "confirmation required"
    }


def main():

    tests = [
        {
            "scenario": "restore_without_confirmation",
            "confirmed": False
        },
        {
            "scenario": "restore_with_confirmation",
            "confirmed": True
        }
    ]

    plan = {
        "mode": "PREPARE_RESTORE",
        "command": "restore checkpoint checkpoint_latest.json"
    }

    results = []

    for test in tests:
        results.append({
            "scenario": test["scenario"],
            "result": check_confirmation(
                plan,
                test["confirmed"]
            )
        })

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-013.1",
        "tests": results,
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
