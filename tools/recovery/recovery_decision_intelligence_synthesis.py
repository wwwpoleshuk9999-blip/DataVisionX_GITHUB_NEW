#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_intelligence_synthesis_report.json"
)


def synthesize(intelligence, trend, history, correlation):
    intelligence_state = intelligence.get("intelligence_state")
    trend_direction = trend.get("trend_direction")
    history_state = history.get("history_state")
    correlation_state = correlation.get("correlation_state")

    if any(
        value is None
        for value in (
            intelligence_state,
            trend_direction,
            history_state,
            correlation_state,
        )
    ):
        return {
            "synthesis_state": "UNKNOWN",
            "synthesis_strength": 0,
            "dominant_signal": None,
            "recommendation": "NO_DATA",
            "review_required": False,
        }

    critical = (
        intelligence_state == "CRITICAL"
        and trend_direction == "WORSENING"
        and correlation_state == "CRITICAL_ALIGNMENT"
    )

    strong = (
        intelligence_state in ("DEGRADED", "CRITICAL")
        and trend_direction == "WORSENING"
        and correlation_state
        in ("STRONG_ALIGNMENT", "CRITICAL_ALIGNMENT")
    )

    if critical:
        synthesis_state = "CRITICAL"
        synthesis_strength = 1.0
        dominant_signal = "MULTI_LAYER_CRITICAL"
        recommendation = "IMMEDIATE_REVIEW"
        review_required = True

    elif strong:
        synthesis_state = "DEGRADED"
        synthesis_strength = 0.8
        dominant_signal = "MULTI_LAYER_RISK"
        recommendation = "REVIEW_REQUIRED"
        review_required = True

    elif correlation_state == "PARTIAL_ALIGNMENT":
        synthesis_state = "WARNING"
        synthesis_strength = 0.5
        dominant_signal = "PARTIAL_RISK"
        recommendation = "MONITOR"
        review_required = False

    else:
        synthesis_state = "STABLE"
        synthesis_strength = 0.25
        dominant_signal = "STABLE_PATTERN"
        recommendation = "CONTINUE_MONITORING"
        review_required = False

    return {
        "synthesis_state": synthesis_state,
        "synthesis_strength": synthesis_strength,
        "dominant_signal": dominant_signal,
        "recommendation": recommendation,
        "review_required": review_required,
    }


def main():
    intelligence = {
        "intelligence_state": "CRITICAL",
    }

    trend = {
        "trend_direction": "WORSENING",
    }

    history = {
        "history_state": "DOMINANT",
    }

    correlation = {
        "correlation_state": "CRITICAL_ALIGNMENT",
    }

    synthesis = synthesize(
        intelligence,
        trend,
        history,
        correlation,
    )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-027.1",
        "mode": "REPORT_ONLY",
        "synthesis": synthesis,
        "inputs": {
            "intelligence_state":
                intelligence["intelligence_state"],
            "trend_direction":
                trend["trend_direction"],
            "history_state":
                history["history_state"],
            "correlation_state":
                correlation["correlation_state"],
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
