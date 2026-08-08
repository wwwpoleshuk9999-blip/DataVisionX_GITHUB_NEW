import json
from pathlib import Path
from datetime import datetime, UTC

from devtools.auditor.auditor import TechnicalAuditor
from devtools.validator.validator import TechnicalValidator
from devtools.inspector.inspector import TechnicalInspector
from devtools.doctor.doctor import TechnicalDoctor
from devtools.profiler.profiler import TechnicalProfiler


class DevToolsManager:
    def __init__(self, project_root="."):
        self.root = Path(project_root).resolve()

        self.auditor = TechnicalAuditor(self.root)
        self.validator = TechnicalValidator()
        self.inspector = TechnicalInspector(self.root)
        self.doctor = TechnicalDoctor()
        self.profiler = TechnicalProfiler(self.root)

    def run(self, component="devtools"):
        audit_report = self.auditor.scan()

        validation_report = self.validator.validate(audit_report)

        inspection_report = self.inspector.inspect(component)

        diagnosis = self.doctor.diagnose(
            audit_report=audit_report,
            validation_report=validation_report,
            inspection_report=inspection_report,
        )

        profile_report = self.profiler.profile()

        return {
            "manager": "DTA-007.1",
            "timestamp": datetime.now(UTC).isoformat(),
            "project": self.root.name,
            "audit": audit_report,
            "validation": validation_report,
            "inspection": inspection_report,
            "diagnosis": diagnosis,
            "profile": profile_report,
            "safety": {
                "automatic_recovery": False,
                "execution_allowed": False,
                "action": "NO_EXECUTION",
            },
            "status": "READY",
        }


def save_report(data, output="runtime/recovery/devtools_manager_report.json"):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    manager = DevToolsManager()
    report = manager.run("devtools")

    save_report(report)

    print(json.dumps(report, indent=4, ensure_ascii=False))
    print("Report: runtime/recovery/devtools_manager_report.json")
