# tests/test_trade_decision_engine.py

from core.strategy.trade_decision_engine import (
    TradeDecisionEngine
)


def test_trade_decision_engine() -> None:

    print(
        "\n=== TRADE DECISION TEST ===\n"
    )

    engine = (
        TradeDecisionEngine()
    )

    # -------------------------
    # Approved Trade
    # -------------------------

    decision = (
        engine.evaluate(
            score=85,

            direction="LONG",

            confidence="HIGH",

            quantity=150
        )
    )

    print(
        "APPROVED TRADE"
    )

    print(
        f"Approved: "
        f"{decision.approved}"
    )

    print(
        f"Direction: "
        f"{decision.direction}"
    )

    print(
        f"Score: "
        f"{decision.score}"
    )

    print(
        f"Quantity: "
        f"{decision.quantity}"
    )

    print()

    assert (
        decision.approved
        is True
    )

    # -------------------------
    # Rejected Trade
    # -------------------------

    decision = (
        engine.evaluate(
            score=45,

            direction="LONG",

            confidence="LOW",

            quantity=100
        )
    )

    print(
        "REJECTED TRADE"
    )

    print(
        f"Approved: "
        f"{decision.approved}"
    )

    print(
        f"Reason: "
        f"{decision.reason}"
    )

    print()

    assert (
        decision.approved
        is False
    )

    assert (
        decision.reason
        ==
        "SCORE_TOO_LOW"
    )

    print(
        "=== TEST COMPLETE ==="
    )