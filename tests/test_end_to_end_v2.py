#tests/test_end_to_end_v2.py

from datetime import datetime

from core.market_data.candle import (
    Candle
)

from core.indicators.moving_average import (
    MovingAverage
)

from core.signals.crossover_signal import (
    CrossoverSignal
)

from core.strategy.crossover_strategy import (
    CrossoverStrategy
)

from core.positions.position_manager import (
    PositionManager
)

from core.risk.risk_engine import (
    RiskEngine
)

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.trade_management.trade_manager import (
    TradeManager
)


def test_end_to_end_v2() -> None:

    print(
        "\n=== END TO END V2 TEST ===\n"
    )

    # ===================================
    # Infrastructure
    # ===================================

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

    trade_manager = (
        TradeManager(
            position_manager,
            execution_engine
        )
    )

    # ===================================
    # Indicators
    # ===================================

    ema_fast = MovingAverage(
        name="EMA3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3,
        ma_type="EMA"
    )

    ema_slow = MovingAverage(
        name="EMA5",
        symbol="RELIANCE",
        timeframe="1m",
        period=5,
        ma_type="EMA"
    )

    signal_generator = (
        CrossoverSignal(
            name="EMA_CROSS",
            fast_indicator=ema_fast,
            slow_indicator=ema_slow
        )
    )

    strategy = (
        CrossoverStrategy(
            name="EMA_STRATEGY",
            symbol="RELIANCE",
            timeframe="1m"
        )
    )

    # ===================================
    # Price Series
    # ===================================

    prices = [
        100,
        99,
        98,
        97,
        96,
        110,
        120,
        130
    ]

    position_opened = False

    # ===================================
    # Runtime Loop
    # ===================================

    for price in prices:

        candle = Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=price,
            high=price,
            low=price,
            close=price,
            volume=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        )

        ema_fast.update(
            candle
        )

        ema_slow.update(
            candle
        )

        signal = (
            signal_generator.evaluate()
        )

        if signal is None:

            continue

        print(
            f"Signal: "
            f"{signal.signal_type}"
        )

        action = (
            strategy.on_signal(
                signal
            )
        )

        if action is None:

            continue

        print(
            f"Strategy Action: "
            f"{action.signal_type}"
        )

        decision = (
            risk_engine.evaluate(
                action
            )
        )

        print(
            f"Risk: "
            f"{decision.reason}"
        )

        assert (
            decision.approved
        )

        result = (
            execution_engine.execute_buy(
                symbol="RELIANCE",
                segment="EQUITY",
                quantity=100,
                ltp=price,
                stop_loss=95,
                target=110
            )
        )

        print(
            f"Execution: "
            f"{result.message}"
        )

        assert (
            result.success
        )

        position_opened = True

        break

    # ===================================
    # Validate Entry
    # ===================================

    assert position_opened

    assert (
        position_manager
        .get_open_position_count()
        == 1
    )

    print(
        "\nPosition Opened"
    )

    # ===================================
    # Simulate Target Hit
    # ===================================

    closed = (
        trade_manager.evaluate_position(
            symbol="RELIANCE",
            current_price=110
        )
    )

    assert closed

    # ===================================
    # Validate Exit
    # ===================================

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
        f"Net PnL: "
        f"{position_manager.get_total_net_pnl()}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )