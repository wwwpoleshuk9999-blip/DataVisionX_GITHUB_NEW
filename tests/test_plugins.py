import json

from plugin_manager.loader import PluginLoader
from plugin_manager.models import PluginInfo
from plugin_manager.validator import PluginValidator
from plugin_manager.health import PluginHealthManager
from plugin_manager.manager import PluginManager
import plugin_manager.manager as manager_module


def test_plugin_loader_discovers_manifest(tmp_path):
    plugin_dir = tmp_path / "sample"
    plugin_dir.mkdir()

    manifest = {
        "name": "Sample Plugin",
        "version": "1.0.0"
    }
    (plugin_dir / "manifest.json").write_text(
        json.dumps(manifest),
        encoding="utf-8"
    )

    loader = PluginLoader(str(tmp_path))
    plugins = loader.discover()

    assert len(plugins) == 1
    assert plugins[0].id == "sample"
    assert plugins[0].name == "Sample Plugin"
    assert plugins[0].version == "1.0.0"


def test_plugin_validator():
    plugin_dir = PluginInfo(
        id="sample",
        name="Sample",
        version="1.0.0",
        author="Test",
        description="Test plugin",
        api_version="1.0",
        path="."
    )

    valid, errors = PluginValidator().validate(plugin_dir)

    assert valid is True
    assert errors == []


def test_plugin_manager_start_and_stop(monkeypatch, tmp_path):
    manager = PluginManager()

    plugin = PluginInfo(
        id="sample",
        name="Sample",
        version="1.0.0",
        author="Test",
        description="Test plugin",
        api_version="1.0",
        path=str(tmp_path)
    )

    manager.plugins[plugin.id] = plugin

    class FakeLifecycle:
        def start(self, plugin):
            return object()

        def stop(self, plugin_id):
            return True

    manager.lifecycle = FakeLifecycle()

    monkeypatch.setattr(
        manager_module,
        "update_plugin_status",
        lambda *args: None
    )

    assert manager.start("sample") is True
    assert plugin.status == "RUNNING"
    assert manager.health.get("sample")["status"] == "RUNNING"

    assert manager.stop("sample") is True
    assert plugin.status == "STOPPED"
    assert manager.health.get("sample")["status"] == "STOPPED"


def test_plugin_health_recovery():
    health = PluginHealthManager()

    health.started("sample")
    health.failed("sample", "Test error")
    health.recovered("sample")

    result = health.get("sample")

    assert result["status"] == "RUNNING"
    assert result["health"] == "RECOVERED"
    assert result["restart_count"] == 1
    assert result["last_error"] == "Test error"
