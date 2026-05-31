# tests/test_atr.py

from datetime import datetime

from core.indicators.atr import (
    ATR
)

from core.market_data.candle import (
    Candle
)


def test_atr() -> None:

    atr = ATR(
        name="ATR3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3
    )

    candles = [

        Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=45,
            high=48,
            low=41,
            close=45,
            volume=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        ),

        Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=45,
            high=47,
            low=43,
            close=46,
            volume=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        ),

        Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=46,
            high=49,
            low=44,
            close=48,
            volume=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        )

    ]

    for candle in candles:

        atr.update(
            candle
        )

    assert atr.is_ready()

    assert (
        atr.get_value()
        > 0
    )