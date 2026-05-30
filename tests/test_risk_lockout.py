# tests/test_risk_lockout.py

from datetime import datetime

from core.positions.position import (
    Position
)

from core.positions.position_manager import (
    PositionManager
)

from core.risk.risk_engine import (
    RiskEngine
)


def test_risk_lockout() -> None:

    print(
        "\n=== RISK LOCKOUT TEST ===\n"
    )

    # -------------------------
    # Infrastructure
    # -------------------------

    position_manager = (
        PositionManager()
    )

    risk_engine = (
        RiskEngine(
            position_manager
        )
    )

    # -------------------------
    # Create Losing Trades
    # -------------------------

    for trade_number in range(3):

        position = Position(
            symbol=f"TEST{trade_number}",
            segment="EQUITY",
            side="LONG",
            quantity=100,
            entry_price=100.0,
            entry_time=datetime.now(),
            stop_loss=95.0,
            target=110.0
        )

        assert (
            position_manager
            .open_position(
                position
            )
        )

        assert (
            position_manager
            .close_position(
                symbol=f"TEST{trade_number}",
                exit_price=95.0
            )
        )

    # -------------------------
    # Verify Loss Counter
    # -------------------------

    losses = (
        position_manager
        .get_consecutive_losses()
    )

    print(
        f"Consecutive Losses: "
        f"{losses}"
    )

    # -------------------------
    # Risk Evaluation
    # -------------------------

    decision = (
        risk_engine.evaluate(
            signal=None
        )
    )

    print(
        f"Risk Approved: "
        f"{decision.approved}"
    )

    print(
        f"Reason: "
        f"{decision.reason}"
    )

    assert (
        decision.approved
        is False
    )

    assert (
        decision.reason
        ==
        "MAX_CONSECUTIVE_LOSSES"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )