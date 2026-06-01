# core/strategy/trade_decision.py

from dataclasses import dataclass, field


@dataclass(slots=True)
class TradeDecision:
    """
    Final trade decision.

    Generated after:

    - strategy evaluation
    - risk validation
    - position sizing
    """

    approved: bool

    direction: str

    score: float

    quantity: int

    reason: str

    confidence: str

    metadata: dict = field(
        default_factory=dict
    )

    def is_long(self) -> bool:

        return (
            self.direction.upper()
            == "LONG"
        )

    def is_short(self) -> bool:

        return (
            self.direction.upper()
            == "SHORT"
        )

    def is_approved(self) -> bool:

        return self.approved