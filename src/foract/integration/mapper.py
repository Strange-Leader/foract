from __future__ import annotations

from typing import Any

from foract.graph.enums import EdgeType, NodeType
from foract.integration.models import (
    MappedEntity,
    RelationshipDescriptor,
)
from foract.registry import SchemaRegistry
from foract.schema.definition import SchemaDefinition


class EvidenceMapper:
    """
    Converts validated forensic records into semantic entities.

    The mapper produces unresolved MappedEntity objects.
    Entity resolution and graph persistence occur later in the
    integration pipeline.
    """

    def __init__(
        self,
        registry: SchemaRegistry,
    ) -> None:
        self._registry = registry

        self._node_types: dict[str, NodeType] = {
            "Process": NodeType.PROCESS,
            "File": NodeType.FILE,
            "PE": NodeType.PE,
            "Socket": NodeType.SOCKET,
            "RegistryKey": NodeType.REGISTRY_KEY,
        }

    def map(
        self,
        schema_name: str,
        records: list[dict[str, Any]],
    ) -> list[MappedEntity]:
        """
        Convert validated records into semantic entities.
        """

        schema = self._registry.get(schema_name)

        node_type = self._node_types.get(schema.name)

        if node_type is None:
            raise ValueError(f"No NodeType registered for schema '{schema.name}'.")

        entities: list[MappedEntity] = []

        for record in records:

            identity_key = self._build_identity_key(
                schema,
                record,
            )

            relationships = self._build_relationships(
                schema.name,
                record,
            )

            entities.append(
                MappedEntity(
                    schema_name=schema.name,
                    node_type=node_type,
                    properties=dict(record),
                    identity_key=identity_key,
                    relationships=relationships,
                )
            )

        return entities

    def _build_identity_key(
        self,
        schema: SchemaDefinition,
        record: dict[str, Any],
    ) -> str:
        """
        Construct the semantic identity key using the schema's
        identity fields.
        """

        identity_parts = []

        for field in schema.identity_fields:
            identity_parts.append(f"{field.name}={record[field.name]}")

        return f"{schema.name}:" + "|".join(identity_parts)

    def _build_relationships(
        self,
        schema_name: str,
        record: dict[str, Any],
    ) -> list[RelationshipDescriptor]:
        """
        Produce logical relationship descriptors.

        These relationships are resolved later after node UUIDs
        are known.
        """

        relationships: list[RelationshipDescriptor] = []

        if schema_name == "Process":

            parent_pid = record.get("ppid")

            if parent_pid is not None:

                relationships.append(
                    RelationshipDescriptor(
                        edge_type=EdgeType.PARENT_OF,
                        target_identity_key=(f"Process:pid={parent_pid}"),
                    )
                )

        return relationships
