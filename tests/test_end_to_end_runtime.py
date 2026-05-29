
# tests/test_end_to_end_runtime.py

from datetime import datetime
from pathlib import Path

from database.db_manager import (
    DatabaseManager
)

from core.execution.paper_broker import (
    PaperBroker
)

from core.execution.tradebook import (
    Tradebook
)

from core.indicators.moving_average import (
    MovingAverage
)

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle

from core.signals.crossover_signal import (
    CrossoverSignal
)

from core.strategy.crossover_strategy import (
    CrossoverStrategy
)


def test_end_to_end_runtime() -> None:

    LoggingManager.initialize()

    print(
        "\n=== STARTING "
        "END-TO-END TEST ===\n"
    )

    # ========================================
    # Database Setup
    # ========================================

  
    database_manager = (
        DatabaseManager()
    )

    database_manager.connect()

    database_manager.initialize_schema()



    # ========================================
    # Tradebook
    # ========================================

    tradebook = Tradebook(
        database_manager
    )

    # ========================================
    # Paper Broker
    # ========================================

    paper_broker = PaperBroker(
        tradebook
    )

    # ========================================
    # Indicators
    # ========================================

    fast_ema = MovingAverage(
        name="EMA_FAST",

        symbol="TEST",

        timeframe="1m",

        period=2,

        ma_type="EMA"
    )

    slow_ema = MovingAverage(
        name="EMA_SLOW",

        symbol="TEST",

        timeframe="1m",

        period=3,

        ma_type="EMA"
    )

    # ========================================
    # Signal Generator
    # ========================================

    crossover_signal = (
        CrossoverSignal(
            name="EMA_CROSS",

            fast_indicator=fast_ema,

            slow_indicator=slow_ema
        )
    )

    # ========================================
    # Strategy
    # ========================================

    strategy = CrossoverStrategy(
        name="EMA_STRATEGY",

        symbol="TEST",

        timeframe="1m"
    )

    # ========================================
    # Test Candle Data
    # ========================================

    prices = [
        107,
        105,
        102,
        99,
        100,
        102,
        105,
        108,
        104,
        100,
        96
    ]


    generated_signals = []

    strategy_actions = []

    # ========================================
    # Runtime Loop
    # ========================================

    for index, price in enumerate(
        prices
    ):

        candle = Candle(
            symbol="TEST",

            timeframe="1m",

            start_time=datetime.now(),

            end_time=datetime.now(),

            open=price,

            high=price,

            low=price,

            close=price,

            volume=100
        )

        # ====================================
        # Indicator Updates
        # ====================================

        fast_ema.update(candle)

        slow_ema.update(candle)

        # ====================================
        # Skip Until Ready
        # ====================================

        if not (
            fast_ema.is_ready()
            and
            slow_ema.is_ready()
        ):

            continue

        # ====================================
        # Signal Evaluation
        # ====================================

        signal = (
            crossover_signal.evaluate()
        )

        if signal is None:

            continue

        generated_signals.append(
            signal
        )

        print(
            f"Signal Generated: "
            f"{signal.signal_type}"
        )

        # ====================================
        # Strategy Processing
        # ====================================

        action = strategy.on_signal(
            signal
        )

        if action is None:

            continue

        strategy_actions.append(
            action
        )

        print(
            f"Strategy Action: "
            f"{action.signal_type}"
        )

        # ====================================
        # Create Order
        # ====================================

        if action.is_buy():

            order = (
                paper_broker
                .create_market_order(
                    symbol="TEST",

                    side="BUY",

                    price=price,

                    strategy_name=(
                        strategy.get_name()
                    )
                )
            )

            executed = (
                paper_broker
                .execute_order(order)
            )

            assert executed is True

        elif action.is_exit():

            order = (
                paper_broker
                .create_market_order(
                    symbol="TEST",

                    side="SELL",

                    price=price,

                    strategy_name=(
                        strategy.get_name()
                    )
                )
            )

            executed = (
                paper_broker
                .execute_order(order)
            )

            assert executed is True

    # ========================================
    # Runtime Assertions
    # ========================================

    assert (
        fast_ema.is_ready()
    )

    assert (
        slow_ema.is_ready()
    )

    assert (
        len(generated_signals)
        >= 1
    )

    assert (
        len(strategy_actions)
        >= 1
    )

    # ========================================
    # Tradebook Validation
    # ========================================

    total_trades = (
        tradebook.total_trades()
    )

    print(
        f"\nTotal Trades: "
        f"{total_trades}"
    )

    assert total_trades >= 1

    print(
        f"Total PnL: "
        f"{tradebook.total_pnl():.2f}"
    )

    print(
        f"Win Rate: "
        f"{tradebook.win_rate():.2f}%"
    )

    # ========================================
    # SQLite Validation
    # ========================================

    query = """
    SELECT
        symbol,
        side,
        quantity,
        pnl
    FROM trades
    """

    cursor = database_manager.execute( query ) 
    rows = cursor.fetchall()

    assert len(rows) >= 1

    print(
        "\nPersisted Trades:"
    )

    for row in rows:

        print(row)

    print(
        "\n=== END-TO-END "
        "TEST COMPLETE ===\n"
    )
