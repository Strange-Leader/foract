from __future__ import annotations

from foract.execution.execution_memory import ExecutionMemory
from foract.execution.execution_record import ExecutionRecord
from foract.graph.enums import NodeType
from foract.graph.models.node import Node
from foract.graph.store.graph_store import GraphStore
from foract.integration.mapper import EvidenceMapper
from foract.integration.models import (
    ResolutionResult,
)
from foract.integration.normalizer import Normalizer
from foract.integration.parser_registry import ParserRegistry
from foract.integration.provenance import ProvenanceBuilder
from foract.integration.report import (
    IntegrationReport,
    IntegrationStatus,
)
from foract.integration.resolver import EntityResolver
from foract.integration.validator import Validator

_PROCESS_SCHEMA = "Process"


class IntegrationEngine:
    """
    Orchestrates the complete Phase 3 evidence integration pipeline.

    Responsibilities
    ----------------
    - Parse raw forensic output.
    - Normalize plugin-specific fields.
    - Validate against FORACT schemas.
    - Map semantic entities.
    - Resolve identities.
    - Build provenance.
    - Produce an IntegrationReport.
    """

    def __init__(
        self,
        execution_memory: ExecutionMemory,
        graph_store: GraphStore,
        parser_registry: ParserRegistry,
        normalizer: Normalizer,
        validator: Validator,
        mapper: EvidenceMapper,
        resolver: EntityResolver,
        provenance_builder: ProvenanceBuilder,
    ) -> None:
        self._execution_memory = execution_memory
        self._graph_store = graph_store

        self._parser_registry = parser_registry
        self._normalizer = normalizer
        self._validator = validator
        self._mapper = mapper
        self._resolver = resolver
        self._provenance_builder = provenance_builder

    def _build_execution_node(
        self,
        execution: ExecutionRecord,
    ) -> Node:
        """
        Convert an ExecutionRecord into a graph node.

        This node becomes the provenance source for all semantic
        evidence produced during the execution.
        """

        return Node(
            type=NodeType.EXECUTION_RECORD,
            properties={
                "execution_id": execution.execution_id,
                "plugin_id": execution.plugin_id,
                "command": execution.command,
                "started_at": execution.started_at.isoformat(),
                "finished_at": execution.finished_at.isoformat(),
                "status": execution.status.name,
                "parameters": dict(execution.parameters),
                "metadata": dict(execution.metadata),
            },
        )

    def _determine_status(
        self,
        processed: int,
        integrated: int,
    ) -> IntegrationStatus:
        """
        Determine the overall integration status.
        """

        if processed == 0:
            return IntegrationStatus.FAILED

        if integrated == 0:
            return IntegrationStatus.FAILED

        if integrated == processed:
            return IntegrationStatus.SUCCESS

        return IntegrationStatus.PARTIAL_SUCCESS

    def integrate(
        self,
        execution_id: str,
    ) -> IntegrationReport:
        """
        Integrate a completed plugin execution into the Evidence Graph.

        Returns
        -------
        IntegrationReport
            Operational summary of the integration.
        """

        #
        # Retrieve execution
        #
        execution = self._execution_memory.get_execution(execution_id)

        #
        # Load raw stdout
        #
        raw_output = self._execution_memory.get_stdout(execution.execution_id)

        #
        # Select parser
        #
        parser = self._parser_registry.get(execution.plugin_id)

        #
        # Parse plugin output
        #
        try:
            parsed_records = parser.parse(raw_output)
        except Exception as exc:
            report = IntegrationReport(
                execution_id=execution.execution_id,
                status=IntegrationStatus.FAILED,
                parser_warnings=[str(exc)],
            )

            self._execution_memory.attach_integration_report(report)

            return report

        processed_records = len(parsed_records)

        #
        # Normalize plugin-specific fields
        #
        normalized_records = self._normalizer.normalize(
            execution.plugin_id,
            parsed_records,
        )

        #
        # Phase 3 currently supports one schema:
        #
        # TODO (Phase 4):
        # Resolve schema name using the Plugin Intelligence Database.
        schema_name = _PROCESS_SCHEMA

        #
        # Validate normalized records
        #
        (
            valid_records,
            validation_failures,
        ) = self._validator.validate(
            schema_name,
            normalized_records,
        )

        #
        # Convert records into semantic entities
        #
        if valid_records:

            entities = self._mapper.map(
                schema_name,
                valid_records,
            )

            #
            # Resolve semantic entities
            #
            resolution = self._resolver.resolve(
                entities,
                execution.execution_id,
            )

        else:

            entities = []

            resolution = ResolutionResult()

            #
        # Create execution node
        #
        execution_node = self._build_execution_node(execution)
        # Execution records are immutable.
        # Integration is expected to occur once.

        self._graph_store.add_node(execution_node)

        #
        # Build provenance relationships
        #
        provenance_edges = self._provenance_builder.build(
            execution_node,
            resolution.nodes,
        )

        for edge in provenance_edges:
            self._graph_store.add_edge(edge)

        # That's actually acceptable for Phase 3 because
        # ExecutionMemory is append-only a
        # nd each ExecutionRecord has a unique execution_id. Normally, an execution is
        # integrated only once.
        #
        # Determine integration status
        #
        integrated_records = len(resolution.nodes)

        rejected_records = processed_records - integrated_records

        status = self._determine_status(
            processed_records,
            integrated_records,
        )

        #
        # Build IntegrationReport
        #
        report = IntegrationReport(
            execution_id=execution.execution_id,
            status=status,
            processed_records=processed_records,
            integrated_records=integrated_records,
            rejected_records=rejected_records,
            validation_failures=validation_failures,
            integration_warnings=resolution.warnings,
            conflicts=resolution.conflicts,
        )

        #
        # Store report
        #
        self._execution_memory.attach_integration_report(report)

        return report
