#!/usr/bin/env python3

import json
import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
POLICY_FILE = os.path.join(
    BASE,
    "runtime",
    "recovery",
    "policy_report.json",
)
BACKUP_DIR = os.path.join(BASE, "backups", "phoenix")


def load_policy_checkpoint():
    if not os.path.exists(POLICY_FILE):
        raise RuntimeError("Recovery policy report not found")

    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        policy = json.load(f)

    selected = policy.get("selected") or {}
    checkpoint_name = selected.get("file")

    if not checkpoint_name:
        raise RuntimeError("Policy does not contain selected.file")

    if selected.get("status") != "READY":
        raise RuntimeError("Policy-selected checkpoint is not READY")

    if selected.get("backup") != "VERIFIED":
        raise RuntimeError("Policy-selected checkpoint is not VERIFIED")

    checkpoint_path = os.path.join(BACKUP_DIR, checkpoint_name)

    if not os.path.isfile(checkpoint_path):
        raise RuntimeError(
            f"Policy-selected checkpoint not found: {checkpoint_path}"
        )

    with open(checkpoint_path, "r", encoding="utf-8") as f:
        checkpoint = json.load(f)

    backup = checkpoint.get("backup") or {}

    if backup.get("status") != "VERIFIED":
        raise RuntimeError("Checkpoint backup is not VERIFIED")

    return checkpoint_name, checkpoint


try:
    checkpoint_name, checkpoint = load_policy_checkpoint()

    print("=== DataVisionX Recovery Point ===")
    print()
    print("POLICY SELECTED:")
    print("File:", checkpoint_name)
    print("Created:", checkpoint.get("created"))
    print("Branch:", checkpoint.get("git", {}).get("branch"))
    print("Commit:", checkpoint.get("git", {}).get("commit"))
    print("Status:", checkpoint.get("status"))
    print("Backup:", checkpoint.get("backup", {}).get("status"))

except RuntimeError as exc:
    print(f"Recovery policy error: {exc}")
    raise SystemExit(1)
