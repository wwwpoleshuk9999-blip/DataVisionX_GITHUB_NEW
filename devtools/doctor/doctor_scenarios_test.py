import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from devtools.doctor.doctor import TechnicalDoctor


def run_scenario(name, kwargs, expected):
    result = TechnicalDoctor().diagnose(**kwargs)

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


def valid_audit(status="HEALTHY"):
    return {
        "status": status,
    }


def valid_validation(state="VALID"):
    return {
        "validation_state": state,
    }


def valid_inspection(status="HEALTHY"):
    return {
        "status": status,
    }


def main():
    tests = [
        run_scenario(
            "missing_all_data",
            {},
            {
                "diagnosis": "INCOMPLETE_DATA",
                "severity": "WARNING",
                "findings": [
                    "AUDIT_DATA_MISSING",
                    "VALIDATION_DATA_MISSING",
                    "INSPECTION_DATA_MISSING",
                ],
                "recommendations": [
                    "RUN_AUDITOR",
                    "RUN_VALIDATOR",
                    "RUN_INSPECTOR",
                ],
                "repair_allowed": False,
                "execution_allowed": False,
                "action": "NO_EXECUTION",
            },
        ),
        run_scenario(
            "healthy_project",
            {
                "audit_report": valid_audit(),
                "validation_report": valid_validation(),
                "inspection_report": valid_inspection(),
            },
            {
                "diagnosis": "NO_ACTION_REQUIRED",
                "severity": "HEALTHY",
                "findings": [],
                "recommendations": [],
                "repair_allowed": False,
                "execution_allowed": False,
                "action": "NO_EXECUTION",
            },
        ),
        run_scenario(
            "invalid_validation",
            {
                "audit_report": valid_audit(),
                "validation_report": valid_validation("INVALID"),
                "inspection_report": valid_inspection(),
            },
            {
                "diagnosis": "INVALID_AUDIT_DATA",
                "severity": "CRITICAL",
                "findings": [
                    "VALIDATOR_REJECTED_REPORT",
                ],
                "recommendations": [
                    "REVIEW_AUDIT_REPORT",
                ],
                "repair_allowed": False,
                "execution_allowed": False,
                "action": "NO_EXECUTION",
            },
        ),
        run_scenario(
            "critical_audit",
            {
                "audit_report": valid_audit("CRITICAL"),
                "validation_report": valid_validation(),
                "inspection_report": valid_inspection(),
            },
            {
                "diagnosis": "CRITICAL_PROJECT_STATE",
                "severity": "CRITICAL",
                "findings": [
                    "AUDITOR_CRITICAL",
                ],
                "recommendations": [
                    "REVIEW_MISSING_COMPONENTS",
                ],
                "repair_allowed": False,
                "execution_allowed": False,
                "action": "NO_EXECUTION",
            },
        ),
        run_scenario(
            "inspection_warning",
            {
                "audit_report": valid_audit(),
                "validation_report": valid_validation(),
                "inspection_report": valid_inspection("WARNING"),
            },
            {
                "diagnosis": "INSPECTION_FINDINGS",
                "severity": "WARNING",
                "findings": [
                    "INSPECTOR_WARNING",
                ],
                "recommendations": [
                    "REVIEW_COMPONENT_STRUCTURE",
                ],
                "repair_allowed": False,
                "execution_allowed": False,
                "action": "NO_EXECUTION",
            },
        ),
        run_scenario(
            "validation_warning",
            {
                "audit_report": valid_audit(),
                "validation_report": valid_validation(
                    "VALID_WITH_WARNINGS"
                ),
                "inspection_report": valid_inspection(),
            },
            {
                "diagnosis": "VALID_WITH_WARNINGS",
                "severity": "WARNING",
                "findings": [
                    "VALIDATOR_WARNINGS",
                ],
                "recommendations": [
                    "REVIEW_VALIDATION_WARNINGS",
                ],
                "repair_allowed": False,
                "execution_allowed": False,
                "action": "NO_EXECUTION",
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
        "engine": "DTA-005.2",
        "mode": "SCENARIO_TEST",
        "tests": tests,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "devtools_doctor_scenarios_report.json"
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
