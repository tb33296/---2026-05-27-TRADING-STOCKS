# tests/test_trade_decision_engine_v2.py

from core.strategy.trade_decision_engine import (
    TradeDecisionEngine
)


def test_trade_decision_engine_v2() -> None:

    print(
        "\n=== TRADE DECISION V2 TEST ===\n"
    )

    engine = (
        TradeDecisionEngine()
    )

    # ==================================
    # STRONG LONG
    # ==================================

    decision = (
        engine.evaluate(
            score=95,

            direction="STRONG_LONG",

            confidence="HIGH",

            quantity=100
        )
    )

    print(
        "STRONG LONG"
    )

    print(
        f"Direction: "
        f"{decision.direction}"
    )

    assert (
        decision.direction
        ==
        "LONG"
    )

    # ==================================
    # STRONG SHORT
    # ==================================

    decision = (
        engine.evaluate(
            score=95,

            direction="STRONG_SHORT",

            confidence="HIGH",

            quantity=100
        )
    )

    print(
        "STRONG SHORT"
    )

    print(
        f"Direction: "
        f"{decision.direction}"
    )

    assert (
        decision.direction
        ==
        "SHORT"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )