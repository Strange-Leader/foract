from foract.enums import PluginStatus, PluginType
from foract.models import PluginDefinition, Result


def test_plugin_definition_defaults() -> None:
    plugin = PluginDefinition(
        name="windows.pslist",
        version="1.0",
        plugin_type=PluginType.VOLATILITY,
    )
    assert plugin.status == PluginStatus.ENABLED
    assert plugin.description == ""


def test_result_model() -> None:
    result = Result[int](
        success=True,
        data=42,
    )
    assert result.success
    assert result.data == 42
