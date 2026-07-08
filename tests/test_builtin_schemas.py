import pytest

from foract.exceptions import RegistryError
from foract.registry import SchemaRegistry
from foract.schema import register_builtin_schemas


def test_register_builtin_schemas() -> None:
    registry = SchemaRegistry()

    register_builtin_schemas(registry)

    assert len(registry) == 6


def test_builtin_schema_names() -> None:
    registry = SchemaRegistry()

    register_builtin_schemas(registry)

    assert registry.exists("Process")
    assert registry.exists("File")
    assert registry.exists("PE")
    assert registry.exists("Socket")
    assert registry.exists("RegistryKey")
    assert registry.exists("ExecutionRecord")


def test_get_builtin_schemas() -> None:
    registry = SchemaRegistry()

    register_builtin_schemas(registry)

    assert registry.get("Process").name == "Process"
    assert registry.get("File").name == "File"
    assert registry.get("PE").name == "PE"
    assert registry.get("Socket").name == "Socket"
    assert registry.get("RegistryKey").name == "RegistryKey"
    assert registry.get("ExecutionRecord").name == "ExecutionRecord"


def test_duplicate_builtin_registration() -> None:
    registry = SchemaRegistry()

    register_builtin_schemas(registry)

    with pytest.raises(RegistryError):
        register_builtin_schemas(registry)
