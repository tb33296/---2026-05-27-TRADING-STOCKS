#tests/test_moving_average.py
from datetime import datetime

from core.market_data.candle import Candle
from core.indicators.moving_average import (
    MovingAverage
)


def test_moving_average() -> None:

    print(
        "\n=== MOVING AVERAGE TEST ===\n"
    )

    ma = MovingAverage(
        name="EMA3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3,
        ma_type="EMA"
    )

    prices = [
        100,
        105,
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
            end_time=datetime.now()
        )

        ma.update(candle)

        print(
            f"Close={price} "
            f"EMA={ma.get_value():.2f} "
            f"Ready={ma.is_ready()}"
        )

    assert ma.is_ready()

    print(
        "\n=== TEST COMPLETE ==="
    )