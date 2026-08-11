#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
REPORT = BASE / "runtime" / "recovery" / "runtime_event_bridge_report.json"


class RuntimeEventBridge:
    """Bridge real Runtime EventBus events into the recovery layer."""

    EVENT_MAP = {
        "runtime_started": {
            "runtime_state": "RUNNING",
            "timeline_state": "HEALTHY",
            "recovery_state": "MONITORING",
            "result": "SUCCESS",
        },
        "runtime_stopped": {
            "runtime_state": "STOPPED",
            "timeline_state": "RECOVERY_REQUIRED",
            "recovery_state": "RECOVERY_REQUIRED",
            "result": "TRIGGERED",
        },
        "runtime_reloaded": {
            "runtime_state": "RUNNING",
            "timeline_state": "HEALTHY",
            "recovery_state": "MONITORING",
            "result": "SUCCESS",
        },
    }

    def __init__(self):
        self.events = []

    def handle(self, payload):
        event_name = payload.get("event", "unknown")
        data = payload.get("data", {})

        mapped = self.EVENT_MAP.get(event_name)

        if mapped is None:
            return None

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_name,
            "runtime_state": mapped["runtime_state"],
            "timeline_state": mapped["timeline_state"],
            "recovery_state": mapped["recovery_state"],
            "result": mapped["result"],
            "data": data,
        }

        self.events.append(event)
        self.save()

        return event

    def save(self):
        REPORT.parent.mkdir(parents=True, exist_ok=True)

        report = {
            "project": BASE.name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": "DTA-019.3",
            "mode": "EVENTBUS",
            "events": self.events,
            "status": "READY",
        }

        REPORT.write_text(
            json.dumps(report, indent=4),
            encoding="utf-8",
        )

    def register(self, event_bus):
        if event_bus is None:
            return False

        registered = []

        for event_name in self.EVENT_MAP:
            if event_bus.register(
                "system",
                event_name,
                self.handle,
            ):
                registered.append(event_name)

        return registered


bridge = RuntimeEventBridge()


if __name__ == "__main__":
    bridge.save()
    print(json.dumps({
        "engine": "DTA-019.3",
        "mode": "EVENTBUS",
        "status": "READY",
    }, indent=4))
