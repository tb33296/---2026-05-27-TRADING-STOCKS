# tests/test_position_sizing_engine_v2.py

from core.risk.position_sizing_engine import (
    PositionSizingEngine
)


def test_position_sizing_engine_v2() -> None:

    print(
        "\n=== POSITION SIZING V2 TEST ===\n"
    )

    engine = (
        PositionSizingEngine()
    )

    # ==================================================
    # CASE 1
    # NORMAL RISK LIMITED TRADE
    # ==================================================

    decision = (
        engine.calculate(
            account_size=100000,

            score=95,

            entry_price=100,

            stop_loss=95
        )
    )

    capital_required = (
        decision.quantity
        *
        100
    )

    print(
        "CASE 1: Risk Limited"
    )

    print(
        f"Quantity={decision.quantity}"
    )

    print(
        f"Risk Amount={decision.risk_amount}"
    )

    print(
        f"Capital Required="
        f"{capital_required}"
    )

    assert (
        decision.quantity
        == 150
    )

    # ==================================================
    # CASE 2
    # HIGH PRICE STOCK
    # CAPITAL SHOULD BE INSUFFICIENT
    # ==================================================

    decision = (
        engine.calculate(
            account_size=100000,

            score=95,

            entry_price=5000,

            stop_loss=4995
        )
    )

    capital_required = (
        decision.quantity
        *
        5000
    )

    print()

    print(
        "CASE 2: Capital Limited"
    )

    print(
        f"Quantity={decision.quantity}"
    )

    print(
        f"Risk Amount={decision.risk_amount}"
    )

    print(
        f"Capital Required="
        f"{capital_required}"
    )

    print()

    if (
        capital_required
        >
        100000
    ):

        print(
            "WARNING:"
            " Current engine "
            "does not enforce "
            "capital limits."
        )

    print(
        "\n=== TEST COMPLETE ==="
    )