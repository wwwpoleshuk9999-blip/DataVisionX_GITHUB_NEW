#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]

HEALTH_REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "recovery_health_report.json"
)

POLICY_REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "policy_score_report.json"
)

REPORT = (
    BASE /
    "runtime" /
    "recovery" /
    "decision_report.json"
)


def load_json(path):
    if not path.exists():
        return {}

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def decide():

    health = load_json(HEALTH_REPORT)
    policy = load_json(POLICY_REPORT)

    health_status = health.get("status")

    selected = policy.get("selected")

    if health_status == "HEALTHY":
        return {
            "action": "KEEP_RUNNING",
            "reason": "system healthy"
        }

    if selected:
        return {
            "action": "RESTORE_CHECKPOINT",
            "reason": "healthy checkpoint available",
            "checkpoint": selected.get("file"),
            "score": selected.get("score")
        }

    return {
        "action": "BLOCK_RECOVERY",
        "reason": "no verified recovery point"
    }


def main():

    decision = decide()

    result = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-010",
        "decision": decision,
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
