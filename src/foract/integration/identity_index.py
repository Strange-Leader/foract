"""
Identity index used by the Evidence Integration Engine.

The IdentityIndex provides a fast lookup from a semantic identity key
to the corresponding graph node identifier.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class IdentityIndex(ABC):
    """
    Abstract interface for semantic identity lookup.
    """

    @abstractmethod
    def lookup(self, identity_key: str) -> str | None:
        """
        Return the graph node ID associated with the identity key,
        or None if the entity does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        identity_key: str,
        node_id: str,
    ) -> None:
        """
        Register a new identity.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        identity_key: str,
    ) -> None:
        """
        Remove an identity from the index.
        """
        raise NotImplementedError


class MemoryIdentityIndex(IdentityIndex):
    """
    In-memory implementation of the IdentityIndex.

    Used during Phase 3.
    """

    def __init__(self) -> None:
        self._index: dict[str, str] = {}

    def lookup(self, identity_key: str) -> str | None:
        return self._index.get(identity_key)

    def register(
        self,
        identity_key: str,
        node_id: str,
    ) -> None:
        self._index[identity_key] = node_id

    def remove(
        self,
        identity_key: str,
    ) -> None:
        self._index.pop(identity_key, None)
