#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REPORT = (
    BASE
    / "runtime"
    / "recovery"
    / "recovery_decision_intelligence_report.json"
)


def analyze_intelligence(
    health_state,
    risk_level,
    dominant_decision,
    confidence,
    trend_direction,
    trend_strength,
):
    if health_state == "UNKNOWN":
        return {
            "intelligence_state": "UNKNOWN",
            "priority": "LOW",
            "recommendation": "NO_DATA",
            "review_required": False,
        }

    if risk_level == "HIGH":
        priority = "CRITICAL"
    elif risk_level == "MEDIUM":
        priority = "HIGH"
    else:
        priority = "LOW"

    if trend_direction == "WORSENING":
        recommendation = "IMMEDIATE_REVIEW"
        review_required = True
    elif trend_direction == "IMPROVING":
        recommendation = "CONTINUE_MONITORING"
        review_required = False
    elif risk_level == "HIGH":
        recommendation = "REVIEW_REQUIRED"
        review_required = True
    else:
        recommendation = "MONITOR"
        review_required = False

    if (
        confidence >= 0.9
        and risk_level == "HIGH"
        and trend_direction == "WORSENING"
    ):
        intelligence_state = "CRITICAL"
    elif risk_level == "HIGH":
        intelligence_state = "DEGRADED"
    elif risk_level == "MEDIUM":
        intelligence_state = "WARNING"
    else:
        intelligence_state = "STABLE"

    return {
        "intelligence_state": intelligence_state,
        "priority": priority,
        "dominant_decision": dominant_decision,
        "confidence": confidence,
        "trend_direction": trend_direction,
        "trend_strength": trend_strength,
        "recommendation": recommendation,
        "review_required": review_required,
    }


def main():
    analysis = analyze_intelligence(
        health_state="DEGRADED",
        risk_level="HIGH",
        dominant_decision="RECOVER",
        confidence=0.925,
        trend_direction="WORSENING",
        trend_strength=0.5,
    )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "engine": "DTA-025.1",
        "mode": "REPORT_ONLY",
        "analysis": analysis,
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

    print(json.dumps(report, indent=4))
    print()
    print("Report:", REPORT)


if __name__ == "__main__":
    main()
