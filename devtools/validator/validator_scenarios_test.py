import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from devtools.validator.validator import TechnicalValidator


def make_report(**overrides):
    report = {
        "project": "DataVisionX",
        "timestamp": "2026-08-08T00:00:00+00:00",
        "checks": {
            "core": True,
            "api": True,
            "services": True,
            "web": True,
            "plugins": True,
            "devtools": True,
            "recovery": True,
        },
        "runtime": {
            "present": True,
            "classification": "runtime-layer",
        },
        "tests": {
            "present": True,
            "classification": "optional",
        },
        "git": {
            "branch": "phoenix-build-012-dev",
            "commit": "abc123",
            "status": "CLEAN",
        },
        "missing_critical": [],
        "status": "HEALTHY",
    }
    report.update(overrides)
    return report


def run_scenario(name, report, expected_state, expected_valid):
    result = TechnicalValidator().validate(report)

    passed = (
        result["validation_state"] == expected_state
        and result["valid"] == expected_valid
    )

    return {
        "scenario": name,
        "result": result,
        "expected": {
            "validation_state": expected_state,
            "valid": expected_valid,
        },
        "passed": passed,
    }


def main():
    tests = [
        run_scenario(
            "healthy_report",
            make_report(),
            "VALID",
            True,
        ),
        run_scenario(
            "warning_runtime_missing",
            make_report(
                runtime={
                    "present": False,
                    "classification": "runtime-layer",
                },
                status="WARNING",
            ),
            "VALID_WITH_WARNINGS",
            True,
        ),
        run_scenario(
            "dirty_git",
            make_report(
                git={
                    "branch": "phoenix-build-012-dev",
                    "commit": "abc123",
                    "status": "DIRTY",
                },
            ),
            "VALID_WITH_WARNINGS",
            True,
        ),
        run_scenario(
            "missing_critical",
            make_report(
                checks={
                    "core": False,
                    "api": True,
                    "services": True,
                    "web": True,
                    "plugins": True,
                    "devtools": True,
                    "recovery": True,
                },
                missing_critical=["core"],
                status="CRITICAL",
            ),
            "VALID",
            True,
        ),
        run_scenario(
            "missing_required_field",
            {
                key: value
                for key, value in make_report().items()
                if key != "checks"
            },
            "INVALID",
            False,
        ),
        run_scenario(
            "invalid_status",
            make_report(status="BROKEN"),
            "INVALID",
            False,
        ),
        run_scenario(
            "inconsistent_missing_critical",
            make_report(
                checks={
                    "core": False,
                    "api": True,
                    "services": True,
                    "web": True,
                    "plugins": True,
                    "devtools": True,
                    "recovery": True,
                },
                missing_critical=[],
                status="CRITICAL",
            ),
            "INVALID",
            False,
        ),
        run_scenario(
            "non_object_report",
            None,
            "INVALID",
            False,
        ),
    ]

    status = "READY" if all(
        item["passed"] for item in tests
    ) else "FAILED"

    report = {
        "project": BASE.name,
        "engine": "DTA-003.2",
        "mode": "SCENARIO_TEST",
        "tests": tests,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "devtools_validator_scenarios_report.json"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
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
