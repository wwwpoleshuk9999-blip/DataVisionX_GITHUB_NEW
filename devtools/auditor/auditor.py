import json
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
            "runtime": self._exists("runtime"),
            "tests": self._exists("tests"),
        }

        return {
            "project": self.root.name,
            "timestamp": datetime.now(UTC).isoformat(),
            "checks": checks,
            "status": "OK" if all(checks.values()) else "WARNING"
        }

    def _exists(self, path):
        return (self.root / path).exists()


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
