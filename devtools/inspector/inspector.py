import json
from pathlib import Path
from datetime import datetime, UTC


class TechnicalInspector:
    def __init__(self, project_root="."):
        self.root = Path(project_root).resolve()

    def inspect(self, component):
        target = self.root / component

        if not target.exists():
            return {
                "inspector": "DTA-004.1",
                "timestamp": datetime.now(UTC).isoformat(),
                "component": component,
                "exists": False,
                "type": "missing",
                "file_count": 0,
                "python_file_count": 0,
                "has_init": False,
                "test_file_count": 0,
                "status": "MISSING",
            }

        if target.is_file():
            return {
                "inspector": "DTA-004.1",
                "timestamp": datetime.now(UTC).isoformat(),
                "component": component,
                "exists": True,
                "type": "file",
                "file_count": 1,
                "python_file_count": 1
                if target.suffix == ".py"
                else 0,
                "has_init": target.name == "__init__.py",
                "test_file_count": 1
                if "test" in target.name.lower()
                else 0,
                "status": "HEALTHY",
            }

        files = [
            path for path in target.rglob("*")
            if path.is_file()
        ]

        python_files = [
            path for path in files
            if path.suffix == ".py"
        ]

        test_files = [
            path for path in files
            if "test" in path.name.lower()
        ]

        has_init = (target / "__init__.py").exists()

        if not python_files:
            status = "WARNING"
        elif not has_init:
            status = "WARNING"
        else:
            status = "HEALTHY"

        return {
            "inspector": "DTA-004.1",
            "timestamp": datetime.now(UTC).isoformat(),
            "component": component,
            "exists": True,
            "type": "directory",
            "file_count": len(files),
            "python_file_count": len(python_files),
            "has_init": has_init,
            "test_file_count": len(test_files),
            "status": status,
        }


def save_report(data, output):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    inspector = TechnicalInspector()
    report = inspector.inspect("devtools")

    output = Path(
        "runtime/recovery/devtools_inspector_report.json"
    )

    save_report(report, output)
    print(json.dumps(
        report,
        indent=4,
        ensure_ascii=False,
    ))
    print(f"Report: {output}")
