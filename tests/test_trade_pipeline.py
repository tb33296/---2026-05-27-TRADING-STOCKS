# tests/test_trade_pipeline.py

from runtime.trade_pipeline import (
    TradePipeline
)
from core.strategy.trade_context import (
    TradeContext
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
    # -----------------------------------------------------------------
    trade_context = (
    TradeContext(
        symbol="RELIANCE",

        segment="EQUITY",

        score=85.0,

        direction="LONG",

        confidence="HIGH",

        reasons=[
            "EMA Bullish",
            "Above VWAP"
        ],

        entry_price=100.0,

        stop_loss=95.0,

        target=110.0
    )
)

    decision, risk, execution = (
        pipeline.execute_trade(
            trade_context=(
                trade_context
            ),

            account_size=100000
        )
    )
    #------------------------------------------------------------------
    assert decision is not None
    assert risk is not None
    assert execution is not None
    print(
    f"Symbol: "
    f"{trade_context.symbol}"
)

    print(
        f"Direction: "
        f"{trade_context.direction}"
    )

    print(
        f"Score: "
        f"{trade_context.score}"
    )

    print(
        f"Reasons: "
        f"{len(trade_context.reasons)}"
    )

    print()

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