import importlib
import json

import pytest

watchdog_module = importlib.import_module("core.watchdog")
Watchdog = watchdog_module.Watchdog


@pytest.fixture
def watchdog(tmp_path, monkeypatch):
    monkeypatch.setattr(
        watchdog_module,
        "WATCHDOG_LOG",
        tmp_path / "runtime" / "watchdog.log"
    )
    monkeypatch.setattr(
        watchdog_module,
        "EVENT_LOG",
        tmp_path / "runtime" / "events.log"
    )
    return Watchdog()


def test_healthy_runtime(watchdog, monkeypatch):
    monkeypatch.setattr(
        watchdog_module.runtime,
        "read",
        lambda: {"status": "RUNNING"}
    )
    monkeypatch.setattr(
        watchdog_module.service,
        "is_running",
        lambda: True
    )

    result = watchdog.check()

    assert result["status"] == "HEALTHY"
    assert result["runtime"] == "RUNNING"
    assert result["process"] == "RUNNING"
    assert watchdog.healthy_count == 1
    assert watchdog.warning_count == 0


def test_runtime_failure_triggers_recovery(watchdog, monkeypatch):
    monkeypatch.setattr(
        watchdog_module.runtime,
        "read",
        lambda: {"status": "STOPPED"}
    )
    monkeypatch.setattr(
        watchdog_module.service,
        "is_running",
        lambda: False
    )
    monkeypatch.setattr(
        watchdog_module.service,
        "read_pid",
        lambda: None
    )

    recovery_calls = []
    monkeypatch.setattr(
        watchdog_module.recovery,
        "check_and_recover",
        lambda: recovery_calls.append(True) or {
            "status": "RECOVERED",
            "plugins": ["example"]
        }
    )

    result = watchdog.check()

    assert result["status"] == "WARNING"
    assert result["recovery"]["status"] == "RECOVERED"
    assert len(recovery_calls) == 1
    assert watchdog.warning_count == 1


def test_watchdog_writes_logs(watchdog, monkeypatch):
    monkeypatch.setattr(
        watchdog_module.runtime,
        "read",
        lambda: {"status": "RUNNING"}
    )
    monkeypatch.setattr(
        watchdog_module.service,
        "is_running",
        lambda: True
    )

    watchdog.check()

    log_data = json.loads(
        watchdog_module.WATCHDOG_LOG.read_text(encoding="utf-8").strip()
    )
    event_data = json.loads(
        watchdog_module.EVENT_LOG.read_text(encoding="utf-8").strip()
    )

    assert log_data["status"] == "HEALTHY"
    assert event_data["action"] == "WATCHDOG_HEALTHY"
    assert watchdog.last_event == "WATCHDOG_HEALTHY"
