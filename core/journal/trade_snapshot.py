# core\journal\trade_snapshot.py
from dataclasses import dataclass


@dataclass(slots=True)
class TradeSnapshot:
    """
    Trade journal record.
    """

    trade_id: int | None

    symbol: str

    segment: str

    strategy_name: str

    direction: str

    entry_time: str

    quantity: int

    entry_price: float

    stop_loss: float

    target: float

    score: float

    confidence: str

    risk_amount: float

    risk_percent: float

    status: str