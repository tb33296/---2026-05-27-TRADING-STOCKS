from config.config import ACTIVE_TIMEFRAMES

from core.indicators.ema import EMA
from core.indicators.rvol import RVOL
from core.indicators.vwap import VWAP

from core.signals.crossover_signal import CrossoverSignal
from core.signals.vwap_signal import VWAPSignal

from runtime.indicator_runtime import IndicatorRuntime
from runtime.signal_runtime import SignalRuntime

from core.instruments.symbol_registry import SymbolRegistry


class SignalRegistration:
    """
    Creates and registers signals.

    Responsibilities:
    - EMA crossover signals
    - VWAP crossover signals
    """

    def __init__(
        self,
        signal_runtime: SignalRuntime,
        indicator_runtime: IndicatorRuntime,
        symbol_registry: SymbolRegistry,
    ) -> None:

        self.signal_runtime = signal_runtime

        self.indicator_runtime = indicator_runtime

        self.symbol_registry = symbol_registry

    def register_all(self) -> int:

        count = 0

        symbols = self.symbol_registry.get_all_symbols()

        for symbol in symbols:
            for timeframe in ACTIVE_TIMEFRAMES:
                ema9 = self.indicator_runtime.indicator_manager.get_indicator(
                    symbol, timeframe, "EMA9"
                )

                ema20 = self.indicator_runtime.indicator_manager.get_indicator(
                    symbol, timeframe, "EMA20"
                )

                rvol = self.indicator_runtime.indicator_manager.get_indicator(
                    symbol, timeframe, "RVOL20"
                )

                vwap = self.indicator_runtime.indicator_manager.get_indicator(
                    symbol, timeframe, "VWAP"
                )

                # ==========================
                # EMA CROSSOVER
                # ==========================

                if isinstance(ema9, EMA) and isinstance(ema20, EMA):
                    signal = CrossoverSignal(
                        name=(f"{symbol}_{timeframe}_EMA9_EMA20"),
                        fast_indicator=ema9,
                        slow_indicator=ema20,
                        signal_strength=1.0,
                        rvol_indicator=rvol,
                        min_rvol=1.0,
                    )

                    if self.signal_runtime.register_crossover_signal(
                        signal.name, signal
                    ):
                        count += 1

                # ==========================
                # VWAP SIGNAL
                # ==========================

                if isinstance(vwap, VWAP):
                    signal = VWAPSignal(
                        name=(f"{symbol}_{timeframe}_VWAP"),
                        vwap_indicator=vwap,
                        signal_strength=1.0,
                    )

                    if (self.signal_runtime.register_vwap_signal(signal.name, signal)):
                        count += 1

        return count
