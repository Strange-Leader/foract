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

    @property
    def identity_fields(self) -> list[FieldDefinition]:
        """
        Return all fields that participate in the semantic identity.
        """

        return [field for field in self.fields if field.identity]
