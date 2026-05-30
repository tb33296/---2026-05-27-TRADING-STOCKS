# tests/test_stop_loss_exit.py

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.positions.position_manager import (
    PositionManager
)

from core.trade_management.trade_manager import (
    TradeManager
)


def test_stop_loss_exit() -> None:

    print(
        "\n=== STOP LOSS TEST ===\n"
    )

    # -------------------------
    # Infrastructure
    # -------------------------

    position_manager = (
        PositionManager()
    )

    execution_engine = (
        PaperExecutionEngine(
            position_manager
        )
    )

    trade_manager = (
        TradeManager(
            position_manager,
            execution_engine
        )
    )

    # -------------------------
    # Open Position
    # -------------------------

    result = (
        execution_engine.execute_buy(
            symbol="RELIANCE",
            segment="EQUITY",
            quantity=100,
            ltp=100.0,
            stop_loss=95.0,
            target=110.0
        )
    )

    assert result.success

    print(
        "Position Opened"
    )

    # -------------------------
    # Simulated Price Decline
    # -------------------------

    prices = [
        99,
        98,
        97,
        96,
        95
    ]

    closed = False

    for price in prices:

        print(
            f"Price: {price}"
        )

        if (
            trade_manager
            .evaluate_position(
                symbol="RELIANCE",
                current_price=price
            )
        ):

            closed = True

            print(
                f"Position Closed "
                f"at {price}"
            )

            break

    assert closed

    # -------------------------
    # Validation
    # -------------------------

    print(
        "\nOpen Positions:"
    )

    print(
        position_manager
        .get_open_position_count()
    )

    print(
        "\nClosed Positions:"
    )

    print(
        len(
            position_manager
            .get_closed_positions()
        )
    )

    print(
        f"\nGross PnL: "
        f"{position_manager.get_total_gross_pnl()}"
    )

    print(
        f"Charges: "
        f"{position_manager.get_total_charges()}"
    )

    print(
        f"Net PnL: "
        f"{position_manager.get_total_net_pnl()}"
    )

    print(
        f"Consecutive Losses: "
        f"{position_manager.get_consecutive_losses()}"
    )

    assert (
        position_manager
        .get_open_position_count()
        == 0
    )

    assert (
        len(
            position_manager
            .get_closed_positions()
        )
        == 1
    )

    assert (
        position_manager
        .get_total_net_pnl()
        < 0
    )

    assert (
        position_manager
        .get_consecutive_losses()
        == 1
    )

    print(
        "\n=== TEST COMPLETE ==="
    )