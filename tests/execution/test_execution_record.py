from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from foract.execution.execution_record import ExecutionRecord
from foract.execution.execution_status import ExecutionStatus


def test_execution_record_is_immutable() -> None:
    record = ExecutionRecord(
        execution_id="1",
        plugin_id="plugin",
        command="cmd",
        parameters={},
        status=ExecutionStatus.SUCCESS,
        started_at=datetime.now(UTC),
        finished_at=datetime.now(UTC),
        stdout_blob_id="out",
        stderr_blob_id="err",
        metadata={},
    )

    with pytest.raises(FrozenInstanceError):
        record.command = "new"
def test_parameters_are_read_only() -> None:
    record = ExecutionRecord(
        execution_id="1",
        plugin_id="plugin",
        command="cmd",
        parameters={"pid": 1},
        status=ExecutionStatus.SUCCESS,
        started_at=datetime.now(UTC),
        finished_at=datetime.now(UTC),
        stdout_blob_id="out",
        stderr_blob_id="err",
        metadata={},
    )

    with pytest.raises(TypeError):
        record.parameters["pid"] = 2
