from datetime import datetime

from config.config import ACTIVE_TIMEFRAMES

from core.indicators.ema import EMA
from core.indicators.atr import ATR
from core.indicators.rvol import RVOL
from core.indicators.vwap import VWAP

from core.market_data.market_clock import MarketClock

from runtime.indicator_runtime import IndicatorRuntime

from core.instruments.symbol_registry import SymbolRegistry


class IndicatorRegistration:

    def __init__(
        self,
        indicator_runtime: IndicatorRuntime,
        symbol_registry: SymbolRegistry,
        market_clock: MarketClock
    ) -> None:

        self.indicator_runtime = indicator_runtime

        self.symbol_registry = symbol_registry

        self.market_clock = market_clock

    def register_all(self) -> int:
        """
        Register all indicators.

        Returns:
            Total indicators registered.
        """

        count = 0

        symbols = (
            self.symbol_registry
            .get_all_symbols()
        )

        for symbol in symbols:

            for timeframe in ACTIVE_TIMEFRAMES:

                indicators = [

                    EMA(
                        name="EMA9",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=9
                    ),

                    EMA(
                        name="EMA20",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=20
                    ),

                    ATR(
                        name="ATR14",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=14
                    ),

                    RVOL(
                        name="RVOL20",
                        symbol=symbol,
                        timeframe=timeframe,
                        period=20
                    ),

                    VWAP(
                        name="VWAP",
                        symbol=symbol,
                        timeframe=timeframe,
                        market_clock=self.market_clock
                    ),
                ]

                for indicator in indicators:

                    if (
                        self.indicator_runtime
                        .register_indicator(
                            indicator
                        )
                    ):
                        count += 1

        return count