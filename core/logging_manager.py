import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.config import (
    LOG_FOLDER,
    LOG_LEVEL,
    LOG_ROTATION_SIZE,
    SYSTEM_LOG_FILE,
    ERROR_LOG_FILE
)


class LoggingManager:
    """
    Centralized logging manager.
    """

    @staticmethod
    def initialize() -> None:
        """
        Initialize application logging.
        """

        Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        system_handler = RotatingFileHandler(
            SYSTEM_LOG_FILE,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )

        system_handler.setFormatter(formatter)

        error_handler = RotatingFileHandler(
            ERROR_LOG_FILE,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )

        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        logging.basicConfig(
            level=LOG_LEVEL,
            handlers=[
                system_handler,
                error_handler
            ]
        )

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get named logger.
        """

        return logging.getLogger(name)