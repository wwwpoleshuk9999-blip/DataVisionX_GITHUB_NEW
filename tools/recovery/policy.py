#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
BACKUP_DIR = BASE / "backups" / "phoenix"
REPORT = BASE / "runtime" / "recovery" / "policy_report.json"


def load_checkpoints():
    files = sorted(
        BACKUP_DIR.glob("checkpoint_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    result = []

    for file in files:
        data = json.loads(
            file.read_text(encoding="utf-8")
        )

        result.append({
            "file": file.name,
            "created": data.get("created"),
            "commit": data.get("git", {}).get("commit"),
            "status": data.get("status"),
            "backup": data.get("backup", {}).get("status")
        })

    return result


def choose_checkpoint(checkpoints):
    valid = [
        c for c in checkpoints
        if c["status"] == "READY"
        and c["backup"] == "VERIFIED"
    ]

    if not valid:
        return None

    return valid[0]


def main():
    checkpoints = load_checkpoints()
    selected = choose_checkpoint(checkpoints)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "policy": "latest_verified_checkpoint",
        "available": len(checkpoints),
        "selected": selected,
        "status": "READY" if selected else "FAILED"
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
