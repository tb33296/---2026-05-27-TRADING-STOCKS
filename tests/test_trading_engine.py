# tests/test_trading_engine.py

from typing import Any

from runtime.trading_engine import (
    TradingEngine
)

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

from core.strategy.multifactor_decision import (
    MultiFactorDecision
)

from database.db_manager import (
    DatabaseManager
)

from core.journal.trade_journal_manager import (
    TradeJournalManager
)


class MockStrategy:

    def evaluate(
        self,
        current_price: float
    ) -> MultiFactorDecision:

        return MultiFactorDecision(
            score=85.0,

            direction="STRONG_LONG",

            confidence="HIGH",

            reasons=[
                "Test"
            ]
        )


def test_trading_engine() -> None:

    print(
        "\n=== TRADING ENGINE TEST ===\n"
    )

    # =====================================
    # Database
    # =====================================

    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    journal_manager = (
        TradeJournalManager(
            db
        )
    )

    # =====================================
    # Core Components
    # =====================================

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

    trade_pipeline = (
        TradePipeline(
            risk_engine=(
                risk_engine
            ),

            execution_engine=(
                execution_engine
            ),

            journal_manager=(
                journal_manager
            )
        )
    )

    # =====================================
    # Strategy
    # =====================================

    strategy = (
        MockStrategy()
    )

    engine = (
        TradingEngine(
            strategy=strategy,

            trade_pipeline=(
                trade_pipeline
            ),

            account_size=100000
        )
    )

    # =====================================
    # Execute
    # =====================================

    result = (
        engine.evaluate_trade(
            symbol="RELIANCE",

            segment="EQUITY",

            current_price=100,

            stop_loss=95,

            target=110
        )
    )

    assert result is not None

    # Pipeline now returns sizing too

    decision, risk, execution, sizing = (
        result
    )

    assert decision is not None
    assert risk is not None
    assert execution is not None
    assert sizing is not None

    # =====================================
    # Output
    # =====================================

    print(
        f"Score="
        f"{decision.score}"
    )

    print(
        f"Direction="
        f"{decision.direction}"
    )

    print(
        f"Risk Approved="
        f"{risk.approved}"
    )

    print(
        f"Execution="
        f"{execution.success}"
    )

    print(
        f"Risk Amount="
        f"{sizing.risk_amount}"
    )

    print(
        f"Risk Percent="
        f"{sizing.risk_percent}"
    )

    # =====================================
    # Assertions
    # =====================================

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

    db.close()