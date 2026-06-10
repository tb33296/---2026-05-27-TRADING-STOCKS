# core/strategy/crossover_strategy.py

from datetime import datetime

from core.logging_manager import LoggingManager

from core.signals.signal import Signal

from core.strategy.strategy_base import StrategyBase

from core.strategy.trade_intent import TradeIntent


class CrossoverStrategy(StrategyBase):
    """
    Simple LONG-only crossover strategy.

    Logic:

    BUY signal
        -> enter LONG

    SELL signal
        -> exit LONG

    Produces:
        TradeIntent objects
    """

    def __init__(self, name: str, symbol: str, timeframe: str) -> None:

        super().__init__(name=name, symbol=symbol, timeframe=timeframe)

        self.logger = LoggingManager.get_logger(__name__)

        self.entry_count = 0

        self.exit_count = 0

        self.mark_ready()

    def on_signal(self, signal: Signal) -> TradeIntent | None:
        """
        Process incoming signal.

        Returns:
            TradeIntent or None
        """

        try:
            self.increment_signal_count()

            self.last_signal = signal

            # ==========================
            # ENTRY
            # ==========================

            if self.should_enter(signal):
                self.set_state("LONG")

                self.entry_count += 1

                intent = self._create_trade_intent(action="BUY", source_signal=signal)

                self.logger.info(f"{self.name} entered LONG")

                return intent

            # ==========================
            # EXIT
            # ==========================

            if self.should_exit(signal):
                self.set_state("EXITED")

                self.exit_count += 1

                intent = self._create_trade_intent(
                    action="EXIT_LONG", source_signal=signal
                )

                self.logger.info(f"{self.name} exited LONG")

                return intent

            return None

        except Exception as error:
            self.logger.error(f"Strategy signal processing failed: {error}")

            return None

    def should_enter(self, signal: Signal) -> bool:
        """
        Determine LONG entry.
        """

        if not self.is_idle():
            return False

        return signal.is_buy()

    def should_exit(self, signal: Signal) -> bool:
        """
        Determine LONG exit.
        """

        if not self.is_long():
            return False

        return signal.is_sell()

    def _create_trade_intent(self, action: str, source_signal: Signal) -> TradeIntent:
        """
        Create TradeIntent.
        """

        return TradeIntent(
            symbol=self.symbol,
            timeframe=self.timeframe,
            action=action,
            quantity=1,
            timestamp=datetime.now(),
            strategy_name=self.name,
            signal_name=(source_signal.metadata.get("signal_name")),
            confidence=(source_signal.strength),
            reason=(f"{self.name} triggered {source_signal.signal_type}"),
            metadata={
                "strategy_state": self.state,
                "source_signal": source_signal.signal_type,
                "signal_name": source_signal.metadata.get("signal_name"),
            },
        )

    def reset(self) -> None:
        """
        Reset strategy state.
        """

        self.set_state("IDLE")

        self.last_signal = None

        self.entry_count = 0

        self.exit_count = 0

        self.total_signals_processed = 0

        self.logger.info(f"{self.name} reset")

    def get_entry_count(self) -> int:

        return self.entry_count

    def get_exit_count(self) -> int:

        return self.exit_count
