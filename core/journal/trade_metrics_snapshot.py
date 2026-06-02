from dataclasses import dataclass


@dataclass(slots=True)
class TradeMetricsSnapshot:
    """
    Raw indicator values captured
    at trade entry.
    """

    trade_id: int

    atr: float

    rvol: float

    vwap: float

    awvap: float

    vwma: float

    liquidity_ratio: float

    liquidity_delta: float

    cvd: float