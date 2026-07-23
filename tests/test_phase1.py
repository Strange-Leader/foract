from __future__ import annotations

from uuid import uuid4

import pytest

from foract.exceptions import (
    DuplicateNodeError,
    NodeNotFoundError,
)
from foract.graph.models.node import Node
from foract.graph.store.memory_graph_store import (
    MemoryGraphStore,
)

# ==========================================================
# Node Model
# ==========================================================


def test_node_defaults() -> None:
    node = Node(
        schema="Process",
    )

    assert node.schema == "Process"
    assert node.properties == {}
    assert node.id is not None
    assert node.created_at is not None


def test_node_custom_properties() -> None:
    node = Node(
        schema="Process",
        properties={
            "pid": 1234,
            "name": "cmd.exe",
        },
    )

    assert node.properties["pid"] == 1234
    assert node.properties["name"] == "cmd.exe"


# ==========================================================
# Node Operations
# ==========================================================


def test_add_node() -> None:
    store = MemoryGraphStore()

    node = Node(
        schema="Process",
    )

    store.add_node(node)

    assert store.get_node(node.id) == node


def test_duplicate_node() -> None:
    store = MemoryGraphStore()

    node = Node(
        schema="Process",
    )

    store.add_node(node)

    with pytest.raises(DuplicateNodeError):
        store.add_node(node)


def test_get_unknown_node() -> None:
    store = MemoryGraphStore()

    assert store.get_node(uuid4()) is None


def test_update_node() -> None:
    store = MemoryGraphStore()

    node = Node(
        schema="Process",
        properties={
            "pid": 1,
        },
    )

    store.add_node(node)

    updated = node.model_copy(
        update={
            "properties": {
                "pid": 2,
            }
        }
    )

    store.update_node(updated)

    assert store.get_node(node.id) == updated


def test_update_unknown_node() -> None:
    store = MemoryGraphStore()

    with pytest.raises(NodeNotFoundError):
        store.update_node(
            Node(schema="Process"),
        )


def test_remove_node() -> None:
    store = MemoryGraphStore()

    node = Node(
        schema="Process",
    )

    store.add_node(node)

    store.remove_node(node.id)

    assert store.get_node(node.id) is None


def test_remove_unknown_node() -> None:
    store = MemoryGraphStore()

    with pytest.raises(NodeNotFoundError):
        store.remove_node(uuid4())


def test_list_nodes_empty() -> None:
    store = MemoryGraphStore()

    assert store.list_nodes() == []


def test_list_nodes() -> None:
    store = MemoryGraphStore()

    n1 = Node(schema="Process")
    n2 = Node(schema="File")

    store.add_node(n1)
    store.add_node(n2)

    nodes = store.list_nodes()

    assert len(nodes) == 2

    assert n1 in nodes
    assert n2 in nodes


from foract.exceptions import (
    DuplicateEdgeError,
    EdgeNotFoundError,
)
from foract.graph.models.edge import Edge

# ==========================================================
# Edge Model
# ==========================================================


def test_edge_defaults() -> None:
    source = uuid4()
    target = uuid4()

    edge = Edge(
        source=source,
        target=target,
        relationship="PARENT_OF",
    )

    assert edge.source == source
    assert edge.target == target
    assert edge.relationship == "PARENT_OF"
    assert edge.properties == {}
    assert edge.id is not None
    assert edge.created_at is not None


def test_edge_custom_properties() -> None:
    edge = Edge(
        source=uuid4(),
        target=uuid4(),
        relationship="CONNECTED_TO",
        properties={
            "protocol": "TCP",
        },
    )

    assert edge.properties["protocol"] == "TCP"


# ==========================================================
# Edge Operations
# ==========================================================


def test_add_edge() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    assert store.get_edge(edge.id) == edge


def test_duplicate_edge() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    with pytest.raises(DuplicateEdgeError):
        store.add_edge(edge)


def test_add_edge_unknown_source() -> None:
    store = MemoryGraphStore()

    target = Node(schema="Process")

    store.add_node(target)

    edge = Edge(
        source=uuid4(),
        target=target.id,
        relationship="PARENT_OF",
    )

    with pytest.raises(NodeNotFoundError):
        store.add_edge(edge)


