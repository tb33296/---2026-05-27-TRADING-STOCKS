# tests/test_liquidity_delta.py

from core.indicators.liquidity_delta import (
    LiquidityDelta
)


def test_liquidity_delta() -> None:

    indicator = LiquidityDelta(
        name="LIQUIDITY",
        symbol="SBIN",
        timeframe="L2"
    )

    depth = {

        "buy": [
            {"quantity": 100},
            {"quantity": 200},
            {"quantity": 300}
        ],

        "sell": [
            {"quantity": 50},
            {"quantity": 100},
            {"quantity": 150}
        ]
    }

    indicator.update(
        depth
    )

    assert (
        indicator.get_bid_quantity()
        == 600
    )

    assert (
        indicator.get_ask_quantity()
        == 300
    )

    assert (
        indicator.get_delta()
        == 300
    )

    assert (
        indicator.is_bullish()
    )