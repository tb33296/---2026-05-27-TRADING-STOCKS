# tests/test_position_sizing_engine.py

from core.risk.position_sizing_engine import (
    PositionSizingEngine
)


def test_position_sizing_engine() -> None:

    print(
        "\n=== POSITION SIZING TEST ===\n"
    )

    engine = (
        PositionSizingEngine()
    )

    decision = (
        engine.calculate(
            account_size=100000,

            score=95,

            entry_price=100,

            stop_loss=95
        )
    )

    print(
        f"Quantity: "
        f"{decision.quantity}"
    )

    print(
        f"Risk Amount: "
        f"{decision.risk_amount}"
    )

    print(
        f"Risk Percent: "
        f"{decision.risk_percent}"
    )

    print(
        f"Multiplier: "
        f"{decision.score_multiplier}"
    )

    assert (
        decision.quantity
        == 150
    )

    assert (
        decision.risk_amount
        == 750.0
    )

    assert (
        decision.score_multiplier
        == 1.5
    )

    print(
        "\n=== TEST COMPLETE ==="
    )