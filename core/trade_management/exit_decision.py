# core/trade_management/exit_decision.py
from dataclasses import dataclass


@dataclass(slots=True)
class ExitDecision:
    """
    Result of exit evaluation.
    """

    should_exit: bool

    reason: str