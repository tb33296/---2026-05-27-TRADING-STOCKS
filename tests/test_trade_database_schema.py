# tests/test_trade_database_schema.py

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

    # =====================================
    # Verify Tables
    # =====================================

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
            f"Found Table: "
            f"{table_name}"
        )

        assert (
            table_name
            in tables
        )

    # =====================================
    # Verify Trades Columns
    # =====================================

    cursor = db.execute(
        """
        PRAGMA table_info(trades)
        """
    )

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    expected_columns = {

        "trade_id",

        "symbol",

        "segment",

        "strategy_name",

        "direction",

        "entry_time",

        "exit_time",

        "quantity",

        "entry_price",

        "exit_price",

        "stop_loss",

        "target",

        "score",

        "confidence",

        "risk_amount",

        "risk_percent",

        "gross_pnl",

        "net_pnl",

        "charges",

        "exit_reason",

        "trade_duration_seconds",

        "status"
    }

    print(
        "\nTrades Table Columns:"
    )

    for column in sorted(
        expected_columns
    ):

        print(
            f"  {column}"
        )

        assert (
            column
            in columns
        )

    db.close()

    print(
        "\n=== TEST COMPLETE ==="
    )