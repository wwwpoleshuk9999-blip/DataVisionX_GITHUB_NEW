#!/data/data/com.termux/files/usr/bin/bash

set -e

PROJECT="$(pwd)"
DATE=$(date +"%Y%m%d_%H%M%S")

echo "=== DataVisionX Phoenix Backup ==="

echo "[1/3] Creating checkpoint..."
python tools/recovery/checkpoint.py

echo "[2/3] Creating archive..."

mkdir -p backups/phoenix

tar \
--exclude=".venv" \
--exclude=".git" \
--exclude="runtime" \
-czf \
backups/phoenix/DataVisionX_${DATE}.tar.gz .

echo "[3/3] Git state"

git status

echo
echo "Backup complete:"
echo "backups/phoenix/DataVisionX_${DATE}.tar.gz"
