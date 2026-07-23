from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID


class IntegrationStatus(StrEnum):
    """
    Overall outcome of an evidence integration run.
    """

    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class IntegrationReport:
    """
    Operational summary of a completed evidence integration.

    The report describes the outcome of integrating a single
    ExecutionRecord into the Evidence Graph.
    """

    execution_id: UUID

    plugin_id: str

    status: IntegrationStatus

    processed_artifacts: int = 0

    integrated_nodes: int = 0

    integrated_edges: int = 0

    duplicate_artifacts: int = 0

    validation_failures: tuple[str, ...] = field(default_factory=tuple)

    warnings: tuple[str, ...] = field(default_factory=tuple)
