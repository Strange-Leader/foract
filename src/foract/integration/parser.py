from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    """
    Base interface for forensic output parsers.
    """

    @abstractmethod
    def parse(
        self,
        raw_output: bytes,
    ) -> list[dict[str, Any]]:
        """
        Convert raw plugin output into structured records.
        """
        raise NotImplementedError
