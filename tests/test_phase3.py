from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from foract.integration.models import (
    ArtifactSource,
    MappedEntity,
    ParsedArtifact,
    RelationshipDescriptor,
    ResolutionResult,
)
from foract.integration.report import (
    IntegrationReport,
    IntegrationStatus,
)

from foract.enums.schema import HypothesisStatus
from foract.graph.models.node import Node
from foract.integration.models import ResolutionStatus

# ==========================================================
# ArtifactSource
# ==========================================================


def test_artifact_source_creation() -> None:
    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    assert source.plugin_id == "pslist"


# ==========================================================
# ParsedArtifact
# ==========================================================


def test_parsed_artifact_creation() -> None:
    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
        },
        source=source,
    )

    assert artifact.schema == "Process"
    assert artifact.properties["pid"] == 4
    assert artifact.source is source


# ==========================================================
# RelationshipDescriptor
# ==========================================================


def test_relationship_descriptor_creation() -> None:
    descriptor = RelationshipDescriptor(
        relationship="PARENT_OF",
        target_identity_key="Process:pid=4",
    )

    assert descriptor.relationship == "PARENT_OF"
    assert descriptor.target_identity_key == "Process:pid=4"


# ==========================================================
# MappedEntity
# ==========================================================


def test_mapped_entity_creation() -> None:
    entity = MappedEntity(
        schema="Process",
        properties={
            "pid": 10,
        },
        identity_key="Process:pid=10",
    )

    assert entity.schema == "Process"
    assert entity.identity_key == "Process:pid=10"
    assert entity.relationships == ()


def test_mapped_entity_relationships() -> None:
    rel = RelationshipDescriptor(
        relationship="PARENT_OF",
        target_identity_key="Process:pid=4",
    )

    entity = MappedEntity(
        schema="Process",
        properties={"pid": 10},
        identity_key="Process:pid=10",
        relationships=(rel,),
    )

    assert len(entity.relationships) == 1
    assert entity.relationships[0] is rel


# ==========================================================
# ResolutionResult
# ==========================================================
from foract.integration.models import ResolutionStatus


def test_resolution_result_existing() -> None:
    node_id = uuid4()

    result = ResolutionResult(
        identity_key="Process:pid=4",
        existing_node_id=node_id,
        status=ResolutionStatus.EXISTING,
    )

    assert result.identity_key == "Process:pid=4"
    assert result.existing_node_id == node_id
    assert result.status is ResolutionStatus.EXISTING


def test_resolution_result_new() -> None:
    result = ResolutionResult(
        identity_key="Process:pid=99",
        existing_node_id=None,
        status=ResolutionStatus.NEW,
    )

    assert result.identity_key == "Process:pid=99"
    assert result.existing_node_id is None
    assert result.status is ResolutionStatus.NEW


# ==========================================================
# IntegrationReport
# ==========================================================


def test_integration_report_creation() -> None:
    report = IntegrationReport(
        execution_id=uuid4(),
        plugin_id="pslist",
        status=IntegrationStatus.SUCCESS,
    )

    assert report.status == IntegrationStatus.SUCCESS

    assert report.processed_artifacts == 0
    assert report.integrated_nodes == 0
    assert report.integrated_edges == 0
    assert report.duplicate_artifacts == 0
    assert report.validation_failures == ()
    assert report.warnings == ()


from foract.exceptions import ValidationError
from foract.integration.identity_index import (
    MemoryIdentityIndex,
)

# ==========================================================
# MemoryIdentityIndex
# ==========================================================


def test_identity_index_register() -> None:
    index = MemoryIdentityIndex()

    node_id = uuid4()

    index.register(
        "Process:pid=4",
        node_id,
    )

    assert index.lookup("Process:pid=4") == node_id


def test_identity_index_lookup_unknown() -> None:
    index = MemoryIdentityIndex()

    assert (
        index.lookup(
            "Process:pid=999",
        )
        is None
    )


