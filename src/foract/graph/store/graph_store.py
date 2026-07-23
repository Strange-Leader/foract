from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from foract.graph.models.edge import Edge
from foract.graph.models.node import Node


class GraphStore(ABC):
    """
    Abstract storage interface for the Evidence Graph.

    The GraphStore is responsible only for storing and retrieving
    nodes and edges. It performs no querying, traversal, validation,
    or reasoning.
    """

    # ==========================================================
    # Node Operations
    # ==========================================================

    @abstractmethod
    def add_node(self, node: Node) -> None:
        """Store a node."""
        raise NotImplementedError

    @abstractmethod
    def get_node(self, node_id: UUID) -> Node | None:
        """Retrieve a node by its ID."""
        raise NotImplementedError

    @abstractmethod
    def update_node(self, node: Node) -> None:
        """Replace an existing node."""
        raise NotImplementedError

    @abstractmethod
    def remove_node(self, node_id: UUID) -> None:
        """Remove a node."""
        raise NotImplementedError

    @abstractmethod
    def list_nodes(self) -> list[Node]:
        """Return all stored nodes."""
        raise NotImplementedError

    # ==========================================================
    # Edge Operations
    # ==========================================================

    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        """Store an edge."""
        raise NotImplementedError

    @abstractmethod
    def get_edge(self, edge_id: UUID) -> Edge | None:
        """Retrieve an edge."""
        raise NotImplementedError

    @abstractmethod
    def remove_edge(self, edge_id: UUID) -> None:
        """Remove an edge."""
        raise NotImplementedError

    @abstractmethod
    def list_edges(self) -> list[Edge]:
        """Return all stored edges."""
        raise NotImplementedError

    @abstractmethod
    def outgoing_edge_ids(self, node_id: UUID) -> list[UUID]:
        """Return outgoing edge IDs."""
        raise NotImplementedError

    @abstractmethod
    def incoming_edge_ids(self, node_id: UUID) -> list[UUID]:
        """Return incoming edge IDs."""
        raise NotImplementedError

    # ==========================================================
    # Batch Operations
    # ==========================================================

    @abstractmethod
    def commit(
        self,
        nodes: list[Node],
        edges: list[Edge],
    ) -> None:
        """
        Atomically store a batch of nodes and edges.

        Implementations must validate the entire batch before
        performing any writes. If validation fails, the graph
        must remain unchanged.
        """
        raise NotImplementedError
