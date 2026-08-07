#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(BASE)
)

from tools.recovery.recovery_audit_storage import (
    save_audit_event,
    load_history,
    audit_summary,
    STORAGE,
)


def clear_storage():
    if STORAGE.exists():
        STORAGE.unlink()


def main():

    clear_storage()

    tests = []

    # empty storage
    empty = audit_summary()

    tests.append({
        "scenario": "empty_storage",
        "result": empty,
        "passed": empty["total_events"] == 0,
    })


    # single event
    save_audit_event({
        "decision": "RECOVER",
        "confidence": 0.9,
        "target_state": "RECOVERY_REQUIRED",
        "status": "BLOCKED",
    })

    single = audit_summary()

    tests.append({
        "scenario": "single_event",
        "result": single,
        "passed": single["total_events"] == 1,
    })


    # multiple events
    save_audit_event({
        "decision": "ESCALATE",
        "confidence": 0.95,
        "target_state": "ESCALATION_REQUIRED",
        "status": "BLOCKED",
    })

    multi = audit_summary()

    tests.append({
        "scenario": "multiple_events",
        "result": multi,
        "passed": multi["total_events"] == 2,
    })


    # persistence
    history = load_history()

    tests.append({
        "scenario": "history_persistence",
        "result": {
            "stored_events": len(history)
        },
        "passed": len(history) == 2,
    })


    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-022.2",
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
        / "recovery_audit_storage_scenarios_report.json"
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
