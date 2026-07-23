from __future__ import annotations

from foract.integration.identity_index import IdentityIndex
from foract.integration.models import (
    MappedEntity,
    ResolutionResult,
    ResolutionStatus,
)


class Deduplicator:
    """
    Resolves semantic identities using the IdentityIndex.

    The Deduplicator determines whether a semantic entity already
    exists in the Evidence Graph.

    It performs no graph mutations, UUID allocation, or identity
    registration.
    """

    def __init__(
        self,
        identity_index: IdentityIndex,
    ) -> None:
        self._identity_index = identity_index

    def resolve(
        self,
        entity: MappedEntity,
    ) -> ResolutionResult:
        """
        Resolve the semantic identity of a mapped entity.
        """

        existing_node_id = self._identity_index.lookup(
            entity.identity_key,
        )

        if existing_node_id is not None:
            return ResolutionResult(
                identity_key=entity.identity_key,
                existing_node_id=existing_node_id,
                status=ResolutionStatus.EXISTING,
            )

        return ResolutionResult(
            identity_key=entity.identity_key,
            existing_node_id=None,
            status=ResolutionStatus.NEW,
        )
