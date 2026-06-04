# tests/test_trading_runtime.py
# tests/test_trading_runtime.py

from datetime import datetime

from runtime.trading_runtime import (
    TradingRuntime
)

from runtime.tick_processor import (
    TickProcessor
)

from core.websocket.tick_queue import (
    TickQueue
)

from core.positions.position_manager import (
    PositionManager
)

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.trade_management.trade_manager import (
    TradeManager
)
from core.risk.risk_engine import (
    RiskEngine
)

from runtime.trade_pipeline import (
    TradePipeline
)

from core.journal.trade_journal_manager import (
    TradeJournalManager
)

from database.db_manager import (
    DatabaseManager
)

def test_trading_runtime() -> None:

    print(
        "\n=== TRADING RUNTIME TEST ===\n"
    )

    # ----------------------------------
    # Infrastructure
    # ----------------------------------

    tick_queue = TickQueue(
        max_size=100
    )

    tick_processor = TickProcessor(
        tick_queue
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

    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    journal_manager = (
        TradeJournalManager(
            db
        )
    )

    trade_pipeline = (
        TradePipeline(
            risk_engine=risk_engine,
            execution_engine=execution_engine,
            journal_manager=journal_manager
        )
    )

    trade_manager = (
        TradeManager(
            position_manager,
            trade_pipeline
        )
    )

    runtime = (
        TradingRuntime(
            tick_processor,
            trade_manager
        )
    )

    # ----------------------------------
    # Open Position
    # ----------------------------------

    result = (
        execution_engine.execute_buy(
            symbol="RELIANCE",
            segment="EQUITY",
            quantity=100,
            ltp=100,
            stop_loss=95,
            target=110
        )
    )

    assert result.success

    print(
        "Position Opened"
    )

    # ----------------------------------
    # Feed Tick
    # ----------------------------------

    tick_queue.enqueue(
        {
            "symbol": "RELIANCE",
            "ltp": 110.0,
            "timestamp": (
                datetime.now()
            )
        }
    )

    tick_processor.process_all_available()

    # ----------------------------------
    # Runtime Evaluation
    # ----------------------------------

    closed = (
        runtime.process_market()
    )

    print(
        f"Positions Closed: "
        f"{closed}"
    )

    assert closed == 0
    # Expected.
    # Trade opened directly through
    # PaperExecutionEngine.
    # No trade_id assigned.

    # ----------------------------------
    # Validation
    # ----------------------------------

    assert (
        position_manager
        .get_open_position_count()
        == 0
    )

    assert (
        len(
            position_manager
            .get_closed_positions()
        )
        == 1
    )

    print(
        "\nPosition Closed"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )