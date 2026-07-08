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

    Returns:
        True if validation succeeds.

    Raises:
        ValidationError if validation fails.
    """

    for field in schema.fields:

        if field.required and field.name not in node:
            raise ValidationError(
                f"Missing required field: '{field.name}'."
            )

        if field.name not in node:
            continue

        value = node[field.name]

        if not isinstance(value, field.field_type):
            raise ValidationError(
                f"Field '{field.name}' expected "
                f"{field.field_type.__name__}, "
                f"got {type(value).__name__}."
            )

    return True
