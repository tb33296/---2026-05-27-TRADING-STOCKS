# tests/test_vwap_signal.py

from datetime import datetime

from core.indicators.vwap import VWAP

from core.market_data.candle import (
    Candle
)

from core.market_data.market_clock import (
    MarketClock
)

from core.signals.vwap_signal import (
    VWAPSignal
)


def test_vwap_signal() -> None:

    print(
        "\n=== VWAP SIGNAL TEST ===\n"
    )

    market_clock = MarketClock(
        holiday_file=""
    )

    vwap = VWAP(
        name="VWAP",
        symbol="RELIANCE",
        timeframe="1m",
        market_clock=market_clock
    )

    signal_engine = VWAPSignal(
        name="VWAP_CROSS",
        vwap_indicator=vwap
    )

    candles = [

        # VWAP initialization

        (100, 100),
        (100, 100),
        (100, 100),

        # Move above VWAP

        (105, 100),

        # Stay above

        (110, 100),

        # Move below VWAP

        (95, 100)

    ]

    for close_price, volume in candles:

        candle = Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=close_price,
            high=close_price,
            low=close_price,
            close=close_price,
            volume=volume,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        )

        vwap.update(
            candle
        )

        signal = (
            signal_engine.evaluate(
                candle
            )
        )

        print(
            f"Close={close_price} "
            f"VWAP={round(vwap.get_value(),2)}"
        )

        if signal:

            print(
                f"SIGNAL="
                f"{signal.signal_type}"
            )

    print(
        "\n=== TEST COMPLETE ==="
    )