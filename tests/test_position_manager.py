# tests/test_position_manager.py

from datetime import datetime

from core.positions.position import (
    Position
)

from core.positions.position_manager import (
    PositionManager
)


def test_position_manager() -> None:

    print(
        "\n=== POSITION MANAGER TEST ===\n"
    )

    manager = PositionManager()

    position = Position(
        symbol="RELIANCE",
        segment="EQUITY",
        side="LONG",
        quantity=100,
        entry_price=100.0,
        entry_time=datetime.now(),
        stop_loss=95.0,
        target=110.0
    )

    assert (
        manager.open_position(
            position
        )
        is True
    )

    print(
        "Position Opened"
    )

    print(
        f"Open Positions: "
        f"{manager.get_open_position_count()}"
    )

    assert (
        manager.close_position(
            symbol="RELIANCE",
            exit_price=105.0,

        )
        is True
    )

    print(
        "\nPosition Closed"
    )

    print(
        f"Gross PnL: "
        f"{manager.get_total_gross_pnl()}"
    )

    print(
        f"Charges: "
        f"{manager.get_total_charges()}"
    )

    print(
        f"Net PnL: "
        f"{manager.get_total_net_pnl()}"
    )

    print(
        f"Consecutive Losses: "
        f"{manager.get_consecutive_losses()}"
    )

    assert (
        manager.get_open_position_count()
        == 0
    )

    assert (
        manager.get_total_gross_pnl()
        == 500.0
    )

    assert (
        manager.get_total_charges()
        == 20.0
    )

    assert (
        manager.get_total_net_pnl()
        == 480.0
    )

    print(
        "\n=== TEST COMPLETE ==="
    )