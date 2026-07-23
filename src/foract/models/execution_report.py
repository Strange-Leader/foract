from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import ClassVar
from uuid import UUID

from foract.enums.artifact import ArtifactType
from foract.enums.schema import ExecutionReportStatus
from foract.models.operational_artifact import OperationalArtifact


@dataclass(frozen=True, slots=True)
class ExecutionReport(OperationalArtifact):
    """
    Immutable summary of an orchestration execution batch.

    An ExecutionReport represents the outcome of executing a single
    execution plan. It references ExecutionRecords by ID rather than
    duplicating execution data.
    """

    artifact_type: ClassVar[ArtifactType] = ArtifactType.EXECUTION_REPORT

    batch_id: UUID
    plan_id: UUID

    status: ExecutionReportStatus
    duration: timedelta
    completed_execution_ids: tuple[UUID, ...] = field(default_factory=tuple)

    failed_execution_ids: tuple[UUID, ...] = field(default_factory=tuple)

    skipped_execution_ids: tuple[UUID, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """
        Validate that execution IDs appear in only one result category.
        """

        completed = set(self.completed_execution_ids)
        failed = set(self.failed_execution_ids)
        skipped = set(self.skipped_execution_ids)

        if completed & failed:
            raise ValueError(
                "Execution IDs cannot appear in both completed " "and failed."
            )

        if completed & skipped:
            raise ValueError(
                "Execution IDs cannot appear in both completed " "and skipped."
            )

        if failed & skipped:
            raise ValueError(
                "Execution IDs cannot appear in both failed " "and skipped."
            )
