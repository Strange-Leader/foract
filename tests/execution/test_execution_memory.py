from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from foract.exceptions.execution import (
    DuplicateExecutionError,
    ExecutionNotFoundError,
)
from foract.execution.execution_memory import ExecutionMemory
from foract.execution.execution_record import ExecutionRecord
from foract.execution.execution_status import ExecutionStatus
from foract.storage.in_memory_blob_store import InMemoryBlobStore


def create_record(
    execution_id: str,
    plugin_id: str,
    stdout_blob_id: str,
    stderr_blob_id: str,
) -> ExecutionRecord:
    return ExecutionRecord(
        execution_id=execution_id,
        plugin_id=plugin_id,
        command="test-command",
        parameters={"pid": 1234},
        status=ExecutionStatus.SUCCESS,
        started_at=datetime.now(UTC),
        finished_at=datetime.now(UTC),
        stdout_blob_id=stdout_blob_id,
        stderr_blob_id=stderr_blob_id,
        metadata={"source": "pytest"},
    )


def test_append_and_get_execution() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = create_record(
        "exec-1",
        "plugin-a",
        "stdout-1",
        "stderr-1",
    )

    memory.append_execution(record)

    assert memory.get_execution("exec-1") == record


def test_duplicate_execution_raises() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = create_record(
        "exec-1",
        "plugin-a",
        "stdout-1",
        "stderr-1",
    )

    memory.append_execution(record)

    with pytest.raises(DuplicateExecutionError):
        memory.append_execution(record)


def test_get_missing_execution_raises() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    with pytest.raises(ExecutionNotFoundError):
        memory.get_execution("does-not-exist")


def test_list_executions() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record1 = create_record(
        "exec-1",
        "plugin-a",
        "stdout-1",
        "stderr-1",
    )

    record2 = create_record(
        "exec-2",
        "plugin-b",
        "stdout-2",
        "stderr-2",
    )

    memory.append_execution(record1)
    memory.append_execution(record2)

    executions = memory.list_executions()

    assert len(executions) == 2
    assert record1 in executions
    assert record2 in executions


def test_find_executions_by_plugin() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record1 = create_record(
        "exec-1",
        "plugin-a",
        "stdout-1",
        "stderr-1",
    )

    record2 = create_record(
        "exec-2",
        "plugin-a",
        "stdout-2",
        "stderr-2",
    )

    record3 = create_record(
        "exec-3",
        "plugin-b",
        "stdout-3",
        "stderr-3",
    )

    memory.append_execution(record1)
    memory.append_execution(record2)
    memory.append_execution(record3)

    executions = memory.find_executions_by_plugin("plugin-a")

    assert len(executions) == 2
    assert record1 in executions
    assert record2 in executions
    assert record3 not in executions


def test_get_stdout() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    blob_store.store("stdout-1", b"stdout data")
    blob_store.store("stderr-1", b"stderr data")

    record = create_record(
        "exec-1",
        "plugin-a",
        "stdout-1",
        "stderr-1",
    )

    memory.append_execution(record)

    assert memory.get_stdout("exec-1") == b"stdout data"


def test_get_stderr() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    blob_store.store("stdout-1", b"stdout data")
    blob_store.store("stderr-1", b"stderr data")

    record = create_record(
        "exec-1",
        "plugin-a",
        "stdout-1",
        "stderr-1",
    )

    memory.append_execution(record)

    assert memory.get_stderr("exec-1") == b"stderr data"


def test_retrieved_execution_is_immutable() -> None:
    blob_store = InMemoryBlobStore()
    memory = ExecutionMemory(blob_store)

    record = create_record(
        "exec-1",
        "plugin-a",
        "stdout-1",
        "stderr-1",
    )

    memory.append_execution(record)

    stored = memory.get_execution("exec-1")

    with pytest.raises(FrozenInstanceError):
        stored.command = "modified"
