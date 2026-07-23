from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from foract.enums.artifact import ArtifactType
from foract.enums.schema import (
    ExecutionReportStatus,
    VerificationResult,
)
from foract.execution.execution_status import ExecutionStatus
from foract.models.execution_record import ExecutionRecord

# ==========================================================
# ArtifactType
# ==========================================================


def test_artifact_type_values() -> None:
    assert ArtifactType.EXECUTION_RECORD.value == "execution_record"

    assert ArtifactType.EXECUTION_REPORT.value == "execution_report"

    assert ArtifactType.VERIFICATION_REPORT.value == "verification_report"


# ==========================================================
# ExecutionRecord
# ==========================================================


def test_execution_record_creation() -> None:
    now = datetime.now(UTC)

    record = ExecutionRecord(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        batch_id=uuid4(),
        plugin="pslist",
        capability="process_listing",
        status=ExecutionStatus.SUCCESS,
        started_at=now,
        completed_at=now,
        stdout_blob_id=uuid4(),
        stderr_blob_id=uuid4(),
    )

    assert record.artifact_type == ArtifactType.EXECUTION_RECORD

    assert record.plugin == "pslist"

    assert record.capability == "process_listing"

    assert record.status == ExecutionStatus.SUCCESS


def test_execution_record_metadata_defaults() -> None:
    now = datetime.now(UTC)

    record = ExecutionRecord(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        batch_id=uuid4(),
        plugin="pslist",
        capability="process_listing",
        status=ExecutionStatus.SUCCESS,
        started_at=now,
        completed_at=now,
        stdout_blob_id=uuid4(),
        stderr_blob_id=uuid4(),
    )

    assert dict(record.metadata) == {}


def test_execution_record_metadata_is_immutable() -> None:
    now = datetime.now(UTC)

    record = ExecutionRecord(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        batch_id=uuid4(),
        plugin="pslist",
        capability="process_listing",
        status=ExecutionStatus.SUCCESS,
        started_at=now,
        completed_at=now,
        stdout_blob_id=uuid4(),
        stderr_blob_id=uuid4(),
        metadata={
            "profile": "Win10",
        },
    )

    with pytest.raises(TypeError):
        record.metadata["new"] = "value"


def test_execution_record_invalid_timestamps() -> None:
    start = datetime.now(UTC)

    end = start - timedelta(
        seconds=1,
    )

    with pytest.raises(ValueError):
        ExecutionRecord(
            id=uuid4(),
            investigation_id=uuid4(),
            created_at=start,
            batch_id=uuid4(),
            plugin="pslist",
            capability="process_listing",
            status=ExecutionStatus.SUCCESS,
            started_at=start,
            completed_at=end,
            stdout_blob_id=uuid4(),
            stderr_blob_id=uuid4(),
        )


from foract.exceptions.execution import (
    BlobNotFoundError,
    DuplicateBlobError,
)
from foract.storage.in_memory_blob_store import (
    InMemoryBlobStore,
)

# ==========================================================
# Blob Store
# ==========================================================


def test_store_blob() -> None:
    store = InMemoryBlobStore()

    blob_id = uuid4()

    data = b"hello world"

    store.store(
        blob_id,
        data,
    )

    assert store.retrieve(blob_id) == data


def test_duplicate_blob() -> None:
    store = InMemoryBlobStore()

    blob_id = uuid4()

    store.store(
        blob_id,
        b"abc",
    )

    with pytest.raises(DuplicateBlobError):
        store.store(
            blob_id,
            b"xyz",
        )


def test_unknown_blob() -> None:
    store = InMemoryBlobStore()

    with pytest.raises(BlobNotFoundError):
        store.retrieve(
            uuid4(),
        )


def test_blob_is_immutable() -> None:
    store = InMemoryBlobStore()

    blob_id = uuid4()

    original = bytearray(b"abcdef")

    store.store(
        blob_id,
        original,
    )

    #
    # Mutate original buffer.
    #
    original[0] = ord("Z")

    assert store.retrieve(blob_id) == b"abcdef"


