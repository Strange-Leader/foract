from __future__ import annotations

from collections import defaultdict
from uuid import UUID

from foract.enums.artifact import ArtifactType
from foract.exceptions.execution import (
    ArtifactNotFoundError,
    DuplicateArtifactError,
    InvalidArtifactTypeError,
)
from foract.models.execution_record import ExecutionRecord
from foract.models.execution_report import ExecutionReport
from foract.models.operational_artifact import OperationalArtifact
from foract.storage.blob_store import BlobStore


class ExecutionMemory:
    """
    Append-only repository for immutable operational artifacts.
    """

    def __init__(
        self,
        blob_store: BlobStore,
    ) -> None:

        self._blob_store = blob_store

        self._artifacts: dict[
            UUID,
            OperationalArtifact,
        ] = {}

        self._type_index: dict[
            ArtifactType,
            set[UUID],
        ] = defaultdict(set)

        self._investigation_index: dict[
            UUID,
            set[UUID],
        ] = defaultdict(set)

        self._batch_index: dict[
            UUID,
            set[UUID],
        ] = defaultdict(set)

    def store_artifact(
        self,
        artifact: OperationalArtifact,
    ) -> None:

        if artifact.id in self._artifacts:
            raise DuplicateArtifactError(f"Artifact '{artifact.id}' already exists.")

        self._artifacts[artifact.id] = artifact

        self._type_index[artifact.artifact_type].add(artifact.id)

        self._investigation_index[artifact.investigation_id].add(artifact.id)

        if isinstance(
            artifact,
            (
                ExecutionRecord,
                ExecutionReport,
            ),
        ):
            self._batch_index[artifact.batch_id].add(artifact.id)

    def get_artifact(
        self,
        artifact_id: UUID,
    ) -> OperationalArtifact:

        try:
            return self._artifacts[artifact_id]

        except KeyError as exc:
            raise ArtifactNotFoundError(f"Artifact '{artifact_id}' not found.") from exc

    def get_artifacts(
        self,
    ) -> list[OperationalArtifact]:

        return list(self._artifacts.values())

    def get_artifacts_by_type(
        self,
        artifact_type: ArtifactType,
    ) -> list[OperationalArtifact]:
        """
        Return all artifacts of the requested type.
        """

        return [
            self._artifacts[artifact_id]
            for artifact_id in self._type_index[artifact_type]
        ]

    def get_artifacts_by_investigation(
        self,
        investigation_id: UUID,
    ) -> list[OperationalArtifact]:
        """
        Return all artifacts belonging to an investigation.
        """

        return [
            self._artifacts[artifact_id]
            for artifact_id in self._investigation_index[investigation_id]
        ]

    def get_artifacts_by_batch(
        self,
        batch_id: UUID,
    ) -> list[OperationalArtifact]:
        """
        Return all artifacts belonging to an execution batch.
        """

        return [
            self._artifacts[artifact_id] for artifact_id in self._batch_index[batch_id]
        ]

    def get_stdout(
        self,
        execution_id: UUID,
    ) -> bytes:

        artifact = self.get_artifact(execution_id)

        if not isinstance(
            artifact,
            ExecutionRecord,
        ):
            raise InvalidArtifactTypeError("Artifact is not an ExecutionRecord.")

        return self._blob_store.retrieve(artifact.stdout_blob_id)

    def get_stderr(
        self,
        execution_id: UUID,
    ) -> bytes:

        artifact = self.get_artifact(execution_id)

        if not isinstance(
            artifact,
            ExecutionRecord,
        ):
            raise InvalidArtifactTypeError("Artifact is not an ExecutionRecord.")

        return self._blob_store.retrieve(artifact.stderr_blob_id)
