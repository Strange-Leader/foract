from foract.graph.enums import HypothesisStatus, NodeType
from foract.graph.models.hypothesis import HypothesisNode


def test_hypothesis_creation():
    hypothesis = HypothesisNode(
        properties={
            "description": "Process may have executed PowerShell"
        }
    )

    assert hypothesis.type == NodeType.HYPOTHESIS
    assert hypothesis.status == HypothesisStatus.PROPOSED
    assert hypothesis.confidence == 0.0
    assert hypothesis.supporting_evidence == []
    assert hypothesis.contradicting_evidence == []
    assert hypothesis.missing_capabilities == []
    assert hypothesis.updated_at is not None
