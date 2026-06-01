from core.strategy.crossover_strategy import (
    CrossoverStrategy
)


class OrderFlowStrategy(
    CrossoverStrategy
):
    """
    Order Flow based strategy.

    Consumes:

    - BUY signals from OrderFlowSignal
    - SELL signals from OrderFlowSignal

    Produces:

    - BUY actions
    - EXIT actions
    """

    pass