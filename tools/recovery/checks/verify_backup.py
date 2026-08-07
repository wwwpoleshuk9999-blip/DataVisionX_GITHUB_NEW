import os
import tarfile
import glob

BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

BACKUP_DIR = os.path.join(BASE, "backups", "phoenix")

archives = sorted(
    glob.glob(os.path.join(BACKUP_DIR, "DataVisionX_*.tar.gz"))
)

if not archives:
    print("No backup archives found")
    exit(1)

latest = archives[-1]

print("Checking:")
print(latest)

try:
    with tarfile.open(latest, "r:gz") as tar:
        members = tar.getmembers()

    print("Files inside:", len(members))

    if len(members) == 0:
        print("STATUS: FAILED (empty archive)")
    else:
        print("STATUS: OK")

except Exception as e:
    print("STATUS: FAILED")
    print(e)
