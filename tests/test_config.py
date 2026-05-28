from config.config import (
    TIMEZONE,
    SQLITE_DB_PATH
)


def test_config_loaded() -> None:
    assert TIMEZONE == "Asia/Kolkata"
    assert SQLITE_DB_PATH is not None