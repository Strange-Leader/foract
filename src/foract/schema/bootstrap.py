from __future__ import annotations

from foract.schema.builtin import (
    BUILTIN_RELATIONSHIPS,
    BUILTIN_SCHEMAS,
)
from foract.schema.registry import SchemaRegistry


def create_schema_registry() -> SchemaRegistry:
    """
    Create a SchemaRegistry preloaded with all built-in
    FORACT schemas and relationship definitions.
    """

    registry = SchemaRegistry()

    for schema in BUILTIN_SCHEMAS:
        registry.register_schema(schema)

    for relationship in BUILTIN_RELATIONSHIPS:
        registry.register_relationship(relationship)

    return registry
