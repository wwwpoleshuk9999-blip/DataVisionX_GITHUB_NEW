#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BACKUP_DIR = BASE / "backups" / "phoenix"


def load_policy():
    policy_file = BASE / "runtime" / "recovery" / "policy_report.json"

    if not policy_file.is_file():
        raise RuntimeError(f"Policy report not found: {policy_file}")

    return json.loads(policy_file.read_text(encoding="utf-8"))


def get_policy_selected_checkpoint():
    policy = load_policy()
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

    return checkpoint, data


def list_checkpoints():
    try:
        checkpoint, data = get_policy_selected_checkpoint()
    except RuntimeError as exc:
        print(f"Policy error: {exc}")
        return 1

    print("=== DataVisionX Recovery Checkpoints ===")
    print()
    print("[POLICY SELECTED]")
    print("File:", checkpoint.name)
    print("Created:", data.get("created"))
    print("Commit:", data.get("git", {}).get("commit"))
    print("Status:", data.get("status"))
    print("Backup:", data.get("backup", {}).get("status"))
    return 0



def restore_policy_selected(target):
    policy_file = BASE / "runtime" / "recovery" / "policy_report.json"

    if not policy_file.is_file():
        print("Policy report not found:", policy_file)
        return 1

    policy = json.loads(policy_file.read_text(encoding="utf-8"))
    selected = policy.get("selected") or {}

    checkpoint_name = selected.get("file")

    if not checkpoint_name:
        print("Policy does not contain selected.file")
        return 1

    if selected.get("status") != "READY":
        print("Policy-selected checkpoint is not READY")
        return 1

    if selected.get("backup") != "VERIFIED":
        print("Policy-selected checkpoint is not VERIFIED")
        return 1

    checkpoint = BACKUP_DIR / checkpoint_name

    if not checkpoint.is_file():
        print("Policy-selected checkpoint not found:", checkpoint)
        return 1

    data = json.loads(checkpoint.read_text(encoding="utf-8"))

    backup = data.get("backup", {})

    if backup.get("status") != "VERIFIED":
        print("Checkpoint is not VERIFIED")
        return 1

    print("Policy-selected checkpoint:", checkpoint.name)

    print("=== DataVisionX DTA-005 Restore ===")
    print("Checkpoint:", checkpoint.name)
    print("Target:", target)

    cmd = [
        sys.executable,
        str(BASE / "tools" / "recovery" / "restore_v2.py"),
        "--target",
        str(target),
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("RESTORE FAILED")
        return result.returncode

    print("=== DTA-005 RESTORE STATUS: READY ===")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="DataVisionX Recovery CLI"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list")

    restore = sub.add_parser("restore")
    restore.add_argument(
        "checkpoint",
        choices=["latest"],
    )
    restore.add_argument(
        "--target",
        required=True,
    )

    args = parser.parse_args()

    if args.command == "list":
        list_checkpoints()

    elif args.command == "restore":
        sys.exit(
            restore_policy_selected(Path(args.target))
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
