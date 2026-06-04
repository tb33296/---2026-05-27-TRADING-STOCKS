# tests/test_trade_journal_lifecycle.py
from database.db_manager import (
    DatabaseManager
)

from core.journal.trade_journal_manager import (
    TradeJournalManager
)

from core.strategy.trade_context import (
    TradeContext
)

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.positions.position_manager import (
    PositionManager
)

from core.risk.risk_engine import (
    RiskEngine
)

from runtime.trade_pipeline import (
    TradePipeline
)


def test_trade_journal_lifecycle() -> None:

    print(
        "\n=== TRADE JOURNAL LIFECYCLE TEST ===\n"
    )

    # ---------------------------------
    # Infrastructure
    # ---------------------------------

    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    journal_manager = (
        TradeJournalManager(
            db
        )
    )

    position_manager = (
        PositionManager()
    )

    risk_engine = (
        RiskEngine(
            position_manager
        )
    )

    execution_engine = (
        PaperExecutionEngine(
            position_manager
        )
    )

    pipeline = (
        TradePipeline(
            risk_engine=risk_engine,
            execution_engine=execution_engine,
            journal_manager=journal_manager
        )
    )

    # ---------------------------------
    # Trade Context
    # ---------------------------------

    trade_context = (
        TradeContext(
            symbol="RELIANCE",

            segment="EQUITY",

            score=85.0,

            direction="LONG",

            confidence="HIGH",

            reasons=[
                "EMA Bullish",
                "Above VWAP"
            ],

            entry_price=100.0,

            stop_loss=95.0,

            target=110.0
        )
    )

    # ---------------------------------
    # Open Trade
    # ---------------------------------

    decision, risk, execution, sizing = (
        pipeline.execute_trade(
            trade_context=trade_context,
            account_size=100000
        )
    )

    assert decision is not None
    assert risk is not None
    assert execution is not None

    assert execution.success

    print(
        "Trade Opened"
    )

    # ---------------------------------
    # Verify Trade ID
    # ---------------------------------

    position = (
        position_manager
        .get_open_positions()
        .get("RELIANCE")
    )

    assert position is not None

    assert (
        position.trade_id
        is not None
    )

    trade_id = (
        position.trade_id
    )

    print(
        f"Trade ID: "
        f"{trade_id}"
    )

    # ---------------------------------
    # Close Trade
    # ---------------------------------

    result = (
        pipeline.close_trade(
            symbol="RELIANCE",
            exit_price=110.0,
            exit_reason="TARGET"
        )
    )

    assert result is True

    print(
        "Trade Closed"
    )

    # ---------------------------------
    # Verify Journal
    # ---------------------------------

    trade = (
        journal_manager
        .get_trade(
            trade_id
        )
    )

    assert trade is not None

    print(
        "\nTrade Record:"
    )

    print(trade)

    # status column
    assert (
        trade[-1]
        ==
        "CLOSED"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )

    db.close()