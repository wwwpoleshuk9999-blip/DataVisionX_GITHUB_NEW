import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from devtools.manager.manager import DevToolsManager


def run_scenario(name, component="devtools"):
    manager = DevToolsManager(BASE)
    result = manager.run(component)

    checks = {
        "manager": result.get("manager") == "DTA-007.1",
        "status": result.get("status") == "READY",
        "audit_present": isinstance(result.get("audit"), dict),
        "validation_present": isinstance(result.get("validation"), dict),
        "inspection_present": isinstance(result.get("inspection"), dict),
        "diagnosis_present": isinstance(result.get("diagnosis"), dict),
        "profile_present": isinstance(result.get("profile"), dict),
        "safety_present": isinstance(result.get("safety"), dict),
        "execution_disabled": (
            result.get("safety", {}).get("execution_allowed") is False
        ),
        "recovery_disabled": (
            result.get("safety", {}).get("automatic_recovery") is False
        ),
        "action_no_execution": (
            result.get("safety", {}).get("action") == "NO_EXECUTION"
        ),
    }

    passed = all(checks.values())

    return {
        "scenario": name,
        "checks": checks,
        "passed": passed,
        "summary": {
            "audit_status": result.get("audit", {}).get("status"),
            "validation_state": result.get("validation", {}).get(
                "validation_state"
            ),
            "inspection_status": result.get("inspection", {}).get("status"),
            "diagnosis": result.get("diagnosis", {}).get("diagnosis"),
            "severity": result.get("diagnosis", {}).get("severity"),
            "profile_state": result.get("profile", {})
            .get("profile", {})
            .get("profile_state"),
        },
    }


def main():
    tests = [
        run_scenario("default_devtools"),
        run_scenario("manager_self_inspection", "devtools/manager"),
        run_scenario("auditor_inspection", "devtools/auditor"),
    ]

    status = "READY" if all(item["passed"] for item in tests) else "FAILED"

    report = {
        "project": BASE.name,
        "engine": "DTA-007.2",
        "mode": "SCENARIO_TEST",
        "tests": tests,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "devtools_manager_scenarios_report.json"
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4, ensure_ascii=False))
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
