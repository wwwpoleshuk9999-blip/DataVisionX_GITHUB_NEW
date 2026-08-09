#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP_DIR="$BASE/backups/phoenix"
DATE="$(date +"%Y%m%d_%H%M%S")"

CODE_ARCHIVE="$BACKUP_DIR/DataVisionX_${DATE}.tar.gz"
RUNTIME_ARCHIVE="$BACKUP_DIR/runtime_${DATE}.tar.gz"
CODE_SHA="$BACKUP_DIR/DataVisionX_${DATE}.sha256"
RUNTIME_SHA="$BACKUP_DIR/runtime_${DATE}.sha256"

cd "$BASE"

echo "=== DataVisionX Phoenix Backup v2 ==="
echo "Project: $BASE"
echo "Timestamp: $DATE"
echo

echo "[1/5] Git state"
git status --short
BRANCH="$(git branch --show-current)"
COMMIT="$(git rev-parse HEAD)"
echo "Branch: $BRANCH"
echo "Commit: $COMMIT"
echo

mkdir -p "$BACKUP_DIR"

echo "[2/5] Creating CODE archive"
tar \
    --exclude=".venv" \
    --exclude=".git" \
    --exclude="runtime" \
    --exclude="backups" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    -czf "$CODE_ARCHIVE" .

echo "[3/5] Creating RUNTIME archive"
tar \
    --exclude="runtime/plugin_storage" \
    -czf "$RUNTIME_ARCHIVE" runtime

echo "[4/5] Creating SHA-256 checksums"
sha256sum "$CODE_ARCHIVE" | tee "$CODE_SHA"
sha256sum "$RUNTIME_ARCHIVE" | tee "$RUNTIME_SHA"

echo "[5/5] Creating checkpoint"
CHECKPOINT_OUTPUT="$(python tools/recovery/checkpoint.py)"
printf "%s\n" "$CHECKPOINT_OUTPUT"
CHECKPOINT="$(printf "%s\n" "$CHECKPOINT_OUTPUT" | sed -n "s/^saved: //p")"
if [ -z "$CHECKPOINT" ] || [ ! -f "$CHECKPOINT" ]; then
    echo "ERROR: checkpoint.py did not return a valid checkpoint path" >&2
    exit 1
fi

python - "$CHECKPOINT" "$CODE_ARCHIVE" "$RUNTIME_ARCHIVE" "$CODE_SHA" "$RUNTIME_SHA" <<'PY'
import json
import hashlib
import os
import sys

checkpoint_path, code_archive, runtime_archive, code_sha, runtime_sha = sys.argv[1:]

def read_sha(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().split()[0]

with open(checkpoint_path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["backup"] = {
    "code_archive": os.path.basename(code_archive),
    "runtime_archive": os.path.basename(runtime_archive),
    "code_sha256": read_sha(code_sha),
    "runtime_sha256": read_sha(runtime_sha),
    "status": "VERIFIED"
}

with open(checkpoint_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("checkpoint updated:", checkpoint_path)
PY

echo
echo "=== BACKUP COMPLETE ==="
echo "Code:    $CODE_ARCHIVE"
echo "Runtime: $RUNTIME_ARCHIVE"
echo "SHA256:  $CODE_SHA"
echo "SHA256:  $RUNTIME_SHA"
echo "Checkpoint: $CHECKPOINT"
echo
echo "=== FILES ==="
ls -lh "$CODE_ARCHIVE" "$RUNTIME_ARCHIVE" "$CODE_SHA" "$RUNTIME_SHA" "$CHECKPOINT"
