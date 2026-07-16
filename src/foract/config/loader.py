from functools import cache
from pathlib import Path

import yaml
from pydantic import ValidationError as PydanticValidationError

from foract.config.settings import Settings
from foract.exceptions import ConfigurationError

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "default.yaml"


@cache
def load_settings(path: str | Path | None = None) -> Settings:
    """
    Load and validate the FORACT configuration.
    """
    config_path = Path(path) if path else DEFAULT_CONFIG

    try:
        with config_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError as exc:
        raise ConfigurationError(
            f"Configuration file not found: {config_path}"
        ) from exc
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"Invalid YAML configuration: {config_path}") from exc

    try:
        return Settings.model_validate(data)
    except PydanticValidationError as exc:
        raise ConfigurationError("Configuration validation failed.") from exc


# using @cache is a reasonable optimization here because configuration is typically loaded once and treated as immutable. The tradeoff is that if you later modify config/default.yaml while the process is still running (for example, in a test or during development), load_settings() will continue returning the cached object until the cache is cleared with:  # noqa: E501
