# core/market_data/candle_builder.py

from threading import Lock
from typing import Optional

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle

from core.market_data.market_clock import (
    MarketClock
)


class CandleBuilder:
    """
    Handles live candle generation from ticks.

    Responsibilities:
    - tick aggregation
    - candle rollover
    - OHLC updates
    - closed candle management
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

        self.current_candles: dict[
            tuple[str, str],
            Candle
        ] = {}

        self.closed_candles: dict[
            tuple[str, str],
            list[Candle]
        ] = {}

    def process_tick(
        self,
        tick: dict,
        timeframe: str = "1m"
    ) -> Optional[Candle]:
        """
        Process incoming tick and update candle.

        Returns:
            Closed candle if rollover occurs.
        """

        try:

            symbol = str(
                tick.get("symbol", "")
            )

            price = float(
                tick.get("ltp", 0)
            )

            volume = int(
                tick.get("volume", 0)
            )

            timestamp = tick.get(
                "timestamp"
            )

            if not symbol:

                return None

            if timestamp is None:

                return None

            timeframe_minutes = (
                self._parse_timeframe(
                    timeframe
                )
            )

            candle_start = (
                self.market_clock
                .get_candle_start_time(
                    timestamp,
                    timeframe_minutes
                )
            )

            candle_end = (
                self.market_clock
                .get_candle_end_time(
                    candle_start,
                    timeframe_minutes
                )
            )

            key = (
                symbol,
                timeframe
            )

            with self.lock:

                current_candle = (
                    self.current_candles
                    .get(key)
                )

                # ====================================
                # CREATE NEW CANDLE
                # ====================================

                if current_candle is None:

                    new_candle = (
                        Candle.from_tick(
                            symbol=symbol,

                            timeframe=timeframe,

                            price=price,

                            volume=volume,

                            start_time=(
                                candle_start
                            ),

                            end_time=(
                                candle_end
                            )
                        )
                    )

                    self.current_candles[
                        key
                    ] = new_candle

                    return None

                # ====================================
                # SAME CANDLE UPDATE
                # ====================================

                if (
                    timestamp
                    < current_candle.end_time
                ):

                    current_candle.update(
                        price=price,
                        volume=volume
                    )

                    return None

                # ====================================
                # CANDLE ROLLOVER
                # ====================================

                current_candle.close_candle()

                if (
                    key
                    not in self.closed_candles
                ):

                    self.closed_candles[
                        key
                    ] = []

                self.closed_candles[
                    key
                ].append(
                    current_candle
                )

                new_candle = (
                    Candle.from_tick(
                        symbol=symbol,

                        timeframe=timeframe,

                        price=price,

                        volume=volume,

                        start_time=(
                            candle_start
                        ),

                        end_time=(
                            candle_end
                        )
                    )
                )

                self.current_candles[
                    key
                ] = new_candle

                self.logger.info(
                    f"Candle closed: "
                    f"{symbol} "
                    f"{timeframe}"
                )

                return current_candle

        except Exception as error:

            self.logger.error(
                f"Candle processing failed: "
                f"{error}"
            )

            return None

    def get_current_candle(
        self,
        symbol: str,
        timeframe: str = "1m"
    ) -> Optional[Candle]:
        """
        Return active candle.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            return self.current_candles.get(
                key
            )

    def get_closed_candles(
        self,
        symbol: str,
        timeframe: str = "1m"
    ) -> list[Candle]:
        """
        Return closed candles.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            return list(
                self.closed_candles.get(
                    key,
                    []
                )
            )

    def force_close_all(self) -> None:
        """
        Force close all active candles.
        """

        with self.lock:

            for (
                key,
                candle
            ) in self.current_candles.items():

                candle.close_candle()

                if (
                    key
                    not in self.closed_candles
                ):

                    self.closed_candles[
                        key
                    ] = []

                self.closed_candles[
                    key
                ].append(candle)

            self.current_candles.clear()

            self.logger.info(
                "All candles force closed"
            )

    def clear(self) -> None:
        """
        Clear candle state.
        """

        with self.lock:

            self.current_candles.clear()

            self.closed_candles.clear()

            self.logger.info(
                "Candle builder cleared"
            )

    def _parse_timeframe(
        self,
        timeframe: str
    ) -> int:
        """
        Convert timeframe string to minutes.

        Examples:
            1m -> 1
            5m -> 5
            15m -> 15
        """

        normalized = (
            timeframe
            .lower()
            .replace("m", "")
        )

        return int(normalized)
