from __future__ import annotations

from uuid import UUID

from foract.exceptions.execution import (
    BlobNotFoundError,
    DuplicateBlobError,
)
from foract.storage.blob_store import BlobStore


class InMemoryBlobStore(BlobStore):
    """
    In-memory implementation of BlobStore.

    Intended for testing and development.

    This implementation is append-only. Once a blob has been stored
    under a blob ID, it cannot be modified, overwritten, or deleted.
    """

    def __init__(self) -> None:
        self._blobs: dict[UUID, bytes] = {}

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
            If the blob ID already exists.
        """

        if blob_id in self._blobs:
            raise DuplicateBlobError(f"Blob '{blob_id}' already exists.")

        # Defensive copy to preserve immutability.
        self._blobs[blob_id] = bytes(data)

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

        try:
            return self._blobs[blob_id]

        except KeyError as exc:
            raise BlobNotFoundError(f"Blob '{blob_id}' not found.") from exc
