# core/risk/position_sizing_engine.py

from config.risk_config_loader import RiskConfigLoader

from core.logging_manager import LoggingManager

from core.risk.position_size_decision import PositionSizeDecision


class PositionSizingEngine:
    """
    Calculates position size based on:

    - account size
    - trade score
    - stop distance

    Formula:

    risk_budget =
        account_size
        *
        risk_percent
        *
        score_multiplier

    quantity =
        risk_budget
        /
        stop_distance
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.config = RiskConfigLoader()

    def calculate(
        self, account_size: float, score: float, entry_price: float, stop_loss: float
    ) -> PositionSizeDecision:
        """
        Calculate position size.
        """

        stop_distance = abs(entry_price - stop_loss)

        if stop_distance <= 0:
            raise ValueError("Invalid stop distance")

        base_risk_percent = self.config.get_base_risk_percent()

        multiplier = self._get_score_multiplier(score)

        effective_risk_percent = base_risk_percent * multiplier

        risk_amount = account_size * (effective_risk_percent / 100.0)

        # --------------------------------
        # Risk Limited Quantity
        # --------------------------------

        risk_quantity = int(risk_amount / stop_distance)

        # --------------------------------
        # Capital Limited Quantity
        # --------------------------------

        capital_quantity = int(account_size / entry_price)

        # --------------------------------
        # Final Quantity
        # --------------------------------

        final_quantity = min(risk_quantity, capital_quantity)

        return PositionSizeDecision(
            quantity=max(final_quantity, 1),
            risk_amount=round(risk_amount, 2),
            risk_percent=round(effective_risk_percent, 4),
            score_multiplier=round(multiplier, 4),
        )
        # __________________________________________________________________________----

    def _get_score_multiplier(self, score: float) -> float:
        """
        Return score multiplier.
        """

        sizing = self.config.get_position_sizing()
        score = abs(score)
        
        if score >= 90:
            return float(sizing.get("score_90_plus_multiplier", 1.5))

        if score >= 80:
            return float(sizing.get("score_80_to_90_multiplier", 1.25))

        if score >= 60:
            return float(sizing.get("score_60_to_80_multiplier", 1.0))

        return float(sizing.get("score_40_to_60_multiplier", 0.5))
