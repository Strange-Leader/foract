from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel


class FieldDefinition(BaseModel):
    """
    Defines a single field within a schema.
    """

    name: str

    field_type: type

    required: bool = True

    description: str = ""

    # Allowed values for this field.
    enum_values: tuple[Any, ...] | None = None

    # Optional custom validation function.
    validation_rule: Callable[[Any], bool] | None = None

    # Whether this field contributes to the entity identity.
    identity: bool = False