def test_add_edge_unknown_target() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")

    store.add_node(source)

    edge = Edge(
        source=source.id,
        target=uuid4(),
        relationship="PARENT_OF",
    )

    with pytest.raises(NodeNotFoundError):
        store.add_edge(edge)


def test_get_unknown_edge() -> None:
    store = MemoryGraphStore()

    assert store.get_edge(uuid4()) is None


def test_remove_edge() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    store.remove_edge(edge.id)

    assert store.get_edge(edge.id) is None


def test_remove_unknown_edge() -> None:
    store = MemoryGraphStore()

    with pytest.raises(EdgeNotFoundError):
        store.remove_edge(uuid4())


def test_list_edges_empty() -> None:
    store = MemoryGraphStore()

    assert store.list_edges() == []


def test_list_edges() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    edges = store.list_edges()

    assert len(edges) == 1
    assert edge in edges


# ==========================================================
# Adjacency
# ==========================================================


def test_outgoing_edge_ids() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    outgoing = store.outgoing_edge_ids(source.id)

    assert outgoing == [edge.id]


def test_incoming_edge_ids() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    incoming = store.incoming_edge_ids(target.id)

    assert incoming == [edge.id]


def test_remove_edge_updates_adjacency() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    store.remove_edge(edge.id)

    assert store.outgoing_edge_ids(source.id) == []

    assert store.incoming_edge_ids(target.id) == []


def test_remove_node_removes_connected_edges() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    store.remove_node(source.id)

    assert store.get_edge(edge.id) is None

    assert store.incoming_edge_ids(target.id) == []


def test_remove_target_node_removes_connected_edges() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    store.add_node(source)
    store.add_node(target)

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.add_edge(edge)

    store.remove_node(target.id)

    assert store.get_edge(edge.id) is None

    assert store.outgoing_edge_ids(source.id) == []


# ==========================================================
# Batch Commit
# ==========================================================


def test_commit_nodes_only() -> None:
    store = MemoryGraphStore()

    n1 = Node(schema="Process")
    n2 = Node(schema="File")

    store.commit(
        nodes=[n1, n2],
        edges=[],
    )

    assert store.get_node(n1.id) == n1
    assert store.get_node(n2.id) == n2


def test_commit_nodes_and_edges() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.commit(
        nodes=[source, target],
        edges=[edge],
    )

    assert store.get_node(source.id) == source
    assert store.get_node(target.id) == target
    assert store.get_edge(edge.id) == edge


def test_commit_duplicate_node_ids_in_batch() -> None:
    store = MemoryGraphStore()

    node = Node(schema="Process")

    duplicate = node.model_copy()

    with pytest.raises(DuplicateNodeError):
        store.commit(
            nodes=[node, duplicate],
            edges=[],
        )


def test_commit_duplicate_existing_node() -> None:
    store = MemoryGraphStore()

    node = Node(schema="Process")

    store.add_node(node)

    with pytest.raises(DuplicateNodeError):
        store.commit(
            nodes=[node],
            edges=[],
        )


def test_commit_duplicate_edge_ids_in_batch() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    duplicate = edge.model_copy()

    with pytest.raises(DuplicateEdgeError):
        store.commit(
            nodes=[source, target],
            edges=[edge, duplicate],
        )


def test_commit_duplicate_existing_edge() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.commit(
        nodes=[source, target],
        edges=[edge],
    )

    new_source = Node(schema="Process")
    new_target = Node(schema="Process")

    with pytest.raises(DuplicateEdgeError):
        store.commit(
            nodes=[new_source, new_target],
            edges=[edge],
        )


def test_commit_missing_source_node() -> None:
    store = MemoryGraphStore()

    target = Node(schema="Process")

    edge = Edge(
        source=uuid4(),
        target=target.id,
        relationship="PARENT_OF",
    )

    with pytest.raises(NodeNotFoundError):
        store.commit(
            nodes=[target],
            edges=[edge],
        )


