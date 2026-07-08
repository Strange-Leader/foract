import logging

from foract.config import load_settings
from foract.log import configure_logging, get_logger


def test_get_logger_returns_logger() -> None:
    logger = get_logger(__name__)

    assert isinstance(logger, logging.Logger)


def test_configure_logging() -> None:
    settings = load_settings()

    configure_logging(settings)

    logger = get_logger(__name__)
    logger.info("Test log message")
