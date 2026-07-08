from __future__ import annotations

import logging
from pathlib import Path

from foract.config.settings import Settings


def configure_logging(settings: Settings) -> None:
    """
    Configure the global FORACT logging system.

    This function is safe to call multiple times. Logging will only be
    configured once.
    """
    root_logger = logging.getLogger()

    # Already configured
    if root_logger.handlers:
        return

    log_file = Path(settings.logging.file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    handlers: list[logging.Handler] = [
        logging.FileHandler(log_file, encoding="utf-8"),
    ]

    if settings.logging.console:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=getattr(logging, settings.logging.level.value),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the given module.

    Example:
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)
