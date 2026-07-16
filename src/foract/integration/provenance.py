from __future__ import annotations

from foract.graph.enums import EdgeType, NodeType
from foract.graph.models.edge import Edge
from foract.graph.models.node import Node


class ProvenanceBuilder:
    """
    Builds provenance relationships between an execution and the
    semantic evidence it produced.
    """

    def build(
        self,
        execution_node: Node,
        evidence_nodes: list[Node],
    ) -> list[Edge]:
        """
        Build provenance edges.

        Each evidence node receives exactly one PRODUCED_BY edge
        pointing to the execution that produced it.
        """

        if execution_node.type != NodeType.EXECUTION_RECORD:
            raise ValueError("execution_node must be an ExecutionRecord node.")

        edges: list[Edge] = []

        for node in evidence_nodes:

            edges.append(
                Edge(
                    source=node.id,
                    target=execution_node.id,
                    type=EdgeType.PRODUCED_BY,
                )
            )

        return edges
