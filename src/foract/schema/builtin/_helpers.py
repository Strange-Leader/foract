from __future__ import annotations

from typing import Any

from foract.schema.field import FieldDefinition


def field(
    name: str,
    type_: Any,
    *,
    required: bool = True,
    identity: bool = False,
    description: str = "",
    enum_values: tuple[Any, ...] | None = None,
    validation_rule=None,
) -> FieldDefinition:
    return FieldDefinition(
        name=name,
        type=type_,
        required=required,
        identity=identity,
        description=description,
        enum_values=enum_values,
        validation_rule=validation_rule,
    )
