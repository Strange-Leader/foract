from __future__ import annotations

from typing import Any

from foract.exceptions import ValidationError
from foract.schema.definition import SchemaDefinition


def validate_data(
    schema: SchemaDefinition,
    data: dict[str, Any],
) -> bool:
    """
    Validate data against a schema.

    Validation checks:
        - Required fields
        - Field types
        - Enum constraints
        - Custom validation rules
        - Identity fields are present
    """

    for field in schema.fields:

        if field.required and field.name not in data:
            raise ValidationError(f"Missing required field: '{field.name}'.")

        if field.name not in data:
            continue

        value = data[field.name]

        # TODO:
        # Extend validation to support parameterized generic types
        # (e.g. list[UUID], dict[str, Any]) if richer field typing
        # is introduced in future phases.

        if not isinstance(value, field.type):
            raise ValidationError(
                f"Field '{field.name}' expected "
                f"{field.type.__name__}, "
                f"got {type(value).__name__}."
            )

        if field.enum_values is not None and value not in field.enum_values:
            raise ValidationError(
                f"Field '{field.name}' must be one of " f"{field.enum_values}."
            )

        if field.validation_rule is not None and not field.validation_rule(value):
            raise ValidationError(f"Validation failed for field '{field.name}'.")

    for field in schema.identity_fields:

        if field.name not in data:
            raise ValidationError(f"Missing identity field: '{field.name}'.")

    return True
