from foract.graph.models.edge import Edge


def test_edge_creation():
    edge = Edge(
        source="process-1",
        target="file-1",
        type="OPENED",
        properties={
            "access": "READ",
        },
    )

    assert edge.source == "process-1"
    assert edge.target == "file-1"
    assert edge.type == "OPENED"
    assert edge.properties["access"] == "READ"
    assert edge.id
    assert edge.created_at is not None
