from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Any, ClassVar
from uuid import UUID

from foract.enums.artifact import ArtifactType
from foract.execution.execution_status import ExecutionStatus
from foract.models.operational_artifact import OperationalArtifact


@dataclass(frozen=True, slots=True)
class ExecutionRecord(OperationalArtifact):
    """
    Immutable record of a completed plugin execution.

    Every ExecutionRecord belongs to exactly one orchestration batch
    and references immutable stdout/stderr blobs stored in the BlobStore.
    """

    artifact_type: ClassVar[ArtifactType] = ArtifactType.EXECUTION_RECORD

    batch_id: UUID

    plugin: str
    capability: str

    status: ExecutionStatus

    started_at: datetime
    completed_at: datetime

    stdout_blob_id: UUID
    stderr_blob_id: UUID

    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Freeze metadata and validate execution timestamps.
        """

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )

        if self.completed_at < self.started_at:
            raise ValueError("completed_at cannot be earlier than started_at.")
