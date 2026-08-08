import json
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from devtools.inspector.inspector import TechnicalInspector


def run_scenario(name, inspector, component, expected):
    result = inspector.inspect(component)

    passed = all(
        result.get(key) == value
        for key, value in expected.items()
    )

    return {
        "scenario": name,
        "result": result,
        "expected": expected,
        "passed": passed,
    }


def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        # Healthy directory with Python module, init and test.
        healthy = root / "healthy"
        healthy.mkdir()
        (healthy / "__init__.py").write_text(
            "",
            encoding="utf-8",
        )
        (healthy / "module.py").write_text(
            "VALUE = 1\n",
            encoding="utf-8",
        )
        (healthy / "test_module.py").write_text(
            "def test_ok():\n    assert True\n",
            encoding="utf-8",
        )

        # Warning directory: files exist but no Python package init.
        warning = root / "warning"
        warning.mkdir()
        (warning / "readme.txt").write_text(
            "warning\n",
            encoding="utf-8",
        )

        # Python file component.
        python_file = root / "single.py"
        python_file.write_text(
            "VALUE = 1\n",
            encoding="utf-8",
        )

        inspector = TechnicalInspector(root)

        tests = [
            run_scenario(
                "missing_component",
                inspector,
                "missing",
                {
                    "exists": False,
                    "type": "missing",
                    "file_count": 0,
                    "python_file_count": 0,
                    "has_init": False,
                    "test_file_count": 0,
                    "status": "MISSING",
                },
            ),
            run_scenario(
                "healthy_directory",
                inspector,
                "healthy",
                {
                    "exists": True,
                    "type": "directory",
                    "file_count": 3,
                    "python_file_count": 3,
                    "has_init": True,
                    "test_file_count": 1,
                    "status": "HEALTHY",
                },
            ),
            run_scenario(
                "warning_directory",
                inspector,
                "warning",
                {
                    "exists": True,
                    "type": "directory",
                    "file_count": 1,
                    "python_file_count": 0,
                    "has_init": False,
                    "test_file_count": 0,
                    "status": "WARNING",
                },
            ),
            run_scenario(
                "python_file",
                inspector,
                "single.py",
                {
                    "exists": True,
                    "type": "file",
                    "file_count": 1,
                    "python_file_count": 1,
                    "has_init": False,
                    "test_file_count": 0,
                    "status": "HEALTHY",
                },
            ),
        ]

        status = (
            "READY"
            if all(item["passed"] for item in tests)
            else "FAILED"
        )

        report = {
            "project": BASE.name,
            "engine": "DTA-004.2",
            "mode": "SCENARIO_TEST",
            "tests": tests,
            "status": status,
        }

        report_path = (
            BASE
            / "runtime"
            / "recovery"
            / "devtools_inspector_scenarios_report.json"
        )

        report_path.write_text(
            json.dumps(
                report,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        print(json.dumps(
            report,
            indent=4,
            ensure_ascii=False,
        ))
        print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
