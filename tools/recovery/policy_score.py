#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
BACKUP_DIR = BASE / "backups" / "phoenix"
REPORT = BASE / "runtime" / "recovery" / "policy_score_report.json"


def git_exists(commit):
    if not commit:
        return False

    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=BASE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


def score_checkpoint(file):
    data = json.loads(
        file.read_text(encoding="utf-8")
    )

    score = 0
    reasons = []

    backup = data.get("backup", {})

    if backup.get("status") == "VERIFIED":
        score += 40
        reasons.append("backup_verified")

    runtime = BASE / "runtime"

    if runtime.exists():
        score += 20
        reasons.append("runtime_present")

    commit = data.get("git", {}).get("commit")

    if git_exists(commit):
        score += 10
        reasons.append("git_commit_available")

    auditor = BASE / "audit_report.json"

    if auditor.exists():
        try:
            audit = json.loads(
                auditor.read_text(encoding="utf-8")
            )

            if audit.get("status") == "HEALTHY":
                score += 30
                reasons.append("auditor_healthy")

        except Exception:
            pass

    return {
        "file": file.name,
        "score": score,
        "reasons": reasons,
        "commit": commit
    }


def main():

    checkpoints = sorted(
        BACKUP_DIR.glob("checkpoint_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    results = [
        score_checkpoint(c)
        for c in checkpoints
    ]

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    selected = results[0] if results else None

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "policy": "highest_score",
        "checkpoints": results,
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
