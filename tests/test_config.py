from foract.config import load_settings
from foract.config.settings import Settings


def test_load_settings_returns_settings() -> None:
    settings = load_settings()

    assert isinstance(settings, Settings)


def test_project_configuration() -> None:
    settings = load_settings()

    assert settings.project.name == "FORACT"
    assert settings.project.version == "0.1.0"
    assert settings.project.debug is False


def test_logging_configuration() -> None:
    settings = load_settings()

    assert settings.logging.level == "INFO"
    assert settings.logging.file == "logs/foract.log"


def test_registry_configuration() -> None:
    settings = load_settings()

    assert settings.registry.auto_discover is True
    assert settings.registry.plugin_directory == "plugins"
