# core/execution/pending_order.py
from dataclasses import dataclass
from datetime import datetime


from core.strategy.trade_context import TradeContext


@dataclass(slots=True)
class PendingOrder:

    symbol: str

    direction: str

    exchange: str

    segment: str

    trade_context: TradeContext

    account_size: float

    quantity: int

    risk_amount: float

    risk_percent: float

    signal_price: float

    stop_loss: float

    target: float

    remaining_ticks: int

    slippage_ticks: int

    fill_price: float | None = None

    fill_time: datetime | None = None

    created_time: datetime | None = None