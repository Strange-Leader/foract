from __future__ import annotations

import pytest

from foract.exceptions import ValidationError
from foract.schema.definition import SchemaDefinition
from foract.schema.field import FieldDefinition
from foract.schema.registry import SchemaRegistry
from foract.enums.schema import SchemaCategory

# ==========================================================
# Helpers
# ==========================================================


def make_schema(
    name: str = "TestSchema",
) -> SchemaDefinition:
    return SchemaDefinition(
        name=name,
        category=SchemaCategory.ENTITY,
        version="1.0",
        fields=[
            FieldDefinition(
                name="id",
                type=int,
                identity=True,
            ),
        ],
    )


# ==========================================================
# Schema Registry
# ==========================================================


def test_register_schema() -> None:
    registry = SchemaRegistry()

    schema = make_schema()

    registry.register_schema(schema)

    assert registry.has_schema("TestSchema")


def test_duplicate_schema_registration() -> None:
    registry = SchemaRegistry()

    schema = make_schema()

    registry.register_schema(schema)

    with pytest.raises(ValidationError):
        registry.register_schema(schema)


def test_get_schema() -> None:
    registry = SchemaRegistry()

    schema = make_schema()

    registry.register_schema(schema)

    retrieved = registry.get_schema(
        "TestSchema",
    )

    assert retrieved == schema


def test_get_unknown_schema() -> None:
    registry = SchemaRegistry()

    with pytest.raises(ValidationError):
        registry.get_schema("Unknown")


def test_has_schema_true() -> None:
    registry = SchemaRegistry()

    registry.register_schema(
        make_schema(),
    )

    assert registry.has_schema(
        "TestSchema",
    )


def test_has_schema_false() -> None:
    registry = SchemaRegistry()

    assert not registry.has_schema(
        "TestSchema",
    )


def test_list_schemas_empty() -> None:
    registry = SchemaRegistry()

    assert registry.list_schemas() == ()


def test_list_schemas_sorted() -> None:
    registry = SchemaRegistry()

    registry.register_schema(
        make_schema("B"),
    )

    registry.register_schema(
        make_schema("A"),
    )

    registry.register_schema(
        make_schema("C"),
    )

    names = [schema.name for schema in registry.list_schemas()]

    assert names == [
        "A",
        "B",
        "C",
    ]


# ==========================================================
# Relationship Registry
# ==========================================================

from foract.schema.relationship import (
    RelationshipDefinition,
)


def make_relationship(
    name: str = "TEST_RELATIONSHIP",
) -> RelationshipDefinition:
    return RelationshipDefinition(
        name=name,
        description="Test relationship.",
    )


def test_register_relationship() -> None:
    registry = SchemaRegistry()

    relationship = make_relationship()

    registry.register_relationship(
        relationship,
    )

    assert registry.has_relationship(
        "TEST_RELATIONSHIP",
    )


def test_duplicate_relationship_registration() -> None:
    registry = SchemaRegistry()

    relationship = make_relationship()

    registry.register_relationship(
        relationship,
    )

    with pytest.raises(ValidationError):
        registry.register_relationship(
            relationship,
        )


def test_get_relationship() -> None:
    registry = SchemaRegistry()

    relationship = make_relationship()

    registry.register_relationship(
        relationship,
    )

    retrieved = registry.get_relationship(
        "TEST_RELATIONSHIP",
    )

    assert retrieved == relationship


def test_get_unknown_relationship() -> None:
    registry = SchemaRegistry()

    with pytest.raises(ValidationError):
        registry.get_relationship(
            "UNKNOWN",
        )


def test_has_relationship_true() -> None:
    registry = SchemaRegistry()

    registry.register_relationship(
        make_relationship(),
    )

    assert registry.has_relationship(
        "TEST_RELATIONSHIP",
    )


def test_has_relationship_false() -> None:
    registry = SchemaRegistry()

    assert not registry.has_relationship(
        "TEST_RELATIONSHIP",
    )


def test_list_relationships_empty() -> None:
    registry = SchemaRegistry()

    assert registry.list_relationships() == ()


def test_list_relationships_sorted() -> None:
    registry = SchemaRegistry()

    registry.register_relationship(
        make_relationship("B"),
    )

    registry.register_relationship(
        make_relationship("A"),
    )

    registry.register_relationship(
        make_relationship("C"),
    )

    names = [relationship.name for relationship in registry.list_relationships()]

    assert names == [
        "A",
        "B",
        "C",
    ]


# ==========================================================
# Relationship Mapping Registry
# ==========================================================

from foract.schema.relationship_mapping import (
    RelationshipMappingDefinition,
)


def make_relationship_mapping(
    source_schema: str = "Process",
) -> RelationshipMappingDefinition:
    return RelationshipMappingDefinition(
        relationship=make_relationship("PARENT_OF"),
        source_schema=source_schema,
        target_schema="Process",
        source_field="ppid",
        target_field="pid",
    )


def test_register_relationship_mapping() -> None:
    registry = SchemaRegistry()

    mapping = make_relationship_mapping()

    registry.register_relationship_mapping(
        mapping,
    )

    mappings = registry.get_relationship_mappings()

    assert mapping in mappings


def test_duplicate_relationship_mapping_registration() -> None:
    registry = SchemaRegistry()

    mapping = make_relationship_mapping()

    registry.register_relationship_mapping(
        mapping,
    )

    with pytest.raises(ValidationError):
        registry.register_relationship_mapping(
            mapping,
        )


def test_get_relationship_mappings_empty() -> None:
    registry = SchemaRegistry()

    assert registry.get_relationship_mappings() == ()


def test_get_relationship_mappings() -> None:
    registry = SchemaRegistry()

    mapping = make_relationship_mapping()

    registry.register_relationship_mapping(
        mapping,
    )

    mappings = registry.get_relationship_mappings()

    assert mappings == (mapping,)