def test_store_multiple_blobs() -> None:
    store = InMemoryBlobStore()

    first = uuid4()
    second = uuid4()

    store.store(
        first,
        b"one",
    )

    store.store(
        second,
        b"two",
    )

    assert store.retrieve(first) == b"one"

    assert store.retrieve(second) == b"two"


def test_empty_blob() -> None:
    store = InMemoryBlobStore()

    blob_id = uuid4()

    store.store(
        blob_id,
        b"",
    )

    assert store.retrieve(blob_id) == b""


from foract.models.execution_report import ExecutionReport
from foract.models.verification_report import (
    VerificationReport,
)

# ==========================================================
# ExecutionReport
# ==========================================================


def test_execution_report_creation() -> None:
    now = datetime.now(UTC)

    report = ExecutionReport(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        batch_id=uuid4(),
        plan_id=uuid4(),
        status=ExecutionReportStatus.SUCCESS,
        duration=timedelta(seconds=10),
    )

    assert report.artifact_type == ArtifactType.EXECUTION_REPORT

    assert report.completed_execution_ids == ()

    assert report.failed_execution_ids == ()

    assert report.skipped_execution_ids == ()


def test_execution_report_duplicate_completed_failed() -> None:
    execution_id = uuid4()

    with pytest.raises(ValueError):
        ExecutionReport(
            id=uuid4(),
            investigation_id=uuid4(),
            created_at=datetime.now(UTC),
            batch_id=uuid4(),
            plan_id=uuid4(),
            status=ExecutionReportStatus.SUCCESS,
            duration=timedelta(seconds=1),
            completed_execution_ids=(execution_id,),
            failed_execution_ids=(execution_id,),
        )


def test_execution_report_duplicate_completed_skipped() -> None:
    execution_id = uuid4()

    with pytest.raises(ValueError):
        ExecutionReport(
            id=uuid4(),
            investigation_id=uuid4(),
            created_at=datetime.now(UTC),
            batch_id=uuid4(),
            plan_id=uuid4(),
            status=ExecutionReportStatus.SUCCESS,
            duration=timedelta(seconds=1),
            completed_execution_ids=(execution_id,),
            skipped_execution_ids=(execution_id,),
        )


def test_execution_report_duplicate_failed_skipped() -> None:
    execution_id = uuid4()

    with pytest.raises(ValueError):
        ExecutionReport(
            id=uuid4(),
            investigation_id=uuid4(),
            created_at=datetime.now(UTC),
            batch_id=uuid4(),
            plan_id=uuid4(),
            status=ExecutionReportStatus.SUCCESS,
            duration=timedelta(seconds=1),
            failed_execution_ids=(execution_id,),
            skipped_execution_ids=(execution_id,),
        )


# ==========================================================
# VerificationReport
# ==========================================================


def test_verification_report_creation() -> None:
    now = datetime.now(UTC)

    report = VerificationReport(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        hypothesis_id=uuid4(),
        assessment=VerificationResult.SUPPORTED,
        confidence_before=0.5,
        confidence_after=0.8,
        timestamp=now,
    )

    assert report.artifact_type == ArtifactType.VERIFICATION_REPORT

    assert report.supporting_evidence_ids == ()

    assert report.contradicting_evidence_ids == ()


@pytest.mark.parametrize(
    "before,after",
    [
        (-0.1, 0.5),
        (0.5, -0.1),
        (1.1, 0.5),
        (0.5, 1.1),
    ],
)
def test_verification_report_invalid_confidence(
    before: float,
    after: float,
) -> None:
    with pytest.raises(ValueError):
        VerificationReport(
            id=uuid4(),
            investigation_id=uuid4(),
            created_at=datetime.now(UTC),
            hypothesis_id=uuid4(),
            assessment=VerificationResult.SUPPORTED,
            confidence_before=before,
            confidence_after=after,
            timestamp=datetime.now(UTC),
        )


def test_verification_report_duplicate_evidence() -> None:
    evidence = uuid4()

    with pytest.raises(ValueError):
        VerificationReport(
            id=uuid4(),
            investigation_id=uuid4(),
            created_at=datetime.now(UTC),
            hypothesis_id=uuid4(),
            assessment=VerificationResult.SUPPORTED,
            confidence_before=0.2,
            confidence_after=0.8,
            timestamp=datetime.now(UTC),
            supporting_evidence_ids=(evidence,),
            contradicting_evidence_ids=(evidence,),
        )


