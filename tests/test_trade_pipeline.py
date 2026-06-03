# tests/test_trade_pipeline.py

from runtime.trade_pipeline import TradePipeline
from core.strategy.trade_context import TradeContext
from core.execution.paper_execution_engine import PaperExecutionEngine

from core.positions.position_manager import PositionManager

from core.risk.risk_engine import RiskEngine
from database.db_manager import DatabaseManager

from core.journal.trade_journal_manager import TradeJournalManager


def test_trade_pipeline() -> None:

    print("\n=== TRADE PIPELINE TEST ===\n")

    position_manager = PositionManager()

    risk_engine = RiskEngine(position_manager)

    execution_engine = PaperExecutionEngine(position_manager)

    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    journal_manager = TradeJournalManager(db)

    pipeline = TradePipeline(
        risk_engine=risk_engine,
        execution_engine=execution_engine,
        journal_manager=journal_manager,
    )

    # -----------------------------------------------------------------
    trade_context = TradeContext(
        symbol="RELIANCE",
        segment="EQUITY",
        score=85.0,
        direction="LONG",
        confidence="HIGH",
        reasons=["EMA Bullish", "Above VWAP"],
        entry_price=100.0,
        stop_loss=95.0,
        target=110.0,
    )

    decision, risk, execution, sizing = pipeline.execute_trade(
        trade_context=(trade_context), account_size=100000
    )
    # ------------------------------------------------------------------
    assert decision is not None
    assert risk is not None
    assert execution is not None
    assert sizing is not None
    print(f"Symbol: {trade_context.symbol}")

    print(f"Direction: {trade_context.direction}")

    print(f"Score: {trade_context.score}")

    print(f"Reasons: {len(trade_context.reasons)}")

    print()

    print(f"Decision Approved: {decision.approved}")

    print(f"Risk Approved: {risk.approved}")

    print(f"Execution Success: {execution.success}")

    print(f"Quantity: {execution.quantity}")

    print(f"Fill Price: {execution.fill_price}")

    print(f"Risk Amount: {sizing.risk_amount}")

    print(f"Risk Percent:{sizing.risk_percent}")

    assert decision.approved is True

    assert risk.approved is True

    assert execution.success is True

    print("\n=== TEST COMPLETE ===")
