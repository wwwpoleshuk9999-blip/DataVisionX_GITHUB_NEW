#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BACKUP_DIR = BASE / "backups" / "phoenix"


def list_checkpoints():
    checkpoints = sorted(
        BACKUP_DIR.glob("checkpoint_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

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


def main():
    parser = argparse.ArgumentParser(
        description="DataVisionX Recovery CLI"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list")

    args = parser.parse_args()

    if args.command == "list":
        list_checkpoints()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
