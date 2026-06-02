from dataclasses import dataclass


@dataclass(slots=True)
class TradeContext:
    """
    Complete trade context passed
    through the trading workflow.

    Contains strategy output,
    trade parameters and
    future journal data.
    """

    symbol: str

    segment: str

    score: float

    direction: str

    confidence: str

    reasons: list[str]

    entry_price: float

    stop_loss: float

    target: float