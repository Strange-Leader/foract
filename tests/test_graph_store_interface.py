import pytest

from foract.graph.store.graph_store import GraphStore


def test_graph_store_is_abstract():
    with pytest.raises(TypeError):
        GraphStore()
