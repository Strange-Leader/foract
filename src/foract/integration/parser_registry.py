from __future__ import annotations

from foract.exceptions import ValidationError
from foract.integration.parser import Parser


class ParserRegistry:
    """
    Registry of evidence parsers.

    The registry maps a plugin identifier to the parser capable of
    interpreting that plugin's output.

    The registry performs no parsing itself; it only manages parser
    registration and lookup.
    """

    def __init__(self) -> None:
        self._parsers: dict[str, Parser] = {}

    def register(
        self,
        plugin_id: str,
        parser: Parser,
    ) -> None:
        """
        Register a parser for a plugin.
        """

        if plugin_id in self._parsers:
            raise ValidationError(f"Parser already registered for '{plugin_id}'.")

        self._parsers[plugin_id] = parser

    def get_parser(
        self,
        plugin_id: str,
    ) -> Parser:
        """
        Return the parser registered for a plugin.
        """

        try:
            return self._parsers[plugin_id]

        except KeyError as exc:
            raise ValidationError(f"No parser registered for '{plugin_id}'.") from exc

    def has(
        self,
        plugin_id: str,
    ) -> bool:
        """
        Return True if a parser is registered.
        """

        return plugin_id in self._parsers

    def registered_plugins(
        self,
    ) -> tuple[str, ...]:
        """
        Return registered plugin identifiers in deterministic order.
        """

        return tuple(sorted(self._parsers))
