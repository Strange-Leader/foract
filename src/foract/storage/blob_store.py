from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class BlobStore(ABC):
    """
    Abstract append-only storage for immutable binary blobs.

    BlobStore stores large binary outputs produced during execution
    (for example stdout and stderr).

    Invariants
    ----------
    - Blob IDs are globally unique.
    - Blob contents are immutable once stored.
    - Existing blobs can never be overwritten.
    - Blobs can never be deleted.
    """

    @abstractmethod
    def store(
        self,
        blob_id: UUID,
        data: bytes,
    ) -> None:
        """
        Store a new immutable blob.

        Raises
        ------
        DuplicateBlobError
            If the blob already exists.
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve(
        self,
        blob_id: UUID,
    ) -> bytes:
        """
        Retrieve a previously stored blob.

        Raises
        ------
        BlobNotFoundError
            If the blob does not exist.
        """
        raise NotImplementedError
