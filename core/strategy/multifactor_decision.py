from dataclasses import dataclass


@dataclass(slots=True)
class MultiFactorDecision:
    """
    Multi-factor trade decision.
    """

    score: float

    direction: str

    confidence: str

    reasons: list[str]

    stop_loss: float

    target: float