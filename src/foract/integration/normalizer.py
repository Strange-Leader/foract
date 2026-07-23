from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from foract.integration.models import (
    ParsedArtifact,
)


class Normalizer:
    """
    Canonicalizes parsed artifacts.

    The Normalizer converts parser-specific output into the
    canonical representation expected by the Validator and the
    remaining integration pipeline.

    It performs no validation or graph operations.
    """

    def normalize(
        self,
        artifact: ParsedArtifact,
    ) -> ParsedArtifact:
        """
        Normalize a parsed artifact.
        """

        return ParsedArtifact(
            schema=artifact.schema,
            properties=self._normalize_properties(
                artifact.properties,
            ),
            source=artifact.source,
        )

    def _normalize_properties(
        self,
        properties: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize property names and values.
        """

        normalized: dict[str, Any] = {}

        for key, value in properties.items():
            normalized[key] = self._normalize_value(
                value,
            )

        return normalized

    def _normalize_value(
        self,
        value: Any,
    ) -> Any:
        """
        Normalize a single property value.
        """

        #
        # Strip surrounding whitespace.
        #
        if isinstance(value, str):
            return value.strip()

        #
        # Recursively normalize lists.
        #
        if isinstance(value, list):
            return [self._normalize_value(v) for v in value]

        #
        # Recursively normalize dictionaries.
        #
        if isinstance(value, dict):
            return {k: self._normalize_value(v) for k, v in value.items()}

        return value
