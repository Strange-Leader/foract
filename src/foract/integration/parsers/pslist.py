"""
Parser for the Volatility windows.pslist plugin.

Expected input format:
    vol.py -r json windows.pslist
"""

from __future__ import annotations

import json
from typing import Any

from .base import Parser


class WindowsPsListParser(Parser):
    """
    Parses JSON output produced by Volatility's windows.pslist plugin.
    """

    def parse(
        self,
        raw: bytes,
    ) -> list[dict[str, Any]]:
        """
        Parse raw JSON bytes into a list of dictionaries.
        """

        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid windows.pslist JSON output.") from exc

        #
        # Support wrapped JSON
        #
        if isinstance(data, dict):

            if "rows" not in data:
                raise ValueError("Missing 'rows' field in windows.pslist JSON.")

            data = data["rows"]

        #
        # Validate top-level structure
        #
        if not isinstance(data, list):
            raise ValueError("windows.pslist JSON output must be a list of records.")

        #
        # Validate records
        #
        for record in data:

            if not isinstance(record, dict):
                raise ValueError("Each windows.pslist record must be a dictionary.")

        return data
