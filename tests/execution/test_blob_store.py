import pytest

from foract.storage.in_memory_blob_store import InMemoryBlobStore


def test_store_and_retrieve_blob() -> None:
    store = InMemoryBlobStore()

    store.store("blob-1", b"hello")

    assert store.retrieve("blob-1") == b"hello"


def test_duplicate_blob_id_raises() -> None:
    store = InMemoryBlobStore()

    store.store("blob-1", b"hello")

    with pytest.raises(ValueError):
        store.store("blob-1", b"world")


def test_missing_blob_raises() -> None:
    store = InMemoryBlobStore()

    with pytest.raises(KeyError):
        store.retrieve("missing")
