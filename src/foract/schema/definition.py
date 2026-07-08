from __future__ import annotations

from pydantic import BaseModel, Field

from foract.schema.field import FieldDefinition


class SchemaDefinition(BaseModel):
    """
    Defines the structure of a FORACT schema.
    """

    name: str
    version: str
    description: str = ""
    fields: list[FieldDefinition] = Field(default_factory=list)
