import json
from pathlib import Path
from datetime import datetime, UTC


class TechnicalDoctor:
    def diagnose(
        self,
        audit_report=None,
        validation_report=None,
        inspection_report=None,
    ):
        findings = []
        recommendations = []

        if not audit_report:
            findings.append("AUDIT_DATA_MISSING")
            recommendations.append("RUN_AUDITOR")

        if not validation_report:
            findings.append("VALIDATION_DATA_MISSING")
            recommendations.append("RUN_VALIDATOR")

        if not inspection_report:
            findings.append("INSPECTION_DATA_MISSING")
            recommendations.append("RUN_INSPECTOR")

        if findings:
            severity = "WARNING"
            diagnosis = "INCOMPLETE_DATA"
        else:
            audit_status = audit_report.get("status")
            validation_state = validation_report.get(
                "validation_state"
            )
            inspection_status = inspection_report.get("status")

            if validation_state == "INVALID":
                severity = "CRITICAL"
                diagnosis = "INVALID_AUDIT_DATA"
                findings.append("VALIDATOR_REJECTED_REPORT")
                recommendations.append("REVIEW_AUDIT_REPORT")

            elif audit_status == "CRITICAL":
                severity = "CRITICAL"
                diagnosis = "CRITICAL_PROJECT_STATE"
                findings.append("AUDITOR_CRITICAL")
                recommendations.append("REVIEW_MISSING_COMPONENTS")

            elif (
                inspection_status == "MISSING"
                or inspection_status == "WARNING"
            ):
                severity = "WARNING"
                diagnosis = "INSPECTION_FINDINGS"
                findings.append("INSPECTOR_WARNING")
                recommendations.append("REVIEW_COMPONENT_STRUCTURE")

            elif validation_state == "VALID_WITH_WARNINGS":
                severity = "WARNING"
                diagnosis = "VALID_WITH_WARNINGS"
                findings.append("VALIDATOR_WARNINGS")
                recommendations.append("REVIEW_VALIDATION_WARNINGS")

            else:
                severity = "HEALTHY"
                diagnosis = "NO_ACTION_REQUIRED"

        return {
            "doctor": "DTA-005.1",
            "timestamp": datetime.now(UTC).isoformat(),
            "diagnosis": diagnosis,
            "severity": severity,
            "findings": findings,
            "recommendations": recommendations,
            "repair_allowed": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
        }


def load_json(path):
    return json.loads(
        Path(path).read_text(encoding="utf-8")
    )


if __name__ == "__main__":
    audit_path = Path("audit_report.json")
    validation_path = Path(
        "runtime/recovery/devtools_validator_scenarios_report.json"
    )
    inspection_path = Path(
        "runtime/recovery/devtools_inspector_report.json"
    )

    audit = load_json(audit_path) if audit_path.exists() else None
    validation = (
        load_json(validation_path)
        if validation_path.exists()
        else None
    )
    inspection = (
        load_json(inspection_path)
        if inspection_path.exists()
        else None
    )

    result = TechnicalDoctor().diagnose(
        audit_report=audit,
        validation_report=validation,
        inspection_report=inspection,
    )

    output = Path(
        "runtime/recovery/devtools_doctor_report.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    ))
    print(f"Report: {output}")