def test_identity_index_duplicate_registration() -> None:
    index = MemoryIdentityIndex()

    node_id = uuid4()

    index.register(
        "Process:pid=4",
        node_id,
    )

    with pytest.raises(ValidationError):
        index.register(
            "Process:pid=4",
            uuid4(),
        )


def test_identity_index_contains_true() -> None:
    index = MemoryIdentityIndex()

    node_id = uuid4()

    index.register(
        "Process:pid=4",
        node_id,
    )

    assert index.contains(
        "Process:pid=4",
    )


def test_identity_index_contains_false() -> None:
    index = MemoryIdentityIndex()

    assert (
        index.contains(
            "Process:pid=4",
        )
        is False
    )


def test_identity_index_remove() -> None:
    index = MemoryIdentityIndex()

    node_id = uuid4()

    index.register(
        "Process:pid=4",
        node_id,
    )

    index.remove(
        "Process:pid=4",
    )

    assert (
        index.lookup(
            "Process:pid=4",
        )
        is None
    )


def test_identity_index_remove_unknown() -> None:
    index = MemoryIdentityIndex()

    #
    # Should not raise.
    #
    index.remove(
        "Process:pid=999",
    )

    assert (
        index.lookup(
            "Process:pid=999",
        )
        is None
    )


def test_identity_index_clear() -> None:
    index = MemoryIdentityIndex()

    index.register(
        "Process:pid=4",
        uuid4(),
    )

    index.register(
        "Process:pid=8",
        uuid4(),
    )

    index.clear()

    assert (
        index.lookup(
            "Process:pid=4",
        )
        is None
    )

    assert (
        index.lookup(
            "Process:pid=8",
        )
        is None
    )

    assert (
        index.contains(
            "Process:pid=4",
        )
        is False
    )


from foract.integration.deduplicator import Deduplicator

# ==========================================================
# Deduplicator
# ==========================================================


def test_deduplicator_existing_identity() -> None:
    index = MemoryIdentityIndex()

    node_id = uuid4()

    index.register(
        "Process:pid=4",
        node_id,
    )

    deduplicator = Deduplicator(index)

    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=4",
    )

    result = deduplicator.resolve(entity)

    assert result.identity_key == "Process:pid=4"
    assert result.existing_node_id == node_id
    assert result.status is ResolutionStatus.EXISTING


def test_deduplicator_new_identity() -> None:
    index = MemoryIdentityIndex()

    deduplicator = Deduplicator(index)

    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=999",
    )

    result = deduplicator.resolve(entity)

    assert result.identity_key == "Process:pid=999"
    assert result.existing_node_id is None
    assert result.status is ResolutionStatus.NEW


def test_deduplicator_multiple_existing() -> None:
    index = MemoryIdentityIndex()

    node1 = uuid4()
    node2 = uuid4()

    index.register(
        "Process:pid=1",
        node1,
    )

    index.register(
        "Process:pid=2",
        node2,
    )

    deduplicator = Deduplicator(index)
    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=1",
    )
    first = deduplicator.resolve(
        entity,
    )
    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=2",
    )
    second = deduplicator.resolve(
        entity,
    )

    assert first.existing_node_id == node1
    assert second.existing_node_id == node2

    assert first.status is ResolutionStatus.EXISTING
    assert second.status is ResolutionStatus.EXISTING


def test_deduplicator_multiple_new() -> None:
    index = MemoryIdentityIndex()

    deduplicator = Deduplicator(index)

    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=4",
    )
    first = deduplicator.resolve(
        entity,
    )
    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=8",
    )
    second = deduplicator.resolve(
        entity,
    )

    assert first.status is ResolutionStatus.NEW
    assert second.status is ResolutionStatus.NEW

    assert first.existing_node_id is None
    assert second.existing_node_id is None


