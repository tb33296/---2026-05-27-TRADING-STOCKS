#core/strategy/trade_context.py
from dataclasses import dataclass
from datetime import datetime


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

    # strategy_name: str

    # timestamp: datetime

    score: float

    direction: str

    confidence: str

    reasons: list[str]

    entry_price: float

    stop_loss: float

    target: float