from __future__ import annotations

from pydantic import BaseModel

from foract.schema.relationship import RelationshipDefinition


class RelationshipMappingDefinition(BaseModel):
    """
    Defines how a semantic relationship is derived from an entity.

    Relationship mappings are consumed by the Evidence Integration
    pipeline. They describe how relationships are inferred from
    schema fields and do not define graph behavior or validation.
    """

    relationship: RelationshipDefinition

    source_schema: str

    target_schema: str

    source_field: str

    target_field: str
