from foract.graph.enums import (
    EdgeType,
    HypothesisStatus,
    NodeType,
)
from foract.graph.models.edge import Edge
from foract.graph.models.hypothesis import HypothesisNode
from foract.graph.models.node import Node
from foract.graph.query.query_engine import GraphQueryEngine
from foract.graph.store.memory_graph_store import MemoryGraphStore


def test_find_by_property():
    store = MemoryGraphStore()

    process = Node(
        type=NodeType.PROCESS,
        properties={"pid": 1234},
    )

    file = Node(
        type=NodeType.FILE,
        properties={},
    )

    store.add_node(process)
    store.add_node(file)

    engine = GraphQueryEngine(store)

    result = engine.find_by_property("pid", 1234)

    assert result == [process]

def test_find_by_type():
    store = MemoryGraphStore()

    process = Node(
        type=NodeType.PROCESS,
        properties={},
    )

    file = Node(
        type=NodeType.FILE,
        properties={},
    )

    store.add_node(process)
    store.add_node(file)

    engine = GraphQueryEngine(store)

    result = engine.find_by_type(NodeType.PROCESS)

    assert result == [process]



def test_find_hypotheses_by_status():
    store = MemoryGraphStore()

    hypothesis = HypothesisNode(
        status=HypothesisStatus.ACTIVE,
        confidence=0.8,
        properties={},
    )

    store.add_node(hypothesis)

    engine = GraphQueryEngine(store)

    result = engine.find_hypotheses(HypothesisStatus.ACTIVE)

    assert result == [hypothesis]



def test_find_all_hypotheses():
    store = MemoryGraphStore()

    h1 = HypothesisNode(
        status=HypothesisStatus.ACTIVE,
        properties={},
    )

    h2 = HypothesisNode(
        status=HypothesisStatus.PROPOSED,
        properties={},
    )

    store.add_node(h1)
    store.add_node(h2)

    engine = GraphQueryEngine(store)

    result = engine.find_hypotheses()

    assert len(result) == 2
    assert h1 in result
    assert h2 in result


def test_relationship_traversal():
    store = MemoryGraphStore()

    process = Node(type=NodeType.PROCESS, properties={})
    file = Node(type=NodeType.FILE, properties={})

    store.add_node(process)
    store.add_node(file)

    edge = Edge(
        source=process.id,
        target=file.id,
        type=EdgeType.OPENED,
    )

    store.add_edge(edge)

    engine = GraphQueryEngine(store)

    result = engine.traverse_relationships(process.id)

    assert result == [file]

def test_two_hop_traversal():
    store = MemoryGraphStore()

    a = Node(type=NodeType.PROCESS, properties={})
    b = Node(type=NodeType.FILE, properties={})
    c = Node(type=NodeType.SOCKET, properties={})

    store.add_node(a)
    store.add_node(b)
    store.add_node(c)

    store.add_edge(
        Edge(
            source=a.id,
            target=b.id,
            type=EdgeType.OPENED,
        )
    )

    store.add_edge(
        Edge(
            source=b.id,
            target=c.id,
            type=EdgeType.CONNECTED_TO,
        )
    )

    engine = GraphQueryEngine(store)

    result = engine.traverse_two_hops(a.id)

    assert b in result
    assert c in result

def test_traverse_provenance():
    store = MemoryGraphStore()

    n1 = Node(
        type=NodeType.PROCESS,
        properties={
            "provenance": "plugin:pslist"
        },
    )

    n2 = Node(
        type=NodeType.FILE,
        properties={
            "provenance": "plugin:pslist"
        },
    )

    n3 = Node(
        type=NodeType.SOCKET,
        properties={
            "provenance": "plugin:netscan"
        },
    )

    store.add_node(n1)
    store.add_node(n2)
    store.add_node(n3)

    engine = GraphQueryEngine(store)

    result = engine.traverse_provenance(n1.id)

    assert result == [n2]
