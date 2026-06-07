# runtime/signal_runtime.py
from typing import Optional

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle

from core.signals.crossover_signal import CrossoverSignal
from core.signals.signal import Signal
from core.signals.signal_manager import SignalManager
from core.signals.vwap_signal import VWAPSignal


class SignalRuntime:
    """
    Runtime layer for signal generation.

    Responsibilities:
    - register signal generators
    - evaluate signals
    - publish signals
    - provide signal lookup
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.signal_manager = SignalManager()

        self.crossover_signals: dict[str, CrossoverSignal] = {}

        self.vwap_signals: dict[str, VWAPSignal] = {}

    def register_crossover_signal(
        self, signal_name: str, signal_generator: CrossoverSignal
    ) -> bool:

        if signal_name in self.crossover_signals:
            self.logger.warning(f"Signal already registered: {signal_name}")

            return False

        self.crossover_signals[signal_name] = signal_generator

        return True

    def register_vwap_signal(
        self, signal_name: str, signal_generator: VWAPSignal
    ) -> bool:

        if signal_name in self.vwap_signals:
            self.logger.warning(f"Signal already registered: {signal_name}")

            return False

        self.vwap_signals[signal_name] = signal_generator
        self.logger.info(f"Registered VWAP signal: {signal_name}")

        return True

    def evaluate_signals(self, candle: Candle) -> list[Signal]:

        generated_signals: list[Signal] = []

        try:
            # ==========================
            # CROSSOVER SIGNALS
            # ==========================

            for signal_generator in self.crossover_signals.values():
                signal = signal_generator.evaluate()

                if signal is None:
                    continue

                self.signal_manager.publish_signal(signal)

                generated_signals.append(signal)

            # ==========================
            # VWAP SIGNALS
            # ==========================

            for signal_generator in self.vwap_signals.values():
                signal = signal_generator.evaluate(candle)

                if signal is None:
                    continue

                self.signal_manager.publish_signal(signal)

                generated_signals.append(signal)

            return generated_signals

        except Exception as error:
            self.logger.error(f"Signal evaluation failed: {error}")

            return generated_signals

    def get_latest_signal(self, symbol: str, timeframe: str) -> Optional[Signal]:

        return self.signal_manager.get_latest_signal(symbol, timeframe)

    def get_signal_history(self, symbol: str, timeframe: str) -> list[Signal]:

        return self.signal_manager.get_signal_history(symbol, timeframe)

    def get_total_signal_count(self) -> int:

        return self.signal_manager.get_total_signal_count()

    def clear(self) -> None:

        self.signal_manager.clear_all()

        self.crossover_signals.clear()

        self.vwap_signals.clear()

        self.logger.info("Signal runtime cleared")
