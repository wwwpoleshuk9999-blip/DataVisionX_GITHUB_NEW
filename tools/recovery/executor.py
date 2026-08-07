#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

PLAN_FILE = (
    BASE /
    "runtime" /
    "recovery" /
    "automation_plan_report.json"
)

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "executor_report.json"
)


def load_plan():
    if not PLAN_FILE.exists():
        return {}

    return json.loads(
        PLAN_FILE.read_text(encoding="utf-8")
    )


def execute_dry_run(plan):

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

    data = load_plan()

    result = execute_dry_run(
        data.get("plan", {})
    )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-012.1",
        "mode": "DRY_RUN",
        "result": result,
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
