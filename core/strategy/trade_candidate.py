# core/strategy/trade_candidate.py

from dataclasses import dataclass
from datetime import datetime

from core.strategy.trade_context import TradeContext


@dataclass(slots=True)
class TradeCandidate:
    trade_context: TradeContext

    account_size: float

    ranking_score: float

    created_time: datetime
