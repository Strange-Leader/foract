from __future__ import annotations

from foract.integration.parser import Parser


class ParserRegistry:
    """
    Registry of forensic output parsers.
    """

    def __init__(self) -> None:
        self._parsers: dict[str, Parser] = {}

    def register(
        self,
        plugin_id: str,
        parser: Parser,
    ) -> None:
        self._parsers[plugin_id] = parser

    def get(
        self,
        plugin_id: str,
    ) -> Parser:
        try:
            return self._parsers[plugin_id]
        except KeyError as exc:
            raise ValueError(f"No parser registered for '{plugin_id}'.") from exc
