from __future__ import annotations

from uuid import UUID

from foract.execution.execution_memory import ExecutionMemory
from foract.integration.deduplicator import Deduplicator
from foract.integration.graph_persistence_service import (
    GraphPersistenceService,
)
from foract.integration.mapper import Mapper
from foract.integration.models import ArtifactSource
from foract.integration.normalizer import Normalizer
from foract.integration.parser_registry import ParserRegistry
from foract.integration.report import IntegrationReport
from foract.integration.validator import Validator


class IntegrationEngine:
    """
    Coordinates the complete Evidence Integration pipeline.

    The IntegrationEngine performs no parsing, validation,
    mapping, deduplication, or persistence itself.

    Its responsibility is to orchestrate the individual
    pipeline components.
    """

    def __init__(
        self,
        execution_memory: ExecutionMemory,
        parser_registry: ParserRegistry,
        normalizer: Normalizer,
        validator: Validator,
        mapper: Mapper,
        deduplicator: Deduplicator,
        persistence: GraphPersistenceService,
    ) -> None:
        self._execution_memory = execution_memory
        self._parser_registry = parser_registry
        self._normalizer = normalizer
        self._validator = validator
        self._mapper = mapper
        self._deduplicator = deduplicator
        self._persistence = persistence

    def integrate(
        self,
        execution_id: UUID,
    ) -> IntegrationReport:
        """
        Integrate the output of one completed execution into
        the Evidence Graph.
        """

        #
        # Retrieve execution record.
        #
        #
        # Retrieve execution record.
        #
        execution = self._execution_memory.get_artifact(
            execution_id,
        )

        #
        # Load parser.
        #
        parser = self._parser_registry.get_parser(
            execution.plugin,
        )

        #
        # Read raw stdout from Execution Memory.
        #
        raw_output = self._execution_memory.get_stdout(
            execution_id,
        )

        #
        # Build artifact source.
        #
        source = ArtifactSource(
            execution_id=execution.id,
            plugin_id=execution.plugin,
        )

        #
        # Parse raw output.
        #
        parsed = parser.parse(
            raw_output,
            source,
        )
        #
        # Normalize.
        #
        normalized = [
            self._normalizer.normalize(
                artifact,
            )
            for artifact in parsed
        ]

        #
        # Validate.
        #
        validated = []
        validation_errors: list[str] = []

        for artifact in normalized:
            try:
                validated.append(
                    self._validator.validate(
                        artifact,
                    )
                )
            except Exception as exc:
                validation_errors.append(
                    str(exc),
                )

        #
        # Map.
        #
        mapped = [
            self._mapper.map(
                artifact,
            )
            for artifact in validated
        ]

        #
        # Deduplicate.
        #
        resolutions = [
            self._deduplicator.resolve(
                entity,
            )
            for entity in mapped
        ]

        #
        # Persist.
        #
        return self._persistence.persist(
            execution_id=execution_id,
            plugin_id=execution.plugin,
            entities=mapped,
            resolutions=resolutions,
            validation_errors=validation_errors,
        )
