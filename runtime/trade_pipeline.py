# runtime/trade_pipeline.py

from core.execution.paper_execution_engine import PaperExecutionEngine

from core.logging_manager import LoggingManager

from core.risk.position_sizing_engine import PositionSizingEngine

from core.risk.risk_engine import RiskEngine

from core.strategy.trade_context import TradeContext

from core.strategy.trade_decision_engine import TradeDecisionEngine


class TradePipeline:
    """
    Trading orchestration layer.

    Responsibilities:

    - trade approval
    - risk validation
    - position sizing
    - execution
    """

    def __init__(
        self, risk_engine: RiskEngine, execution_engine: PaperExecutionEngine
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.risk_engine = risk_engine

        self.execution_engine = execution_engine

        self.trade_decision_engine = TradeDecisionEngine()

        self.position_sizing_engine = PositionSizingEngine()

    def execute_trade(self, trade_context: TradeContext, account_size: float):
        """
        Execute full trade workflow.
        """

        try:
            sizing = self.position_sizing_engine.calculate(
                account_size=account_size,
                score=(trade_context.score),
                entry_price=(trade_context.entry_price),
                stop_loss=(trade_context.stop_loss),
            )

            decision = self.trade_decision_engine.evaluate(
                score=(trade_context.score),
                direction=(trade_context.direction),
                confidence=(trade_context.confidence),
                quantity=(sizing.quantity),
            )

            if not decision.approved:
                return (decision, None, None, sizing)

            risk = self.risk_engine.evaluate(decision)

            if not risk.approved:
                return (decision, risk, None, sizing)

            if decision.is_long():
                execution = self.execution_engine.execute_buy(
                    symbol=(trade_context.symbol),
                    segment=(trade_context.segment),
                    quantity=(sizing.quantity),
                    ltp=(trade_context.entry_price),
                    stop_loss=(trade_context.stop_loss),
                    target=(trade_context.target),
                )

                return (decision, risk, execution, sizing)

            return (decision, risk, None, sizing)

        except Exception as error:
            self.logger.error(f"Trade pipeline failed: {error}")

            return (None, None, None, None)
