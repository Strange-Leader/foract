from __future__ import annotations

from foract.schema.relationship import RelationshipDefinition

SUPPORTS = RelationshipDefinition(
    name="SUPPORTS",
    description="Evidence supports a hypothesis.",
)

CONTRADICTS = RelationshipDefinition(
    name="CONTRADICTS",
    description="Evidence contradicts a hypothesis.",
)

GENERATED_FROM = RelationshipDefinition(
    name="GENERATED_FROM",
    description="Evidence originated from an execution record.",
)

PART_OF_INVESTIGATION = RelationshipDefinition(
    name="PART_OF_INVESTIGATION",
    description="Evidence or hypothesis belongs to an investigation.",
)
PARENT_OF = RelationshipDefinition(
    name="PARENT_OF",
    description="Parent process relationship.",
)
BUILTIN_RELATIONSHIPS = (
    SUPPORTS,
    CONTRADICTS,
    GENERATED_FROM,
    PART_OF_INVESTIGATION,
    PARENT_OF,
)
