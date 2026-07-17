from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

ValidationRule = Callable[[Any], bool]


class FieldDefinition(BaseModel):
    """
    Defines a single field within a FORACT schema.
    """

    name: str

    # Python type describing the field.
    # Using Any allows future generic types such as
    # list[UUID], dict[str, Any], etc.
    type: Any

    required: bool = True

    description: str = ""

    enum_values: tuple[Any, ...] | None = None

    validation_rule: ValidationRule | None = None

    identity: bool = False
