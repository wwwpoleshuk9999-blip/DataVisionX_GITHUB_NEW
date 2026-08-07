import json
import subprocess
from pathlib import Path
from datetime import datetime, UTC


class TechnicalAuditor:
    def __init__(self, project_root="."):
        self.root = Path(project_root).resolve()

    def scan(self):
        checks = {
            "core": self._exists("core"),
            "api": self._exists("api"),
            "services": self._exists("services"),
            "web": self._exists("web"),
            "plugins": self._exists("plugins"),
            "devtools": self._exists("devtools"),
            "recovery": self._exists("tools/recovery"),
        }

        runtime = self._exists("runtime")
        tests = self._exists("tests")

        git = self._git_info()

        critical_missing = [
            name for name, value in checks.items()
            if not value
        ]

        if critical_missing:
            status = "CRITICAL"
        elif not runtime or not tests:
            status = "WARNING"
        else:
            status = "HEALTHY"

        return {
            "project": self.root.name,
            "timestamp": datetime.now(UTC).isoformat(),
            "checks": checks,
            "runtime": {
                "present": runtime,
                "classification": "runtime-layer"
            },
            "tests": {
                "present": tests,
                "classification": "optional"
            },
            "git": git,
            "missing_critical": critical_missing,
            "status": status
        }

    def _exists(self, path):
        return (self.root / path).exists()

    def _git_info(self):
        def run(command):
            try:
                return subprocess.check_output(
                    command,
                    cwd=self.root,
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                return None

        return {
            "branch": run(["git", "branch", "--show-current"]),
            "commit": run(["git", "rev-parse", "HEAD"]),
            "status": "CLEAN"
            if run(["git", "status", "--porcelain"]) == ""
            else "DIRTY"
        }


def save_report(data, output="audit_report.json"):
    path = Path(output)
    path.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )


if __name__ == "__main__":
    auditor = TechnicalAuditor()
    report = auditor.scan()
    save_report(report)
    print(json.dumps(report, indent=4))
