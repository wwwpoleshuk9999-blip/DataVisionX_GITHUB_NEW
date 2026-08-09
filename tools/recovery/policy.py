#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
BACKUP_DIR = BASE / "backups" / "phoenix"
REPORT = BASE / "runtime" / "recovery" / "policy_report.json"


def load_policy_selected_checkpoint():
    if not REPORT.is_file():
        raise RuntimeError(f"Policy report not found: {REPORT}")

    policy = json.loads(REPORT.read_text(encoding="utf-8"))
    selected = policy.get("selected") or {}

    checkpoint_name = selected.get("file")
    if not checkpoint_name:
        raise RuntimeError("Policy does not contain selected.file")

    if selected.get("status") != "READY":
        raise RuntimeError("Policy-selected checkpoint is not READY")

    if selected.get("backup") != "VERIFIED":
        raise RuntimeError("Policy-selected checkpoint is not VERIFIED")

    checkpoint = BACKUP_DIR / checkpoint_name

    if not checkpoint.is_file():
        raise RuntimeError(
            f"Policy-selected checkpoint not found: {checkpoint}"
        )

    data = json.loads(checkpoint.read_text(encoding="utf-8"))

    if data.get("status") != "READY":
        raise RuntimeError("Checkpoint is not READY")

    backup = data.get("backup") or {}

    if backup.get("status") != "VERIFIED":
        raise RuntimeError("Checkpoint backup is not VERIFIED")

    return {
        "file": checkpoint.name,
        "created": data.get("created"),
        "commit": data.get("git", {}).get("commit"),
        "status": data.get("status"),
        "backup": backup.get("status"),
    }


def main():
    selected = load_policy_selected_checkpoint()

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "policy": "policy_bound_verified_checkpoint",
        "available": 1,
        "selected": selected,
        "status": "READY",
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
