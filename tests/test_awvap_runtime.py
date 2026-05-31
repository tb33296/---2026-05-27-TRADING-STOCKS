# tests/test_awvap_runtime.py

from datetime import datetime

from core.indicators.awvap import (
    AWVAP
)

from core.market_data.candle import (
    Candle
)


def test_awvap_runtime() -> None:

    print(
        "\n=== AWVAP RUNTIME TEST ===\n"
    )

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

    data = [

        (9, 29, 100),
        (9, 30, 105),
        (9, 31, 110),
        (9, 32, 120),
        (9, 33, 130)

    ]

    for hour, minute, close in data:

        candle = Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=close,
            high=close,
            low=close,
            close=close,
            volume=100,
            start_time=datetime(
                2026,
                5,
                30,
                hour,
                minute
            ),
            end_time=datetime(
                2026,
                5,
                30,
                hour,
                minute + 1
            ),
            is_closed=True
        )

        awvap.update(
            candle
        )

        print(
            f"Time={hour:02}:{minute:02} "
            f"AWVAP={round(awvap.get_value(),2)} "
            f"Ready={awvap.is_ready()}"
        )

    print(
        f"\nFinal AWVAP: "
        f"{round(awvap.get_value(),2)}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )