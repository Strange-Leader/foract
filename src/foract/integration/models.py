from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from foract.graph.enums import EdgeType, NodeType
from foract.graph.models.edge import Edge
from foract.graph.models.node import Node
from foract.integration.report import ConflictEntry


@dataclass(frozen=True)
class RelationshipDescriptor:
    """
    Describes a logical relationship between two entities before
    graph node IDs have been resolved.
    """

    edge_type: EdgeType

    target_identity_key: str


@dataclass
class MappedEntity:
    schema_name: str
    node_type: NodeType
    properties: dict[str, Any]
    identity_key: str
    relationships: list[RelationshipDescriptor] = field(default_factory=list)


@dataclass
class ResolutionResult:
    """
    Result produced by the EntityResolver.
    """

    nodes: list[Node] = field(default_factory=list)

    edges: list[Edge] = field(default_factory=list)

    conflicts: list[ConflictEntry] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    identity_map: dict[str, str] = field(default_factory=dict)


@dataclass
class RelationshipBuildResult:
    """
    Result produced by the RelationshipBuilder.
    """

    edges: list[Edge] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)


@dataclass
class MergeResult:
    """
    Result produced by the NodeMerger.
    """

    node: Node

    conflicts: list[ConflictEntry] = field(default_factory=list)
