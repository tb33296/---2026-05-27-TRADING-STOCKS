# tests/test_trade_context.py
from core.strategy.trade_context import (
    TradeContext
)


def test_trade_context() -> None:

    print(
        "\n=== TRADE CONTEXT TEST ===\n"
    )

    context = (
        TradeContext(
            symbol="RELIANCE",

            segment="EQUITY",

            score=85.0,

            direction="LONG",

            confidence="HIGH",

            reasons=[
                "EMA Bullish",
                "Above VWAP"
            ],

            entry_price=100.0,

            stop_loss=95.0,

            target=110.0
        )
    )

    print(
        f"Symbol: {context.symbol}"
    )

    print(
        f"Direction: {context.direction}"
    )

    print(
        f"Score: {context.score}"
    )

    print(
        f"Reasons: {len(context.reasons)}"
    )

    assert (
        context.symbol
        == "RELIANCE"
    )

    assert (
        context.direction
        == "LONG"
    )

    assert (
        context.score
        == 85.0
    )

    print(
        "\n=== TEST COMPLETE ==="
    )