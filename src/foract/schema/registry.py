from __future__ import annotations

from foract.exceptions import ValidationError
from foract.schema.definition import SchemaDefinition
from foract.schema.relationship import RelationshipDefinition
from foract.schema.relationship_mapping import RelationshipMappingDefinition


class SchemaRegistry:
    """
    Central registry for the FORACT ontology.

    Owns:

    - Schema definitions
    - Relationship definitions

    The registry is purely structural. It does not implement graph logic,
    execution logic, reasoning, or integrity enforcement.
    """

    def __init__(self) -> None:
        self._schemas: dict[str, SchemaDefinition] = {}
        self._relationships: dict[str, RelationshipDefinition] = {}
        self._relationship_mappings: dict[
            str,
            list[RelationshipMappingDefinition],
        ] = {}

    # ==========================================================
    # Schema registration
    # ==========================================================

    def register_schema(self, schema: SchemaDefinition) -> None:
        if schema.name in self._schemas:
            raise ValidationError(f"Schema '{schema.name}' is already registered.")

        self._schemas[schema.name] = schema

    def get_schema(self, name: str) -> SchemaDefinition:
        try:
            return self._schemas[name]
        except KeyError as exc:
            raise ValidationError(f"Unknown schema '{name}'.") from exc

    def has_schema(self, name: str) -> bool:
        return name in self._schemas

    def list_schemas(self) -> tuple[SchemaDefinition, ...]:
        """
        Return all registered schemas in deterministic order.
        """

        return tuple(
            sorted(
                self._schemas.values(),
                key=lambda schema: schema.name,
            )
        )

    # ==========================================================
    # Relationship registration
    # ==========================================================

    def register_relationship(
        self,
        relationship: RelationshipDefinition,
    ) -> None:

        if relationship.name in self._relationships:
            raise ValidationError(
                f"Relationship '{relationship.name}' " "is already registered."
            )

        self._relationships[relationship.name] = relationship

    def register_relationship_mapping(
        self,
        mapping: RelationshipMappingDefinition,
    ) -> None:
        """
        Register a relationship mapping.
        """

        mappings = self._relationship_mappings.setdefault(
            mapping.source_schema,
            [],
        )

        for existing in mappings:

            if (
                existing.relationship.name == mapping.relationship.name
                and existing.source_schema == mapping.source_schema
                and existing.source_field == mapping.source_field
            ):
                raise ValidationError(
                    "Relationship mapping "
                    f"'{mapping.relationship.name}' "
                    "is already registered."
                )

        mappings.append(mapping)

    def get_relationship_mappings_for_schema(
        self,
        schema_name: str,
    ) -> tuple[RelationshipMappingDefinition, ...]:
        return tuple(
            self._relationship_mappings.get(
                schema_name,
                [],
            )
        )

    def list_relationship_mappings(
        self,
    ) -> tuple[RelationshipMappingDefinition, ...]:
        """
        Return all registered relationship mappings.
        """

        mappings: list[RelationshipMappingDefinition] = []

        for schema_mappings in self._relationship_mappings.values():
            mappings.extend(schema_mappings)

        return tuple(
            sorted(
                mappings,
                key=lambda mapping: (
                    mapping.source_schema,
                    mapping.relationship.name,
                ),
            )
        )

    def get_relationship(
        self,
        name: str,
    ) -> RelationshipDefinition:

        try:
            return self._relationships[name]

        except KeyError as exc:
            raise ValidationError(f"Unknown relationship '{name}'.") from exc

    def has_relationship(self, name: str) -> bool:
        return name in self._relationships

    def list_relationships(
        self,
    ) -> tuple[RelationshipDefinition, ...]:
        """
        Return all registered relationships in deterministic order.
        """

        return tuple(
            sorted(
                self._relationships.values(),
                key=lambda relationship: relationship.name,
            )
        )

    def get_relationship_mappings(
        self,
    ) -> tuple[RelationshipMappingDefinition, ...]:
        """
        Return all registered relationship mappings.
        """

        mappings: list[RelationshipMappingDefinition] = []

        for schema_mappings in self._relationship_mappings.values():
            mappings.extend(schema_mappings)

        return tuple(mappings)
