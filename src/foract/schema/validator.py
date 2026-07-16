from __future__ import annotations

from typing import Any

from foract.exceptions import ValidationError
from foract.schema.definition import SchemaDefinition


def validate_node(
    schema: SchemaDefinition,
    node: dict[str, Any],
) -> bool:
    """
    Validate a node against a schema.

    Validation checks:
        - Required fields
        - Field types
        - Enum constraints
        - Custom validation rules
        - Identity fields are present
    """

    for field in schema.fields:

        # ----------------------------
        # Required fields
        # ----------------------------
        if field.required and field.name not in node:
            raise ValidationError(f"Missing required field: '{field.name}'.")

        if field.name not in node:
            continue

        value = node[field.name]

        # ----------------------------
        # Type validation
        # ----------------------------
        if not isinstance(value, field.field_type):
            raise ValidationError(
                f"Field '{field.name}' expected "
                f"{field.field_type.__name__}, "
                f"got {type(value).__name__}."
            )

        # ----------------------------
        # Enum validation
        # ----------------------------
        if field.enum_values is not None and value not in field.enum_values:
            raise ValidationError(
                f"Field '{field.name}' must be one of " f"{field.enum_values}."
            )

        # ----------------------------
        # Custom validator
        # ----------------------------
        if field.validation_rule is not None and not field.validation_rule(value):
            raise ValidationError(f"Validation failed for field " f"'{field.name}'.")

    # --------------------------------
    # Identity fields
    # --------------------------------
    for field in schema.identity_fields:

        if field.name not in node:
            raise ValidationError(f"Missing identity field: " f"'{field.name}'.")

    return True
