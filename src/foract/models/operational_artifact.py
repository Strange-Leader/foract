from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from foract.enums.artifact import ArtifactType


@dataclass(frozen=True, slots=True)
class OperationalArtifact(ABC):
    """
    Immutable base class for all operational artifacts stored in
    Execution Memory.

    Every operational artifact:

    - Has a globally unique identifier.
    - Belongs to exactly one investigation.
    - Has a fixed artifact type.
    - Is immutable after creation.
    """

    id: UUID
    investigation_id: UUID
    created_at: datetime

    artifact_type: ClassVar[ArtifactType]
