# tests/test_trading_cycle_engine.py

from datetime import datetime

from core.websocket.tick_queue import (
    TickQueue
)

from runtime.tick_processor import (
    TickProcessor
)

from runtime.candle_runtime import (
    CandleRuntime
)

from runtime.indicator_runtime import (
    IndicatorRuntime
)

from runtime.trading_runtime import (
    TradingRuntime
)

from runtime.trading_cycle_engine import (
    TradingCycleEngine
)

from core.positions.position_manager import (
    PositionManager
)

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
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

from core.trade_management.trade_manager import (
    TradeManager
)


def test_trading_cycle_engine() -> None:

    print(
        "\n=== TRADING CYCLE ENGINE TEST ===\n"
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

    candle_runtime = (
        CandleRuntime(
            tick_processor
        )
    )

    indicator_runtime = (
        IndicatorRuntime()
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

    trading_runtime = (
        TradingRuntime(
            tick_processor,
            trade_manager
        )
    )

    cycle_engine = (
        TradingCycleEngine(
            tick_processor=tick_processor,
            candle_runtime=candle_runtime,
            indicator_runtime=indicator_runtime,
            trading_runtime=trading_runtime
        )
    )

    # ----------------------------------
    # Feed Tick
    # ----------------------------------

    tick_queue.enqueue(
        {
            "symbol": "RELIANCE",
            "ltp": 100.0,
            "volume": 100,
            "timestamp": datetime.now()
        }
    )

    # ----------------------------------
    # Execute Cycle
    # ----------------------------------

    closed_positions = (
        cycle_engine.process_cycle()
    )

    print(
        f"Closed Positions: "
        f"{closed_positions}"
    )

    # ----------------------------------
    # Validation
    # ----------------------------------

    assert (
        tick_processor
        .get_total_processed()
        == 1
    )

    candle = (
        candle_runtime
        .get_current_candle(
            "RELIANCE"
        )
    )

    assert candle is not None

    print(
        f"Current Candle Close: "
        f"{candle.close}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )

    db.close()