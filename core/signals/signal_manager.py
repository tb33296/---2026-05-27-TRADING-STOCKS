# core/signals/signal_manager.py

from threading import Lock
from typing import Optional

from core.logging_manager import LoggingManager

from core.signals.signal import Signal


class SignalManager:
    """
    Handles signal orchestration.

    Responsibilities:
    - signal storage
    - signal routing
    - latest signal tracking
    - signal retrieval
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.lock = Lock()

        self.latest_signals: dict[
            tuple[str, str],
            Signal
        ] = {}

        self.signal_history: dict[
            tuple[str, str],
            list[Signal]
        ] = {}

    def publish_signal(
        self,
        signal: Signal
    ) -> None:
        """
        Publish new signal.
        """

        try:

            key = (
                signal.symbol,
                signal.timeframe
            )

            with self.lock:

                self.latest_signals[
                    key
                ] = signal

                if (
                    key
                    not in self.signal_history
                ):

                    self.signal_history[
                        key
                    ] = []

                self.signal_history[
                    key
                ].append(signal)

            self.logger.info(
                f"Signal published: "
                f"{signal.symbol} "
                f"{signal.timeframe} "
                f"{signal.signal_type}"
            )

        except Exception as error:

            self.logger.error(
                f"Signal publish failed: "
                f"{error}"
            )

    def get_latest_signal(
        self,
        symbol: str,
        timeframe: str
    ) -> Optional[Signal]:
        """
        Return latest signal.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            return self.latest_signals.get(
                key
            )

    def get_signal_history(
        self,
        symbol: str,
        timeframe: str
    ) -> list[Signal]:
        """
        Return signal history.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            return list(
                self.signal_history.get(
                    key,
                    []
                )
            )

    def clear_symbol_signals(
        self,
        symbol: str,
        timeframe: str
    ) -> None:
        """
        Clear signals for symbol/timeframe.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            self.latest_signals.pop(
                key,
                None
            )

            self.signal_history.pop(
                key,
                None
            )

        self.logger.info(
            f"Cleared signals: "
            f"{symbol} "
            f"{timeframe}"
        )

    def clear_all(self) -> None:
        """
        Clear all signal state.
        """

        with self.lock:

            self.latest_signals.clear()

            self.signal_history.clear()

        self.logger.info(
            "All signals cleared"
        )

    def get_total_signal_count(
        self
    ) -> int:
        """
        Return total stored signals.
        """

        total = 0

        with self.lock:

            for signals in (
                self.signal_history.values()
            ):

                total += len(signals)

        return total

    def has_signal(
        self,
        symbol: str,
        timeframe: str
    ) -> bool:
        """
        Check whether signal exists.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            return (
                key
                in self.latest_signals
            )
