from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from foract.enums.artifact import ArtifactType
from foract.enums.schema import VerificationResult
from foract.models.operational_artifact import OperationalArtifact


@dataclass(frozen=True, slots=True)
class VerificationReport(OperationalArtifact):
    """
    Immutable verification result for a hypothesis.

    A VerificationReport captures how the confidence of a hypothesis
    changed after evaluating the available evidence. It references
    supporting and contradicting evidence by ID instead of embedding
    evidence directly.
    """

    artifact_type: ClassVar[ArtifactType] = ArtifactType.VERIFICATION_REPORT
    hypothesis_id: UUID

    assessment: VerificationResult

    confidence_before: float
    confidence_after: float
    timestamp: datetime
    supporting_evidence_ids: tuple[UUID, ...] = field(default_factory=tuple)

    contradicting_evidence_ids: tuple[UUID, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """
        Validate confidence values and referenced evidence.
        """

        for value, name in (
            (self.confidence_before, "confidence_before"),
            (self.confidence_after, "confidence_after"),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0.0 and 1.0.")

        overlap = set(self.supporting_evidence_ids) & set(
            self.contradicting_evidence_ids
        )

        if overlap:
            raise ValueError(
                "Evidence cannot simultaneously support and "
                "contradict the same hypothesis."
            )
