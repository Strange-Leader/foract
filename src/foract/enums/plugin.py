from enum import StrEnum


class PluginStatus(StrEnum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class PluginType(StrEnum):
    VOLATILITY = "volatility"
    NATIVE = "native"
    EXTERNAL = "external"
