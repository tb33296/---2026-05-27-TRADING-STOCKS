# tests/test_atr_runtime.py

from datetime import datetime

from core.indicators.atr import (
    ATR
)

from core.market_data.candle import (
    Candle
)


def test_atr_runtime() -> None:

    print(
        "\n=== ATR RUNTIME TEST ===\n"
    )

    atr = ATR(
        name="ATR3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3
    )

    data = [

        (48, 41, 45),
        (47, 43, 46),
        (49, 44, 48),
        (50, 45, 49),
        (52, 46, 51)

    ]

    for high, low, close in data:

        candle = Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=close,
            high=high,
            low=low,
            close=close,
            volume=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True
        )

        atr.update(
            candle
        )

        print(
            f"ATR={atr.get_value()}  "
            f"Ready={atr.is_ready()}"
        )

    print(
        f"\nFinal ATR: "
        f"{atr.get_value()}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )