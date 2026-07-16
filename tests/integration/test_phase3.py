from __future__ import annotations

import json

# ==========================================================
# Parser
# ==========================================================
import pytest

from foract.graph.enums import EdgeType, NodeType
from foract.graph.models.node import Node
from foract.graph.store.memory_graph_store import MemoryGraphStore
from foract.integration.identity_index import (
    MemoryIdentityIndex,
)
from foract.integration.models import MappedEntity, RelationshipDescriptor
from foract.integration.node_merger import NodeMerger
from foract.integration.normalizer import Normalizer
from foract.integration.parsers.pslist import WindowsPsListParser
from foract.integration.provenance import ProvenanceBuilder
from foract.integration.relationship_builder import RelationshipBuilder
from foract.integration.resolver import EntityResolver
from foract.registry import SchemaRegistry
from foract.schema.builtin import register_builtin_schemas


@pytest.fixture
def schema_registry() -> SchemaRegistry:
    registry = SchemaRegistry()
    register_builtin_schemas(registry)
    return registry


def test_pslist_parser_parses_list() -> None:
    parser = WindowsPsListParser()

    raw = json.dumps(
        [
            {
                "PID": 4,
                "PPID": 0,
                "Name": "System",
            },
            {
                "PID": 520,
                "PPID": 4,
                "Name": "smss.exe",
            },
        ]
    ).encode()

    records = parser.parse(raw)

    assert len(records) == 2
    assert records[0]["PID"] == 4
    assert records[1]["Name"] == "smss.exe"


def test_pslist_parser_supports_rows_wrapper() -> None:
    parser = WindowsPsListParser()

    raw = json.dumps(
        {
            "rows": [
                {
                    "PID": 4,
                    "PPID": 0,
                    "Name": "System",
                }
            ]
        }
    ).encode()

    records = parser.parse(raw)

    assert len(records) == 1
    assert records[0]["PID"] == 4


def test_pslist_parser_invalid_json() -> None:
    parser = WindowsPsListParser()

    try:
        parser.parse(b"not json")
        assert False
    except ValueError:
        pass


# ==========================================================
# Normalizer
# ==========================================================


def test_normalizer_maps_fields() -> None:
    normalizer = Normalizer()

    records = [
        {
            "PID": 4,
            "PPID": 0,
            "Name": "System",
        }
    ]

    normalized = normalizer.normalize(
        "windows.pslist",
        records,
    )

    assert normalized[0]["pid"] == 4
    assert normalized[0]["ppid"] == 0
    assert normalized[0]["name"] == "System"


def test_normalizer_unknown_plugin() -> None:
    normalizer = Normalizer()

    try:
        normalizer.normalize("abc", [])
        assert False
    except ValueError:
        pass


# ==========================================================
# Provenance
# ==========================================================


def test_provenance_builder() -> None:
    from foract.graph.models.node import Node

    execution = Node(
        type=NodeType.EXECUTION_RECORD,
        properties={},
    )

    process = Node(
        type=NodeType.PROCESS,
        properties={"pid": 4},
    )

    builder = ProvenanceBuilder()

    edges = builder.build(
        execution,
        [process],
    )

    assert len(edges) == 1

    edge = edges[0]

    assert edge.type == EdgeType.PRODUCED_BY
    assert edge.source == process.id
    assert edge.target == execution.id


def test_provenance_requires_execution_node() -> None:
    from foract.graph.models.node import Node

    builder = ProvenanceBuilder()

    process = Node(
        type=NodeType.PROCESS,
        properties={},
    )

    try:
        builder.build(
            process,
            [],
        )
        assert False
    except ValueError:
        pass


# ==========================================================
# IdentityIndex
# ==========================================================

from foract.integration.identity_index import MemoryIdentityIndex


def test_identity_register_lookup() -> None:
    index = MemoryIdentityIndex()

    index.register("Process:pid=4", "node-1")

    assert index.lookup("Process:pid=4") == "node-1"


