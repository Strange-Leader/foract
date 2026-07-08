from foract.models import PluginDefinition
from foract.registry.base import Registry


class PluginRegistry(Registry[PluginDefinition]):
    """
    Registry for plugin definitions.
    """
