from database.db_manager import DatabaseManager


def test_database_connection() -> None:
    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    assert db.connection is not None

    db.close()