from threading import Lock
from typing import Any, Optional

from core.logging_manager import (
    LoggingManager
)

from core.websocket.tick_queue import (
    TickQueue
)


class TickProcessor:
    """
    Consumes ticks from TickQueue and maintains
    latest market state.

    Responsibilities:
    - consume queue
    - store latest tick per token
    - provide lookup access
    - track processing statistics

    Does NOT:
    - build candles
    - calculate indicators
    - generate signals
    """

    def __init__(
        self,
        tick_queue: TickQueue
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.tick_queue = tick_queue

        self.lock = Lock()

        self.latest_ticks: dict[
            str,
            dict[str, Any]
        ] = {}

        self.total_processed = 0

        self.invalid_ticks = 0

    def process_next_tick(
        self
    ) -> bool:
        """
        Process a single tick.

        Returns:
            True if tick processed.
        """

        tick = self.tick_queue.dequeue()

        if tick is None:
            return False

        try:

            symbol = str(
                tick.get(
                    "symbol",
                    ""
                )
            )

            if not symbol:

                self.invalid_ticks += 1

                return False

            with self.lock:

                self.latest_ticks[
                    symbol
                ] = tick

                self.total_processed += 1

                return True

        except Exception as error:

            self.logger.error(
                f"Tick processing failed: "
                f"{error}"
            )

            self.invalid_ticks += 1

            return False

    def process_all_available(
        self
    ) -> int:
        """
        Process all queued ticks.

        Returns:
            Number of ticks processed.
        """

        processed = 0

        while self.process_next_tick():

            processed += 1

        return processed

    def get_latest_tick(
        self,
        token: str
    ) -> Optional[dict[str, Any]]:
        """
        Return latest tick for token.
        """

        with self.lock:

            return self.latest_ticks.get(
                token
            )

    def get_all_latest_ticks(
        self
    ) -> dict[str, dict[str, Any]]:
        """
        Return snapshot of latest ticks.
        """

        with self.lock:

            return dict(
                self.latest_ticks
            )

    def get_total_processed(
        self
    ) -> int:
        """
        Return processed tick count.
        """

        return self.total_processed

    def get_invalid_tick_count(
        self
    ) -> int:
        """
        Return invalid tick count.
        """

        return self.invalid_ticks

    def get_tracked_symbol_count(
        self
    ) -> int:
        """
        Return unique token count.
        """

        with self.lock:

            return len(
                self.latest_ticks
            )

    def clear(
        self
    ) -> None:
        """
        Reset processor state.
        """

        with self.lock:

            self.latest_ticks.clear()

            self.total_processed = 0

            self.invalid_ticks = 0