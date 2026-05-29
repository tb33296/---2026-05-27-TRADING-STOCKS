# tests/test_timeframe_manager.py

from datetime import datetime

from config.config import (
    MARKET_HOLIDAY_FILE
)

from core.market_data.market_clock import (
    MarketClock
)

from core.market_data.timeframe_manager import (
    TimeframeManager
)


def test_timeframe_manager() -> None:

    print(
        "\n=== TIMEFRAME MANAGER TEST ===\n"
    )

    market_clock = MarketClock(
        MARKET_HOLIDAY_FILE
    )

    manager = TimeframeManager(
        market_clock
    )

    print(
        "Registered Timeframes:"
    )

    print(
        manager.get_registered_timeframes()
    )

    # =================================================
    # Minute 09:30
    # =================================================

    ticks = [

        {
            "symbol": "RELIANCE",
            "token": "2885",
            "ltp": 100.0,
            "volume": 10,
            "timestamp": datetime(
                2026, 5, 29,
                9, 30, 10
            )
        },

        {
            "symbol": "RELIANCE",
            "token": "2885",
            "ltp": 105.0,
            "volume": 20,
            "timestamp": datetime(
                2026, 5, 29,
                9, 30, 30
            )
        },

        {
            "symbol": "RELIANCE",
            "token": "2885",
            "ltp": 95.0,
            "volume": 30,
            "timestamp": datetime(
                2026, 5, 29,
                9, 30, 50
            )
        },

        # =============================================
        # Minute 09:31
        # =============================================

        {
            "symbol": "RELIANCE",
            "token": "2885",
            "ltp": 102.0,
            "volume": 40,
            "timestamp": datetime(
                2026, 5, 29,
                9, 31, 5
            )
        },

        {
            "symbol": "RELIANCE",
            "token": "2885",
            "ltp": 110.0,
            "volume": 50,
            "timestamp": datetime(
                2026, 5, 29,
                9, 31, 30
            )
        },

        # =============================================
        # Minute 09:35
        # Forces 5m rollover
        # =============================================

        {
            "symbol": "RELIANCE",
            "token": "2885",
            "ltp": 115.0,
            "volume": 60,
            "timestamp": datetime(
                2026, 5, 29,
                9, 35, 5
            )
        },

        # =============================================
        # Minute 09:45
        # Forces 15m rollover
        # =============================================

        {
            "symbol": "RELIANCE",
            "token": "2885",
            "ltp": 120.0,
            "volume": 70,
            "timestamp": datetime(
                2026, 5, 29,
                9, 45, 5
            )
        }

    ]

    all_closed = []

    for tick in ticks:

        closed = manager.process_tick(
            tick
        )

        if closed:

            all_closed.extend(
                closed
            )

    print(
        "\nClosed Candles:\n"
    )

    for candle in all_closed:

        print(
            candle
        )

    print(
        "\nCurrent Candles:\n"
    )

    for timeframe in (
        manager.get_registered_timeframes()
    ):

        candle = (
            manager.get_current_candle(
                symbol="RELIANCE",
                timeframe=timeframe
            )
        )

        print(
            f"{timeframe}:"
        )

        print(
            candle
        )

        print()

    # =================================================
    # Validation
    # =================================================

    assert (
        manager.timeframe_exists(
            "1m"
        )
    )

    assert (
        manager.timeframe_exists(
            "5m"
        )
    )

    assert (
        manager.timeframe_exists(
            "15m"
        )
    )

    current_1m = (
        manager.get_current_candle(
            "RELIANCE",
            "1m"
        )
    )

    current_5m = (
        manager.get_current_candle(
            "RELIANCE",
            "5m"
        )
    )

    current_15m = (
        manager.get_current_candle(
            "RELIANCE",
            "15m"
        )
    )

    assert current_1m is not None
    assert current_5m is not None
    assert current_15m is not None

    print(
        "\n=== TEST COMPLETE ==="
    )