def test_deduplicator_does_not_modify_identity_index() -> None:
    index = MemoryIdentityIndex()

    deduplicator = Deduplicator(index)
    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=4",
    )
    deduplicator.resolve(
        entity,
    )

    #
    # Deduplicator is pure.
    #
    assert (
        index.lookup(
            "Process:pid=55",
        )
        is None
    )


def test_deduplicator_is_repeatable() -> None:
    index = MemoryIdentityIndex()

    deduplicator = Deduplicator(index)

    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=777",
    )
    first = deduplicator.resolve(
        entity,
    )
    entity = MappedEntity(
        schema="Process",
        properties={},
        identity_key="Process:pid=777",
    )
    second = deduplicator.resolve(
        entity,
    )

    assert first == second


from foract.integration.parser import Parser
from foract.integration.parser_registry import ParserRegistry

# ==========================================================
# Dummy Parser
# ==========================================================


class DummyParser(Parser):
    def parse(
        self,
        raw_output: bytes,
        source: ArtifactSource,
    ) -> list[ParsedArtifact]:
        return []


# ==========================================================
# ParserRegistry
# ==========================================================


def test_register_parser() -> None:
    registry = ParserRegistry()

    parser = DummyParser()

    registry.register(
        "pslist",
        parser,
    )

    assert registry.has(
        "pslist",
    )

    assert (
        registry.get_parser(
            "pslist",
        )
        is parser
    )


from foract.exceptions import ValidationError


def test_duplicate_parser_registration() -> None:
    registry = ParserRegistry()

    parser = DummyParser()

    registry.register(
        "pslist",
        parser,
    )

    with pytest.raises(ValidationError):
        registry.register(
            "pslist",
            DummyParser(),
        )


def test_get_unknown_parser() -> None:
    registry = ParserRegistry()

    with pytest.raises(ValidationError):
        registry.get_parser(
            "unknown",
        )


def test_has_parser_true() -> None:
    registry = ParserRegistry()

    registry.register(
        "pslist",
        DummyParser(),
    )

    assert registry.has(
        "pslist",
    )


def test_has_parser_false() -> None:
    registry = ParserRegistry()

    assert (
        registry.has(
            "pslist",
        )
        is False
    )


def test_registered_plugins_empty() -> None:
    registry = ParserRegistry()

    assert registry.registered_plugins() == ()


def test_registered_plugins_sorted() -> None:
    registry = ParserRegistry()

    registry.register(
        "netscan",
        DummyParser(),
    )

    registry.register(
        "pslist",
        DummyParser(),
    )

    registry.register(
        "dlllist",
        DummyParser(),
    )

    assert registry.registered_plugins() == (
        "dlllist",
        "netscan",
        "pslist",
    )


from foract.integration.normalizer import Normalizer

# ==========================================================
# Normalizer
# ==========================================================


def test_normalizer_returns_same_schema() -> None:
    normalizer = Normalizer()

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
            "name": "System",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    normalized = normalizer.normalize(
        artifact,
    )

    assert normalized.schema == artifact.schema


def test_normalizer_preserves_source() -> None:
    normalizer = Normalizer()

    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
        },
        source=source,
    )

    normalized = normalizer.normalize(
        artifact,
    )

    assert normalized.source is source


def test_normalizer_trims_strings() -> None:
    normalizer = Normalizer()

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "name": "  explorer.exe  ",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    normalized = normalizer.normalize(
        artifact,
    )

    assert normalized.properties["name"] == "explorer.exe"


def test_normalizer_keeps_non_strings() -> None:
    normalizer = Normalizer()

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
            "ppid": 0,
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    normalized = normalizer.normalize(
        artifact,
    )

    assert normalized.properties["pid"] == 4
    assert normalized.properties["ppid"] == 0


def test_normalizer_returns_new_object() -> None:
    normalizer = Normalizer()

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    normalized = normalizer.normalize(
        artifact,
    )

    assert normalized is not artifact


from foract.exceptions import ValidationError
from foract.integration.validator import Validator
from foract.schema.bootstrap import create_schema_registry

# ==========================================================
# Validator
# ==========================================================


