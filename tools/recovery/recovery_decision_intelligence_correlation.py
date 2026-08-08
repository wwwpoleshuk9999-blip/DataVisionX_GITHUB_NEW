#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_intelligence_correlation_report.json"
)


def correlate(intelligence, trend, history):
    intelligence_state = intelligence.get(
        "intelligence_state"
    )
    trend_direction = trend.get(
        "trend_direction"
    )
    history_state = history.get(
        "history_state"
    )

    if (
        intelligence_state is None
        or trend_direction is None
        or history_state is None
    ):
        return {
            "correlation_state": "UNKNOWN",
            "correlation_strength": 0,
            "pattern": None,
            "recommendation": "NO_DATA",
        }

    signals = 0

    if intelligence_state in (
        "DEGRADED",
        "CRITICAL",
    ):
        signals += 1

    if trend_direction == "WORSENING":
        signals += 1

    if history_state == "DOMINANT":
        signals += 1

    if signals >= 3:
        correlation_state = "CRITICAL_ALIGNMENT"
        correlation_strength = 1.0
        recommendation = "IMMEDIATE_REVIEW"
    elif signals == 2:
        correlation_state = "STRONG_ALIGNMENT"
        correlation_strength = 0.667
        recommendation = "REVIEW_REQUIRED"
    elif signals == 1:
        correlation_state = "PARTIAL_ALIGNMENT"
        correlation_strength = 0.333
        recommendation = "MONITOR"
    else:
        correlation_state = "NO_ALIGNMENT"
        correlation_strength = 0
        recommendation = "CONTINUE_MONITORING"

    pattern_parts = []

    if intelligence_state in (
        "DEGRADED",
        "CRITICAL",
    ):
        pattern_parts.append(
            "HIGH_RISK_STATE"
        )

    if trend_direction == "WORSENING":
        pattern_parts.append(
            "WORSENING_TREND"
        )

    if history_state == "DOMINANT":
        pattern_parts.append(
            "DOMINANT_HISTORY"
        )

    pattern = (
        "+".join(pattern_parts)
        if pattern_parts
        else "STABLE_PATTERN"
    )

    return {
        "correlation_state": correlation_state,
        "correlation_strength": correlation_strength,
        "pattern": pattern,
        "recommendation": recommendation,
    }


def main():
    intelligence = {
        "intelligence_state": "DEGRADED",
    }

    trend = {
        "trend_direction": "WORSENING",
    }

    history = {
        "history_state": "DOMINANT",
    }

    correlation = correlate(
        intelligence,
        trend,
        history,
    )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-026.1",
        "mode": "REPORT_ONLY",
        "correlation": correlation,
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
