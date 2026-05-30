# core/risk/risk_decision.py

from dataclasses import dataclass


@dataclass(slots=True)
class RiskDecision:
    """
    Result returned by RiskEngine.
    """

    approved: bool

    reason: str