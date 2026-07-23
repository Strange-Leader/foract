from __future__ import annotations

from foract.integration.models import (
    MappedEntity,
    ParsedArtifact,
    RelationshipDescriptor,
)
from foract.schema.definition import SchemaDefinition
from foract.schema.registry import SchemaRegistry


class Mapper:
    """
    Maps validated ParsedArtifacts into semantic MappedEntity objects.

    Responsibilities
    ----------------
    - Build semantic identity keys.
    - Build logical relationship descriptors.
    - Produce immutable MappedEntity objects.

    The Mapper performs no persistence, graph operations,
    deduplication, or UUID allocation.
    """

    def __init__(
        self,
        schema_registry: SchemaRegistry,
    ) -> None:
        self._schema_registry = schema_registry

    def map(
        self,
        artifact: ParsedArtifact,
    ) -> MappedEntity:
        """
        Convert a validated ParsedArtifact into a semantic
        MappedEntity.
        """

        #
        # Lookup schema definition.
        #
        schema = self._schema_registry.get_schema(
            artifact.schema,
        )

        #
        # Build semantic identity key.
        #
        identity_key = self._build_identity_key(
            schema,
            artifact,
        )

        #
        # Build relationship descriptors.
        #
        relationships: list[RelationshipDescriptor] = []

        relationship_mappings = (
            self._schema_registry.get_relationship_mappings_for_schema(
                schema.name,
            )
        )

        for mapping in relationship_mappings:

            source_value = artifact.properties.get(
                mapping.source_field,
            )

            #
            # Relationship cannot be derived.
            #
            if source_value is None:
                continue

            target_identity_key = (
                f"{mapping.target_schema}:" f"{mapping.target_field}={source_value}"
            )

            relationships.append(
                RelationshipDescriptor(
                    relationship=mapping.relationship.name,
                    target_identity_key=target_identity_key,
                )
            )

        #
        # Produce semantic entity.
        #
        return MappedEntity(
            schema=schema.name,
            properties=artifact.properties,
            identity_key=identity_key,
            relationships=tuple(relationships),
        )

    def _build_identity_key(
        self,
        schema: SchemaDefinition,
        artifact: ParsedArtifact,
    ) -> str:
        """
        Build the semantic identity key for a parsed artifact.
        """

        identity_parts: list[str] = []

        for field in schema.identity_fields:
            value = artifact.properties[field.name]

            identity_parts.append(f"{field.name}={value}")

        return f"{schema.name}:" + "|".join(identity_parts)
