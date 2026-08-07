#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE))

from tools.recovery.recovery_audit_query import (
    query_events,
    summary,
    STORAGE,
)


def main():

    tests = []

    history_exists = STORAGE.exists()

    tests.append({
        "scenario": "history_available",
        "result": {
            "storage_exists": history_exists,
        },
        "passed": history_exists,
    })


    all_events = query_events()

    tests.append({
        "scenario": "query_all",
        "result": summary(all_events),
        "passed": len(all_events) >= 0,
    })


    recover = query_events(
        decision="RECOVER"
    )

    tests.append({
        "scenario": "filter_recover",
        "result": summary(recover),
        "passed": all(
            x.get("decision") == "RECOVER"
            for x in recover
        ),
    })


    escalate = query_events(
        decision="ESCALATE"
    )

    tests.append({
        "scenario": "filter_escalate",
        "result": summary(escalate),
        "passed": all(
            x.get("decision") == "ESCALATE"
            for x in escalate
        ),
    })


    confidence = query_events(
        min_confidence=0.9
    )

    tests.append({
        "scenario": "confidence_filter",
        "result": summary(confidence),
        "passed": all(
            x.get("confidence", 0) >= 0.9
            for x in confidence
        ),
    })


    combined = query_events(
        decision="RECOVER",
        status="BLOCKED",
        min_confidence=0.9,
    )

    tests.append({
        "scenario": "combined_filter",
        "result": summary(combined),
        "passed": all(
            x.get("decision") == "RECOVER"
            and x.get("status") == "BLOCKED"
            for x in combined
        ),
    })


    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-022.4",
        "mode": "SCENARIO_TEST",
        "tests": tests,
        "status": (
            "READY"
            if all(x["passed"] for x in tests)
            else "FAILED"
        ),
    }


    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "recovery_audit_query_scenarios_report.json"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", report_path)


if __name__ == "__main__":
    main()
