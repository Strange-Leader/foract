from __future__ import annotations

from foract.graph.models.node import Node
from foract.graph.store.graph_store import GraphStore
from foract.integration.identity_index import IdentityIndex
from foract.integration.models import (
    MappedEntity,
    ResolutionResult,
)
from foract.integration.node_merger import NodeMerger
from foract.integration.relationship_builder import (
    RelationshipBuilder,
)


class EntityResolver:
    """
    Resolves semantic entities into graph nodes and relationships.

    Resolution occurs in two passes:

        Pass 1:
            - Resolve identities
            - Create or merge nodes
            - Build identity -> node ID map

        Pass 2:
            - Resolve logical relationships
            - Build graph edges
    """

    def __init__(
        self,
        graph_store: GraphStore,
        identity_index: IdentityIndex,
    ) -> None:
        self._graph_store = graph_store
        self._identity_index = identity_index

        self._node_merger = NodeMerger()
        self._relationship_builder = RelationshipBuilder()

    def resolve(
        self,
        entities: list[MappedEntity],
        execution_id: str,
    ) -> ResolutionResult:
        """
        Resolve a batch of semantic entities into graph nodes and
        graph edges.
        """

        result = ResolutionResult()

        #
        # ==========================================================
        # Pass 1
        # ==========================================================
        #

        for entity in entities:

            node_id = self._identity_index.lookup(entity.identity_key)

            #
            # New entity
            #
            if node_id is None:

                node = Node(
                    type=entity.node_type,
                    properties=dict(entity.properties),
                )

                self._graph_store.add_node(node)

                self._identity_index.register(
                    entity.identity_key,
                    node.id,
                )

                result.nodes.append(node)

                result.identity_map[entity.identity_key] = node.id

                continue

            #
            # Existing entity
            #

            existing = self._graph_store.get_node(node_id)

            if existing is None:
                #
                # Defensive programming.
                #
                continue

            merge_result = self._node_merger.merge(
                existing,
                entity,
                execution_id,
            )

            self._graph_store.update_node(merge_result.node)

            result.nodes.append(merge_result.node)

            result.conflicts.extend(merge_result.conflicts)

            result.identity_map[entity.identity_key] = merge_result.node.id

        #
        # ==========================================================
        # Pass 2
        # ==========================================================
        #

        relationship_result = self._relationship_builder.build(
            entities,
            result.identity_map,
        )

        for edge in relationship_result.edges:
            self._graph_store.add_edge(edge)

        result.edges.extend(relationship_result.edges)

        result.warnings.extend(relationship_result.warnings)

        return result
