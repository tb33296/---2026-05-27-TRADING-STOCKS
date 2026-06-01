# core/strategy/trade_decision_engine.py

from config.scoring_config_loader import (
    ScoringConfigLoader
)

from core.logging_manager import (
    LoggingManager
)

from core.strategy.trade_decision import (
    TradeDecision
)


class TradeDecisionEngine:
    """
    Converts strategy output
    into executable trade decisions.
    """

    def __init__(
        self
    ) -> None:

        self.logger = (
            LoggingManager.get_logger(
                __name__
            )
        )

        self.config = (
            ScoringConfigLoader()
        )

        self.minimum_score = float(
            self.config
            .get_position_sizing()
            .get(
                "minimum_trade_score",
                50.0
            )
        )

    def evaluate(
        self,
        score: float,
        direction: str,
        confidence: str,
        quantity: int
    ) -> TradeDecision:
        """
        Determine whether
        trade should proceed.
        """

        try:

            if (
                score
                < self.minimum_score
            ):

                return TradeDecision(
                    approved=False,

                    direction="NONE",

                    score=score,

                    quantity=0,

                    reason=(
                        "SCORE_TOO_LOW"
                    ),

                    confidence=confidence
                )

            if (
                quantity <= 0
            ):

                return TradeDecision(
                    approved=False,

                    direction="NONE",

                    score=score,

                    quantity=0,

                    reason=(
                        "INVALID_QUANTITY"
                    ),

                    confidence=confidence
                )

            return TradeDecision(
                approved=True,

                direction=direction,

                score=score,

                quantity=quantity,

                reason="APPROVED",

                confidence=confidence
            )

        except Exception as error:

            self.logger.error(
                f"Trade decision "
                f"failed: {error}"
            )

            return TradeDecision(
                approved=False,

                direction="NONE",

                score=0.0,

                quantity=0,

                reason="ENGINE_ERROR",

                confidence="LOW"
            )