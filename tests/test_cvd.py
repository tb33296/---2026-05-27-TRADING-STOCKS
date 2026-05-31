# tests/test_cvd.py

from core.indicators.cvd import (
    CVD
)


def test_cvd() -> None:

    cvd = CVD(
        name="CVD",
        symbol="RELIANCE",
        timeframe="1m"
    )

    ticks = [

        (100, 100),
        (101, 50),
        (102, 50),
        (101, 20)

    ]

    for price, volume in ticks:

        cvd.update(
            price,
            volume
        )

    assert (
        cvd.get_buy_volume()
        == 100
    )

    assert (
        cvd.get_sell_volume()
        == 20
    )

    assert (
        cvd.get_cvd()
        == 80
    )

    assert (
        cvd.is_bullish()
    )