def test_commit_missing_target_node() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")

    edge = Edge(
        source=source.id,
        target=uuid4(),
        relationship="PARENT_OF",
    )

    with pytest.raises(NodeNotFoundError):
        store.commit(
            nodes=[source],
            edges=[edge],
        )


def test_commit_empty_batch() -> None:
    store = MemoryGraphStore()

    store.commit(
        nodes=[],
        edges=[],
    )

    assert store.list_nodes() == []
    assert store.list_edges() == []


from foract.graph.query.query_engine import GraphQueryEngine

# ==========================================================
# Graph Query Engine
# ==========================================================


def test_find_by_schema() -> None:
    store = MemoryGraphStore()

    process = Node(schema="Process")
    file = Node(schema="File")

    store.add_node(process)
    store.add_node(file)

    engine = GraphQueryEngine(store)

    result = engine.find_by_schema("Process")

    assert result == [process]


def test_find_by_schema_unknown() -> None:
    store = MemoryGraphStore()

    engine = GraphQueryEngine(store)

    assert engine.find_by_schema("Unknown") == []


def test_find_by_property() -> None:
    store = MemoryGraphStore()

    p1 = Node(
        schema="Process",
        properties={"pid": 100},
    )

    p2 = Node(
        schema="Process",
        properties={"pid": 200},
    )

    store.add_node(p1)
    store.add_node(p2)

    engine = GraphQueryEngine(store)

    result = engine.find_by_property(
        "pid",
        200,
    )

    assert result == [p2]


def test_find_by_property_unknown() -> None:
    store = MemoryGraphStore()

    node = Node(
        schema="Process",
        properties={"pid": 100},
    )

    store.add_node(node)

    engine = GraphQueryEngine(store)

    assert (
        engine.find_by_property(
            "pid",
            999,
        )
        == []
    )


def test_traverse_outgoing() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.commit(
        nodes=[source, target],
        edges=[edge],
    )

    engine = GraphQueryEngine(store)

    result = engine.traverse(
        source.id,
        incoming=False,
    )

    assert result == [target]


def test_traverse_incoming() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="PARENT_OF",
    )

    store.commit(
        nodes=[source, target],
        edges=[edge],
    )

    engine = GraphQueryEngine(store)

    result = engine.traverse(
        target.id,
        outgoing=False,
    )

    assert result == [source]


def test_traverse_relationship_filter() -> None:
    store = MemoryGraphStore()

    source = Node(schema="Process")
    target = Node(schema="Process")

    edge = Edge(
        source=source.id,
        target=target.id,
        relationship="CONNECTED_TO",
    )

    store.commit(
        nodes=[source, target],
        edges=[edge],
    )

    engine = GraphQueryEngine(store)

    assert (
        engine.traverse(
            source.id,
            relationship="PARENT_OF",
            incoming=False,
        )
        == []
    )


def test_traverse_two_hops() -> None:
    store = MemoryGraphStore()

    a = Node(schema="Process")
    b = Node(schema="Process")
    c = Node(schema="Process")

    store.commit(
        nodes=[a, b, c],
        edges=[
            Edge(
                source=a.id,
                target=b.id,
                relationship="PARENT_OF",
            ),
            Edge(
                source=b.id,
                target=c.id,
                relationship="PARENT_OF",
            ),
        ],
    )

    engine = GraphQueryEngine(store)

    result = engine.traverse_n_hops(
        a.id,
        hops=2,
    )

    assert len(result) == 2

    assert b in result
    assert c in result


def test_traverse_zero_hops() -> None:
    store = MemoryGraphStore()

    node = Node(schema="Process")

    store.add_node(node)

    engine = GraphQueryEngine(store)

    assert (
        engine.traverse_n_hops(
            node.id,
            hops=0,
        )
        == []
    )


def test_traverse_disconnected_graph() -> None:
    store = MemoryGraphStore()

    a = Node(schema="Process")
    b = Node(schema="Process")

    store.add_node(a)
    store.add_node(b)

    engine = GraphQueryEngine(store)

    assert (
        engine.traverse(
            a.id,
        )
        == []
    )
