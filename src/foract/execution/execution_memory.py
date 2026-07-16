from __future__ import annotations

from foract.exceptions.execution import (
    DuplicateExecutionError,
    ExecutionNotFoundError,
)
from foract.execution.execution_record import ExecutionRecord
from foract.integration.report import IntegrationReport, IntegrationStatus
from foract.storage.blob_store import BlobStore


class ExecutionMemory:
    """
    Append-only repository of completed execution records.
    """

    def __init__(self, blob_store: BlobStore) -> None:
        self._blob_store = blob_store
        self._records: dict[str, ExecutionRecord] = {}
        self._reports: dict[str, IntegrationReport] = {}

    def append_execution(self, record: ExecutionRecord) -> None:
        """
        Append a completed execution record.

        Raises:
            DuplicateExecutionError:
                If the execution ID already exists.
        """
        if record.execution_id in self._records:
            raise DuplicateExecutionError(
                f"Execution '{record.execution_id}' already exists."
            )

        self._records[record.execution_id] = record

    def get_execution(self, execution_id: str) -> ExecutionRecord:
        """
        Retrieve an execution by ID.

        Raises:
            ExecutionNotFoundError:
                If the execution does not exist.
        """
        try:
            return self._records[execution_id]
        except KeyError as exc:
            raise ExecutionNotFoundError(
                f"Execution '{execution_id}' not found."
            ) from exc

    def list_executions(self) -> list[ExecutionRecord]:
        """
        Return all execution records.
        """
        return list(self._records.values())

    def find_executions_by_plugin(
        self,
        plugin_id: str,
    ) -> list[ExecutionRecord]:
        """
        Return all executions produced by a plugin.
        """
        return [
            record for record in self._records.values() if record.plugin_id == plugin_id
        ]

    def get_stdout(self, execution_id: str) -> bytes:
        """
        Retrieve stdout for an execution.
        """
        record = self.get_execution(execution_id)
        return self._blob_store.retrieve(record.stdout_blob_id)

    def get_stderr(self, execution_id: str) -> bytes:
        """
        Retrieve stderr for an execution.
        """
        record = self.get_execution(execution_id)
        return self._blob_store.retrieve(record.stderr_blob_id)

    def attach_integration_report(
        self,
        report: IntegrationReport,
    ) -> None:
        """
        Store the IntegrationReport for an execution.
        """

        self._reports[report.execution_id] = report

    def get_integration_report(
        self,
        execution_id: str,
    ) -> IntegrationReport:
        """
        Retrieve the IntegrationReport for an execution.
        """

        try:
            return self._reports[execution_id]

        except KeyError as exc:
            raise ExecutionNotFoundError(
                f"Integration report for " f"'{execution_id}' not found."
            ) from exc

    def find_executions_by_integration_status(
        self,
        status: IntegrationStatus,
    ) -> list[ExecutionRecord]:
        """
        Return executions having the requested
        integration status.
        """

        records: list[ExecutionRecord] = []

        for execution_id, report in self._reports.items():

            if report.status == status:

                records.append(self.get_execution(execution_id))

        return records
