from __future__ import annotations

from foract.exceptions import ValidationError
from foract.schema.definition import SchemaDefinition
from foract.schema.relationship import RelationshipDefinition


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

    # ==========================================================
    # Schema registration
    # ==========================================================

    def register_schema(self, schema: SchemaDefinition) -> None:
        if schema.name in self._schemas:
            raise ValidationError(
                f"Schema '{schema.name}' is already registered."
            )

        self._schemas[schema.name] = schema

    def get_schema(self, name: str) -> SchemaDefinition:
        try:
            return self._schemas[name]
        except KeyError as exc:
            raise ValidationError(
                f"Unknown schema '{name}'."
            ) from exc

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
                f"Relationship '{relationship.name}' "
                "is already registered."
            )

        self._relationships[
            relationship.name
        ] = relationship

    def get_relationship(
        self,
        name: str,
    ) -> RelationshipDefinition:

        try:
            return self._relationships[name]

        except KeyError as exc:
            raise ValidationError(
                f"Unknown relationship '{name}'."
            ) from exc

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
