from pydantic import BaseModel

from foract.enums import PluginStatus, PluginType


class PluginDefinition(BaseModel):
    name: str
    version: str
    plugin_type: PluginType
    status: PluginStatus = PluginStatus.ENABLED
    description: str = ""
