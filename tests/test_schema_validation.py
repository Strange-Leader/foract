import pytest

from foract.exceptions import ValidationError
from foract.schema import (
    FieldDefinition,
    SchemaDefinition,
    validate_node,
)


@pytest.fixture
def process_schema() -> SchemaDefinition:
    return SchemaDefinition(
        name="Process",
        version="1.0",
        fields=[
            FieldDefinition(
                name="pid",
                field_type=int,
            ),
            FieldDefinition(
                name="name",
                field_type=str,
            ),
            FieldDefinition(
                name="path",
                field_type=str,
                required=False,
            ),
        ],
    )


def test_valid_node(process_schema: SchemaDefinition) -> None:
    node = {
        "pid": 100,
        "name": "cmd.exe",
    }

    assert validate_node(process_schema, node)


def test_missing_required(process_schema: SchemaDefinition) -> None:
    node = {
        "pid": 100,
    }

    with pytest.raises(ValidationError):
        validate_node(process_schema, node)


def test_optional_field(process_schema: SchemaDefinition) -> None:
    node = {
        "pid": 100,
        "name": "cmd.exe",
    }

    assert validate_node(process_schema, node)


def test_wrong_type(process_schema: SchemaDefinition) -> None:
    node = {
        "pid": "100",
        "name": "cmd.exe",
    }

    with pytest.raises(ValidationError):
        validate_node(process_schema, node)


def test_extra_field(process_schema: SchemaDefinition) -> None:
    node = {
        "pid": 100,
        "name": "cmd.exe",
        "extra": 123,
    }

    assert validate_node(process_schema, node)
