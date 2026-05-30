# tests/test_indicator_runtime.py

from datetime import datetime

from runtime.indicator_runtime import (
    IndicatorRuntime
)

from core.market_data.candle import (
    Candle
)

from core.indicators.moving_average import (
    MovingAverage
)


def test_indicator_runtime() -> None:

    print(
        "\n=== INDICATOR RUNTIME TEST ===\n"
    )

    # ---------------------------------
    # Runtime
    # ---------------------------------

    runtime = IndicatorRuntime()

    # ---------------------------------
    # Register Indicator
    # ---------------------------------

    ema = MovingAverage(
        name="EMA3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3,
        ma_type="EMA"
    )

    assert (
        runtime.register_indicator(
            ema
        )
        is True
    )

    print(
        "Registered EMA3"
    )

    # ---------------------------------
    # Closed Candles
    # ---------------------------------

    closes = [
        100.0,
        105.0,
        110.0,
        120.0,
        130.0
    ]

    for close_price in closes:

        candle = Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=close_price,
            high=close_price,
            low=close_price,
            close=close_price,
            volume=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        )

        runtime.process_closed_candle(
            candle
        )

        value = (
            runtime.get_indicator_value(
                symbol="RELIANCE",
                timeframe="1m",
                indicator_name="EMA3"
            )
        )

        print(
            f"Close={close_price}"
            f"  EMA={value}"
            f"  Ready={ema.is_ready()}"
        )

    # ---------------------------------
    # Validation
    # ---------------------------------

    assert ema.is_ready()

    final_value = (
        runtime.get_indicator_value(
            symbol="RELIANCE",
            timeframe="1m",
            indicator_name="EMA3"
        )
    )

    assert final_value is not None

    print(
        f"\nFinal EMA: "
        f"{final_value:.2f}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )