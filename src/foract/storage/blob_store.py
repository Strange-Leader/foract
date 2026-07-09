from __future__ import annotations

from abc import ABC, abstractmethod


class BlobStore(ABC):
    """
    Abstract storage for immutable binary blobs.
    """

    @abstractmethod
    def store(self, blob_id: str, data: bytes) -> None:
        """
        Store a blob.

        Raises:
            ValueError:
                If the blob_id already exists.
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, blob_id: str) -> bytes:
        """
        Retrieve a previously stored blob.

        Raises:
            KeyError:
                If the blob does not exist.
        """
        raise NotImplementedError
