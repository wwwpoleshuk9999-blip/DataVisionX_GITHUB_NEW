#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_intelligence_outcome_report.json"
)


def build_outcome(synthesis):
    state = synthesis.get("synthesis_state")
    strength = synthesis.get("synthesis_strength", 0)
    signal = synthesis.get("dominant_signal")
    recommendation = synthesis.get("recommendation")
    review_required = synthesis.get("review_required", False)

    if state is None:
        return {
            "outcome_state": "UNKNOWN",
            "outcome_strength": 0,
            "outcome_signal": None,
            "recommendation": "NO_DATA",
            "review_required": False,
        }

    if state == "CRITICAL":
        outcome_state = "CRITICAL"
    elif state == "DEGRADED":
        outcome_state = "DEGRADED"
    elif state == "WARNING":
        outcome_state = "WARNING"
    else:
        outcome_state = "STABLE"

    return {
        "outcome_state": outcome_state,
        "outcome_strength": strength,
        "outcome_signal": signal,
        "recommendation": recommendation,
        "review_required": review_required,
    }


def main():
    synthesis = {
        "synthesis_state": "CRITICAL",
        "synthesis_strength": 1.0,
        "dominant_signal": "MULTI_LAYER_CRITICAL",
        "recommendation": "IMMEDIATE_REVIEW",
        "review_required": True,
    }

    outcome = build_outcome(synthesis)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-028.1",
        "mode": "REPORT_ONLY",
        "outcome": outcome,
        "source": {
            "engine": "DTA-027.1",
            "synthesis_state": synthesis[
                "synthesis_state"
            ],
        },
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

    REPORT.write_text(
        json.dumps(
            report,
            indent=4,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            report,
            indent=4,
        )
    )

    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
