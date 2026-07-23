from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Edge(BaseModel):
    """
    Generic directed relationship stored in the Evidence Graph.

    The semantic meaning of the relationship is defined by the
    Schema Registry. The graph stores relationships generically
    and performs no interpretation of their meaning.
    """

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)

    source: UUID

    target: UUID

    # Name of the registered relationship
    # (e.g. SUPPORTS, GENERATED_FROM).
    relationship: str

    properties: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