def test_identity_remove() -> None:
    index = MemoryIdentityIndex()

    index.register("Process:pid=4", "node-1")
    index.remove("Process:pid=4")

    assert index.lookup("Process:pid=4") is None


# ==========================================================
# NodeMerger
# ==========================================================


def test_node_merger_adds_missing_property() -> None:
    existing = Node(
        type=NodeType.PROCESS,
        properties={
            "pid": 4,
        },
    )

    incoming = MappedEntity(
        schema_name="Process",
        node_type=NodeType.PROCESS,
        identity_key="Process:pid=4",
        properties={
            "pid": 4,
            "name": "System",
        },
        relationships=[],
    )

    merger = NodeMerger()

    result = merger.merge(
        existing,
        incoming,
        "exec-1",
    )

    assert result.node.properties["pid"] == 4
    assert result.node.properties["name"] == "System"
    assert len(result.conflicts) == 0


def test_node_merger_detects_conflict() -> None:
    existing = Node(
        type=NodeType.PROCESS,
        properties={
            "pid": 4,
            "name": "System",
        },
    )

    incoming = MappedEntity(
        schema_name="Process",
        node_type=NodeType.PROCESS,
        identity_key="Process:pid=4",
        properties={
            "pid": 4,
            "name": "Explorer",
        },
        relationships=[],
    )

    merger = NodeMerger()

    result = merger.merge(
        existing,
        incoming,
        "exec-1",
    )

    assert len(result.conflicts) == 1

    conflict = result.conflicts[0]

    assert conflict.field == "name"
    assert conflict.existing_value == "System"
    assert conflict.incoming_value == "Explorer"


# ==========================================================
# RelationshipBuilder
# ==========================================================


def test_relationship_builder_creates_parent_edge() -> None:
    entity = MappedEntity(
        schema_name="Process",
        node_type=NodeType.PROCESS,
        identity_key="Process:pid=520",
        properties={},
        relationships=[
            RelationshipDescriptor(
                edge_type=EdgeType.PARENT_OF,
                target_identity_key="Process:pid=4",
            )
        ],
    )

    builder = RelationshipBuilder()

    result = builder.build(
        [entity],
        {
            "Process:pid=520": "child",
            "Process:pid=4": "parent",
        },
    )

    assert len(result.edges) == 1

    edge = result.edges[0]

    assert edge.source == "parent"
    assert edge.target == "child"
    assert edge.type == EdgeType.PARENT_OF


def test_relationship_builder_missing_target() -> None:
    entity = MappedEntity(
        schema_name="Process",
        node_type=NodeType.PROCESS,
        identity_key="Process:pid=520",
        properties={},
        relationships=[
            RelationshipDescriptor(
                edge_type=EdgeType.PARENT_OF,
                target_identity_key="Process:pid=4",
            )
        ],
    )

    builder = RelationshipBuilder()

    result = builder.build(
        [entity],
        {
            "Process:pid=520": "child",
        },
    )

    assert len(result.edges) == 0
    assert len(result.warnings) == 1


# ==========================================================
# Validator
# ==========================================================

from foract.integration.validator import Validator


def test_validator_accepts_valid_process(
    schema_registry,
) -> None:
    validator = Validator(schema_registry)

    records = [
        {
            "pid": 4,
            "ppid": 0,
            "name": "System",
        }
    ]

    valid, failures = validator.validate(
        "Process",
        records,
    )

    assert len(valid) == 1
    assert failures == []


def test_validator_rejects_missing_required(
    schema_registry,
) -> None:
    validator = Validator(schema_registry)

    records = [
        {
            "pid": 4,
            "ppid": 0,
        }
    ]

    valid, failures = validator.validate(
        "Process",
        records,
    )

    assert valid == []
    assert len(failures) == 1


# ==========================================================
# EvidenceMapper
# ==========================================================

from foract.integration.mapper import EvidenceMapper


def test_mapper_generates_identity_key(
    schema_registry,
) -> None:
    mapper = EvidenceMapper(schema_registry)

    entities = mapper.map(
        "Process",
        [
            {
                "pid": 520,
                "ppid": 4,
                "name": "smss.exe",
            }
        ],
    )

    assert len(entities) == 1

    entity = entities[0]

    assert entity.identity_key == "Process:pid=520"