def test_validator_accepts_valid_artifact() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
            "ppid": 0,
            "name": "System",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    assert (
        validator.validate(
            artifact,
        )
        is artifact
    )


def test_validator_unknown_schema() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="UnknownSchema",
        properties={},
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="test",
        ),
    )

    with pytest.raises(ValidationError):
        validator.validate(
            artifact,
        )


def test_validator_missing_required_field() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
            "name": "System",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    with pytest.raises(ValidationError):
        validator.validate(
            artifact,
        )


def test_validator_invalid_field_type() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": "4",
            "ppid": 0,
            "name": "System",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    with pytest.raises(ValidationError):
        validator.validate(
            artifact,
        )


def test_validator_optional_field_missing() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="File",
        properties={
            "path": "/tmp/test.txt",
            "size": 100,
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="filescan",
        ),
    )

    validator.validate(
        artifact,
    )


def test_validator_custom_validation_rule() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Hypothesis",
        properties={
            "id": uuid4(),
            "title": "Test",
            "status": HypothesisStatus.PROPOSED,
            "confidence": 1.5,
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "update_count": 0,
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="test",
        ),
    )

    with pytest.raises(ValidationError):
        validator.validate(
            artifact,
        )


def test_validator_enum_validation() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Investigation",
        properties={
            "id": uuid4(),
            "title": "Investigation",
            "status": "INVALID",
            "started_at": datetime.now(UTC),
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="test",
        ),
    )

    with pytest.raises(ValidationError):
        validator.validate(
            artifact,
        )


