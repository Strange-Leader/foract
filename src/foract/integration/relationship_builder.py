from __future__ import annotations

from foract.graph.enums import EdgeType
from foract.graph.models.edge import Edge
from foract.integration.models import (
    MappedEntity,
    RelationshipBuildResult,
)


class RelationshipBuilder:
    """
    Builds graph edges from resolved semantic entities.
    """

    def build(
        self,
        entities: list[MappedEntity],
        identity_map: dict[str, str],
    ) -> RelationshipBuildResult:
        """
        Convert logical relationship descriptors into graph edges.
        """

        edges: list[Edge] = []
        warnings: list[str] = []

        for entity in entities:

            source_id = identity_map.get(entity.identity_key)

            if source_id is None:
                continue

            for relationship in entity.relationships:

                target_id = identity_map.get(relationship.target_identity_key)

                if target_id is None:
                    warnings.append(
                        "Relationship target "
                        f"'{relationship.target_identity_key}' "
                        "could not be resolved."
                    )
                    continue

                if relationship.edge_type == EdgeType.PARENT_OF:
                    # Parent ──PARENT_OF──► Child
                    edge = Edge(
                        source=target_id,
                        target=source_id,
                        type=relationship.edge_type,
                    )
                else:
                    edge = Edge(
                        source=source_id,
                        target=target_id,
                        type=relationship.edge_type,
                    )

                edges.append(edge)

        return RelationshipBuildResult(
            edges=edges,
            warnings=warnings,
        )
