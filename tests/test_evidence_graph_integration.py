from foract.graph import (
    Edge,
    EdgeType,
    GraphQueryEngine,
    MemoryGraphStore,
    Node,
    NodeType,
)


def test_evidence_graph_end_to_end():
    store = MemoryGraphStore()

    process = Node(
        type=NodeType.PROCESS,
        properties={"pid": 100},
    )

    file = Node(
        type=NodeType.FILE,
        properties={"path": "/tmp/test.txt"},
    )

    socket = Node(
        type=NodeType.SOCKET,
        properties={"port": 80},
    )

    store.add_node(process)
    store.add_node(file)
    store.add_node(socket)

    store.add_edge(
        Edge(
            source=process.id,
            target=file.id,
            type=EdgeType.OPENED,
        )
    )

    store.add_edge(
        Edge(
            source=file.id,
            target=socket.id,
            type=EdgeType.CONNECTED_TO,
        )
    )

    engine = GraphQueryEngine(store)

    #
    # Property query
    #
    assert engine.find_by_property("pid", 100) == [process]

    #
    # Type query
    #
    assert engine.find_by_type(NodeType.PROCESS) == [process]

    #
    # One hop
    #
    one_hop = engine.traverse_relationships(process.id)
    assert file in one_hop

    #
    # Two hop
    #
    two_hop = engine.traverse_two_hops(process.id)
    assert socket in two_hop

    #
    # Remove process
    #
    store.remove_node(process.id)

    #
    # Node removed
    #
    assert store.get_node(process.id) is None

    #
    # File still exists
    #
    assert store.get_node(file.id) is not None

    #
    # No incoming edges remain for file
    #
    assert store.incoming_edge_ids(file.id) == []
