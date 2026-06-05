# tests/test_signal_trading_engine_runtime.py
from database.db_manager import DatabaseManager

from core.journal.trade_journal_manager import TradeJournalManager

from core.positions.position_manager import PositionManager

from core.risk.risk_engine import RiskEngine

from core.execution.paper_execution_engine import PaperExecutionEngine

from runtime.trade_pipeline import TradePipeline

from runtime.trading_engine import TradingEngine

from core.strategy.multifactor_decision import MultiFactorDecision


class MockStrategy:
    """
    Returns a BUY decision.
    """

    def evaluate(self, current_price: float) -> MultiFactorDecision:

        return MultiFactorDecision(
            score=85.0,
            direction="LONG",
            confidence="HIGH",
            reasons=["EMA Bullish", "Above VWAP"],
            stop_loss=95.0,
            target=110.0,
        )


def test_signal_trading_engine_runtime() -> None:

    print("\n=== SIGNAL -> TRADING ENGINE TEST ===\n")

    # ----------------------------------
    # Infrastructure
    # ----------------------------------

    position_manager = PositionManager()

    risk_engine = RiskEngine(position_manager)

    execution_engine = PaperExecutionEngine(position_manager)

    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    journal_manager = TradeJournalManager(db)

    trade_pipeline = TradePipeline(
        risk_engine=risk_engine,
        execution_engine=execution_engine,
        journal_manager=journal_manager,
    )

    # ----------------------------------
    # Trading Engine
    # ----------------------------------

    trading_engine = TradingEngine(
        strategy=MockStrategy(), trade_pipeline=trade_pipeline, account_size=100000
    )

    # ----------------------------------
    # Execute Trade
    # ----------------------------------

    result = trading_engine.evaluate_trade(
        symbol="RELIANCE",
        segment="EQUITY",
        current_price=100.0,
    )

    assert result is not None

    decision = result[0]
    risk = result[1]
    execution = result[2]
    sizing = result[3]

    assert decision is not None
    assert risk is not None
    assert execution is not None
    assert sizing is not None

    print(type(decision))
    print(type(risk))
    print(type(execution))
    print(type(sizing))

    (decision, risk, execution, sizing) = result
   
    # ----------------------------------
    # Validation
    # ----------------------------------

    assert decision is not None
    assert risk is not None
    assert execution is not None

    assert decision.approved
    assert risk.approved
    assert execution.success

    print(f"Decision Approved: {decision.approved}")

    print(f"Risk Approved: {risk.approved}")

    print(f"Execution Success: {execution.success}")

    print(f"Quantity: {execution.quantity}")

    # ----------------------------------
    # Position Validation
    # ----------------------------------

    assert position_manager.get_open_position_count() == 1

    position = position_manager.get_open_positions().get("RELIANCE")

    assert position is not None

    assert position.trade_id is not None

    print(f"Trade ID: {position.trade_id}")

    # ----------------------------------
    # Journal Validation
    # ----------------------------------

    trade = journal_manager.get_trade(position.trade_id)

    assert trade is not None

    print("\nTrade Record:")

    print(trade)

    print("\n=== TEST COMPLETE ===")

    db.close()
