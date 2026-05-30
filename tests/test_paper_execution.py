# tests/test_paper_execution.py

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.positions.position_manager import (
    PositionManager
)


def test_paper_execution() -> None:

    print(
        "\n=== PAPER EXECUTION TEST ===\n"
    )

    manager = PositionManager()

    execution_engine = (
        PaperExecutionEngine(
            manager
        )
    )

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

    print(
        "BUY RESULT:"
    )

    print(
        result
    )

    assert result.success

    print(
        "\nOpen Positions:"
    )

    print(
        manager.get_open_position_count()
    )

    assert (
        manager.get_open_position_count()
        == 1
    )

    closed = (
        execution_engine.execute_sell(
            symbol="RELIANCE",
            exit_price=105.0
        )
    )

    assert closed

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
        "\n=== TEST COMPLETE ==="
    )