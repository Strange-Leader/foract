"""
Operational reporting models for the Evidence Integration Engine.

An IntegrationReport summarizes the outcome of a single evidence
integration run. It records processing statistics, validation failures,
parser warnings, and semantic conflicts encountered while ingesting
forensic evidence into the Evidence Graph.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class IntegrationStatus(Enum):
    """
    Overall outcome of an evidence integration run.
    """

    SUCCESS = auto()
    PARTIAL_SUCCESS = auto()
    FAILED = auto()


@dataclass(frozen=True)
class ConflictEntry:
    """
    Records a semantic conflict encountered during entity resolution.

    Conflicts are never resolved during Phase 3.
    They are recorded for future reasoning phases.
    """

    entity_identity_key: str
    field: str
    existing_value: Any
    incoming_value: Any
    execution_id: str


@dataclass
class IntegrationReport:
    """
    Operational summary produced after integrating forensic evidence.
    """

    execution_id: str
    status: IntegrationStatus

    processed_records: int = 0
    integrated_records: int = 0
    rejected_records: int = 0

    parser_warnings: list[str] = field(default_factory=list)
    validation_failures: list[str] = field(default_factory=list)
    conflicts: list[ConflictEntry] = field(default_factory=list)
    integration_warnings: list[str] = field(default_factory=list)
