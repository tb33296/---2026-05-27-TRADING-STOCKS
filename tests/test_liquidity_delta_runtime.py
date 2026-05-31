# tests/test_liquidity_delta_runtime.py

from core.indicators.liquidity_delta import (
    LiquidityDelta
)


def test_liquidity_delta_runtime() -> None:

    print(
        "\n=== LIQUIDITY DELTA TEST ===\n"
    )

    indicator = LiquidityDelta(
        name="LIQUIDITY",
        symbol="SBIN",
        timeframe="L2"
    )

    snapshots = [

        {
            "buy": [
                {"quantity": 100},
                {"quantity": 200}
            ],
            "sell": [
                {"quantity": 500},
                {"quantity": 300}
            ]
        },

        {
            "buy": [
                {"quantity": 500},
                {"quantity": 600}
            ],
            "sell": [
                {"quantity": 200},
                {"quantity": 100}
            ]
        },

        {
            "buy": [
                {"quantity": 1000},
                {"quantity": 900}
            ],
            "sell": [
                {"quantity": 300},
                {"quantity": 200}
            ]
        }

    ]

    for snapshot in snapshots:

        indicator.update(
            snapshot
        )

        print(
            f"Bid={indicator.get_bid_quantity()}  "
            f"Ask={indicator.get_ask_quantity()}  "
            f"Delta={indicator.get_delta()}  "
            f"Ratio={indicator.get_ratio()}  "
            f"Bullish={indicator.is_bullish()}"
        )

    print(
        "\n=== TEST COMPLETE ==="
    )