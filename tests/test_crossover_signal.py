# tests/test_crossover_signal.py
from datetime import datetime

from core.market_data.candle import Candle

from core.indicators.moving_average import (
    MovingAverage
)

from core.signals.crossover_signal import (
    CrossoverSignal
)


def test_crossover_signal() -> None:

    print(
        "\n=== CROSSOVER TEST ===\n"
    )

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

    crossover = CrossoverSignal(
        name="EMA3_EMA5",
        fast_indicator=ema_fast,
        slow_indicator=ema_slow
    )

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

        ema_fast.update(candle)
        ema_slow.update(candle)

        signal = crossover.evaluate()

        print(
            f"Close={price}"
        )

        print(
            f"EMA3="
            f"{ema_fast.get_value():.2f}"
        )

        print(
            f"EMA5="
            f"{ema_slow.get_value():.2f}"
        )

        if signal:

            print(
                f"SIGNAL="
                f"{signal.signal_type}"
            )

            assert (
                signal.signal_type
                == "BUY"
            )

    print(
        "\n=== TEST COMPLETE ==="
    )