def test_validator_returns_original_object() -> None:
    validator = Validator(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
            "ppid": 0,
            "name": "System",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    validated = validator.validate(
        artifact,
    )

    assert validated is artifact


from foract.integration.mapper import Mapper

# ==========================================================
# Mapper
# ==========================================================


def test_mapper_process_entity() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 123,
            "ppid": 4,
            "name": "cmd.exe",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    assert entity.schema == "Process"

    assert entity.identity_key == "Process:pid=123"

    assert entity.properties == artifact.properties


def test_mapper_process_relationship() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 123,
            "ppid": 4,
            "name": "cmd.exe",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    assert len(entity.relationships) == 1

    relationship = entity.relationships[0]

    assert relationship.relationship == "PARENT_OF"

    assert relationship.target_identity_key == "Process:pid=4"


def test_mapper_missing_relationship_source_field() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 123,
            "name": "cmd.exe",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    #
    # ppid missing
    #
    assert entity.relationships == ()


def test_mapper_file_identity_key() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="File",
        properties={
            "path": "/tmp/test.txt",
            "size": 100,
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="filescan",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    assert entity.identity_key == "File:path=/tmp/test.txt"


def test_mapper_registry_key_identity() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="RegistryKey",
        properties={
            "path": r"HKLM\\Software",
            "last_write_time": datetime.now(UTC),
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="printkey",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    assert entity.identity_key == r"RegistryKey:path=HKLM\\Software"


def test_mapper_hypothesis_identity() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    hypothesis_id = uuid4()

    artifact = ParsedArtifact(
        schema="Hypothesis",
        properties={
            "id": hypothesis_id,
            "title": "Test",
            "status": HypothesisStatus.PROPOSED,
            "confidence": 0.8,
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "update_count": 0,
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="test",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    assert entity.identity_key == f"Hypothesis:id={hypothesis_id}"


def test_mapper_preserves_properties() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    props = {
        "pid": 4,
        "ppid": 0,
        "name": "System",
    }

    artifact = ParsedArtifact(
        schema="Process",
        properties=props,
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    assert entity.properties == props


def test_mapper_returns_tuple_relationships() -> None:
    mapper = Mapper(
        create_schema_registry(),
    )

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 10,
            "ppid": 1,
            "name": "init",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    entity = mapper.map(
        artifact,
    )

    assert isinstance(
        entity.relationships,
        tuple,
    )


from foract.graph.store.memory_graph_store import MemoryGraphStore
from foract.integration.graph_persistence_service import (
    GraphPersistenceService,
)
from foract.integration.identity_index import (
    MemoryIdentityIndex,
)

# ==========================================================
# GraphPersistenceService
# ==========================================================


def make_resolution(
    identity_key: str,
    *,
    existing_node_id=None,
):
    return ResolutionResult(
        identity_key=identity_key,
        existing_node_id=existing_node_id,
        status=(
            ResolutionStatus.EXISTING
            if existing_node_id is not None
            else ResolutionStatus.NEW
        ),
    )


def test_persist_single_new_entity() -> None:
    graph = MemoryGraphStore()
    identities = MemoryIdentityIndex()

    service = GraphPersistenceService(
        graph,
        identities,
    )

    entity = MappedEntity(
        schema="Process",
        properties={
            "pid": 4,
            "ppid": 0,
            "name": "System",
        },
        identity_key="Process:pid=4",
    )

    report = service.persist(
        execution_id=uuid4(),
        plugin_id="pslist",
        entities=[entity],
        resolutions=[
            make_resolution(
                "Process:pid=4",
            )
        ],
        validation_errors=[],
    )

    assert report.integrated_nodes == 1
    assert report.integrated_edges == 0
    assert report.duplicate_artifacts == 0

    assert len(graph.list_nodes()) == 1
    assert identities.contains(
        "Process:pid=4",
    )


def test_existing_entity_creates_no_node() -> None:
    graph = MemoryGraphStore()
    identities = MemoryIdentityIndex()

    existing = Node(
        id=uuid4(),
        schema="Process",
        properties={
            "pid": 4,
        },
    )

    graph.add_node(existing)

    identities.register(
        "Process:pid=4",
        existing.id,
    )

    service = GraphPersistenceService(
        graph,
        identities,
    )

    entity = MappedEntity(
        schema="Process",
        properties={
            "pid": 4,
        },
        identity_key="Process:pid=4",
    )

    report = service.persist(
        execution_id=uuid4(),
        plugin_id="pslist",
        entities=[entity],
        resolutions=[
            make_resolution(
                "Process:pid=4",
                existing_node_id=existing.id,
            )
        ],
        validation_errors=[],
    )

    assert report.integrated_nodes == 0
    assert report.duplicate_artifacts == 1

    assert len(graph.list_nodes()) == 1


def test_new_relationship_same_batch() -> None:
    graph = MemoryGraphStore()
    identities = MemoryIdentityIndex()

    service = GraphPersistenceService(
        graph,
        identities,
    )

    parent = MappedEntity(
        schema="Process",
        properties={
            "pid": 1,
        },
        identity_key="Process:pid=1",
    )

    child = MappedEntity(
        schema="Process",
        properties={
            "pid": 2,
            "ppid": 1,
        },
        identity_key="Process:pid=2",
        relationships=(
            RelationshipDescriptor(
                relationship="PARENT_OF",
                target_identity_key="Process:pid=1",
            ),
        ),
    )

    report = service.persist(
        execution_id=uuid4(),
        plugin_id="pslist",
        entities=[
            parent,
            child,
        ],
        resolutions=[
            make_resolution("Process:pid=1"),
            make_resolution("Process:pid=2"),
        ],
        validation_errors=[],
    )

    assert report.integrated_nodes == 2
    assert report.integrated_edges == 1

    assert len(graph.list_nodes()) == 2
    assert len(graph.list_edges()) == 1


def test_relationship_to_existing_node() -> None:
    graph = MemoryGraphStore()
    identities = MemoryIdentityIndex()

    existing = Node(
        id=uuid4(),
        schema="Process",
        properties={
            "pid": 1,
        },
    )

    graph.add_node(existing)

    identities.register(
        "Process:pid=1",
        existing.id,
    )

    service = GraphPersistenceService(
        graph,
        identities,
    )

    child = MappedEntity(
        schema="Process",
        properties={
            "pid": 2,
            "ppid": 1,
        },
        identity_key="Process:pid=2",
        relationships=(
            RelationshipDescriptor(
                relationship="PARENT_OF",
                target_identity_key="Process:pid=1",
            ),
        ),
    )

    report = service.persist(
        execution_id=uuid4(),
        plugin_id="pslist",
        entities=[child],
        resolutions=[
            make_resolution(
                "Process:pid=2",
            )
        ],
        validation_errors=[],
    )

    assert report.integrated_nodes == 1
    assert report.integrated_edges == 1


def test_unresolved_relationship_target() -> None:
    graph = MemoryGraphStore()
    identities = MemoryIdentityIndex()

    service = GraphPersistenceService(
        graph,
        identities,
    )

    entity = MappedEntity(
        schema="Process",
        properties={
            "pid": 2,
        },
        identity_key="Process:pid=2",
        relationships=(
            RelationshipDescriptor(
                relationship="PARENT_OF",
                target_identity_key="Process:pid=999",
            ),
        ),
    )

    with pytest.raises(ValueError):
        service.persist(
            execution_id=uuid4(),
            plugin_id="pslist",
            entities=[entity],
            resolutions=[
                make_resolution(
                    "Process:pid=2",
                )
            ],
            validation_errors=[],
        )


def test_validation_errors_produce_partial_success() -> None:
    graph = MemoryGraphStore()
    identities = MemoryIdentityIndex()

    service = GraphPersistenceService(
        graph,
        identities,
    )

    entity = MappedEntity(
        schema="Process",
        properties={
            "pid": 4,
        },
        identity_key="Process:pid=4",
    )

    report = service.persist(
        execution_id=uuid4(),
        plugin_id="pslist",
        entities=[entity],
        resolutions=[
            make_resolution(
                "Process:pid=4",
            )
        ],
        validation_errors=[
            "warning",
        ],
    )

    assert report.status == IntegrationStatus.PARTIAL_SUCCESS


def test_entity_resolution_length_mismatch() -> None:
    graph = MemoryGraphStore()
    identities = MemoryIdentityIndex()

    service = GraphPersistenceService(
        graph,
        identities,
    )

    with pytest.raises(ValueError):
        service.persist(
            execution_id=uuid4(),
            plugin_id="pslist",
            entities=[],
            resolutions=[
                make_resolution(
                    "Process:pid=1",
                )
            ],
            validation_errors=[],
        )


from unittest.mock import MagicMock

from foract.integration.engine import IntegrationEngine

# ==========================================================
# IntegrationEngine
# ==========================================================


def test_engine_calls_pipeline() -> None:
    execution_memory = MagicMock()
    parser_registry = MagicMock()

    parser = MagicMock()

    parser_registry.get_parser.return_value = parser

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
            "ppid": 0,
            "name": "System",
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    parser.parse.return_value = [
        artifact,
    ]

    execution = MagicMock()

    execution.id = uuid4()
    execution.plugin = "pslist"

    execution_memory.get_artifact.return_value = execution

    execution_memory.get_stdout.return_value = b"output"

    normalizer = MagicMock()
    validator = MagicMock()
    mapper = MagicMock()
    deduplicator = MagicMock()
    persistence = MagicMock()

    normalizer.normalize.return_value = artifact
    validator.validate.return_value = artifact

    mapped = MappedEntity(
        schema="Process",
        properties={
            "pid": 4,
        },
        identity_key="Process:pid=4",
    )

    mapper.map.return_value = mapped

    resolution = ResolutionResult(
        identity_key="Process:pid=4",
        existing_node_id=None,
        status=ResolutionStatus.NEW,
    )

    deduplicator.resolve.return_value = resolution

    report = IntegrationReport(
        execution_id=execution.id,
        plugin_id="pslist",
        status=IntegrationStatus.SUCCESS,
    )

    persistence.persist.return_value = report

    engine = IntegrationEngine(
        execution_memory,
        parser_registry,
        normalizer,
        validator,
        mapper,
        deduplicator,
        persistence,
    )

    result = engine.integrate(
        execution.id,
    )

    parser_registry.get_parser.assert_called_once_with(
        "pslist",
    )

    parser.parse.assert_called_once()

    normalizer.normalize.assert_called_once()

    validator.validate.assert_called_once()

    mapper.map.assert_called_once()
    entity = MappedEntity(
        schema="Process",
        properties={
            "pid": 4,
        },
        identity_key="Process:pid=4",
    )

    deduplicator.resolve.assert_called_once_with(entity)

    persistence.persist.assert_called_once()

    assert result is report


def test_engine_collects_validation_errors() -> None:
    execution_memory = MagicMock()
    parser_registry = MagicMock()

    parser = MagicMock()

    parser_registry.get_parser.return_value = parser

    artifact = ParsedArtifact(
        schema="Process",
        properties={
            "pid": 4,
        },
        source=ArtifactSource(
            execution_id=uuid4(),
            plugin_id="pslist",
        ),
    )

    parser.parse.return_value = [
        artifact,
    ]

    execution = MagicMock()

    execution.id = uuid4()
    execution.plugin = "pslist"

    execution_memory.get_artifact.return_value = execution

    execution_memory.get_stdout.return_value = b""

    normalizer = MagicMock()
    validator = MagicMock()
    mapper = MagicMock()
    deduplicator = MagicMock()
    persistence = MagicMock()

    normalizer.normalize.return_value = artifact

    validator.validate.side_effect = Exception(
        "validation failed",
    )

    persistence.persist.return_value = MagicMock()

    engine = IntegrationEngine(
        execution_memory,
        parser_registry,
        normalizer,
        validator,
        mapper,
        deduplicator,
        persistence,
    )

    engine.integrate(
        execution.id,
    )

    kwargs = persistence.persist.call_args.kwargs

    assert kwargs["validation_errors"] == [
        "validation failed",
    ]

    assert kwargs["entities"] == []


import json

from foract.integration.parsers.pslist import (
    WindowsPsListParser,
)

# ==========================================================
# WindowsPsListParser
# ==========================================================


def test_pslist_parser_single_record() -> None:
    parser = WindowsPsListParser()

    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    raw = json.dumps(
        [
            {
                "pid": 4,
                "ppid": 0,
                "name": "System",
            }
        ]
    ).encode()

    artifacts = parser.parse(
        raw,
        source,
    )

    assert len(artifacts) == 1

    artifact = artifacts[0]

    assert artifact.schema == "Process"
    assert artifact.properties["pid"] == 4
    assert artifact.source is source


def test_pslist_parser_wrapped_json() -> None:
    parser = WindowsPsListParser()

    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    raw = json.dumps(
        {
            "rows": [
                {
                    "pid": 10,
                    "ppid": 4,
                    "name": "cmd.exe",
                }
            ]
        }
    ).encode()

    artifacts = parser.parse(
        raw,
        source,
    )

    assert len(artifacts) == 1

    assert artifacts[0].properties["pid"] == 10


def test_pslist_parser_invalid_json() -> None:
    parser = WindowsPsListParser()

    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    with pytest.raises(ValueError):
        parser.parse(
            b"not json",
            source,
        )


def test_pslist_parser_missing_rows() -> None:
    parser = WindowsPsListParser()

    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    raw = json.dumps({"foo": []}).encode()

    with pytest.raises(ValueError):
        parser.parse(
            raw,
            source,
        )


def test_pslist_parser_invalid_record() -> None:
    parser = WindowsPsListParser()

    source = ArtifactSource(
        execution_id=uuid4(),
        plugin_id="pslist",
    )

    raw = json.dumps(
        [
            1,
            2,
            3,
        ]
    ).encode()

    with pytest.raises(ValueError):
        parser.parse(
            raw,
            source,
        )
