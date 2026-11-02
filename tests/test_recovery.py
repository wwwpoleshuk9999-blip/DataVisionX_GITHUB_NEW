import importlib
import json

import pytest

recovery_module = importlib.import_module("core.recovery")
RecoveryManager = recovery_module.RecoveryManager


@pytest.fixture
def manager(tmp_path, monkeypatch):
    monkeypatch.setattr(
        recovery_module,
        "EVENT_LOG",
        tmp_path / "runtime" / "events.log"
    )
    monkeypatch.setattr(
        recovery_module,
        "RECOVERY_LOG",
        tmp_path / "runtime" / "recovery.log"
    )
    return RecoveryManager()


def test_write_event(manager):
    manager.write_event("TEST_EVENT", {"value": 123})

    assert manager.last_action == "TEST_EVENT"
    assert len(manager.history) == 1

    event = json.loads(
        recovery_module.EVENT_LOG.read_text(encoding="utf-8").strip()
    )

    assert event["action"] == "TEST_EVENT"
    assert event["data"]["value"] == 123


def test_status_and_history(manager):
    manager.write_event("FIRST")
    manager.write_event("SECOND")

    status = manager.status()

    assert status["last_action"] == "SECOND"
    assert status["history_count"] == 2
    assert len(manager.get_history()) == 2


def test_successful_recovery(manager, monkeypatch):
    monkeypatch.setattr(
        recovery_module.runtime,
        "read",
        lambda: {"status": "STOPPED"}
    )
    monkeypatch.setattr(
        recovery_module.service,
        "is_running",
        lambda: False
    )
    monkeypatch.setattr(
        recovery_module.plugin_recovery,
        "recover",
        lambda: ["example"]
    )

    result = manager.check_and_recover()

    assert result["status"] == "RECOVERED"
    assert result["plugins"] == ["example"]
    assert manager.attempts == 0
    assert manager.last_action == "RECOVERY_SUCCESS"


def test_recovery_attempt_limit(manager, monkeypatch):
    monkeypatch.setattr(
        recovery_module.runtime,
        "read",
        lambda: {"status": "STOPPED"}
    )
    monkeypatch.setattr(
        recovery_module.service,
        "is_running",
        lambda: False
    )

    manager.attempts = manager.MAX_ATTEMPTS

    result = manager.check_and_recover()

    assert result["status"] == "FAILED"
    assert result["attempts"] == manager.MAX_ATTEMPTS
    assert manager.last_action == "RECOVERY_LIMIT_REACHED"
