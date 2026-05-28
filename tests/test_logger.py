from core.logging_manager import LoggingManager


def test_logger_creation() -> None:
    LoggingManager.initialize()

    logger = LoggingManager.get_logger("test")

    logger.info("Logger operational")

    assert logger is not None