from foract.exceptions import (
    ConfigurationError,
    FORACTError,
    PluginError,
    RegistryError,
    SchemaError,
    ValidationError,
)


def test_configuration_error_inheritance() -> None:
    assert issubclass(ConfigurationError, FORACTError)


def test_registry_error_inheritance() -> None:
    assert issubclass(RegistryError, FORACTError)


def test_schema_error_inheritance() -> None:
    assert issubclass(SchemaError, RegistryError)


def test_plugin_error_inheritance() -> None:
    assert issubclass(PluginError, RegistryError)


def test_validation_error_inheritance() -> None:
    assert issubclass(ValidationError, FORACTError)
