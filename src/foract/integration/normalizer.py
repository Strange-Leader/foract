from __future__ import annotations

from typing import Any


class Normalizer:
    """
    Converts plugin-specific field names into FORACT schema field names.
    """

    def __init__(self) -> None:
        self._mappings: dict[str, dict[str, str]] = {
            "windows.pslist": {
                "PID": "pid",
                "PPID": "ppid",
                "Name": "name",
                "ImageFileName": "name",
                "CreateTime": "create_time",
                "Path": "path",
            }
        }

    def normalize(
        self,
        plugin_id: str,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Normalize plugin output into FORACT schema field names.
        """

        mapping = self._mappings.get(plugin_id)

        if mapping is None:
            raise ValueError(
                f"No normalization mapping registered for " f"'{plugin_id}'."
            )

        normalized_records: list[dict[str, Any]] = []

        for record in records:

            normalized_record = {
                mapping.get(field, field): value for field, value in record.items()
            }

            normalized_records.append(normalized_record)

        return normalized_records
