from foract.graph.models.node import Node


def test_node_creation():
    node = Node(type="PROCESS", properties={"pid": 100})

    assert node.type == "PROCESS"
    assert node.properties["pid"] == 100
    assert node.id
