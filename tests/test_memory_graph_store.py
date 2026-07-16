import pytest

from foract.exceptions import (
    DuplicateEdgeError,
    DuplicateNodeError,
    EdgeNotFoundError,
    NodeNotFoundError,
)
from foract.graph.enums import EdgeType, NodeType
from foract.graph.models.edge import Edge
from foract.graph.models.node import Node
from foract.graph.store.memory_graph_store import MemoryGraphStore


def test_store_initially_empty():
    store = MemoryGraphStore()

    assert store.list_nodes() == []
    assert store.list_edges() == []


def test_add_and_get_node():
    store = MemoryGraphStore()

    node = Node(
        type=NodeType.PROCESS,
        properties={"pid": 1234},
    )

    store.add_node(node)

    assert store.get_node(node.id) == node


def test_duplicate_node():
    store = MemoryGraphStore()

    node = Node(
        type=NodeType.PROCESS,
        properties={},
    )

    store.add_node(node)

    with pytest.raises(DuplicateNodeError):
        store.add_node(node)


def test_remove_node():
    store = MemoryGraphStore()

    node = Node(
        type=NodeType.FILE,
        properties={},
    )

    store.add_node(node)

    store.remove_node(node.id)

    assert store.get_node(node.id) is None
    assert node.id not in store._outgoing
    assert node.id not in store._incoming


def test_remove_missing_node():
    store = MemoryGraphStore()

    with pytest.raises(NodeNotFoundError):
        store.remove_node("does-not-exist")


def test_add_and_get_edge():
    store = MemoryGraphStore()

    source = Node(type=NodeType.PROCESS, properties={})
    target = Node(type=NodeType.FILE, properties={})

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        type=EdgeType.OPENED,
    )

    store.add_edge(edge)

    assert store.get_edge(edge.id) == edge


def test_duplicate_edge():
    store = MemoryGraphStore()

    source = Node(type=NodeType.PROCESS, properties={})
    target = Node(type=NodeType.FILE, properties={})

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        type=EdgeType.OPENED,
    )

    store.add_edge(edge)

    with pytest.raises(DuplicateEdgeError):
        store.add_edge(edge)


def test_add_edge_missing_source():
    store = MemoryGraphStore()

    target = Node(type=NodeType.FILE, properties={})
    store.add_node(target)

    edge = Edge(
        source="missing",
        target=target.id,
        type=EdgeType.OPENED,
    )

    with pytest.raises(NodeNotFoundError):
        store.add_edge(edge)


def test_add_edge_missing_target():
    store = MemoryGraphStore()

    source = Node(type=NodeType.PROCESS, properties={})
    store.add_node(source)

    edge = Edge(
        source=source.id,
        target="missing",
        type=EdgeType.OPENED,
    )

    with pytest.raises(NodeNotFoundError):
        store.add_edge(edge)


def test_remove_edge():
    store = MemoryGraphStore()

    source = Node(type=NodeType.PROCESS, properties={})
    target = Node(type=NodeType.FILE, properties={})

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        type=EdgeType.OPENED,
    )

    store.add_edge(edge)

    store.remove_edge(edge.id)

    assert store.get_edge(edge.id) is None
    assert edge.id not in store._outgoing[source.id]
    assert edge.id not in store._incoming[target.id]


def test_remove_missing_edge():
    store = MemoryGraphStore()

    with pytest.raises(EdgeNotFoundError):
        store.remove_edge("missing")


def test_remove_node_also_removes_connected_edges():
    store = MemoryGraphStore()

    source = Node(type=NodeType.PROCESS, properties={})
    target = Node(type=NodeType.FILE, properties={})

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        type=EdgeType.OPENED,
    )

    store.add_edge(edge)

    store.remove_node(source.id)

    assert store.get_edge(edge.id) is None
    assert target.id in store._incoming
    assert store._incoming[target.id] == set()
