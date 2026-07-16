from __future__ import annotations

from typing import Any

from foract.exceptions import ValidationError
from foract.registry import SchemaRegistry
from foract.schema.validator import validate_node


class Validator:
    """
    Validates normalized records against FORACT schemas.

    This class is a thin wrapper around the Phase 0 schema validator.
    """

    def __init__(
        self,
        registry: SchemaRegistry,
    ) -> None:
        self._registry = registry

    def validate(
        self,
        schema_name: str,
        records: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[str]]:
        """
        Validate a batch of normalized records.

        Returns
        -------
        tuple
            (valid_records, validation_failures)
        """

        schema = self._registry.get(schema_name)

        valid_records: list[dict[str, Any]] = []
        failures: list[str] = []

        for record in records:

            try:
                validate_node(
                    schema,
                    record,
                )

                valid_records.append(record)

            except ValidationError as exc:

                failures.append(str(exc))

        return valid_records, failures
