# runtime/strategy_runtime.py

from core.logging_manager import LoggingManager

from core.signals.signal import Signal

from core.strategy.strategy_base import StrategyBase

from core.strategy.trade_intent import TradeIntent

from core.strategy.trade_intent import TradeIntent


class StrategyRuntime:
    """
    Runtime wrapper around strategy evaluation.

    Responsibilities:
    - receive signals
    - route signals to strategy
    - return TradeIntent objects

    Does NOT:
    - manage risk
    - execute orders
    - journal trades
    """

    def __init__(self, strategy: StrategyBase) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.strategy = strategy

        self.total_signals_processed = 0

        self.total_intents_generated = 0

    def process_signal(self, signal: Signal) -> TradeIntent | None:
        """
        Process signal through strategy.

        Returns:
            TradeIntent or None
        """

        try:
            self.total_signals_processed += 1

            intent = self.strategy.on_signal(signal)

            if intent is not None:
                self.total_intents_generated += 1

            return intent

        except Exception as error:
            self.logger.error(f"Strategy runtime failed: {error}")

            return None

    def get_strategy(self) -> StrategyBase:

        return self.strategy

    def get_total_signals_processed(self) -> int:

        return self.total_signals_processed

    def get_total_intents_generated(self) -> int:

        return self.total_intents_generated

    def reset(self) -> None:

        self.total_signals_processed = 0

        self.total_intents_generated = 0

        self.strategy.reset()
