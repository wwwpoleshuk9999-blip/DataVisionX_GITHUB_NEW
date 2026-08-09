#!/usr/bin/env python3

import json
import os
import tarfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
BACKUP_DIR = BASE / "backups" / "phoenix"
POLICY_FILE = BASE / "runtime" / "recovery" / "policy_report.json"


def load_policy_archive():
    if not POLICY_FILE.is_file():
        raise RuntimeError(f"Policy report not found: {POLICY_FILE}")

    policy = json.loads(POLICY_FILE.read_text(encoding="utf-8"))
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
    backup = data.get("backup") or {}

    if backup.get("status") != "VERIFIED":
        raise RuntimeError("Checkpoint backup is not VERIFIED")

    archive_name = backup.get("code_archive")
    if not archive_name:
        raise RuntimeError("Checkpoint does not contain backup.code_archive")

    archive = BACKUP_DIR / archive_name

    if not archive.is_file():
        raise RuntimeError(
            f"Policy-bound code archive not found: {archive}"
        )

    return checkpoint_name, archive_name, archive


checkpoint_name, archive_name, archive = load_policy_archive()

print("Policy checkpoint:")
print(checkpoint_name)
print("Checking code archive:")
print(archive_name)

try:
    with tarfile.open(archive, "r:gz") as tar:
        members = tar.getmembers()
        print("Files inside:", len(members))

        if len(members) == 0:
            print("STATUS: FAILED (empty archive)")
            raise SystemExit(1)

        print("STATUS: OK")
except Exception as e:
    print("STATUS: FAILED")
    print(e)
    raise SystemExit(1)
