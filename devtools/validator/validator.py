import json
from pathlib import Path
from datetime import datetime, UTC


REQUIRED_TOP_LEVEL = {
    "project",
    "timestamp",
    "checks",
    "runtime",
    "tests",
    "git",
    "missing_critical",
    "status",
}

REQUIRED_CHECKS = {
    "core",
    "api",
    "services",
    "web",
    "plugins",
    "devtools",
    "recovery",
}


class TechnicalValidator:
    def validate(self, report):
        errors = []
        warnings = []

        if not isinstance(report, dict):
            return self._result(
                "INVALID",
                errors=["report must be an object"],
                warnings=[],
            )

        missing_fields = sorted(
            REQUIRED_TOP_LEVEL - set(report.keys())
        )

        if missing_fields:
            errors.append(
                f"missing_top_level_fields:{','.join(missing_fields)}"
            )

        checks = report.get("checks")
        if not isinstance(checks, dict):
            errors.append("checks must be an object")
        else:
            missing_checks = sorted(
                REQUIRED_CHECKS - set(checks.keys())
            )
            if missing_checks:
                errors.append(
                    f"missing_checks:{','.join(missing_checks)}"
                )

            invalid_checks = [
                key for key, value in checks.items()
                if not isinstance(value, bool)
            ]
            if invalid_checks:
                errors.append(
                    f"non_boolean_checks:{','.join(sorted(invalid_checks))}"
                )

        status = report.get("status")
        if status not in {"HEALTHY", "WARNING", "CRITICAL"}:
            errors.append("invalid_status")

        missing_critical = report.get("missing_critical")
        if not isinstance(missing_critical, list):
            errors.append("missing_critical must be a list")
        elif isinstance(checks, dict):
            expected_missing = sorted(
                key for key, value in checks.items()
                if value is False
            )
            if sorted(missing_critical) != expected_missing:
                errors.append("missing_critical_inconsistent")

        if status == "CRITICAL" and not missing_critical:
            errors.append("critical_status_without_missing_critical")

        if status == "HEALTHY" and missing_critical:
            errors.append("healthy_status_with_missing_critical")

        runtime = report.get("runtime")
        if isinstance(runtime, dict):
            if runtime.get("present") is False:
                warnings.append("runtime_missing")
        else:
            errors.append("runtime must be an object")

        tests = report.get("tests")
        if isinstance(tests, dict):
            if tests.get("present") is False:
                warnings.append("tests_missing")
        else:
            errors.append("tests must be an object")

        git = report.get("git")
        if not isinstance(git, dict):
            errors.append("git must be an object")
        else:
            if git.get("status") == "DIRTY":
                warnings.append("git_dirty")

        if errors:
            state = "INVALID"
        elif warnings:
            state = "VALID_WITH_WARNINGS"
        else:
            state = "VALID"

        return self._result(
            state,
            errors=errors,
            warnings=warnings,
        )

    def _result(self, state, errors, warnings):
        return {
            "validator": "DTA-003.1",
            "timestamp": datetime.now(UTC).isoformat(),
            "validation_state": state,
            "valid": state in {"VALID", "VALID_WITH_WARNINGS"},
            "errors": errors,
            "warnings": warnings,
        }


def load_report(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    report_path = Path("audit_report.json")

    if report_path.exists():
        report = load_report(report_path)
        result = TechnicalValidator().validate(report)
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print(json.dumps({
            "validator": "DTA-003.1",
            "validation_state": "NO_DATA",
            "valid": False,
            "errors": ["audit_report.json not found"],
            "warnings": [],
        }, indent=4, ensure_ascii=False))
