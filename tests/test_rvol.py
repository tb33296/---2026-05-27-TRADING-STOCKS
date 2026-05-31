# tests/test_rvol.py

from datetime import datetime

from core.indicators.rvol import (
    RVOL
)

from core.market_data.candle import (
    Candle
)


def test_rvol() -> None:

    rvol = RVOL(
        name="RVOL3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3
    )

    volumes = [
        100,
        100,
        300
    ]

    for volume in volumes:

        candle = Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=100,
            high=100,
            low=100,
            close=100,
            volume=volume,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        )

        rvol.update(
            candle
        )

    assert rvol.is_ready()

    assert (
        round(
            rvol.get_value(),
            2
        )
        ==
        1.80
    )