# core/positions/position.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Position:
    """
    Represents a single trade position.
    """

    symbol: str

    segment: str

    side: str

    quantity: int

    entry_price: float

    entry_time: datetime

    stop_loss: float

    target: float

    trade_id: int | None = None

    status: str = "OPEN"

    exit_price: Optional[float] = None

    exit_time: Optional[datetime] = None

    gross_pnl: float = 0.0

    charges: float = 0.0

    net_pnl: float = 0.0
    
    duration_seconds: int = 0