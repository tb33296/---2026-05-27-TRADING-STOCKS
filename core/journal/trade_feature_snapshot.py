from dataclasses import dataclass


@dataclass(slots=True)
class TradeFeatureSnapshot:
    """
    Derived market condition states
    captured at trade entry.
    """

    trade_id: int

    trend_state: str

    vwap_state: str

    awvap_state: str

    vwma_state: str

    rvol_state: str

    atr_state: str

    liquidity_state: str

    cvd_state: str