from __future__ import annotations

from collections import deque
from typing import Any
from uuid import UUID

from foract.graph.models.node import Node
from foract.graph.store.graph_store import GraphStore


class GraphQueryEngine:
    """
    Read-only query engine for the Evidence Graph.

    The query engine performs generic graph queries and traversal.
    It never modifies the graph and does not contain investigation-
    specific or verification-specific logic.
    """

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ==========================================================
    # Find Queries
    # ==========================================================

    def find_by_schema(
        self,
        schema: str,
    ) -> list[Node]:
        """
        Return all nodes belonging to the specified schema.
        """

        return [
            node
            for node in self._store.list_nodes()
            if node.schema == schema
        ]

    def find_by_property(
        self,
        key: str,
        value: Any,
    ) -> list[Node]:
        """
        Return all nodes whose property matches the given value.
        """

        return [
            node
            for node in self._store.list_nodes()
            if node.properties.get(key) == value
        ]

    # ==========================================================
    # Traversal
    # ==========================================================

    def traverse(
        self,
        node_id: UUID,
        *,
        relationship: str | None = None,
        incoming: bool = True,
        outgoing: bool = True,
    ) -> list[Node]:
        """
        Return all neighbouring nodes.

        If 'relationship' is provided, only edges of that relationship
        type are traversed.
        """

        neighbours: dict[Any, Node] = {}

        if outgoing:
            for edge_id in self._store.outgoing_edge_ids(node_id):
                edge = self._store.get_edge(edge_id)

                if edge is None:
                    continue

                if (
                    relationship is not None
                    and edge.relationship != relationship
                ):
                    continue

                node = self._store.get_node(edge.target)

                if node is not None:
                    neighbours[node.id] = node

        if incoming:
            for edge_id in self._store.incoming_edge_ids(node_id):
                edge = self._store.get_edge(edge_id)

                if edge is None:
                    continue

                if (
                    relationship is not None
                    and edge.relationship != relationship
                ):
                    continue

                node = self._store.get_node(edge.source)

                if node is not None:
                    neighbours[node.id] = node

        return list(neighbours.values())

    def traverse_n_hops(
        self,
        node_id: UUID,
        hops: int,
        *,
        relationship: str | None = None,
    ) -> list[Node]:
        """
        Traverse the graph up to the specified number of hops.
        """

        if hops <= 0:
            return []

        visited: set[UUID] = {node_id}
        discovered: dict[UUID, Node] = {}

        queue = deque([(node_id, 0)])

        while queue:
            current_id, depth = queue.popleft()

            if depth >= hops:
                continue

            for neighbour in self.traverse(
                current_id,
                relationship=relationship,
            ):
                if neighbour.id in visited:
                    continue

                visited.add(neighbour.id)
                discovered[neighbour.id] = neighbour

                queue.append(
                    (
                        neighbour.id,
                        depth + 1,
                    )
                )

        return list(discovered.values())
