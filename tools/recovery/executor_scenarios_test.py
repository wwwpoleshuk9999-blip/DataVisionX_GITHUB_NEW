#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "executor_scenarios_report.json"
)


def execute(plan):

    mode = plan.get("mode")

    if mode == "NO_ACTION":
        return {
            "action": "SKIPPED",
            "reason": "system healthy"
        }

    if mode == "PREPARE_RESTORE":
        return {
            "action": "READY",
            "operation": plan.get("command"),
            "confirmation_required": True,
            "execution": "DRY_RUN"
        }

    return {
        "action": "BLOCKED",
        "reason": "unsafe or unavailable recovery plan"
    }


def main():

    scenarios = [
        {
            "name": "healthy_system",
            "plan": {
                "mode": "NO_ACTION"
            }
        },
        {
            "name": "verified_checkpoint",
            "plan": {
                "mode": "PREPARE_RESTORE",
                "command": "restore checkpoint checkpoint_latest.json"
            }
        },
        {
            "name": "missing_checkpoint",
            "plan": {
                "mode": "BLOCK"
            }
        }
    ]

    results = []

    for scenario in scenarios:
        results.append({
            "scenario": scenario["name"],
            "result": execute(
                scenario["plan"]
            )
        })

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-012.2",
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
