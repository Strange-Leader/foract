from __future__ import annotations

from uuid import UUID, uuid4

from foract.graph.models.edge import Edge
from foract.graph.models.node import Node
from foract.graph.store.graph_store import GraphStore
from foract.integration.identity_index import IdentityIndex
from foract.integration.models import (
    MappedEntity,
    ResolutionResult,
    ResolutionStatus,
)
from foract.integration.report import (
    IntegrationReport,
    IntegrationStatus,
)


class GraphPersistenceService:
    """
    Persists semantic entities into the Evidence Graph.

    Responsibilities
    ----------------
    - Allocate UUIDs for new entities.
    - Build graph nodes.
    - Resolve relationship targets.
    - Build graph edges.
    - Atomically commit the graph.
    - Update the IdentityIndex after a successful commit.
    """

    def __init__(
        self,
        graph_store: GraphStore,
        identity_index: IdentityIndex,
    ) -> None:
        self._graph_store = graph_store
        self._identity_index = identity_index

    def persist(
        self,
        execution_id: UUID,
        plugin_id: str,
        entities: list[MappedEntity],
        resolutions: list[ResolutionResult],
        validation_errors: list[str],
    ) -> IntegrationReport:
        """
        Persist a batch of mapped entities.
        """

        if len(entities) != len(resolutions):
            raise ValueError("entities and resolutions must have the same length.")

        #
        # Pass 1
        # Resolve the UUID for every entity.
        #
        resolved_node_ids: dict[str, UUID] = {}

        for entity, result in zip(
            entities,
            resolutions,
            strict=True,
        ):
            if result.status is ResolutionStatus.EXISTING:
                if result.existing_node_id is None:
                    raise ValueError("Existing entity is missing node identifier.")

                resolved_node_ids[entity.identity_key] = result.existing_node_id

            else:
                resolved_node_ids[entity.identity_key] = uuid4()

        #
        # Pass 2
        # Build only NEW nodes.
        #
        nodes: list[Node] = []

        for entity, result in zip(
            entities,
            resolutions,
            strict=True,
        ):
            if result.status is ResolutionStatus.EXISTING:
                continue

            node = Node(
                id=resolved_node_ids[entity.identity_key],
                schema=entity.schema,
                properties=dict(entity.properties),
            )

            nodes.append(node)

        #
        # Pass 3
        # Build edges.
        #
        edges: list[Edge] = []

        for entity in entities:

            source_id = resolved_node_ids[entity.identity_key]

            for relationship in entity.relationships:

                target_id = resolved_node_ids.get(
                    relationship.target_identity_key,
                )

                if target_id is None:
                    target_id = self._identity_index.lookup(
                        relationship.target_identity_key,
                    )

                if target_id is None:
                    raise ValueError(
                        "Unable to resolve relationship target "
                        f"'{relationship.target_identity_key}'."
                    )

                edge = Edge(
                    source=source_id,
                    target=target_id,
                    relationship=relationship.relationship,
                )

                edges.append(edge)

        #
        # Pass 4
        # Atomically persist the graph.
        #
        self._graph_store.commit(
            nodes,
            edges,
        )

        #
        # Pass 5
        # Register newly created semantic identities.
        #
        for entity, result in zip(
            entities,
            resolutions,
            strict=True,
        ):
            if result.status is ResolutionStatus.NEW:
                self._identity_index.register(
                    entity.identity_key,
                    resolved_node_ids[entity.identity_key],
                )

        duplicate_count = sum(
            1 for result in resolutions if result.status is ResolutionStatus.EXISTING
        )

        status = (
            IntegrationStatus.PARTIAL_SUCCESS
            if validation_errors
            else IntegrationStatus.SUCCESS
        )

        return IntegrationReport(
            execution_id=execution_id,
            plugin_id=plugin_id,
            status=status,
            processed_artifacts=len(entities),
            integrated_nodes=len(nodes),
            integrated_edges=len(edges),
            duplicate_artifacts=duplicate_count,
            validation_failures=tuple(validation_errors),
        )
