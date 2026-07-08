from __future__ import annotations

from pydantic import BaseModel


class FieldDefinition(BaseModel):
    """
    Defines a single field within a schema.

    A field specifies its name, expected Python type,
    whether it is required, and an optional description.
    """

    name: str
    field_type: type
    required: bool = True
    description: str = ""
