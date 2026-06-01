# runtime/trade_pipeline.py

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.logging_manager import (
    LoggingManager
)

from core.risk.position_sizing_engine import (
    PositionSizingEngine
)

from core.risk.risk_engine import (
    RiskEngine
)

from core.strategy.trade_decision import (
    TradeDecision
)

from core.strategy.trade_decision_engine import (
    TradeDecisionEngine
)


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
        self,
        risk_engine: RiskEngine,
        execution_engine: PaperExecutionEngine
    ) -> None:

        self.logger = (
            LoggingManager.get_logger(
                __name__
            )
        )

        self.risk_engine = (
            risk_engine
        )

        self.execution_engine = (
            execution_engine
        )

        self.trade_decision_engine = (
            TradeDecisionEngine()
        )

        self.position_sizing_engine = (
            PositionSizingEngine()
        )

    def execute_trade(
        self,
        symbol: str,
        segment: str,
        account_size: float,
        score: float,
        direction: str,
        confidence: str,
        entry_price: float,
        stop_loss: float,
        target: float
    ):
        """
        Execute full trade workflow.
        """

        try:

            sizing = (
                self.position_sizing_engine
                .calculate(
                    account_size=account_size,
                    score=score,
                    entry_price=entry_price,
                    stop_loss=stop_loss
                )
            )

            decision = (
                self.trade_decision_engine
                .evaluate(
                    score=score,
                    direction=direction,
                    confidence=confidence,
                    quantity=sizing.quantity
                )
            )

            if not decision.approved:

                return (
                    decision,
                    None,
                    None
                )

            risk = (
                self.risk_engine
                .evaluate(
                    decision
                )
            )

            if not risk.approved:

                return (
                    decision,
                    risk,
                    None
                )

            if direction.upper() == "LONG":

                execution = (
                    self.execution_engine
                    .execute_buy(
                        symbol=symbol,
                        segment=segment,
                        quantity=sizing.quantity,
                        ltp=entry_price,
                        stop_loss=stop_loss,
                        target=target
                    )
                )

                return (
                    decision,
                    risk,
                    execution
                )

            return (
                decision,
                risk,
                None
            )

        except Exception as error:

            self.logger.error(
                f"Trade pipeline failed: "
                f"{error}"
            )

            return (
                None,
                None,
                None
            )