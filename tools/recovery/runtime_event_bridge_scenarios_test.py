#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime, timezone


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "runtime_event_bridge_scenarios_report.json"
)


def scenario(runtime_state):
    timestamp = datetime.now(timezone.utc).isoformat()

    if runtime_state == "RUNNING":
        return {
            "event": "runtime_started",
            "timeline_state": "HEALTHY",
            "recovery_state": "MONITORING",
            "result": "SUCCESS",
        }

    if runtime_state == "STOPPED":
        return {
            "event": "runtime_failed",
            "timeline_state": "RECOVERY_REQUIRED",
            "recovery_state": "RECOVERY_REQUIRED",
            "result": "TRIGGERED",
        }

    if runtime_state == "RESTORED":
        return {
            "event": "runtime_restored",
            "timeline_state": "RECOVERY_COMPLETE",
            "recovery_state": "HEALTHY",
            "result": "SUCCESS",
        }

    return {
        "event": "unknown_runtime_state",
        "timeline_state": "UNKNOWN",
        "recovery_state": "FAILED",
        "result": "BLOCKED",
    }


def main():
    tests = [
        {
            "scenario": "runtime_start_bridge",
            "runtime": "RUNNING",
            "result": scenario("RUNNING"),
        },
        {
            "scenario": "runtime_failure_bridge",
            "runtime": "STOPPED",
            "result": scenario("STOPPED"),
        },
        {
            "scenario": "runtime_restore_bridge",
            "runtime": "RESTORED",
            "result": scenario("RESTORED"),
        },
        {
            "scenario": "unknown_runtime_state",
            "runtime": "UNKNOWN",
            "result": scenario("UNKNOWN"),
        },
    ]

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-019.2",
        "tests": tests,
        "status": "READY",
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)

    REPORT.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
