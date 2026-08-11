#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
REPORT = BASE / "runtime" / "recovery" / "runtime_monitor_report.json"


class RuntimeMonitor:
    """Runtime health monitor driven by real Runtime events."""

    def __init__(self):
        self.status = "UNKNOWN"
        self.last_event = None
        self.history = []

    def handle(self, event):
        if not event:
            return

        self.status = event.get("runtime_state", "UNKNOWN")
        self.last_event = event

        self.history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "runtime_state": self.status,
            "event": event.get("event"),
            "result": event.get("result"),
        })

        self.save()

    def health(self):
        if self.status == "RUNNING":
            return {
                "status": "HEALTHY",
                "next_state": "MONITORING",
                "reason": "runtime active",
            }

        if self.status == "STOPPED":
            return {
                "status": "RECOVERY_REQUIRED",
                "next_state": "RECOVERY_REQUIRED",
                "reason": "runtime unavailable",
            }

        return {
            "status": "UNKNOWN",
            "next_state": "MONITORING",
            "reason": "runtime state not observed",
        }

    def save(self):
        REPORT.parent.mkdir(parents=True, exist_ok=True)

        report = {
            "project": BASE.name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": "DTA-018.3",
            "mode": "EVENTBUS",
            "runtime_state": self.status,
            "health": self.health(),
            "last_event": self.last_event,
            "history": self.history,
            "status": "READY",
        }

        REPORT.write_text(
            json.dumps(report, indent=4),
            encoding="utf-8",
        )


monitor = RuntimeMonitor()


if __name__ == "__main__":
    monitor.save()

    print(json.dumps(
        monitor.health(),
        indent=4,
    ))

    print("Report:", REPORT)
