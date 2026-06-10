from datetime import datetime

from config.config import (
    ACTIVE_TIMEFRAMES,
    ATR_PERIOD,
    RVOL_PERIOD,
    VWMA_PERIOD,
    EMA_FAST_PERIOD,
    EMA_SLOW_PERIOD,
)

from core.indicators.moving_average import MovingAverage
from core.indicators.atr import ATR
from core.indicators.rvol import RVOL
from core.indicators.vwap import VWAP
from core.indicators.awvap import AWVAP
from core.indicators.vwma import VWMA
from core.indicators.liquidity_delta import LiquidityDelta
from core.indicators.cvd import CVD

from core.market_data.market_clock import MarketClock

from runtime.indicator_runtime import IndicatorRuntime

from core.instruments.symbol_registry import SymbolRegistry


class IndicatorRegistration:
    """
    Register all indicators required by
    MultiFactorStrategy.
    """

    def __init__(
        self,
        indicator_runtime: IndicatorRuntime,
        symbol_registry: SymbolRegistry,
        market_clock: MarketClock,
    ) -> None:

        self.indicator_runtime = indicator_runtime

        self.symbol_registry = symbol_registry

        self.market_clock = market_clock

    def register_all(self) -> int:
        """
        Register indicators for all
        symbols and timeframes.

        Returns:
            total indicators registered
        """

        count = 0

        symbols = self.symbol_registry.get_all_symbols()

        for symbol in symbols:
            for timeframe in ACTIVE_TIMEFRAMES:
                indicators = [
                    # ---------------------------------
                    # Trend
                    # ---------------------------------
                    MovingAverage(
                        name="EMA_FAST",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=EMA_FAST_PERIOD,
                        ma_type="EMA",
                    ),
                    MovingAverage(
                        name="EMA_SLOW",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=EMA_SLOW_PERIOD,
                        ma_type="EMA",
                    ),
                    # ---------------------------------
                    # Fair Value
                    # ---------------------------------
                    VWAP(
                        name="VWAP",
                        symbol=symbol,
                        timeframe=timeframe,
                        market_clock=self.market_clock,
                    ),
                    AWVAP(
                        name="AWVAP",
                        symbol=symbol,
                        timeframe=timeframe,
                        anchor_time=datetime.now(),
                    ),
                    # ---------------------------------
                    # Volume
                    # ---------------------------------
                    RVOL(
                        name="RVOL",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=RVOL_PERIOD,
                    ),
                    VWMA(
                        name="VWMA",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=VWMA_PERIOD,
                    ),
                    # ---------------------------------
                    # Volatility
                    # ---------------------------------
                    ATR(
                        name="ATR",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=ATR_PERIOD,
                    ),
                    # ---------------------------------
                    # Order Flow
                    # ---------------------------------
                    # LiquidityDelta(
                    #     name="LIQUIDITY",
                    #     symbol=symbol,
                    #     timeframe=timeframe,
                    # ),
                    # CVD(
                    #     name="CVD",
                    #     symbol=symbol,
                    #     timeframe=timeframe,
                    # ),
                    #! Temporarily removing the file as there is error in orderflow
                ]

                for indicator in indicators:
                    if self.indicator_runtime.register_indicator(indicator):
                        count += 1

        return count
