
# core/strategy/crossover_strategy.py

from datetime import datetime

from core.logging_manager import LoggingManager

from core.signals.signal import Signal

from core.strategy.strategy_base import (
    StrategyBase
)


class CrossoverStrategy(StrategyBase):
    """
    Simple LONG-only crossover strategy.

    Logic:
    - BUY signal -> enter LONG
    - SELL signal -> EXIT LONG
    """

    def __init__(
        self,
        name: str,
        symbol: str,
        timeframe: str
    ) -> None:

        super().__init__(
            name=name,
            symbol=symbol,
            timeframe=timeframe
        )

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.entry_count = 0

        self.exit_count = 0

        self.mark_ready()

    def on_signal(
        self,
        signal: Signal
    ) -> Signal | None:
        """
        Process incoming signal.

        Returns:
            Strategy action signal.
        """

        try:

            self.increment_signal_count()

            self.last_signal = signal

            # ================================
            # ENTRY LOGIC
            # ================================

            if self.should_enter(signal):

                self.set_state("LONG")

                self.entry_count += 1

                action = self._create_action(
                    signal_type="BUY",

                    source_signal=signal
                )

                self.logger.info(
                    f"{self.name} entered LONG"
                )

                return action

            # ================================
            # EXIT LOGIC
            # ================================

            if self.should_exit(signal):

                self.set_state("EXITED")

                self.exit_count += 1

                action = self._create_action(
                    signal_type="EXIT",

                    source_signal=signal
                )

                self.logger.info(
                    f"{self.name} exited LONG"
                )

                return action

            return None

        except Exception as error:

            self.logger.error(
                f"Strategy signal processing "
                f"failed: {error}"
            )

            return None

    def should_enter(
        self,
        signal: Signal
    ) -> bool:
        """
        Determine LONG entry condition.
        """

        if not self.is_idle():

            return False

        return signal.is_buy()

    def should_exit(
        self,
        signal: Signal
    ) -> bool:
        """
        Determine LONG exit condition.
        """

        if not self.is_long():

            return False

        return signal.is_sell()

    def _create_action(
        self,
        signal_type: str,
        source_signal: Signal
    ) -> Signal:
        """
        Create strategy action signal.
        """

        return Signal(
            symbol=self.symbol,

            timeframe=self.timeframe,

            signal_type=signal_type,

            strength=(
                source_signal.strength
            ),

            timestamp=datetime.now(),

            metadata={
                "strategy_name": (
                    self.name
                ),

                "source_signal": (
                    source_signal.signal_type
                ),

                "strategy_state": (
                    self.state
                )
            }
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

        self.logger.info(
            f"{self.name} reset"
        )

    def get_entry_count(
        self
    ) -> int:
        """
        Return total entries.
        """

        return self.entry_count

    def get_exit_count(
        self
    ) -> int:
        """
        Return total exits.
        """

        return self.exit_count
