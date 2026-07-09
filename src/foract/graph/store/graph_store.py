from __future__ import annotations

from abc import ABC, abstractmethod

from foract.graph.models.edge import Edge
from foract.graph.models.node import Node


class GraphStore(ABC):
    """
    Abstract interface for graph storage backends.

    The GraphStore is responsible ONLY for storing and retrieving
    nodes and edges. It performs no querying, traversal, or reasoning.
    """

    # ------------------------------------------------------------------
    # Node Operations
    # ------------------------------------------------------------------

    @abstractmethod
    def add_node(self, node: Node) -> None:
        """Store a node."""
        raise NotImplementedError

    @abstractmethod
    def get_node(self, node_id: str) -> Node | None:
        """Retrieve a node by its ID."""
        raise NotImplementedError

    @abstractmethod
    def remove_node(self, node_id: str) -> None:
        """Remove a node by its ID."""
        raise NotImplementedError

    @abstractmethod
    def list_nodes(self) -> list[Node]:
        """Return all stored nodes."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Edge Operations
    # ------------------------------------------------------------------

    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        """Store an edge."""
        raise NotImplementedError

    @abstractmethod
    def get_edge(self, edge_id: str) -> Edge | None:
        """Retrieve an edge by its ID."""
        raise NotImplementedError

    @abstractmethod
    def remove_edge(self, edge_id: str) -> None:
        """Remove an edge by its ID."""
        raise NotImplementedError

    @abstractmethod
    def list_edges(self) -> list[Edge]:
        """Return all stored edges."""
        raise NotImplementedError

    @abstractmethod
    def outgoing_edge_ids(self, node_id: str) -> list[str]:
        """
        Return the IDs of all outgoing edges from the given node.
        """
        raise NotImplementedError


    @abstractmethod
    def incoming_edge_ids(self, node_id: str) -> list[str]:
        """
        Return the IDs of all incoming edges to the given node.
        """
        raise NotImplementedError
