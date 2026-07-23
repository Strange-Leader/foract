"""
Identity index used by the Evidence Integration Engine.

The IdentityIndex provides a fast lookup from a semantic identity key
to the corresponding graph node identifier.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from foract.exceptions import ValidationError


class IdentityIndex(ABC):
    """
    Abstract interface for semantic identity lookup.
    """

    @abstractmethod
    def lookup(
        self,
        identity_key: str,
    ) -> UUID | None:
        """
        Return the graph node identifier associated with the identity
        key, or None if the entity does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        identity_key: str,
        node_id: UUID,
    ) -> None:
        """
        Register a new semantic identity.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        identity_key: str,
    ) -> None:
        """
        Remove a semantic identity.
        """
        raise NotImplementedError

    @abstractmethod
    def contains(
        self,
        identity_key: str,
    ) -> bool:
        """
        Return True if the identity exists.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Remove all identities from the index.
        """
        raise NotImplementedError


class MemoryIdentityIndex(IdentityIndex):
    """
    In-memory implementation of the IdentityIndex.

    Used during Phase 3.
    """

    def __init__(self) -> None:
        self._index: dict[str, UUID] = {}

    def lookup(
        self,
        identity_key: str,
    ) -> UUID | None:
        return self._index.get(identity_key)

    def register(
        self,
        identity_key: str,
        node_id: UUID,
    ) -> None:
        if identity_key in self._index:
            raise ValidationError(f"Identity '{identity_key}' is already registered.")

        self._index[identity_key] = node_id

    def remove(
        self,
        identity_key: str,
    ) -> None:
        self._index.pop(identity_key, None)

    def contains(
        self,
        identity_key: str,
    ) -> bool:
        return identity_key in self._index

    def clear(self) -> None:
        self._index.clear()
