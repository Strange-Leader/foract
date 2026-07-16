from __future__ import annotations

from typing import Any

from foract.graph.enums import HypothesisStatus, NodeType
from foract.graph.models.hypothesis import HypothesisNode
from foract.graph.models.node import Node
from foract.graph.store.graph_store import GraphStore


class GraphQueryEngine:
    """
    Read-only query engine for the Evidence Graph.

    The query engine never modifies the graph.
    It only reads from a GraphStore.
    """

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ==========================================================
    # Find Queries
    # ==========================================================

    def find_by_property(
        self,
        key: str,
        value: Any,
    ) -> list[Node]:
        """
        Return every node whose property matches the given value.
        """

        return [
            node
            for node in self._store.list_nodes()
            if node.properties.get(key) == value
        ]

    def find_by_type(
        self,
        node_type: NodeType,
    ) -> list[Node]:
        """
        Return every node of the specified type.
        """

        return [node for node in self._store.list_nodes() if node.type == node_type]

    def find_hypotheses(
        self,
        status: HypothesisStatus | None = None,
    ) -> list[HypothesisNode]:
        """
        Return hypothesis nodes.

        If status is None, return all hypotheses.
        Otherwise, return only hypotheses with the given status.
        """

        hypotheses = [
            node
            for node in self._store.list_nodes()
            if isinstance(node, HypothesisNode)
        ]

        if status is None:
            return hypotheses

        return [hypothesis for hypothesis in hypotheses if hypothesis.status == status]

    def traverse_relationships(
        self,
        node_id: str,
    ) -> list[Node]:
        """
        Return all directly connected neighbour nodes.
        """

        neighbours: list[Node] = []

        #
        # Outgoing
        #
        for edge_id in self._store.outgoing_edge_ids(node_id):
            edge = self._store.get_edge(edge_id)

            if edge is None:
                continue

            node = self._store.get_node(edge.target)

            if node is not None:
                neighbours.append(node)

        #
        # Incoming
        #
        for edge_id in self._store.incoming_edge_ids(node_id):
            edge = self._store.get_edge(edge_id)

            if edge is None:
                continue

            node = self._store.get_node(edge.source)

            if node is not None and node not in neighbours:
                neighbours.append(node)

        return neighbours

    def traverse_two_hops(
        self,
        node_id: str,
    ) -> list[Node]:
        """
        Return every node reachable within two hops.
        """

        visited: dict[str, Node] = {}

        #
        # First hop
        #
        first_hop = self.traverse_relationships(node_id)

        for node in first_hop:
            visited[node.id] = node

        #
        # Second hop
        #
        for node in first_hop:
            second = self.traverse_relationships(node.id)

            for neighbour in second:
                if neighbour.id != node_id:
                    visited[neighbour.id] = neighbour

        return list(visited.values())

    def traverse_provenance(
        self,
        node_id: str,
    ) -> list[Node]:
        """
        Return all nodes sharing the same provenance
        as the specified node.
        """

        node = self._store.get_node(node_id)

        if node is None:
            return []

        provenance = node.properties.get("provenance")

        if provenance is None:
            return []

        result = []

        for candidate in self._store.list_nodes():
            if (
                candidate.id != node.id
                and candidate.properties.get("provenance") == provenance
            ):
                result.append(candidate)

        return result
