#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BACKUP_DIR = BASE / "backups" / "phoenix"


def get_checkpoints():
    return sorted(
        BACKUP_DIR.glob("checkpoint_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def list_checkpoints():
    checkpoints = get_checkpoints()

    if not checkpoints:
        print("No recovery checkpoints found")
        return

    print("=== DataVisionX Recovery Checkpoints ===")

    for index, checkpoint in enumerate(checkpoints, 1):
        data = json.loads(checkpoint.read_text(encoding="utf-8"))

        print()
        print(f"[{index}]")
        print("File:", checkpoint.name)
        print("Created:", data.get("created"))
        print("Commit:", data.get("git", {}).get("commit"))
        print("Status:", data.get("status"))


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
