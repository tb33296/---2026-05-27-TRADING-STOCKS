# runtime/trading_engine.py

from core.logging_manager import (
    LoggingManager
)

from runtime.trade_pipeline import (
    TradePipeline
)

from core.strategy.multifactor_strategy import (
    MultiFactorStrategy
)
from typing import Any

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

        self.strategy = strategy

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

            return (
                self.trade_pipeline
                .execute_trade(
                    symbol=symbol,

                    segment=segment,

                    account_size=(
                        self.account_size
                    ),

                    score=(
                        decision.score
                    ),

                    direction=(
                        decision.direction
                    ),

                    confidence=(
                        decision.confidence
                    ),

                    entry_price=(
                        current_price
                    ),

                    stop_loss=(
                        stop_loss
                    ),

                    target=(
                        target
                    )
                )
            )

        except Exception as error:

            self.logger.error(
                f"Trading engine failed: "
                f"{error}"
            )

            return None