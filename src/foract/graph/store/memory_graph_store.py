from __future__ import annotations

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
    In-memory implementation of GraphStore.

    Stores nodes and edges in dictionaries while maintaining
    adjacency indexes for efficient graph traversal.

    NOTE:
        This class is intentionally "dumb". It performs storage
        operations only. All querying and traversal belong in the
        GraphQueryEngine.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, Edge] = {}

        # node_id -> edge_ids
        self._outgoing: dict[str, set[str]] = {}
        self._incoming: dict[str, set[str]] = {}

    # ==========================================================
    # Node Operations
    # ==========================================================

    def add_node(self, node: Node) -> None:
        if node.id in self._nodes:
            raise DuplicateNodeError(f"Node '{node.id}' already exists.")

        self._nodes[node.id] = node

        # Initialize adjacency sets
        self._outgoing[node.id] = set()
        self._incoming[node.id] = set()

    def get_node(self, node_id: str) -> Node | None:
        return self._nodes.get(node_id)

    def remove_node(self, node_id: str) -> None:
        if node_id not in self._nodes:
            raise NodeNotFoundError(f"Node '{node_id}' does not exist.")

        #
        # Remove all outgoing edges first
        #
        for edge_id in list(self._outgoing[node_id]):
            self.remove_edge(edge_id)

        #
        # Remove all incoming edges
        #
        for edge_id in list(self._incoming[node_id]):
            self.remove_edge(edge_id)

        #
        # Remove adjacency entries
        #
        self._outgoing.pop(node_id, None)
        self._incoming.pop(node_id, None)

        #
        # Finally remove node
        #
        del self._nodes[node_id]

    def list_nodes(self) -> list[Node]:
        return list(self._nodes.values())

    # ==========================================================
    # Edge Operations
    # ==========================================================

    def add_edge(self, edge: Edge) -> None:
        if edge.id in self._edges:
            raise DuplicateEdgeError(f"Edge '{edge.id}' already exists.")

        if edge.source not in self._nodes:
            raise NodeNotFoundError(f"Source node '{edge.source}' does not exist.")

        if edge.target not in self._nodes:
            raise NodeNotFoundError(f"Target node '{edge.target}' does not exist.")

        self._edges[edge.id] = edge

        self._outgoing[edge.source].add(edge.id)
        self._incoming[edge.target].add(edge.id)

    def get_edge(self, edge_id: str) -> Edge | None:
        return self._edges.get(edge_id)

    def remove_edge(self, edge_id: str) -> None:
        if edge_id not in self._edges:
            raise EdgeNotFoundError(f"Edge '{edge_id}' does not exist.")

        edge = self._edges[edge_id]

        #
        # Remove from adjacency indexes first
        #
        self._outgoing[edge.source].discard(edge_id)
        self._incoming[edge.target].discard(edge_id)

        #
        # Remove edge
        #
        del self._edges[edge_id]

    def list_edges(self) -> list[Edge]:
        return list(self._edges.values())

    def outgoing_edge_ids(self, node_id: str) -> list[str]:
        return list(self._outgoing.get(node_id, set()))

    def incoming_edge_ids(self, node_id: str) -> list[str]:
        return list(self._incoming.get(node_id, set()))

    def update_node(self, node: Node) -> None:
        if node.id not in self._nodes:
            raise NodeNotFoundError(f"Node '{node.id}' does not exist.")

        self._nodes[node.id] = node
