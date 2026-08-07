import json
import subprocess
from pathlib import Path
from datetime import datetime, UTC


class RecoveryManager:
    def __init__(self, root="."):
        self.root = Path(root).resolve()

    def git_command(self, args):
        try:
            result = subprocess.check_output(
                ["git"] + args,
                cwd=self.root,
                text=True
            )
            return result.strip()
        except Exception:
            return "unknown"

    def create_manifest(self, output="backups/phoenix/manifest.json"):
        manifest = {
            "project": self.root.name,
            "created": datetime.now(UTC).isoformat(),
            "git": {
                "branch": self.git_command(["branch", "--show-current"]),
                "commit": self.git_command(["rev-parse", "HEAD"]),
                "tag": self.git_command(["describe", "--tags", "--always"])
            },
            "recovery": {
                "status": "READY",
                "type": "checkpoint"
            }
        }

        path = self.root / output
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(manifest, indent=4),
            encoding="utf-8"
        )

        return manifest


if __name__ == "__main__":
    manager = RecoveryManager()
    result = manager.create_manifest()

    print(json.dumps(result, indent=4))
