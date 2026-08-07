#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "automation_scenarios_report.json"
)


def create_plan(action, checkpoint=None):

    if action == "KEEP_RUNNING":
        return {
            "mode": "NO_ACTION",
            "command": None,
            "reason": "system healthy"
        }

    if action == "RESTORE_CHECKPOINT":
        return {
            "mode": "PREPARE_RESTORE",
            "command": f"restore checkpoint {checkpoint}",
            "requires_confirmation": True
        }

    return {
        "mode": "BLOCK",
        "command": None,
        "reason": "no verified recovery point"
    }


def main():

    scenarios = [
        {
            "name": "failure_with_verified_checkpoint",
            "action": "RESTORE_CHECKPOINT",
            "checkpoint": "checkpoint_latest.json"
        },
        {
            "name": "failure_without_checkpoint",
            "action": "BLOCK_RECOVERY",
            "checkpoint": None
        }
    ]

    results = []

    for item in scenarios:
        results.append({
            "scenario": item["name"],
            "plan": create_plan(
                item["action"],
                item["checkpoint"]
            )
        })

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-011.2",
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