from foract.exceptions.execution import (
    ArtifactNotFoundError,
    DuplicateArtifactError,
    InvalidArtifactTypeError,
)
from foract.execution.execution_memory import ExecutionMemory

# ==========================================================
# ExecutionMemory
# ==========================================================


def make_execution_record() -> ExecutionRecord:
    now = datetime.now(UTC)

    return ExecutionRecord(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        batch_id=uuid4(),
        plugin="pslist",
        capability="process_listing",
        status=ExecutionStatus.SUCCESS,
        started_at=now,
        completed_at=now,
        stdout_blob_id=uuid4(),
        stderr_blob_id=uuid4(),
    )


def test_store_artifact() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = make_execution_record()

    memory.store_artifact(record)

    assert memory.get_artifact(record.id) == record


def test_duplicate_artifact() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = make_execution_record()

    memory.store_artifact(record)

    with pytest.raises(DuplicateArtifactError):
        memory.store_artifact(record)


def test_get_unknown_artifact() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    with pytest.raises(ArtifactNotFoundError):
        memory.get_artifact(uuid4())


def test_get_all_artifacts() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    r1 = make_execution_record()
    r2 = make_execution_record()

    memory.store_artifact(r1)
    memory.store_artifact(r2)

    artifacts = memory.get_artifacts()

    assert len(artifacts) == 2

    assert r1 in artifacts
    assert r2 in artifacts


def test_get_artifacts_by_type() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = make_execution_record()

    memory.store_artifact(record)

    result = memory.get_artifacts_by_type(
        ArtifactType.EXECUTION_RECORD,
    )

    assert result == [record]


def test_get_artifacts_by_investigation() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = make_execution_record()

    memory.store_artifact(record)

    result = memory.get_artifacts_by_investigation(
        record.investigation_id,
    )

    assert result == [record]


def test_get_artifacts_by_batch() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = make_execution_record()

    memory.store_artifact(record)

    result = memory.get_artifacts_by_batch(
        record.batch_id,
    )

    assert result == [record]


def test_get_stdout() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = make_execution_record()

    stdout = b"stdout"

    blob_store.store(
        record.stdout_blob_id,
        stdout,
    )

    blob_store.store(
        record.stderr_blob_id,
        b"",
    )

    memory.store_artifact(record)

    assert memory.get_stdout(record.id) == stdout


def test_get_stderr() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = make_execution_record()

    stderr = b"stderr"

    blob_store.store(
        record.stdout_blob_id,
        b"",
    )

    blob_store.store(
        record.stderr_blob_id,
        stderr,
    )

    memory.store_artifact(record)

    assert memory.get_stderr(record.id) == stderr


def test_get_stdout_invalid_artifact() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    now = datetime.now(UTC)

    report = ExecutionReport(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        batch_id=uuid4(),
        plan_id=uuid4(),
        status=ExecutionReportStatus.SUCCESS,
        duration=timedelta(seconds=1),
    )

    memory.store_artifact(report)

    with pytest.raises(
        InvalidArtifactTypeError,
    ):
        memory.get_stdout(report.id)


def test_get_stderr_invalid_artifact() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    now = datetime.now(UTC)

    report = ExecutionReport(
        id=uuid4(),
        investigation_id=uuid4(),
        created_at=now,
        batch_id=uuid4(),
        plan_id=uuid4(),
        status=ExecutionReportStatus.SUCCESS,
        duration=timedelta(seconds=1),
    )

    memory.store_artifact(report)

    with pytest.raises(
        InvalidArtifactTypeError,
    ):
        memory.get_stderr(report.id)


def test_unknown_type_returns_empty() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    assert (
        memory.get_artifacts_by_type(
            ArtifactType.EXECUTION_RECORD,
        )
        == []
    )


def test_unknown_batch_returns_empty() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    assert (
        memory.get_artifacts_by_batch(
            uuid4(),
        )
        == []
    )


def test_unknown_investigation_returns_empty() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    assert (
        memory.get_artifacts_by_investigation(
            uuid4(),
        )
        == []
    )
