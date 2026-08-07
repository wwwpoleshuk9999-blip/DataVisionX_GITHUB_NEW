#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

DECISION_REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "decision_report.json"
)

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "automation_plan_report.json"
)


def load_json(path):
    if not path.exists():
        return {}

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def create_plan(decision):

    action = decision.get("action")

    if action == "KEEP_RUNNING":
        return {
            "mode": "NO_ACTION",
            "command": None,
            "reason": "system healthy"
        }

    if action == "RESTORE_CHECKPOINT":
        return {
            "mode": "PREPARE_RESTORE",
            "command": (
                f"restore checkpoint "
                f"{decision.get('checkpoint')}"
            ),
            "reason": "verified checkpoint available",
            "requires_confirmation": True
        }

    return {
        "mode": "BLOCK",
        "command": None,
        "reason": "recovery unavailable"
    }


def main():

    data = load_json(DECISION_REPORT)

    plan = create_plan(
        data.get("decision", {})
    )

    result = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-011.1",
        "plan": plan,
        "status": "READY"
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT.write_text(
        json.dumps(result, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(result, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
