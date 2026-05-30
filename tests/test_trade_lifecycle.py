# tests/test_trade_lifecycle.py

from datetime import datetime

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.indicators.moving_average import (
    MovingAverage
)

from core.market_data.candle import (
    Candle
)

from core.positions.position_manager import (
    PositionManager
)

from core.risk.risk_engine import (
    RiskEngine
)

from core.signals.crossover_signal import (
    CrossoverSignal
)


def test_trade_lifecycle() -> None:

    print(
        "\n=== TRADE LIFECYCLE TEST ===\n"
    )

    # ---------------------------------
    # Infrastructure
    # ---------------------------------

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

    # ---------------------------------
    # Indicators
    # ---------------------------------

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

    crossover = (
        CrossoverSignal(
            name="EMA3_EMA5",
            fast_indicator=ema_fast,
            slow_indicator=ema_slow
        )
    )

    # ---------------------------------
    # Price Series
    # ---------------------------------

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

    trade_opened = False

    # ---------------------------------
    # Feed Candles
    # ---------------------------------

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
            crossover.evaluate()
        )

        if signal is None:

            continue

        print(
            f"Signal Generated: "
            f"{signal.signal_type}"
        )

        # -----------------------------
        # Risk Check
        # -----------------------------

        decision = (
            risk_engine.evaluate(
                signal
            )
        )

        print(
            f"Risk Decision: "
            f"{decision.reason}"
        )

        assert (
            decision.approved
        )

        # -----------------------------
        # Execute
        # -----------------------------

        result = (
            execution_engine.execute_buy(
                symbol="RELIANCE",
                segment="EQUITY",
                quantity=100,
                ltp=price,
                stop_loss=95.0,
                target=140.0
            )
        )

        print(
            f"Execution: "
            f"{result.message}"
        )

        assert (
            result.success
        )

        trade_opened = True

    # ---------------------------------
    # Validation
    # ---------------------------------

    assert trade_opened

    assert (
        position_manager
        .get_open_position_count()
        == 1
    )

    print(
        "\nOpen Positions:"
    )

    print(
        position_manager
        .get_open_position_count()
    )

    print(
        "\n=== TEST COMPLETE ==="
    )