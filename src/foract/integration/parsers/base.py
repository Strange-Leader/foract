"""
Abstract parser interface for forensic plugins.

A parser converts raw plugin output into a list of Python dictionaries.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    """
    Base class for all forensic parsers.
    """

    @abstractmethod
    def parse(self, raw: bytes) -> list[dict[str, Any]]:
        """
        Parse raw plugin output.

        Parameters
        ----------
        raw:
            Raw bytes produced by a forensic plugin.

        Returns
        -------
        list[dict]
            Parsed forensic records.
        """
        raise NotImplementedError
