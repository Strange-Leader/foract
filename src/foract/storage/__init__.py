"""
Storage abstractions used by FORACT.
"""

from foract.storage.blob_store import BlobStore
from foract.storage.in_memory_blob_store import InMemoryBlobStore

__all__ = [
    "BlobStore",
    "InMemoryBlobStore",
]
