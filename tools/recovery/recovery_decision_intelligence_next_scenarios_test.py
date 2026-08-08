from pathlib import Path
import sys
import json

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from tools.recovery.recovery_decision_intelligence_next import analyze_next_layer


def run_scenario(name, kwargs, expected):
    result = analyze_next_layer(**kwargs)
    passed = all(result.get(k) == v for k, v in expected.items())

    return {
        "scenario": name,
        "result": result,
        "expected": expected,
        "passed": passed,
    }


def main():
    tests = [
        run_scenario(
            "unknown_inputs",
            {},
            {
                "next_state": "UNKNOWN",
                "next_strength": 0,
                "next_signal": None,
                "recommendation": "NO_DATA",
                "review_required": False,
            },
        ),
        run_scenario(
            "stable_inputs",
            {
                "outcome_state": "STABLE",
                "history_state": "ACTIVE",
                "correlation_state": "NO_ALIGNMENT",
            },
            {
                "next_state": "STABLE",
                "next_strength": 0.25,
                "next_signal": "STABLE_PATTERN",
                "recommendation": "CONTINUE_MONITORING",
                "review_required": False,
            },
        ),
        run_scenario(
            "partial_correlation",
            {
                "outcome_state": "STABLE",
                "history_state": "ACTIVE",
                "correlation_state": "PARTIAL_ALIGNMENT",
            },
            {
                "next_state": "WARNING",
                "next_strength": 0.5,
                "next_signal": "CORRELATION_RISK",
                "recommendation": "MONITOR",
                "review_required": False,
            },
        ),
        run_scenario(
            "degraded_outcome",
            {
                "outcome_state": "DEGRADED",
                "history_state": "ACTIVE",
                "correlation_state": "NO_ALIGNMENT",
            },
            {
                "next_state": "DEGRADED",
                "next_strength": 0.8,
                "next_signal": "OUTCOME_RISK",
                "recommendation": "REVIEW_REQUIRED",
                "review_required": True,
            },
        ),
        run_scenario(
            "critical_alignment",
            {
                "outcome_state": "CRITICAL",
                "history_state": "CRITICAL",
                "correlation_state": "CRITICAL_ALIGNMENT",
            },
            {
                "next_state": "CRITICAL",
                "next_strength": 1.0,
                "next_signal": "MULTI_LAYER_CRITICAL",
                "recommendation": "IMMEDIATE_REVIEW",
                "review_required": True,
            },
        ),
        run_scenario(
            "critical_outcome_without_full_alignment",
            {
                "outcome_state": "CRITICAL",
                "history_state": "ACTIVE",
                "correlation_state": "NO_ALIGNMENT",
            },
            {
                "next_state": "DEGRADED",
                "next_strength": 0.8,
                "next_signal": "OUTCOME_RISK",
                "recommendation": "REVIEW_REQUIRED",
                "review_required": True,
            },
        ),
    ]

    status = "READY" if all(item["passed"] for item in tests) else "FAILED"

    report = {
        "project": BASE.name,
        "engine": "DTA-030.2",
        "mode": "SCENARIO_TEST",
        "tests": tests,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_decision_intelligence_next_scenarios_report.json"
    )

    report_path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4, ensure_ascii=False))
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
