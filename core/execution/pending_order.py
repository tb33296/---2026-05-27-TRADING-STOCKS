# core/execution/pending_order.py
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PendingOrder:

    symbol: str

    direction: str
    
    exchange: str

    segment: str
    

    quantity: int

    signal_price: float

    stop_loss: float

    target: float

    remaining_ticks: int
    
    slippage_ticks: int

    fill_price: float | None = None

    fill_time: datetime | None = None

    created_time: datetime | None = None