def test_mapper_creates_parent_relationship(
    schema_registry,
) -> None:
    mapper = EvidenceMapper(schema_registry)

    entity = mapper.map(
        "Process",
        [
            {
                "pid": 520,
                "ppid": 4,
                "name": "smss.exe",
            }
        ],
    )[0]

    assert len(entity.relationships) == 1

    rel = entity.relationships[0]

    assert rel.target_identity_key == "Process:pid=4"


# ==========================================================
# EntityResolver
# ==========================================================


def test_entity_resolver_creates_nodes(
    schema_registry,
) -> None:

    graph = MemoryGraphStore()
    identity = MemoryIdentityIndex()

    resolver = EntityResolver(
        graph,
        identity,
    )

    mapper = EvidenceMapper(schema_registry)

    entities = mapper.map(
        "Process",
        [
            {
                "pid": 4,
                "ppid": 0,
                "name": "System",
            }
        ],
    )

    result = resolver.resolve(
        entities,
        "exec-1",
    )

    assert len(result.nodes) == 1
    assert len(graph.list_nodes()) == 1


def test_entity_resolver_identity_map(
    schema_registry,
) -> None:

    graph = MemoryGraphStore()
    identity = MemoryIdentityIndex()

    resolver = EntityResolver(
        graph,
        identity,
    )

    mapper = EvidenceMapper(schema_registry)

    entities = mapper.map(
        "Process",
        [
            {
                "pid": 4,
                "ppid": 0,
                "name": "System",
            }
        ],
    )

    result = resolver.resolve(
        entities,
        "exec-1",
    )

    assert result.identity_map["Process:pid=4"] == result.nodes[0].id


# ==========================================================
# IntegrationEngine
# ==========================================================

import pytest

from foract.execution.execution_memory import ExecutionMemory
from foract.execution.execution_record import ExecutionRecord
from foract.execution.execution_status import ExecutionStatus

from foract.graph.store.memory_graph_store import MemoryGraphStore

from foract.integration.engine import IntegrationEngine
from foract.integration.mapper import EvidenceMapper
from foract.integration.normalizer import Normalizer
from foract.integration.parser_registry import ParserRegistry
from foract.integration.provenance import ProvenanceBuilder
from foract.integration.report import IntegrationStatus
from foract.integration.resolver import EntityResolver
from foract.integration.validator import Validator

from foract.integration.identity_index import MemoryIdentityIndex

from foract.storage.in_memory_blob_store import (
    InMemoryBlobStore,
)

from datetime import datetime


def test_engine_fails_without_registered_parser(
    schema_registry,
) -> None:

    #
    # Blob store
    #
    blob_store = InMemoryBlobStore()

    blob_store.store(
        "stdout",
        b"[]",
    )

    blob_store.store(
        "stderr",
        b"",
    )

    #
    # Execution memory
    #
    memory = ExecutionMemory(blob_store)

    record = ExecutionRecord(
        execution_id="exec-1",
        plugin_id="windows.pslist",
        command="vol.py windows.pslist",
        parameters={},
        status=ExecutionStatus.SUCCESS,
        started_at=datetime.now(),
        finished_at=datetime.now(),
        stdout_blob_id="stdout",
        stderr_blob_id="stderr",
        metadata={},
    )

    memory.append_execution(record)

    #
    # Empty parser registry
    #
    parser_registry = ParserRegistry()

    graph = MemoryGraphStore()

    engine = IntegrationEngine(
        execution_memory=memory,
        graph_store=graph,
        parser_registry=parser_registry,
        normalizer=Normalizer(),
        validator=Validator(schema_registry),
        mapper=EvidenceMapper(schema_registry),
        resolver=EntityResolver(
            graph,
            MemoryIdentityIndex(),
        ),
        provenance_builder=ProvenanceBuilder(),
    )

    with pytest.raises(ValueError):
        engine.integrate("exec-1")
