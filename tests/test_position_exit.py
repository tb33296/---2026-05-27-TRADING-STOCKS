# tests/test_position_exit.py

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.positions.position_manager import (
    PositionManager
)

from core.trade_management.trade_manager import (
    TradeManager
)


def test_position_exit() -> None:

    print(
        "\n=== POSITION EXIT TEST ===\n"
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
    # Simulated Prices
    # -------------------------

    prices = [
        101,
        103,
        106,
        108,
        110
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

    print(
        "\n=== TEST COMPLETE ==="
    )