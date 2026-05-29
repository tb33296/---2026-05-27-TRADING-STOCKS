
# core/market_data/timeframe_manager.py

from threading import Lock
from typing import Optional

from config.config import (
    ACTIVE_TIMEFRAMES
)

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle

from core.market_data.candle_builder import (
    CandleBuilder
)

from core.market_data.market_clock import (
    MarketClock
)


class TimeframeManager:
    """
    Handles multi-timeframe candle orchestration.

    Responsibilities:
    - timeframe registration
    - centralized tick routing
    - candle builder management
    """

    def __init__(
        self,
        market_clock: MarketClock
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.market_clock = market_clock

        self.lock = Lock()

        self.builders: dict[
            str,
            CandleBuilder
        ] = {}

        self._initialize_timeframes()

    def _initialize_timeframes(
        self
    ) -> None:
        """
        Initialize configured timeframes.
        """

        for timeframe in ACTIVE_TIMEFRAMES:

            self.register_timeframe(
                timeframe
            )

        self.logger.info(
            f"Initialized "
            f"{len(self.builders)} "
            f"timeframes"
        )

    def register_timeframe(
        self,
        timeframe: str
    ) -> bool:
        """
        Register timeframe builder.
        """

        try:

            normalized = (
                timeframe.lower().strip()
            )

            with self.lock:

                if (
                    normalized
                    in self.builders
                ):

                    self.logger.warning(
                        f"Timeframe already "
                        f"registered: "
                        f"{normalized}"
                    )

                    return False

                self.builders[
                    normalized
                ] = CandleBuilder(
                    self.market_clock
                )

            self.logger.info(
                f"Registered timeframe: "
                f"{normalized}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Timeframe registration "
                f"failed: {error}"
            )

            return False

    def process_tick(
        self,
        tick: dict
    ) -> list[Candle]:
        """
        Route tick to all timeframe builders.

        Returns:
            List of closed candles.
        """

        closed_candles: list[
            Candle
        ] = []

        try:

            with self.lock:

                builders = list(
                    self.builders.items()
                )

            for (
                timeframe,
                builder
            ) in builders:

                closed = (
                    builder.process_tick(
                        tick=tick,
                        timeframe=timeframe
                    )
                )

                if closed is not None:

                    closed_candles.append(
                        closed
                    )

            return closed_candles

        except Exception as error:

            self.logger.error(
                f"Tick routing failed: "
                f"{error}"
            )

            return []

    def get_current_candle(
        self,
        symbol: str,
        timeframe: str
    ) -> Optional[Candle]:
        """
        Return current candle.
        """

        builder = self.builders.get(
            timeframe
        )

        if builder is None:

            return None

        return builder.get_current_candle(
            symbol=symbol,
            timeframe=timeframe
        )

    def get_closed_candles(
        self,
        symbol: str,
        timeframe: str
    ) -> list[Candle]:
        """
        Return closed candles.
        """

        builder = self.builders.get(
            timeframe
        )

        if builder is None:

            return []

        return builder.get_closed_candles(
            symbol=symbol,
            timeframe=timeframe
        )

    def force_close_all(
        self
    ) -> None:
        """
        Force close all candles.
        """

        with self.lock:

            builders = list(
                self.builders.values()
            )

        for builder in builders:

            builder.force_close_all()

        self.logger.info(
            "All timeframe candles closed"
        )

    def clear(self) -> None:
        """
        Clear all timeframe builders.
        """

        with self.lock:

            builders = list(
                self.builders.values()
            )

        for builder in builders:

            builder.clear()

        self.logger.info(
            "Timeframe manager cleared"
        )

    def get_registered_timeframes(
        self
    ) -> list[str]:
        """
        Return registered timeframes.
        """

        with self.lock:

            return sorted(
                list(self.builders.keys())
            )

    def timeframe_exists(
        self,
        timeframe: str
    ) -> bool:
        """
        Check whether timeframe exists.
        """

        normalized = (
            timeframe.lower().strip()
        )

        with self.lock:

            return (
                normalized
                in self.builders
            )
