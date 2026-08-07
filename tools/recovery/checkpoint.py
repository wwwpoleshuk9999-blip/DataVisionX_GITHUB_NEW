import os
import json
import subprocess
from datetime import datetime, timezone

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

BACKUP_DIR = os.path.join(BASE, "backups", "phoenix")
RECOVERY_DIR = os.path.join(BASE, "runtime", "recovery")
HISTORY_FILE = os.path.join(RECOVERY_DIR, "history.json")

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(RECOVERY_DIR, exist_ok=True)


def git(cmd):
    return subprocess.check_output(
        ["git"] + cmd,
        cwd=BASE
    ).decode().strip()


checkpoint = {
    "project": os.path.basename(BASE),
    "created": datetime.now(timezone.utc).isoformat(),
    "git": {
        "branch": git(["branch", "--show-current"]),
        "commit": git(["rev-parse", "HEAD"]),
        "tag": git(["describe", "--tags", "--always"])
    },
    "status": "READY"
}


filename = "checkpoint_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"

checkpoint_path = os.path.join(BACKUP_DIR, filename)

with open(checkpoint_path, "w") as f:
    json.dump(checkpoint, f, indent=4)


if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = []


history.append({
    "file": filename,
    "created": checkpoint["created"],
    "branch": checkpoint["git"]["branch"],
    "commit": checkpoint["git"]["commit"],
    "status": checkpoint["status"]
})


with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=4)


print(json.dumps(checkpoint, indent=4))
print("saved:", checkpoint_path)
print("history:", HISTORY_FILE)
