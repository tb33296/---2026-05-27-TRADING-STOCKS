# tests/test_awvap.py

from datetime import datetime

from core.indicators.awvap import (
    AWVAP
)

from core.market_data.candle import (
    Candle
)


def test_awvap() -> None:

    anchor_time = datetime(
        2026,
        5,
        30,
        9,
        30
    )

    awvap = AWVAP(
        name="OPEN_AWVAP",
        symbol="RELIANCE",
        timeframe="1m",
        anchor_time=anchor_time
    )

    candles = [

        Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=100,
            high=100,
            low=100,
            close=100,
            volume=100,
            start_time=datetime(
                2026,
                5,
                30,
                9,
                29
            ),
            end_time=datetime(
                2026,
                5,
                30,
                9,
                30
            ),
            is_closed=True
        ),

        Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=110,
            high=110,
            low=110,
            close=110,
            volume=100,
            start_time=datetime(
                2026,
                5,
                30,
                9,
                30
            ),
            end_time=datetime(
                2026,
                5,
                30,
                9,
                31
            ),
            is_closed=True
        )

    ]

    for candle in candles:

        awvap.update(
            candle
        )

    assert awvap.is_ready()

    assert (
        round(
            awvap.get_value(),
            2
        )
        ==
        110.00
    )