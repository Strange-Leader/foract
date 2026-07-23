from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Node(BaseModel):
    """
    Generic node stored in the Evidence Graph.

    A node represents a semantic entity defined by the Schema Registry.
    The graph stores nodes generically and does not interpret their
    schema-specific meaning.
    """

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)

    # Name of the registered schema (e.g. Process, File, Hypothesis).
    schema: str

    # Schema-defined field values.
    properties: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