def test_get_relationship_mappings_for_schema() -> None:
    registry = SchemaRegistry()

    mapping = make_relationship_mapping()

    registry.register_relationship_mapping(
        mapping,
    )

    mappings = registry.get_relationship_mappings_for_schema(
        "Process",
    )

    assert mappings == (mapping,)


def test_get_relationship_mappings_for_unknown_schema() -> None:
    registry = SchemaRegistry()

    mappings = registry.get_relationship_mappings_for_schema(
        "Unknown",
    )

    assert mappings == ()


# ==========================================================
# SchemaDefinition
# ==========================================================


def test_identity_fields_empty() -> None:
    schema = SchemaDefinition(
        name="Process",
        category=SchemaCategory.ENTITY,
        version="1.0",
        fields=[
            FieldDefinition(
                name="pid",
                type=int,
            ),
            FieldDefinition(
                name="name",
                type=str,
            ),
        ],
    )

    assert schema.identity_fields == []


def test_identity_fields_single() -> None:
    schema = SchemaDefinition(
        name="Process",
        category=SchemaCategory.ENTITY,
        version="1.0",
        fields=[
            FieldDefinition(
                name="pid",
                type=int,
                identity=True,
            ),
            FieldDefinition(
                name="name",
                type=str,
            ),
        ],
    )

    identity_fields = schema.identity_fields

    assert len(identity_fields) == 1
    assert identity_fields[0].name == "pid"


def test_identity_fields_multiple() -> None:
    schema = SchemaDefinition(
        name="NetworkConnection",
        category=SchemaCategory.ENTITY,
        version="1.0",
        fields=[
            FieldDefinition(
                name="local_ip",
                type=str,
                identity=True,
            ),
            FieldDefinition(
                name="local_port",
                type=int,
                identity=True,
            ),
            FieldDefinition(
                name="protocol",
                type=str,
            ),
        ],
    )

    identity_fields = schema.identity_fields

    assert len(identity_fields) == 2

    names = {field.name for field in identity_fields}

    assert names == {
        "local_ip",
        "local_port",
    }


# ==========================================================
# RelationshipDefinition
# ==========================================================


def test_relationship_definition() -> None:
    relationship = RelationshipDefinition(
        name="SUPPORTS",
        description="Supports a hypothesis.",
    )

    assert relationship.name == "SUPPORTS"
    assert relationship.description == "Supports a hypothesis."


# ==========================================================
# RelationshipMappingDefinition
# ==========================================================


def test_relationship_mapping_definition() -> None:
    mapping = RelationshipMappingDefinition(
        relationship=RelationshipDefinition(
            name="PARENT_OF",
        ),
        source_schema="Process",
        target_schema="Process",
        source_field="ppid",
        target_field="pid",
    )

    assert mapping.relationship.name == "PARENT_OF"
    assert mapping.source_schema == "Process"
    assert mapping.target_schema == "Process"
    assert mapping.source_field == "ppid"
    assert mapping.target_field == "pid"


# ==========================================================
# Bootstrap
# ==========================================================

from foract.schema.bootstrap import create_schema_registry


def test_bootstrap_registers_builtin_schemas() -> None:
    registry = create_schema_registry()

    #
    # Entity schemas
    #
    assert registry.has_schema("Process")
    assert registry.has_schema("File")
    assert registry.has_schema("Socket")
    assert registry.has_schema("RegistryKey")

    #
    # Operational artifact schemas
    #
    assert registry.has_schema("ExecutionRecord")


def test_bootstrap_registers_builtin_relationships() -> None:
    registry = create_schema_registry()

    assert registry.has_relationship("SUPPORTS")
    assert registry.has_relationship("CONTRADICTS")
    assert registry.has_relationship("GENERATED_FROM")
    assert registry.has_relationship("PART_OF_INVESTIGATION")


def test_bootstrap_registers_relationship_mappings() -> None:
    registry = create_schema_registry()

    mappings = registry.get_relationship_mappings()

    assert len(mappings) > 0


def test_process_has_parent_mapping() -> None:
    registry = create_schema_registry()

    mappings = registry.get_relationship_mappings_for_schema(
        "Process",
    )

    assert len(mappings) == 1

    mapping = mappings[0]

    assert mapping.relationship.name == "PARENT_OF"

    assert mapping.source_schema == "Process"

    assert mapping.target_schema == "Process"

    assert mapping.source_field == "ppid"

    assert mapping.target_field == "pid"


# ==========================================================
# Built-in Ontology
# ==========================================================

from foract.schema.builtin import (
    BUILTIN_RELATIONSHIP_MAPPINGS,
    BUILTIN_RELATIONSHIPS,
    BUILTIN_SCHEMAS,
)


def test_builtin_schema_names() -> None:
    names = {schema.name for schema in BUILTIN_SCHEMAS}

    assert "Process" in names
    assert "File" in names
    assert "Socket" in names
    assert "RegistryKey" in names
    assert "ExecutionRecord" in names


def test_builtin_relationship_names() -> None:
    names = {relationship.name for relationship in BUILTIN_RELATIONSHIPS}

    assert "SUPPORTS" in names
    assert "CONTRADICTS" in names
    assert "GENERATED_FROM" in names
    assert "PART_OF_INVESTIGATION" in names


def test_builtin_relationship_mappings() -> None:
    assert len(BUILTIN_RELATIONSHIP_MAPPINGS) == 1

    mapping = BUILTIN_RELATIONSHIP_MAPPINGS[0]

    assert mapping.relationship.name == "PARENT_OF"

    assert mapping.source_schema == "Process"

    assert mapping.target_schema == "Process"
