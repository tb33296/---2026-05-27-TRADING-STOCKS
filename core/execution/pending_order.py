# core/execution/pending_order.py
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PendingOrder:

    symbol: str

    direction: str

    segment: str

    quantity: int

    signal_price: float

    stop_loss: float

    target: float

    remaining_ticks: int

    created_time: datetime