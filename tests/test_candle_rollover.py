# tests/test_candle_rollover.py

from datetime import datetime

from config.config import (
    MARKET_HOLIDAY_FILE
)

from core.market_data.market_clock import (
    MarketClock
)

from core.market_data.candle_builder import (
    CandleBuilder
)


def test_candle_rollover() -> None:

    print(
        "\n=== CANDLE ROLLOVER TEST ===\n"
    )

    market_clock = MarketClock(
        MARKET_HOLIDAY_FILE
    )

    builder = CandleBuilder(
        market_clock
    )

    # -----------------------------------
    # Tick 1
    # -----------------------------------

    tick1 = {
        "symbol": "RELIANCE",
        "token": "2885",
        "ltp": 100.0,
        "volume": 10,
        "timestamp": datetime(
            2026, 5, 29,
            9, 30, 10
        )
    }

    builder.process_tick(
        tick1,
        timeframe="1m"
    )

    # -----------------------------------
    # Tick 2
    # -----------------------------------

    tick2 = {
        "symbol": "RELIANCE",
        "token": "2885",
        "ltp": 105.0,
        "volume": 20,
        "timestamp": datetime(
            2026, 5, 29,
            9, 30, 20
        )
    }

    builder.process_tick(
        tick2,
        timeframe="1m"
    )

    # -----------------------------------
    # Tick 3
    # -----------------------------------

    tick3 = {
        "symbol": "RELIANCE",
        "token": "2885",
        "ltp": 95.0,
        "volume": 30,
        "timestamp": datetime(
            2026, 5, 29,
            9, 30, 50
        )
    }

    builder.process_tick(
        tick3,
        timeframe="1m"
    )

    # -----------------------------------
    # Tick 4
    # New Minute
    # -----------------------------------

    tick4 = {
        "symbol": "RELIANCE",
        "token": "2885",
        "ltp": 102.0,
        "volume": 40,
        "timestamp": datetime(
            2026, 5, 29,
            9, 31, 5
        )
    }

    closed_candle = (
        builder.process_tick(
            tick4,
            timeframe="1m"
        )
    )

    print(
        "Closed Candle:"
    )

    print(
        closed_candle
    )

    current_candle = (
        builder.get_current_candle(
            "RELIANCE",
            "1m"
        )
    )

    print(
        "\nCurrent Candle:"
    )

    print(
        current_candle
    )

    # -----------------------------------
    # Validation
    # -----------------------------------

    assert closed_candle is not None

    assert closed_candle.open == 100.0

    assert closed_candle.high == 105.0

    assert closed_candle.low == 95.0

    assert closed_candle.close == 95.0

    assert closed_candle.volume == 60

    assert closed_candle.is_closed is True

    assert current_candle is not None

    assert current_candle.open == 102.0

    assert current_candle.high == 102.0

    assert current_candle.low == 102.0

    assert current_candle.close == 102.0

    print(
        "\n=== TEST COMPLETE ==="
    )