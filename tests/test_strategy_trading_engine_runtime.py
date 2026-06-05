# tests/test_strategy_trading_engine_runtime.py
from database.db_manager import DatabaseManager

from core.journal.trade_journal_manager import TradeJournalManager

from core.positions.position_manager import PositionManager

from core.risk.risk_engine import RiskEngine

from core.execution.paper_execution_engine import PaperExecutionEngine

from runtime.trade_pipeline import TradePipeline

from runtime.trading_engine import TradingEngine

from runtime.strategy_runtime import StrategyRuntime

from core.strategy.multifactor_strategy import MultiFactorStrategy


# ==================================================
# Mock Indicators
# ==================================================


class MockIndicator:
    def __init__(self, value: float) -> None:

        self.value = value

    def get_value(self) -> float:

        return self.value

    def is_ready(self) -> bool:

        return True


class MockLiquidity:
    def is_bullish(self) -> bool:

        return True

    def is_bearish(self) -> bool:

        return False


class MockCVD:
    def is_bullish(self) -> bool:

        return True

    def is_bearish(self) -> bool:

        return False


def test_strategy_trading_engine_runtime() -> None:

    print("\n=== STRATEGY -> TRADING ENGINE TEST ===\n")

    # ------------------------------------------------
    # Infrastructure
    # ------------------------------------------------

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

    # ------------------------------------------------
    # Strategy
    # ------------------------------------------------

    strategy = MultiFactorStrategy(
        ema_fast=MockIndicator(110),
        ema_slow=MockIndicator(100),
        vwap=MockIndicator(100),
        awvap=MockIndicator(100),
        rvol=MockIndicator(2.0),
        vwma=MockIndicator(100),
        atr=MockIndicator(5.0),
        liquidity=MockLiquidity(),
        cvd=MockCVD(),
    )

    strategy_runtime = StrategyRuntime(strategy)

    trading_engine = TradingEngine(
        strategy=strategy, trade_pipeline=trade_pipeline, account_size=100000
    )

    # ------------------------------------------------
    # Strategy Evaluation
    # ------------------------------------------------

    decision = strategy_runtime.evaluate(current_price=110.0)

    print(f"Score: {decision.score}")

    print(f"Direction: {decision.direction}")

    print(f"Confidence: {decision.confidence}")
    print(
    f"Stop Loss: "
    f"{decision.stop_loss}"
)

    print(
        f"Target: "
        f"{decision.target}"
    )

    assert decision.stop_loss > 0

    assert decision.target > 0
    assert decision.direction == "STRONG_LONG"

    # ------------------------------------------------
    # Trading Engine
    # ------------------------------------------------

    result = trading_engine.evaluate_trade(
        symbol="RELIANCE",
        segment="EQUITY",
        current_price=110.0,
    )

    assert result is not None

    (trade_decision, risk_decision, execution_result, sizing_result) = result

    assert trade_decision is not None
    assert risk_decision is not None
    assert execution_result is not None
    assert sizing_result is not None

    # ------------------------------------------------
    # Validation
    # ------------------------------------------------

    assert trade_decision.approved

    assert risk_decision.approved

    assert execution_result.success

    print(f"\nQuantity: {execution_result.quantity}")

    print(f"Fill Price: {execution_result.fill_price}")

    # ------------------------------------------------
    # Position Validation
    # ------------------------------------------------

    assert position_manager.get_open_position_count() == 1

    position = position_manager.get_open_positions().get("RELIANCE")

    assert position is not None

    assert position.trade_id is not None

    print(f"Trade ID: {position.trade_id}")

    # ------------------------------------------------
    # Journal Validation
    # ------------------------------------------------

    trade = journal_manager.get_trade(position.trade_id)

    assert trade is not None

    print("\nTrade Record:")

    print(trade)

    print("\n=== TEST COMPLETE ===")

    db.close()
