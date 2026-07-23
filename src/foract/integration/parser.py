from __future__ import annotations

from abc import ABC, abstractmethod

from foract.integration.models import (
    ArtifactSource,
    ParsedArtifact,
)


class Parser(ABC):
    """
    Base interface for all evidence parsers.

    A parser converts raw output produced by a forensic or utility
    tool into canonical ParsedArtifact objects.

    Parsers perform only syntactic interpretation of tool output.
    They do not normalize, validate, deduplicate, or persist
    evidence.
    """

    @abstractmethod
    def parse(
        self,
        raw_output: bytes,
        source: ArtifactSource,
    ) -> list[ParsedArtifact]:
        """
        Parse raw tool output into parsed artifacts.

        Parameters
        ----------
        raw_output:
            Raw bytes produced by a completed tool execution.

        source:
            Origin of the parsed artifacts.

        Returns
        -------
        list[ParsedArtifact]
            Parsed artifacts extracted from the raw output.
        """
        raise NotImplementedError
