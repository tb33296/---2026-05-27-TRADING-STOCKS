from database.db_manager import (
    DatabaseManager
)


def test_trade_database_schema() -> None:

    print(
        "\n=== TRADE DATABASE SCHEMA TEST ===\n"
    )

    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    cursor = db.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = {
        row[0]
        for row in cursor.fetchall()
    }

    required_tables = {

        "trades",

        "trade_reasons",

        "trade_metrics_snapshot",

        "trade_feature_snapshot"
    }

    for table_name in sorted(
        required_tables
    ):

        print(
            f"Found: "
            f"{table_name}"
        )

        assert (
            table_name
            in tables
        )

    db.close()

    print(
        "\n=== TEST COMPLETE ==="
    )