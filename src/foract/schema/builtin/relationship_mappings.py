from __future__ import annotations

from foract.schema.builtin.relationships import PARENT_OF
from foract.schema.relationship_mapping import RelationshipMappingDefinition

PARENT_PROCESS_MAPPING = RelationshipMappingDefinition(
    relationship=PARENT_OF,
    source_schema="Process",
    target_schema="Process",
    source_field="ppid",
    target_field="pid",
)

BUILTIN_RELATIONSHIP_MAPPINGS = (PARENT_PROCESS_MAPPING,)
