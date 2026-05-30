# runtime/signal_runtime.py

from typing import Optional

from core.logging_manager import (
    LoggingManager
)

from core.signals.crossover_signal import (
    CrossoverSignal
)

from core.signals.signal import (
    Signal
)

from core.signals.signal_manager import (
    SignalManager
)


class SignalRuntime:
    """
    Runtime layer for signal generation.

    Responsibilities:
    - register signal generators
    - evaluate signals
    - publish signals
    - provide signal lookup

    Does NOT:
    - place orders
    - manage positions
    - manage risk
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.signal_manager = (
            SignalManager()
        )

        self.crossover_signals: dict[
            str,
            CrossoverSignal
        ] = {}

    def register_crossover_signal(
        self,
        signal_name: str,
        signal_generator: CrossoverSignal
    ) -> bool:
        """
        Register crossover signal.
        """

        try:

            if (
                signal_name
                in self.crossover_signals
            ):

                self.logger.warning(
                    f"Signal already "
                    f"registered: "
                    f"{signal_name}"
                )

                return False

            self.crossover_signals[
                signal_name
            ] = signal_generator

            self.logger.info(
                f"Registered signal: "
                f"{signal_name}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Signal registration "
                f"failed: {error}"
            )

            return False

    def evaluate_signals(
        self
    ) -> list[Signal]:
        """
        Evaluate all registered signals.
        """

        generated_signals: list[
            Signal
        ] = []

        try:

            for (
                signal_generator
            ) in (
                self.crossover_signals
                .values()
            ):

                signal = (
                    signal_generator
                    .evaluate()
                )

                if signal is None:
                    continue

                self.signal_manager\
                    .publish_signal(
                        signal
                    )

                generated_signals.append(
                    signal
                )

            return generated_signals

        except Exception as error:

            self.logger.error(
                f"Signal evaluation "
                f"failed: {error}"
            )

            return generated_signals

    def get_latest_signal(
        self,
        symbol: str,
        timeframe: str
    ) -> Optional[Signal]:
        """
        Return latest signal.
        """

        return (
            self.signal_manager
            .get_latest_signal(
                symbol,
                timeframe
            )
        )

    def get_signal_history(
        self,
        symbol: str,
        timeframe: str
    ) -> list[Signal]:
        """
        Return signal history.
        """

        return (
            self.signal_manager
            .get_signal_history(
                symbol,
                timeframe
            )
        )

    def get_total_signal_count(
        self
    ) -> int:
        """
        Return total signal count.
        """

        return (
            self.signal_manager
            .get_total_signal_count()
        )

    def clear(self) -> None:
        """
        Clear runtime state.
        """

        self.signal_manager.clear_all()

        self.crossover_signals.clear()

        self.logger.info(
            "Signal runtime cleared"
        )