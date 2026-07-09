from __future__ import annotations

from foract.storage.blob_store import BlobStore


class InMemoryBlobStore(BlobStore):
    """
    In-memory implementation of BlobStore.

    Intended for testing and development.
    """

    def __init__(self) -> None:
        self._blobs: dict[str, bytes] = {}

    def store(self, blob_id: str, data: bytes) -> None:
        """
        Store a new immutable blob.

        Raises:
            ValueError:
                If the blob ID already exists.
        """
        if blob_id in self._blobs:
            raise ValueError(f"Blob '{blob_id}' already exists.")

        # Store a copy to prevent later mutation by the caller.
        self._blobs[blob_id] = bytes(data)

    def retrieve(self, blob_id: str) -> bytes:
        """
        Retrieve a stored blob.

        Raises:
            KeyError:
                If the blob ID does not exist.
        """
        return self._blobs[blob_id]
