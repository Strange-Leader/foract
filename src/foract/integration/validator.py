from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from foract.exceptions import ValidationError
from foract.integration.models import ParsedArtifact
from foract.schema.definition import SchemaDefinition
from foract.schema.field import FieldDefinition
from foract.schema.registry import SchemaRegistry


class Validator:
    """
    Validates normalized ParsedArtifacts against the Schema Registry.

    The Validator performs structural validation only.
    It never modifies artifacts.
    """

    def __init__(
        self,
        schema_registry: SchemaRegistry,
    ) -> None:
        self._schema_registry = schema_registry

    def validate(
        self,
        artifact: ParsedArtifact,
    ) -> ParsedArtifact:
        """
        Validate a parsed artifact.

        Returns the original artifact if validation succeeds.
        Raises ValidationError otherwise.
        """

        schema = self._schema_registry.get_schema(
            artifact.schema,
        )

        self._validate_fields(
            schema,
            artifact.properties,
        )

        return artifact

    def _validate_fields(
        self,
        schema: SchemaDefinition,
        properties: Mapping[str, Any],
    ) -> None:
        """
        Validate every field defined by the schema.
        """

        for field in schema.fields:
            self._validate_field(
                field,
                properties,
            )

    def _validate_field(
        self,
        field: FieldDefinition,
        properties: Mapping[str, Any],
    ) -> None:
        """
        Validate a single field.
        """

        #
        # Required field
        #
        if field.required and field.name not in properties:
            raise ValidationError(f"Missing required field '{field.name}'.")

        #
        # Optional field omitted.
        #
        if field.name not in properties:
            return

        value = properties[field.name]

        #
        # Type validation.
        #
        if not isinstance(value, field.type):
            raise ValidationError(
                f"Field '{field.name}' " f"must be of type " f"{field.type.__name__}."
            )

        #
        # Enum validation.
        #
        if field.enum_values is not None and value not in field.enum_values:
            raise ValidationError(f"Invalid value for field " f"'{field.name}'.")

        #
        # Custom validation rule.
        #
        if field.validation_rule is not None and not field.validation_rule(value):
            raise ValidationError(f"Validation failed for " f"field '{field.name}'.")
