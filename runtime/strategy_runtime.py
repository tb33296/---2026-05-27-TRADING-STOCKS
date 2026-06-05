# runtime/strategy_runtime.py

from core.strategy.multifactor_decision import MultiFactorDecision

from core.strategy.multifactor_strategy import MultiFactorStrategy


class StrategyRuntime:
    """
    Runtime wrapper around strategy evaluation.

    Responsibilities:
    - evaluate strategy
    - return decisions

    Does NOT:
    - execute trades
    - manage risk
    - journal trades
    """

    def __init__(self, strategy: MultiFactorStrategy) -> None:

        self.strategy = strategy

    def evaluate(self, current_price: float) -> MultiFactorDecision:

        return self.strategy.evaluate(current_price)
