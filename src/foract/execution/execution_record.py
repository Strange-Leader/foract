from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any

from foract.execution.execution_status import ExecutionStatus


@dataclass(frozen=True, slots=True)
class ExecutionRecord:
    """
    Immutable record of a completed plugin execution.
    """

    execution_id: str
    plugin_id: str
    command: str
    parameters: Mapping[str, Any]
    status: ExecutionStatus
    started_at: datetime
    finished_at: datetime
    stdout_blob_id: str
    stderr_blob_id: str
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "parameters",
            MappingProxyType(dict(self.parameters)),
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )
