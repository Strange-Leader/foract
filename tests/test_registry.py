import pytest

from foract.enums import PluginType
from foract.exceptions import RegistryError
from foract.models import PluginDefinition
from foract.registry import PluginRegistry


def test_register_plugin() -> None:
    registry = PluginRegistry()

    plugin = PluginDefinition(
        name="windows.pslist",
        version="1.0",
        plugin_type=PluginType.VOLATILITY,
    )

    registry.register(plugin)

    assert registry.exists("windows.pslist")
    assert registry.get("windows.pslist") == plugin
    assert len(registry) == 1
    assert "windows.pslist" in registry


def test_duplicate_registration() -> None:
    registry = PluginRegistry()

    plugin = PluginDefinition(
        name="windows.pslist",
        version="1.0",
        plugin_type=PluginType.VOLATILITY,
    )

    registry.register(plugin)

    with pytest.raises(RegistryError):
        registry.register(plugin)


def test_remove_plugin() -> None:
    registry = PluginRegistry()

    plugin = PluginDefinition(
        name="windows.pslist",
        version="1.0",
        plugin_type=PluginType.VOLATILITY,
    )

    registry.register(plugin)

    registry.remove("windows.pslist")

    assert not registry.exists("windows.pslist")


def test_clear_registry() -> None:
    registry = PluginRegistry()

    registry.register(
        PluginDefinition(
            name="pslist",
            version="1.0",
            plugin_type=PluginType.VOLATILITY,
        )
    )

    registry.clear()

    assert len(registry) == 0


def test_missing_plugin() -> None:
    registry = PluginRegistry()

    with pytest.raises(RegistryError):
        registry.get("does-not-exist")
