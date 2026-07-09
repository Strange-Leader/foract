from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from foract.graph.enums import HypothesisStatus, NodeType
from foract.graph.models.node import Node


class HypothesisNode(Node):
    """
    A first-class hypothesis stored in the Evidence Graph.
    """

    type: NodeType = Field(default=NodeType.HYPOTHESIS)

    status: HypothesisStatus = Field(
        default=HypothesisStatus.PROPOSED
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    supporting_evidence: list[str] = Field(default_factory=list)

    contradicting_evidence: list[str] = Field(default_factory=list)

    missing_capabilities: list[str] = Field(default_factory=list)

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
