#!/usr/bin/env python3

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BACKUP_DIR = BASE / "backups" / "phoenix"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_sha_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").split()[0]


def verify_sha(archive: Path, sha_file: Path):
    expected = read_sha_file(sha_file)
    actual = sha256(archive)

    if expected != actual:
        raise RuntimeError(
            f"SHA-256 mismatch: {archive.name}"
        )

    print(f"SHA256 OK: {archive.name}")


def safe_extract(tar_path: Path, destination: Path):
    destination = destination.resolve()

    with tarfile.open(tar_path, "r:gz") as tar:
        for member in tar.getmembers():
            target = (destination / member.name).resolve()

            if not str(target).startswith(str(destination) + "/") \
                    and target != destination:
                raise RuntimeError(
                    f"Unsafe archive path: {member.name}"
                )

        tar.extractall(destination, filter="data")


def find_latest(prefix: str):
    files = sorted(
        BACKUP_DIR.glob(f"{prefix}_*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not files:
        raise RuntimeError(f"Backup not found: {prefix}_*.tar.gz")

    return files[0]


def find_sha(archive: Path):
    sha_file = archive.parent / (archive.name.removesuffix(".tar.gz") + ".sha256")

    if not sha_file.exists():
        raise RuntimeError(
            f"SHA-256 file not found: {sha_file.name}"
        )

    return sha_file


def find_checkpoint():
    files = sorted(
        BACKUP_DIR.glob("checkpoint_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not files:
        raise RuntimeError("Checkpoint not found")

    return files[0]


def verify_checkpoint(
    checkpoint: Path,
    code_archive: Path,
    runtime_archive: Path,
):
    data = json.loads(checkpoint.read_text(encoding="utf-8"))
    backup = data.get("backup", {})

    if backup.get("status") != "VERIFIED":
        raise RuntimeError("Checkpoint is not VERIFIED")

    if backup.get("code_archive") != code_archive.name:
        raise RuntimeError("Checkpoint CODE archive mismatch")

    if backup.get("runtime_archive") != runtime_archive.name:
        raise RuntimeError("Checkpoint RUNTIME archive mismatch")

    if backup.get("code_sha256") != sha256(code_archive):
        raise RuntimeError("Checkpoint CODE SHA mismatch")

    if backup.get("runtime_sha256") != sha256(runtime_archive):
        raise RuntimeError("Checkpoint RUNTIME SHA mismatch")

    print(f"Checkpoint OK: {checkpoint.name}")


def git_commit_exists(commit: str):
    if not commit:
        return False

    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=BASE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def restore(code_archive, runtime_archive, checkpoint, target):
    target = target.resolve()

    if target.exists() and any(target.iterdir()):
        raise RuntimeError(
            f"Target is not empty: {target}"
        )

    target.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        code_dir = tmp / "code"
        runtime_dir = tmp / "runtime"

        code_dir.mkdir()
        runtime_dir.mkdir()

        print("Extracting CODE...")
        safe_extract(code_archive, code_dir)

        print("Extracting RUNTIME...")
        safe_extract(runtime_archive, runtime_dir)

        source_code = code_dir
        source_runtime = runtime_dir / "runtime"

        if not source_runtime.exists():
            raise RuntimeError("RUNTIME archive structure invalid")

        for item in source_code.iterdir():
            shutil.move(str(item), target / item.name)

        shutil.copytree(
            source_runtime,
            target / "runtime",
            dirs_exist_ok=True,
        )

    print(f"RESTORE COMPLETE: {target}")


def main():
    parser = argparse.ArgumentParser(
        description="DataVisionX DTA-004 Recovery Restore"
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Empty directory where the project will be restored",
    )

    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()

    print("=== DataVisionX DTA-004 Recovery Restore ===")
    print(f"Target: {target}")
    print()

    code_archive = find_latest("DataVisionX")
    runtime_archive = find_latest("runtime")
    checkpoint = find_checkpoint()

    print(f"CODE:    {code_archive.name}")
    print(f"RUNTIME: {runtime_archive.name}")
    print(f"CHECKPOINT: {checkpoint.name}")
    print()

    verify_sha(code_archive, find_sha(code_archive))
    verify_sha(runtime_archive, find_sha(runtime_archive))

    verify_checkpoint(
        checkpoint,
        code_archive,
        runtime_archive,
    )

    checkpoint_data = json.loads(
        checkpoint.read_text(encoding="utf-8")
    )

    commit = checkpoint_data.get("git", {}).get("commit")

    if commit:
        print(
            "Git commit in checkpoint:",
            commit
        )

        if git_commit_exists(commit):
            print("Git commit available locally: YES")
        else:
            print("Git commit available locally: NO")
            print(
                "Restore will recover files; "
                "Git history must be obtained from remote."
            )

    print()

    if target.exists() and any(target.iterdir()):
        raise RuntimeError(
            "Refusing restore: target directory is not empty."
        )

    restore(
        code_archive,
        runtime_archive,
        checkpoint,
        target,
    )

    print()
    print("=== DTA-004 STATUS: READY ===")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESTORE FAILED: {exc}")
        sys.exit(1)
