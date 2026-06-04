# tests/test_candle_indicator_runtime.py

from datetime import datetime
from datetime import timedelta

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

from core.indicators.moving_average import (
    MovingAverage
)


def test_candle_indicator_runtime() -> None:

    print(
        "\n=== CANDLE -> INDICATOR TEST ===\n"
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

    # ----------------------------------
    # Indicator
    # ----------------------------------

    ema = MovingAverage(
        name="EMA3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3,
        ma_type="EMA"
    )

    registered = (
        indicator_runtime
        .register_indicator(
            ema
        )
    )

    assert registered

    # ----------------------------------
    # Tick 1
    # Creates candle
    # ----------------------------------

    tick_queue.enqueue(
        {
            "symbol": "RELIANCE",
            "ltp": 100.0,
            "volume": 100,
            "timestamp": datetime(
                2026, 6, 4, 10, 0, 0
            )
        }
    )

    tick_processor.process_all_available()

    closed_candles = (
        candle_runtime.process_ticks()
    )

    assert len(
        closed_candles
    ) == 0

    # ----------------------------------
    # Tick 2
    # Forces rollover
    # ----------------------------------

    tick_queue.enqueue(
        {
            "symbol": "RELIANCE",
            "ltp": 101.0,
            "volume": 100,
            "timestamp": datetime(
                2026, 6, 4, 10, 1, 0
            )
        }
    )

    tick_processor.process_all_available()

    closed_candles = (
        candle_runtime.process_ticks()
    )

    print(
        f"Closed Candles: "
        f"{len(closed_candles)}"
    )

    assert len(
        closed_candles
    ) == 1

    # ----------------------------------
    # Update Indicators
    # ----------------------------------

    for candle in closed_candles:

        indicator_runtime\
            .process_closed_candle(
                candle
            )

    # ----------------------------------
    # Validation
    # ----------------------------------

    value = (
        indicator_runtime
        .get_indicator_value(
            symbol="RELIANCE",
            timeframe="1m",
            indicator_name="EMA3"
        )
    )

    print(
        f"EMA Value: {value}"
    )

    assert value is not None

    print(
        "\n=== TEST COMPLETE ==="
    )