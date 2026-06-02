# runtime/trading_engine.py

from typing import Any

from core.logging_manager import (
    LoggingManager
)

from runtime.trade_pipeline import (
    TradePipeline
)

from core.strategy.trade_context import (
    TradeContext
)


class TradingEngine:
    """
    High-level trading orchestrator.

    Responsibilities:

    - strategy evaluation
    - trade pipeline execution
    - trade monitoring
    """

    def __init__(
        self,
        strategy: Any,
        trade_pipeline: TradePipeline,
        account_size: float
    ) -> None:

        self.logger = (
            LoggingManager.get_logger(
                __name__
            )
        )

        self.strategy = (
            strategy
        )

        self.trade_pipeline = (
            trade_pipeline
        )

        self.account_size = (
            account_size
        )

    def evaluate_trade(
        self,
        symbol: str,
        segment: str,
        current_price: float,
        stop_loss: float,
        target: float
    ):
        """
        Evaluate trade opportunity.
        """

        try:

            decision = (
                self.strategy.evaluate(
                    current_price
                )
            )

            if (
                decision.direction
                ==
                "NO_TRADE"
            ):

                return None

            trade_context = (
                TradeContext(
                    symbol=symbol,

                    segment=segment,

                    score=decision.score,

                    direction=(
                        decision.direction
                    ),

                    confidence=(
                        decision.confidence
                    ),

                    reasons=(
                        decision.reasons
                    ),

                    entry_price=(
                        current_price
                    ),

                    stop_loss=(
                        stop_loss
                    ),

                    target=target
                )
            )

            return (
                self.trade_pipeline
                .execute_trade(
                    trade_context=(
                        trade_context
                    ),

                    account_size=(
                        self.account_size
                    )
                )
            )

        except Exception as error:

            self.logger.error(
                f"Trading engine failed: "
                f"{error}"
            )

            return None