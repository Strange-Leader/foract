from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ArtifactSource:
    """
    Describes the origin of a parsed artifact.

    Every parsed artifact originates from exactly one completed
    plugin execution.
    """

    execution_id: UUID
    plugin_id: str


@dataclass(frozen=True, slots=True)
class ParsedArtifact:
    """
    Canonical artifact flowing through the Evidence Integration
    pipeline.

    Parsers produce ParsedArtifact objects. Every subsequent stage
    operates on these objects until graph mapping occurs.
    """

    schema: str
    properties: Mapping[str, Any]
    source: ArtifactSource


class ResolutionStatus(StrEnum):
    NEW = "new"
    EXISTING = "existing"


@dataclass(frozen=True, slots=True)
class ResolutionResult:
    """
    Result of semantic identity resolution.
    """

    identity_key: str

    existing_node_id: UUID | None

    status: ResolutionStatus


@dataclass(frozen=True, slots=True)
class RelationshipDescriptor:
    """
    Logical relationship before graph node identifiers have been
    resolved.
    """

    relationship: str
    target_identity_key: str


@dataclass(frozen=True, slots=True)
class MappedEntity:
    """
    Semantic entity produced by the Mapper.

    MappedEntity is the semantic representation of an entity before
    persistence. It is not a graph node.

    Graph nodes are created later by the Graph Persistence layer after
    identity resolution has completed.
    """

    schema: str

    properties: Mapping[str, Any]

    identity_key: str

    relationships: tuple[RelationshipDescriptor, ...] = field(default_factory=tuple)
