# tests/test_trade_journal_data.py
from database.db_manager import (
    DatabaseManager
)


def test_trade_journal_data() -> None:

    print(
        "\n=== TRADE JOURNAL DATA ===\n"
    )

    db = DatabaseManager()

    db.connect()

    cursor = db.execute(
        """
        SELECT
            trade_id,
            symbol,
            direction,
            score,
            confidence,
            status
        FROM trades
        """
    )

    rows = cursor.fetchall()

    print(
        f"Trades Found: "
        f"{len(rows)}"
    )

    print()

    for row in rows:

        print(row)

    print(
        "\n=== TRADE REASONS ===\n"
    )

    cursor = db.execute(
        """
        SELECT
            trade_id,
            reason
        FROM trade_reasons
        """
    )

    rows = cursor.fetchall()

    for row in rows:

        print(row)

    db.close()

    print(
        "\n=== TEST COMPLETE ==="
    )