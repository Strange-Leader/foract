from __future__ import annotations

from pydantic import BaseModel, Field

from foract.enums.schema import SchemaCategory
from foract.schema.field import FieldDefinition


class SchemaDefinition(BaseModel):
    """
    Defines the structural ontology of a FORACT schema.

    A schema describes the fields and validation metadata for either a
    semantic entity stored in the Evidence Graph or an operational artifact
    stored in Execution Memory.
    """

    name: str

    category: SchemaCategory

    version: str

    description: str = ""

    fields: list[FieldDefinition] = Field(default_factory=list)

    @property
    def identity_fields(self) -> list[FieldDefinition]:
        """
        Return all fields participating in the semantic identity of this schema.
        """

        return [field for field in self.fields if field.identity]
