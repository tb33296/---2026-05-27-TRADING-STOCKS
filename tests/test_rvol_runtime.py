# tests/test_rvol_runtime.py

from datetime import datetime

from core.indicators.rvol import (
    RVOL
)

from core.market_data.candle import (
    Candle
)


def test_rvol_runtime() -> None:

    print(
        "\n=== RVOL RUNTIME TEST ===\n"
    )

    rvol = RVOL(
        name="RVOL3",
        symbol="RELIANCE",
        timeframe="1m",
        period=3
    )

    volumes = [
        100,
        100,
        300,
        500,
        1000
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

        print(
            f"Volume={volume}  "
            f"RVOL={rvol.get_value()}  "
            f"Ready={rvol.is_ready()}"
        )

    print(
        f"\nFinal RVOL: "
        f"{rvol.get_value()}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )