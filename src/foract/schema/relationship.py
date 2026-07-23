from __future__ import annotations

from pydantic import BaseModel


class RelationshipDefinition(BaseModel):
    """
    Defines a relationship type within the FORACT ontology.

    Relationship definitions describe the semantic meaning of
    graph relationships.

    They do not define graph behavior, cardinality,
    integrity constraints, or runtime validation.
    """

    name: str

    description: str = ""
