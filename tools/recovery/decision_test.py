#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "decision_test_report.json"
)


def simulate(health, checkpoint):

    if health == "HEALTHY":
        return {
            "action": "KEEP_RUNNING",
            "reason": "system healthy"
        }

    if checkpoint:
        return {
            "action": "RESTORE_CHECKPOINT",
            "checkpoint": checkpoint,
            "reason": "verified recovery point available"
        }

    return {
        "action": "BLOCK_RECOVERY",
        "reason": "no verified recovery point"
    }


def main():

    tests = [
        {
            "name": "healthy_system",
            "health": "HEALTHY",
            "checkpoint": "checkpoint_latest.json"
        },
        {
            "name": "failure_with_checkpoint",
            "health": "FAILED",
            "checkpoint": "checkpoint_latest.json"
        },
        {
            "name": "failure_without_checkpoint",
            "health": "FAILED",
            "checkpoint": None
        }
    ]

    results = []

    for test in tests:
        results.append({
            "scenario": test["name"],
            "decision": simulate(
                test["health"],
                test["checkpoint"]
            )
        })

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-010.1",
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
