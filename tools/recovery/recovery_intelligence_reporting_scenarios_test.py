#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_intelligence_reporter import build_report


def main():

    scenarios = [

        {
            "scenario": "empty_history",
            "events": [],
            "expected": 0,
        },

        {
            "scenario": "recover_only_report",
            "events": [
                {
                    "decision": "RECOVER",
                    "status": "BLOCKED",
                }
            ],
            "expected": 1,
        },

        {
            "scenario": "escalate_only_report",
            "events": [
                {
                    "decision": "ESCALATE",
                    "status": "BLOCKED",
                }
            ],
            "expected": 1,
        },

        {
            "scenario": "mixed_events_report",
            "events": [
                {
                    "decision": "RECOVER",
                    "status": "BLOCKED",
                },
                {
                    "decision": "ESCALATE",
                    "status": "BLOCKED",
                }
            ],
            "expected": 2,
        },

        {
            "scenario": "blocked_ready_statistics",
            "events": [
                {
                    "decision": "RECOVER",
                    "status": "READY_FOR_ORCHESTRATOR",
                }
            ],
            "expected_ready": 1,
        },

    ]


    results = []


    for item in scenarios:

        report = build_report(
            item["events"]
        )

        passed = (
            report["total_events"]
            == item.get(
                "expected",
                report["total_events"]
            )
        )

        if "expected_ready" in item:
            passed = (
                report["ready_events"]
                == item["expected_ready"]
            )

        results.append(
            {
                "scenario": item["scenario"],
                "result": report,
                "passed": passed,
            }
        )


    output = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-023.2",
        "mode": "SCENARIO_TEST",
        "tests": results,
        "status": (
            "READY"
            if all(x["passed"] for x in results)
            else "FAILED"
        ),
    }


    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_intelligence_reporting_scenarios_report.json"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path.write_text(
        json.dumps(output, indent=4),
        encoding="utf-8"
    )


    print(json.dumps(output, indent=4))
    print()
    print("Report:", report_path)


if __name__ == "__main__":
    main()
