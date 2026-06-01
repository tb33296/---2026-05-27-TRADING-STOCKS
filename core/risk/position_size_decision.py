# core/risk/position_size_decision.py

from dataclasses import dataclass


@dataclass(slots=True)
class PositionSizeDecision:
    """
    Position sizing result.
    """

    quantity: int

    risk_amount: float

    risk_percent: float

    score_multiplier: float