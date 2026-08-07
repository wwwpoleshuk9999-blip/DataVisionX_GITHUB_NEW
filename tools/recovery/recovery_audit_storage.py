#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

STORAGE = (
    BASE
    / "runtime"
    / "recovery"
    / "audit_history.json"
)


def save_audit_event(event):

    history = load_history()

    event["stored_at"] = datetime.now(timezone.utc).isoformat()

    history.append(event)

    STORAGE.parent.mkdir(parents=True, exist_ok=True)

    STORAGE.write_text(
        json.dumps(history, indent=4),
        encoding="utf-8",
    )

    return event


def load_history():

    if not STORAGE.exists():
        return []

    return json.loads(
        STORAGE.read_text(
            encoding="utf-8"
        )
    )


def audit_summary():

    history = load_history()

    return {
        "total_events": len(history),
        "blocked": len(
            [
                x for x in history
                if x.get("status") == "BLOCKED"
            ]
        ),
        "ready": len(
            [
                x for x in history
                if x.get("status") == "READY_FOR_ORCHESTRATOR"
            ]
        ),
        "last_event": (
            history[-1]
            if history
            else None
        ),
    }


def main():

    event = {
        "decision": "RECOVER",
        "confidence": 0.9,
        "target_state": "RECOVERY_REQUIRED",
        "status": "BLOCKED",
        "execution_allowed": False,
        "action": "NO_EXECUTION",
        "reason": "confirmation required",
    }

    save_audit_event(event)

    report = {
        "project": BASE.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine": "DTA-022.1",
        "mode": "STORAGE_FOUNDATION",
        "summary": audit_summary(),
        "status": "READY",
    }

    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()
