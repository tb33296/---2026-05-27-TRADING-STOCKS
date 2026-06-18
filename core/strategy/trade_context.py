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

    exchange: str
    
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
    
    # -------------------------------------------------
    # Feature States
    # -------------------------------------------------

    atr: float

    rvol: float

    vwap: float

    awvap: float

    vwma: float

    liquidity_ratio: float

    liquidity_delta: float

    cvd: float

    trend_state: str

    vwap_state: str

    awvap_state: str

    vwma_state: str

    rvol_state: str

    atr_state: str

    liquidity_state: str

    cvd_state: str