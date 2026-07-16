from __future__ import annotations

from foract.graph.models.node import Node
from foract.integration.models import MappedEntity, MergeResult
from foract.integration.report import ConflictEntry


class NodeMerger:
    """
    Merges an incoming semantic entity into an existing graph node.

    Existing values are never overwritten.
    Missing properties are added.
    Conflicts are recorded for later reasoning.
    """

    def merge(
        self,
        existing: Node,
        incoming: MappedEntity,
        execution_id: str,
    ) -> MergeResult:
        """
        Merge an incoming entity into an existing node.

        Returns
            -------
            MergeResult
        """

        properties = dict(existing.properties)

        conflicts: list[ConflictEntry] = []

        for key, incoming_value in incoming.properties.items():

            #
            # New property
            #
            if key not in properties:
                properties[key] = incoming_value
                continue

            #
            # Existing property
            #
            existing_value = properties[key]

            if existing_value == incoming_value:
                continue

            #
            # Conflict
            #
            conflicts.append(
                ConflictEntry(
                    entity_identity_key=incoming.identity_key,
                    field=key,
                    existing_value=existing_value,
                    incoming_value=incoming_value,
                    execution_id=execution_id,
                )
            )

        merged = Node(
            id=existing.id,
            type=existing.type,
            properties=properties,
            created_at=existing.created_at,
        )

        return MergeResult(
            node=merged,
            conflicts=conflicts,
        )
