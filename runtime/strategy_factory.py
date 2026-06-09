# runtime/strategy_factory.py
from datetime import datetime

from runtime.indicator_runtime import IndicatorRuntime

# from runtime.strategy_runtime import StrategyRuntime

from core.strategy.multifactor_strategy import MultiFactorStrategy

from core.indicators.moving_average import MovingAverage

from core.indicators.vwap import VWAP

from core.indicators.awvap import AWVAP

from core.indicators.rvol import RVOL

from core.indicators.vwma import VWMA

from core.indicators.atr import ATR

from core.indicators.liquidity_delta import LiquidityDelta

from core.indicators.cvd import CVD

from core.market_data.market_clock import MarketClock

from config.config import MARKET_HOLIDAY_FILE


class StrategyFactory:
    """
    Creates fully wired strategy runtime.

    Responsibilities:
    - create indicators
    - register indicators
    - create strategy
    - create strategy runtime
    """

    @staticmethod
    def create(
        symbol: str, timeframe: str, indicator_runtime: IndicatorRuntime
    ) -> MultiFactorStrategy:


        ema_fast = MovingAverage(
            name="EMA_FAST", symbol=symbol, timeframe=timeframe, period=3, ma_type="EMA"
        )

        ema_slow = MovingAverage(
            name="EMA_SLOW", symbol=symbol, timeframe=timeframe, period=5, ma_type="EMA"
        )
        market_clock = MarketClock()

        vwap = VWAP(
            name="VWAP", symbol=symbol, timeframe=timeframe, market_clock=market_clock
        )

        awvap = AWVAP(
            name="AWVAP", symbol=symbol, timeframe=timeframe, anchor_time=datetime.now()
        )

        rvol = RVOL(name="RVOL", symbol=symbol, timeframe=timeframe)

        vwma = VWMA(name="VWMA", symbol=symbol, timeframe=timeframe, period=20)

        atr = ATR(name="ATR", symbol=symbol, timeframe=timeframe, period=14)

        liquidity = LiquidityDelta(name="LIQUIDITY", symbol=symbol, timeframe=timeframe)

        cvd = CVD(name="CVD", symbol=symbol, timeframe=timeframe)

        indicators = [ema_fast, ema_slow, vwap, awvap, rvol, vwma, atr,] #liquidity, cvd]

        for indicator in indicators:
            indicator_runtime.register_indicator(indicator)

        strategy = MultiFactorStrategy(
            ema_fast=ema_fast,
            ema_slow=ema_slow,
            vwap=vwap,
            awvap=awvap,
            rvol=rvol,
            vwma=vwma,
            atr=atr,
            liquidity=liquidity,
            cvd=cvd,
        )

        return strategy
