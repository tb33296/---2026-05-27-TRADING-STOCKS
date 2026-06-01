# tests/test_trade_pipeline.py

from runtime.trade_pipeline import (
    TradePipeline
)

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.positions.position_manager import (
    PositionManager
)

from core.risk.risk_engine import (
    RiskEngine
)


def test_trade_pipeline() -> None:

    print(
        "\n=== TRADE PIPELINE TEST ===\n"
    )

    position_manager = (
        PositionManager()
    )

    risk_engine = (
        RiskEngine(
            position_manager
        )
    )

    execution_engine = (
        PaperExecutionEngine(
            position_manager
        )
    )

    pipeline = (
        TradePipeline(
            risk_engine=risk_engine,
            execution_engine=execution_engine
        )
    )

    decision, risk, execution = (
        pipeline.execute_trade(
            symbol="RELIANCE",

            segment="EQUITY",

            account_size=100000,

            score=85,

            direction="LONG",

            confidence="HIGH",

            entry_price=100,

            stop_loss=95,

            target=110
        )
    )
    assert decision is not None
    assert risk is not None
    assert execution is not None
    print(
        f"Decision Approved: "
        f"{decision.approved}"
    )

    print(
        f"Risk Approved: "
        f"{risk.approved}"
    )

    print(
        f"Execution Success: "
        f"{execution.success}"
    )

    print(
        f"Quantity: "
        f"{execution.quantity}"
    )

    print(
        f"Fill Price: "
        f"{execution.fill_price}"
    )

    assert (
        decision.approved
        is True
    )

    assert (
        risk.approved
        is True
    )

    assert (
        execution.success
        is True
    )

    print(
        "\n=== TEST COMPLETE ==="
    )