# tests/test_cvd_runtime.py

from core.indicators.cvd import (
    CVD
)


def test_cvd_runtime() -> None:

    print(
        "\n=== CVD TEST ===\n"
    )

    cvd = CVD(
        name="CVD",
        symbol="RELIANCE",
        timeframe="1m"
    )

    ticks = [

        (100, 100),

        (101, 50),

        (102, 60),

        (101, 20),

        (103, 100),

        (102, 50)

    ]

    for price, volume in ticks:

        cvd.update(
            price,
            volume
        )

        print(
            f"Price={price} "
            f"Volume={volume} "
            f"Delta={cvd.get_delta()} "
            f"CVD={cvd.get_cvd()}"
        )

    print(
        f"\nBuy Volume: "
        f"{cvd.get_buy_volume()}"
    )

    print(
        f"Sell Volume: "
        f"{cvd.get_sell_volume()}"
    )

    print(
        f"CVD: "
        f"{cvd.get_cvd()}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )