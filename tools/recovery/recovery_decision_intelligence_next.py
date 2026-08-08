from pathlib import Path
from datetime import datetime, timezone
import json

BASE = Path(__file__).resolve().parents[2]
REPORT_DIR = BASE / "runtime" / "recovery"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_next_layer(
    outcome_state="UNKNOWN",
    outcome_strength=0,
    history_state="EMPTY",
    correlation_state="UNKNOWN",
):
    signals = [
        outcome_state != "UNKNOWN",
        history_state != "EMPTY",
        correlation_state != "UNKNOWN",
    ]

    active = sum(signals)

    if active == 0:
        state = "UNKNOWN"
        strength = 0
        signal = None
        recommendation = "NO_DATA"
        review_required = False

    elif (
        outcome_state == "CRITICAL"
        and history_state == "CRITICAL"
        and correlation_state == "CRITICAL_ALIGNMENT"
    ):
        state = "CRITICAL"
        strength = 1.0
        signal = "MULTI_LAYER_CRITICAL"
        recommendation = "IMMEDIATE_REVIEW"
        review_required = True

    elif outcome_state in {"CRITICAL", "DEGRADED"}:
        state = "DEGRADED"
        strength = 0.8
        signal = "OUTCOME_RISK"
        recommendation = "REVIEW_REQUIRED"
        review_required = True

    elif correlation_state in {"STRONG_ALIGNMENT", "PARTIAL_ALIGNMENT"}:
        state = "WARNING"
        strength = 0.5
        signal = "CORRELATION_RISK"
        recommendation = "MONITOR"
        review_required = False

    else:
        state = "STABLE"
        strength = 0.25
        signal = "STABLE_PATTERN"
        recommendation = "CONTINUE_MONITORING"
        review_required = False

    return {
        "next_state": state,
        "next_strength": strength,
        "next_signal": signal,
        "recommendation": recommendation,
        "review_required": review_required,
    }


def main():
    result = analyze_next_layer(
        outcome_state="CRITICAL",
        outcome_strength=1.0,
        history_state="CRITICAL",
        correlation_state="CRITICAL_ALIGNMENT",
    )

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-030.1",
        "mode": "REPORT_ONLY",
        "next_layer": result,
        "safety": {
            "automatic_recovery": False,
            "execution_allowed": False,
            "action": "NO_EXECUTION",
        },
        "status": "READY",
    }

    report_path = REPORT_DIR / "recovery_decision_intelligence_next_report.json"
    report_path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=4, ensure_ascii=False))
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
