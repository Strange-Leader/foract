from __future__ import annotations

from uuid import UUID

from foract.exceptions import (
    DuplicateEdgeError,
    DuplicateNodeError,
    EdgeNotFoundError,
    NodeNotFoundError,
)
from foract.graph.models.edge import Edge
from foract.graph.models.node import Node
from foract.graph.store.graph_store import GraphStore


class MemoryGraphStore(GraphStore):
    """
    In-memory implementation of the Evidence Graph.

    This class is responsible only for storing nodes and edges while
    maintaining adjacency indexes for efficient traversal.

    It performs no reasoning, validation, or graph querying.
    """

    def __init__(self) -> None:
        self._nodes: dict[UUID, Node] = {}
        self._edges: dict[UUID, Edge] = {}

        # node_id -> edge_ids
        self._outgoing: dict[UUID, set[UUID]] = {}
        self._incoming: dict[UUID, set[UUID]] = {}

    # ==========================================================
    # Node Operations
    # ==========================================================

    def add_node(self, node: Node) -> None:
        if node.id in self._nodes:
            raise DuplicateNodeError(
                f"Node '{node.id}' already exists."
            )

        self._nodes[node.id] = node

        self._outgoing[node.id] = set()
        self._incoming[node.id] = set()

    def get_node(self, node_id: UUID) -> Node | None:
        return self._nodes.get(node_id)

    def update_node(self, node: Node) -> None:
        if node.id not in self._nodes:
            raise NodeNotFoundError(
                f"Node '{node.id}' does not exist."
            )

        self._nodes[node.id] = node

    def remove_node(self, node_id: UUID) -> None:
        if node_id not in self._nodes:
            raise NodeNotFoundError(
                f"Node '{node_id}' does not exist."
            )

        #
        # Remove outgoing edges
        #
        for edge_id in list(self._outgoing[node_id]):
            self.remove_edge(edge_id)

        #
        # Remove incoming edges
        #
        for edge_id in list(self._incoming[node_id]):
            self.remove_edge(edge_id)

        self._outgoing.pop(node_id, None)
        self._incoming.pop(node_id, None)

        del self._nodes[node_id]

    def list_nodes(self) -> list[Node]:
        return list(self._nodes.values())

    # ==========================================================
    # Edge Operations
    # ==========================================================

    def add_edge(self, edge: Edge) -> None:
        if edge.id in self._edges:
            raise DuplicateEdgeError(
                f"Edge '{edge.id}' already exists."
            )

        if edge.source not in self._nodes:
            raise NodeNotFoundError(
                f"Source node '{edge.source}' does not exist."
            )

        if edge.target not in self._nodes:
            raise NodeNotFoundError(
                f"Target node '{edge.target}' does not exist."
            )

        self._edges[edge.id] = edge

        self._outgoing[edge.source].add(edge.id)
        self._incoming[edge.target].add(edge.id)

    def get_edge(self, edge_id: UUID) -> Edge | None:
        return self._edges.get(edge_id)

    def remove_edge(self, edge_id: UUID) -> None:
        if edge_id not in self._edges:
            raise EdgeNotFoundError(
                f"Edge '{edge_id}' does not exist."
            )

        edge = self._edges[edge_id]

        self._outgoing[edge.source].discard(edge_id)
        self._incoming[edge.target].discard(edge_id)

        del self._edges[edge_id]

    def list_edges(self) -> list[Edge]:
        return list(self._edges.values())

    def outgoing_edge_ids(
        self,
        node_id: UUID,
    ) -> list[UUID]:
        return list(self._outgoing.get(node_id, set()))

    def incoming_edge_ids(
        self,
        node_id: UUID,
    ) -> list[UUID]:
        return list(self._incoming.get(node_id, set()))
