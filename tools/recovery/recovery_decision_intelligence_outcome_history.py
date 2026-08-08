#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

HISTORY_FILE = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_intelligence_outcome_history.json"
)

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_intelligence_outcome_history_report.json"
)


def append_outcome(history, outcome):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "outcome_state": outcome.get("outcome_state", "UNKNOWN"),
        "outcome_strength": outcome.get("outcome_strength", 0),
        "outcome_signal": outcome.get("outcome_signal"),
        "recommendation": outcome.get("recommendation", "NO_DATA"),
        "review_required": outcome.get("review_required", False),
    }

    history.append(record)
    return record


def summarize_history(history):
    total = len(history)

    if total == 0:
        return {
            "total_events": 0,
            "current_state": "UNKNOWN",
            "average_strength": 0,
            "review_required_count": 0,
            "history_state": "EMPTY",
        }

    strengths = [
        item.get("outcome_strength", 0)
        for item in history
        if isinstance(item.get("outcome_strength"), (int, float))
    ]

    review_count = sum(
        1
        for item in history
        if item.get("review_required") is True
    )

    current_state = history[-1].get(
        "outcome_state",
        "UNKNOWN",
    )

    average_strength = round(
        sum(strengths) / len(strengths),
        3,
    ) if strengths else 0

    if current_state == "CRITICAL":
        history_state = "CRITICAL"
    elif current_state == "DEGRADED":
        history_state = "DEGRADED"
    elif total == 1:
        history_state = "INITIAL"
    elif current_state == "WARNING":
        history_state = "WARNING"
    else:
        history_state = "ACTIVE"

    return {
        "total_events": total,
        "current_state": current_state,
        "average_strength": average_strength,
        "review_required_count": review_count,
        "history_state": history_state,
    }


def main():
    history = []

    outcome = {
        "outcome_state": "CRITICAL",
        "outcome_strength": 1.0,
        "outcome_signal": "MULTI_LAYER_CRITICAL",
        "recommendation": "IMMEDIATE_REVIEW",
        "review_required": True,
    }

    append_outcome(history, outcome)
    summary = summarize_history(history)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-029.1",
        "mode": "REPORT_ONLY",
        "summary": summary,
        "latest_outcome": history[-1],
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
        },
        "status": "READY",
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    HISTORY_FILE.write_text(
        json.dumps(
            history,
            indent=4,
        ),
        encoding="utf-8",
    )

    REPORT.write_text(
        json.dumps(
            report,
            indent=4,
        ),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4))
    print()
    print("History:", HISTORY_FILE)
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
